from pathlib import Path
import shutil

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
        Move the temporary uploaded file into permanent storage
        and return the cleaned text.
        """

        destination = self.storage.storage_path / filename
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            temp_path,
            destination,
        )

        extracted_text = self.pdf_service.extract_text(
            str(destination)
        )

        cleaned_text = clean_text(
            extracted_text
        )

        return destination, cleaned_text