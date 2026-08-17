from fastapi import APIRouter, Depends

from app.core.dependencies import get_search_service
from app.schemas.search import SearchRequest
from app.services.search_service import SearchService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post("/")
def semantic_search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
):
    """Search the indexed knowledge base using hybrid retrieval."""

    return service.search(
        question=request.question,
        limit=request.limit,
    )
