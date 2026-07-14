from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.processing import ProcessingResult


class DocumentRepository:
    """
    Handles all database operations for documents.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, result: ProcessingResult) -> Document:
        """
        Save a processed document.
        """

        document = Document(
            filename=result.filename,
            path=result.path,
            status=result.status,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_all(self) -> list[Document]:
        """
        Return all documents ordered by newest first.
        """

        statement = (
            select(Document)
            .order_by(Document.id.desc())
        )

        return list(self.db.scalars(statement).all())

    def get_by_id(self, document_id: int) -> Document | None:
        """
        Return a document by ID.
        """

        statement = (
            select(Document)
            .where(Document.id == document_id)
        )

        return self.db.scalar(statement)

    def delete(self, document: Document) -> None:
        """
        Delete a document.
        """

        self.db.delete(document)
        self.db.commit()