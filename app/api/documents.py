from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.core.config import settings
from app.core.dependencies import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

UPLOAD_BUFFER_SIZE = 1024 * 1024


@router.get("/")
async def get_documents(
    service: DocumentService = Depends(get_document_service),
):
    """Return all uploaded documents."""

    return service.get_documents()


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """
    Stream the upload to a temporary file, then process it in the background.
    """

    filename = file.filename or "document.pdf"
    content_type = file.content_type or ""

    if content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    suffix = Path(filename).suffix.lower()

    if suffix != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file must have a .pdf extension.",
        )

    temp_path: str | None = None
    total_bytes = 0

    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            temp_path = tmp.name

            while True:
                chunk = await file.read(UPLOAD_BUFFER_SIZE)

                if not chunk:
                    break

                total_bytes += len(chunk)

                if total_bytes > settings.max_upload_size:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=(
                            "File is too large. Maximum size is "
                            f"{settings.max_upload_size // (1024 * 1024)} MB."
                        ),
                    )

                tmp.write(chunk)

    except Exception:
        if temp_path:
            Path(temp_path).unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    background_tasks.add_task(
        service.upload_document,
        temp_path,
        filename,
        content_type,
    )

    return {
        "message": "Upload accepted and processing started.",
        "status": "processing",
        "filename": filename,
    }


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
):
    """Delete a document and all of its chunks."""

    deleted = service.delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )
