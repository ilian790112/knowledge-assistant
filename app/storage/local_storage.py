from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")


class LocalStorage:

    def save_file(
        self,
        temp_path: str,
        filename: str,
    ) -> Path:
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