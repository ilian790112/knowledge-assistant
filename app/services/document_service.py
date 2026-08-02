from pathlib import Path

from fastapi import HTTPException

from app.core.logger import logger
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
        temp_path: str,
        filename: str,
        content_type: str,
    ) -> ProcessingResult | None:
        """
        Process a previously uploaded PDF.

        This method is executed as a FastAPI background task.
        """

        try:
            self._validate_pdf(content_type)

            logger.info(
                "Started processing document: %s",
                filename,
            )

            result = self.processor.process(
                temp_path=temp_path,
                filename=filename,
                content_type=content_type,
            )

            logger.info(
                "Finished processing document: %s",
                filename,
            )

            return result

        except Exception:
            logger.exception(
                "Failed to process document: %s",
                filename,
            )
            return None

        finally:
            temp_file = Path(temp_path)

            if temp_file.exists():
                temp_file.unlink()

    def get_documents(self):
        """
        Return all uploaded documents.
        """

        return (
            self.processor.indexing_processor
            .document_repository
            .get_all()
        )

    def delete_document(
        self,
        document_id: int,
    ) -> bool:
        """
        Delete a document, its chunks and its PDF.
        """

        document_repository = (
            self.processor.indexing_processor
            .document_repository
        )

        chunk_repository = (
            self.processor.indexing_processor
            .chunk_repository
        )

        document = document_repository.get_by_id(document_id)

        if document is None:
            return False

        chunk_repository.delete_by_document_id(document_id)

        pdf_path = Path(document.path)

        if pdf_path.exists():
            pdf_path.unlink()

        document_repository.delete(document)

        return True

    @staticmethod
    def _validate_pdf(
        content_type: str,
    ) -> None:
        """
        Validate uploaded file.
        """

        if content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed.",
            )