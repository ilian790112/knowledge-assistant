from app.schemas.chat_response import ChatResponse
from app.schemas.source import Source
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.retriever_service import RetrieverService


class RAGService:
    """
    Coordinates the Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        retriever: RetrieverService,
        prompt_service: PromptService,
        llm_service: LLMService,
    ) -> None:
        self.retriever = retriever
        self.prompt_service = prompt_service
        self.llm_service = llm_service

    def answer(
        self,
        question: str,
    ) -> ChatResponse:
        """
        Generate an answer using retrieval-augmented generation.
        """

        chunks = self.retriever.retrieve(question)

        context = [
            chunk.content
            for chunk in chunks
        ]

        prompt = self.prompt_service.build_prompt(
            question=question,
            context=context,
        )

        answer = self.llm_service.generate(prompt)

        sources = [
            Source(
    document_id=chunk.document_id,
    filename=chunk.filename,
    chunk_id=chunk.chunk_id,
    chunk_index=chunk.chunk_index,
    score=chunk.score,
)
            for chunk in chunks
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
        )