from sqlalchemy import delete
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    """Handles persistence operations for document chunks."""

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def save(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
        """Save a single chunk."""

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)
        return chunk

    def save_many(
        self,
        chunks: list[DocumentChunk],
        batch_size: int = 32,
    ) -> list[DocumentChunk]:
        """Persist chunks in bounded batches."""

        if not chunks:
            return []

        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0.")

        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            self.db.add_all(batch)
            self.db.commit()

        return chunks

    def get_by_document(
        self,
        document_id: int,
    ) -> list[DocumentChunk]:
        """Return all chunks belonging to a document."""

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )
        return list(self.db.scalars(statement).all())

    def get_chunks_without_embeddings(self) -> list[DocumentChunk]:
        """Return chunks missing embeddings."""

        statement = select(DocumentChunk).where(
            DocumentChunk.embedding.is_(None)
        )
        return list(self.db.scalars(statement).all())

    def commit(self) -> None:
        self.db.commit()

    def delete_by_document_id(
        self,
        document_id: int,
    ) -> None:
        """Delete all chunks for a document with one SQL statement."""

        self.db.execute(
            delete(DocumentChunk).where(
                DocumentChunk.document_id == document_id
            )
        )
        self.db.commit()
