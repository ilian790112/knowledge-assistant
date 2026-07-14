from fastapi import APIRouter, Depends
from fastapi import UploadFile, File

from app.core.dependencies import get_document_service
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/")
async def get_documents(
    service: DocumentService = Depends(get_document_service)
):
    return service.get_documents()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service)
):

    return service.upload_document(file)