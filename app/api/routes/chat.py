from fastapi import APIRouter, Depends

from app.core.dependencies import get_rag_service
from app.schemas.chat import ChatRequest
from app.schemas.chat_response import ChatResponse
from app.services.rag_service import RAGService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
) -> ChatResponse:
    """
    Answer a user's question using Retrieval-Augmented Generation.
    """

    return rag_service.answer(request.question)