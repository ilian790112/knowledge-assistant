from pathlib import Path

from fastapi import HTTPException
from fastapi import UploadFile

from app.processors.document_processor import DocumentProcessor
from app.schemas.processing import ProcessingResult


class DocumentService:
    """
    Service responsible for document management.
    """

    def __init__(
        self,
        processor: DocumentProcessor,
    ):
        self.processor = processor

    def upload_document(
        self,
        uploaded_file: UploadFile,
    ) -> ProcessingResult:
        """
        Upload and process a PDF.
        """

        self._validate_pdf(uploaded_file)

        return self.processor.process(uploaded_file)

    def get_documents(self):
        """
        Return all uploaded documents.
        """

        return self.processor.indexing_processor.document_repository.get_all()

    def delete_document(
        self,
        document_id: int,
    ) -> bool:
        """
        Delete a document, its chunks and its PDF.
        """

        document_repository = (
            self.processor.indexing_processor.document_repository
        )

        chunk_repository = (
            self.processor.indexing_processor.chunk_repository
        )

        document = document_repository.get_by_id(document_id)

        if document is None:
            return False

        # Delete all chunks
        chunk_repository.delete_by_document_id(document_id)

        # Delete PDF from disk
        pdf_path = Path(document.path)

        if pdf_path.exists():
            pdf_path.unlink()

        # Delete database record
        document_repository.delete(document)

        return True

    @staticmethod
    def _validate_pdf(
        uploaded_file: UploadFile,
    ):
        if uploaded_file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )