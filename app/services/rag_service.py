import time

from app.core.config import settings
from app.core.logger import logger
from app.schemas.chat_message import ChatMessage
from app.schemas.chat_response import ChatResponse
from app.schemas.source import Source
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.query_rewrite_service import QueryRewriteService
from app.services.retriever_service import RetrieverService


class RAGService:
    """Coordinates query rewriting, retrieval, prompting, and generation."""

    def __init__(
        self,
        retriever: RetrieverService,
        prompt_service: PromptService,
        llm_service: LLMService,
        query_rewriter: QueryRewriteService,
    ) -> None:
        self.retriever = retriever
        self.prompt_service = prompt_service
        self.llm_service = llm_service
        self.query_rewriter = query_rewriter

    def answer(
        self,
        question: str,
        history: list[ChatMessage] | None = None,
    ) -> ChatResponse:
        """Generate an answer grounded in retrieved document context."""

        history = history or []
        start = time.perf_counter()

        logger.info("Starting RAG request")

        rewritten_question = self.query_rewriter.rewrite(
            question=question,
            history=[
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in history
            ],
        )

        logger.info("Retrieving context for rewritten question")
        chunks = self.retriever.retrieve(rewritten_question)

        if not chunks:
            logger.info(
                "No relevant document context found; returning grounded fallback"
            )
            return ChatResponse(
                answer="I don't know.",
                sources=[],
            )

        context: list[str] = []
        context_chars = 0

        for chunk in chunks:
            remaining = settings.max_context_chars - context_chars

            if remaining <= 0:
                break

            content = chunk.content[:remaining]
            context.append(
                f"[Source: {chunk.filename}, chunk {chunk.chunk_index}]\n"
                f"{content}"
            )
            context_chars += len(content)

        prompt = self.prompt_service.build_prompt(
            question=question,
            context=context,
            history=history[-4:],
        )

        logger.info(
            "Context assembled from %d chunks (%d chars)",
            len(context),
            context_chars,
        )

        answer = self.llm_service.generate(prompt)

        sources = [
            Source(
                document_id=chunk.document_id,
                filename=chunk.filename,
                chunk_id=chunk.chunk_id,
                chunk_index=chunk.chunk_index,
                score=chunk.score,
                preview=chunk.content[:250].strip(),
            )
            for chunk in chunks
        ]

        logger.info(
            "RAG request completed in %.3f seconds",
            time.perf_counter() - start,
        )

        return ChatResponse(
            answer=answer,
            sources=sources,
        )
