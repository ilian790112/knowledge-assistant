from fastapi import APIRouter

from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

service = DocumentService()


@router.get("/")
async def get_documents():
    return service.get_documents()