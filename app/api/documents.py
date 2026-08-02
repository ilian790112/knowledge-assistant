from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

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
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    """
    Upload and process a PDF.
    """

    result = service.upload_document(file)

    if result is None:
        raise HTTPException(
            status_code=500,
            detail="Failed to process document.",
        )

    return result


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