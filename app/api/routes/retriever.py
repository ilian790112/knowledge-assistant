from fastapi import APIRouter, Depends

from app.core.dependencies import get_retriever_service
from app.schemas.search import SearchRequest
from app.services.retriever_service import RetrieverService

router = APIRouter(
    prefix="/retrieve",
    tags=["Retriever"],
)


@router.post("/")
def retrieve(
    request: SearchRequest,
    service: RetrieverService = Depends(
        get_retriever_service
    ),
):
    return service.retrieve(
        question=request.question,
        limit=request.limit,
    )