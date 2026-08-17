from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document
from app.schemas.processing import ProcessingResult


class DocumentRepository:
    """Handles persistence operations for documents."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def save(
        self,
        result: ProcessingResult,
    ) -> Document:
        """Create and persist a document record."""

        document = Document(
            filename=result.filename,
            path=result.path,
            status=result.status,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def update_status(
        self,
        document_id: int,
        status: str,
    ) -> None:
        """Update processing status for an existing document."""

        document = self.get_by_id(document_id)

        if document is None:
            return

        document.status = status
        self.db.commit()

    def get_all(self) -> list[Document]:
        """Return all documents ordered by newest first."""

        statement = select(Document).order_by(Document.id.desc())
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        document_id: int,
    ) -> Document | None:
        """Return a document by ID."""

        statement = select(Document).where(Document.id == document_id)
        return self.db.scalar(statement)

    def delete(
        self,
        document: Document,
    ) -> None:
        """Delete a document record."""

        self.db.delete(document)
        self.db.commit()
