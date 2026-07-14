from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")


class LocalStorage:

    def save_file(self, uploaded_file):

        UPLOAD_DIR.mkdir(exist_ok=True)

        destination = UPLOAD_DIR / uploaded_file.filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        return destination