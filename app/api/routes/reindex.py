from fastapi import APIRouter, Depends

from app.core.dependencies import get_reindex_service
from app.services.reindex_service import ReindexService

router = APIRouter(
    prefix="/reindex",
    tags=["Reindex"],
)


@router.post("/embeddings")
def reindex_embeddings(
    service: ReindexService = Depends(get_reindex_service),
):
    updated = service.reindex_embeddings()

    return {
        "message": "Embeddings reindexed successfully.",
        "updated_chunks": updated,
    }