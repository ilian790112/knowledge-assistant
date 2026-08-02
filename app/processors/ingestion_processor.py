from pathlib import Path

from app.services.pdf_service import PDFService
from app.storage.local_storage import LocalStorage
from app.utils.text_cleaner import clean_text


class IngestionProcessor:
    """
    Responsible for getting clean text from an uploaded document.
    """

    def __init__(
        self,
        storage: LocalStorage,
        pdf_service: PDFService,
    ):
        self.storage = storage
        self.pdf_service = pdf_service

    def ingest(
        self,
        temp_path: str,
        filename: str,
    ) -> tuple[Path, str]:
        """
        Save the file and return cleaned text.
        """

        saved_path = self.storage.save_file(
            temp_path=temp_path,
            filename=filename,
        )

        extracted_text = self.pdf_service.extract_text(
            str(saved_path)
        )

        cleaned_text = clean_text(extracted_text)

        return saved_path, cleaned_text