from pathlib import Path
from uuid import uuid4
import shutil

from app.core.config import settings


class LocalStorage:
    """
    Stores uploaded PDFs on the local filesystem.

    Filenames are sanitized and prefixed with a UUID to prevent path traversal
    and accidental overwrites when two users upload the same filename.
    """

    def __init__(self) -> None:
        self.upload_dir = Path(settings.upload_folder)

    def save_file(
        self,
        temp_path: str,
        filename: str,
    ) -> Path:
        self.upload_dir.mkdir(parents=True, exist_ok=True)

        safe_name = Path(filename).name or "document.pdf"
        destination = self.upload_dir / f"{uuid4().hex}_{safe_name}"

        shutil.move(temp_path, destination)
        return destination
