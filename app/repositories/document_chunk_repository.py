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
    ):
        self.db = db

    def save(
        self,
        chunk: DocumentChunk,
    ) -> DocumentChunk:
        """
        Save a single chunk.
        """

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    def save_many(
        self,
        chunks: list[DocumentChunk],
        batch_size: int = 100,
    ) -> list[DocumentChunk]:
        """
        Save chunks in batches instead of a huge transaction.
        """

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]

            self.db.add_all(batch)
            self.db.commit()

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
            .where(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_chunks_without_embeddings(
        self,
    ) -> list[DocumentChunk]:
        """
        Return chunks missing embeddings.
        """

        statement = (
            select(DocumentChunk)
            .where(
                DocumentChunk.embedding.is_(None)
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def commit(
        self,
    ) -> None:
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

    def delete_by_document_id(
        self,
        document_id: int,
    ) -> None:
        """
        Delete all chunks for a document.
        """

        (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .delete(
                synchronize_session=False
            )
        )

        self.db.commit()