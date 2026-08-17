from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.logger import logger
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.retrieved_chunk import RetrievedChunk


class SearchRepository:
    """Performs semantic and keyword search over stored document chunks."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int,
    ) -> list[RetrievedChunk]:
        distance = DocumentChunk.embedding.cosine_distance(query_embedding)

        stmt = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
                DocumentChunk.content,
                Document.filename,
                distance.label("distance"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(Document.status == "processed")
            .order_by(distance)
            .limit(limit)
        )

        rows = self.db.execute(stmt).all()
        results: list[RetrievedChunk] = []

        for (
            chunk_id,
            document_id,
            chunk_index,
            content,
            filename,
            distance_value,
        ) in rows:
            similarity = float(1 - distance_value)

            if similarity < settings.semantic_similarity_threshold:
                continue

            results.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    document_id=document_id,
                    filename=filename,
                    chunk_index=chunk_index,
                    content=content,
                    score=similarity,
                )
            )

        logger.info(
            "Semantic search returned %d/%d candidates",
            len(results),
            len(rows),
        )

        return results

    def keyword_search(
        self,
        question: str,
        limit: int,
    ) -> list[RetrievedChunk]:
        ts_query = func.plainto_tsquery("english", question)
        rank = func.ts_rank_cd(DocumentChunk.search_vector, ts_query)

        stmt = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
                DocumentChunk.content,
                Document.filename,
                rank.label("rank"),
            )
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(
                Document.status == "processed",
                DocumentChunk.search_vector.op("@@")(ts_query),
            )
            .order_by(rank.desc())
            .limit(limit)
        )

        rows = self.db.execute(stmt).all()

        return [
            RetrievedChunk(
                chunk_id=chunk_id,
                document_id=document_id,
                filename=filename,
                chunk_index=chunk_index,
                content=content,
                score=float(rank_value),
            )
            for (
                chunk_id,
                document_id,
                chunk_index,
                content,
                filename,
                rank_value,
            ) in rows
        ]

    def hybrid_search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int,
    ) -> list[RetrievedChunk]:
        candidate_limit = max(limit, settings.semantic_candidate_limit)

        semantic = self.semantic_search(
            query_embedding=query_embedding,
            limit=candidate_limit,
        )
        keyword = self.keyword_search(
            question=question,
            limit=candidate_limit,
        )

        scores: dict[int, float] = {}
        chunks: dict[int, RetrievedChunk] = {}

        for rank, chunk in enumerate(semantic, start=1):
            score = 1 / (settings.rrf_k + rank)
            scores[chunk.chunk_id] = score
            chunks[chunk.chunk_id] = chunk
            chunk.score = score

        for rank, chunk in enumerate(keyword, start=1):
            score = 1 / (settings.rrf_k + rank)

            if chunk.chunk_id in scores:
                scores[chunk.chunk_id] += score
                chunks[chunk.chunk_id].score = scores[chunk.chunk_id]
            else:
                scores[chunk.chunk_id] = score
                chunks[chunk.chunk_id] = chunk
                chunk.score = score

        return sorted(
            chunks.values(),
            key=lambda item: item.score,
            reverse=True,
        )[:limit]

    def search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int,
    ) -> list[RetrievedChunk]:
        return self.hybrid_search(
            query_embedding=query_embedding,
            question=question,
            limit=limit,
        )
