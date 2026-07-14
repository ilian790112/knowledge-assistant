from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.schemas.retrieved_chunk import RetrievedChunk


class SearchRepository:
    """
    Performs semantic search against stored document chunks.
    """

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Return the most similar chunks together with their similarity score.
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

        results: list[RetrievedChunk] = []

        for chunk, filename, distance in rows:
            results.append(
                RetrievedChunk(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    filename=filename,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    score=float(1 - distance),
                )
            )

        return results