from tempfile import NamedTemporaryFile
from pathlib import Path

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)

from app.core.dependencies import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/")
async def get_documents(
    service: DocumentService = Depends(get_document_service),
):
    """
    Return all uploaded documents.
    """
    try:
        return service.get_documents()
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """
    Save the uploaded file first, then process it in the background.
    """

    suffix = Path(file.filename).suffix

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    background_tasks.add_task(
        service.upload_document,
        temp_path,
        file.filename,
        file.content_type,
    )

    return {
        "message": "Upload started.",
        "status": "processing",
    }


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: int,
    service: DocumentService = Depends(get_document_service),
):
    """
    Delete a document and all of its chunks.
    """

    deleted = service.delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found.",
        )