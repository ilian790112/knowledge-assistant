from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")


class LocalStorage:
    """
    Stores uploaded files on disk.
    """

    def save_file(
        self,
        temp_path: str,
        filename: str,
    ) -> Path:
        """
        Move a temporary uploaded file into permanent storage.
        """

        UPLOAD_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = UPLOAD_DIR / filename

        shutil.move(
            temp_path,
            destination,
        )

        return destination