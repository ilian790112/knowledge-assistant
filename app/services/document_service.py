from fastapi import HTTPException, UploadFile

from app.processors.document_processor import DocumentProcessor
from app.schemas.processing import ProcessingResult


class DocumentService:

    def __init__(self, processor: DocumentProcessor):
        self.processor = processor

    def upload_document(
        self,
        uploaded_file: UploadFile,
    ) -> ProcessingResult:

        self._validate_pdf(uploaded_file)

        return self.processor.process(uploaded_file)

    def get_documents(self):
        return self.processor.repository.get_all()

    @staticmethod
    def _validate_pdf(uploaded_file: UploadFile):

        if uploaded_file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )