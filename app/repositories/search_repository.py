from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.retrieved_chunk import RetrievedChunk

RRF_K = 60
MIN_SIMILARITY = 0.20


class SearchRepository:
    """
    Performs semantic and keyword search against stored document chunks.
    """

    def __init__(self, db: Session):
        self.db = db

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        stmt = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
                DocumentChunk.content,
                Document.filename,
                distance.label("distance"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .order_by(distance)
            .limit(limit)
        )

        rows = self.db.execute(stmt).all()

        logger.info(
            "Semantic search returned %d chunks",
            len(rows),
        )

        results: list[RetrievedChunk] = []

        for (
            chunk_id,
            document_id,
            chunk_index,
            content,
            filename,
            distance,
        ) in rows:

            similarity = float(1 - distance)

            logger.info(
                "%s | chunk=%d | similarity=%.4f",
                filename,
                chunk_index,
                similarity,
            )

            if similarity < MIN_SIMILARITY:
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

        return results

    def keyword_search(
        self,
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        ts_query = func.plainto_tsquery(
            "english",
            question,
        )

        rank = func.ts_rank_cd(
            DocumentChunk.search_vector,
            ts_query,
        )

        stmt = (
            select(
                DocumentChunk.id,
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
                DocumentChunk.content,
                Document.filename,
                rank.label("rank"),
            )
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .where(
                DocumentChunk.search_vector.op("@@")(ts_query)
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
                score=float(rank),
            )
            for (
                chunk_id,
                document_id,
                chunk_index,
                content,
                filename,
                rank,
            ) in rows
        ]

    def hybrid_search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        semantic = self.semantic_search(
            query_embedding,
            limit * 2,
        )

        keyword = self.keyword_search(
            question,
            limit * 2,
        )

        scores: dict[int, float] = {}
        chunks: dict[int, RetrievedChunk] = {}

        for rank, chunk in enumerate(semantic, start=1):
            score = 1 / (RRF_K + rank)
            scores[chunk.chunk_id] = score
            chunk.score = score
            chunks[chunk.chunk_id] = chunk

        for rank, chunk in enumerate(keyword, start=1):
            score = 1 / (RRF_K + rank)

            if chunk.chunk_id in scores:
                scores[chunk.chunk_id] += score
                chunks[chunk.chunk_id].score = scores[chunk.chunk_id]
            else:
                scores[chunk.chunk_id] = score
                chunk.score = score
                chunks[chunk.chunk_id] = chunk

        return sorted(
            chunks.values(),
            key=lambda c: c.score,
            reverse=True,
        )[:limit]

    def search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:

        return self.hybrid_search(
            query_embedding=query_embedding,
            question=question,
            limit=limit,
        )