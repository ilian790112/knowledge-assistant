from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    """
    Handles all database operations for document chunks.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, chunk: DocumentChunk) -> DocumentChunk:
        """
        Save a single document chunk.
        """

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    def save_many(
        self,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        """
        Save multiple chunks in one transaction.
        """

        self.db.add_all(chunks)
        self.db.commit()

        for chunk in chunks:
            self.db.refresh(chunk)

        return chunks

    def get_by_document(
        self,
        document_id: int,
    ) -> list[DocumentChunk]:
        """
        Return all chunks belonging to a document.
        """

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_index)
        )

        return list(self.db.scalars(statement).all())

    def get_chunks_without_embeddings(self) -> list[DocumentChunk]:
        """
        Return all document chunks that do not yet have an embedding.
        """

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
        )

        return list(self.db.scalars(statement).all())

    def commit(self) -> None:
        """
        Commit the current transaction.
        """

        self.db.commit()

    def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        """
        Delete all chunks for a document.
        """

        chunks = self.get_by_document(document_id)

        for chunk in chunks:
            self.db.delete(chunk)

        self.db.commit()