from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    """
    Handles all database operations for document chunks.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def save(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
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
        Save multiple document chunks.
        """

        self.db.add_all(chunks)
        self.db.commit()

        for chunk in chunks:
            self.db.refresh(chunk)

        return chunks

    def get_all(
        self,
    ) -> list[DocumentChunk]:
        """
        Return all document chunks.
        """

        statement = (
            select(DocumentChunk)
            .order_by(
                DocumentChunk.document_id,
                DocumentChunk.chunk_index,
            )
        )

        return list(self.db.scalars(statement).all())

    def get_by_document(
        self,
        document_id: int,
    ) -> list[DocumentChunk]:
        """
        Return all chunks belonging to a document.
        """

        statement = (
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id
            )
            .order_by(DocumentChunk.chunk_index)
        )

        return list(self.db.scalars(statement).all())

    def get_chunks_without_embeddings(
        self,
    ) -> list[DocumentChunk]:
        """
        Return chunks missing embeddings.
        """

        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.embedding.is_(None))
        )

        return list(self.db.scalars(statement).all())

    def commit(
        self,
    ) -> None:
        """
        Commit pending changes.
        """

        self.db.commit()

    def delete_by_document(
        self,
        document_id: int,
    ) -> None:
        """
        Delete all chunks belonging to a document.
        """

        (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .delete(synchronize_session=False)
        )

        self.db.commit()