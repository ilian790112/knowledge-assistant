from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.retrieved_chunk import RetrievedChunk
from app.core.logger import logger

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
        """
        Retrieve chunks using vector similarity.
        """

        distance = DocumentChunk.embedding.cosine_distance(
            query_embedding
        )

        statement = (
            select(
                DocumentChunk,
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

        rows = self.db.execute(statement).all()

        logger.info("Semantic search returned %d rows", len(rows))

        for chunk, filename, distance in rows:
            # FIXED: Indented the logger lines below to belong to the loop
            logger.info(
                "Document=%s Chunk=%d Distance=%.4f Similarity=%.4f",
                filename,
                chunk.chunk_index,
                distance,
                1 - distance,
            )

        results: list[RetrievedChunk] = []

        for chunk, filename, distance in rows:
            similarity = float(1 - distance)

            if similarity < MIN_SIMILARITY:
                continue

            results.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    filename=filename,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    score=similarity,
                )
            )

        return results

    def keyword_search(
        self,
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve chunks using PostgreSQL full-text search.
        """

        ts_query = func.plainto_tsquery(
            "english",
            question,
        )

        rank = func.ts_rank_cd(
            DocumentChunk.search_vector,
            ts_query,
        )

        statement = (
            select(
                DocumentChunk,
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

        rows = self.db.execute(statement).all()

        results: list[RetrievedChunk] = []

        for chunk, filename, rank in rows:
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    filename=filename,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    score=float(rank),
                )
            )

        return results

    def hybrid_search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Combine semantic and keyword search using
        Reciprocal Rank Fusion (RRF).
        """

        semantic_results = self.semantic_search(
            query_embedding=query_embedding,
            limit=limit * 2,
        )

        keyword_results = self.keyword_search(
            question=question,
            limit=limit * 2,
        )

        fused_scores: dict[int, float] = {}
        chunks: dict[int, RetrievedChunk] = {}

        for rank, chunk in enumerate(semantic_results, start=1):
            score = 1 / (RRF_K + rank)

            fused_scores[chunk.chunk_id] = score
            chunk.score = score
            chunks[chunk.chunk_id] = chunk

        for rank, chunk in enumerate(keyword_results, start=1):
            score = 1 / (RRF_K + rank)

            if chunk.chunk_id in fused_scores:
                fused_scores[chunk.chunk_id] += score
                chunks[chunk.chunk_id].score = fused_scores[chunk.chunk_id]
            else:
                fused_scores[chunk.chunk_id] = score
                chunk.score = score
                chunks[chunk.chunk_id] = chunk

        return sorted(
            chunks.values(),
            key=lambda chunk: chunk.score,
            reverse=True,
        )[:limit]

    def search(
        self,
        query_embedding: list[float],
        question: str,
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Default search method used by the application.
        """

        return self.hybrid_search(
            query_embedding=query_embedding,
            question=question,
            limit=limit,
        )
