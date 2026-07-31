import time

from app.core.logger import logger
from app.schemas.chat_message import ChatMessage
from app.schemas.chat_response import ChatResponse
from app.schemas.source import Source
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.services.query_rewrite_service import QueryRewriteService
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
        """
        Generate an answer using Retrieval-Augmented Generation.
        """

        history = history or []

        start = time.perf_counter()

        logger.info("=" * 80)
        logger.info("NEW RAG REQUEST")
        logger.info("=" * 80)
        logger.info("Original question: %s", question)

        try:
            # ------------------------------------------------------------------
            # Rewrite
            # ------------------------------------------------------------------

            logger.info("Rewriting question...")

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

            logger.info(
                "Standalone question: %s",
                rewritten_question,
            )

            # ------------------------------------------------------------------
            # Retrieval
            # ------------------------------------------------------------------

            logger.info("Retrieving document chunks...")

            chunks = self.retriever.retrieve(
                rewritten_question,
            )

            retrieval_end = time.perf_counter()

            logger.info(
                "Retrieval completed in %.3f seconds",
                retrieval_end - start,
            )

            logger.info(
                "Retrieved %d chunks",
                len(chunks),
            )

            # ------------------------------------------------------------------
            # Prompt
            # ------------------------------------------------------------------

            logger.info("Building prompt...")

            MAX_CHARS_PER_CHUNK = 700

            context = [
                chunk.content[:MAX_CHARS_PER_CHUNK]
                for chunk in chunks
            ]

            prompt = self.prompt_service.build_prompt(
                question=question,
                context=context,
                history=history[-4:],
            )

            prompt_end = time.perf_counter()

            logger.info(
                "Prompt built in %.3f seconds",
                prompt_end - retrieval_end,
            )

            logger.info("=" * 80)
            logger.info("PROMPT SENT TO LLM")
            logger.info("=" * 80)
            logger.info(prompt)
            logger.info("=" * 80)

            # ------------------------------------------------------------------
            # LLM
            # ------------------------------------------------------------------

            logger.info("Generating answer...")

            answer = self.llm_service.generate(
                prompt,
            )

            llm_end = time.perf_counter()

            logger.info(
                "LLM completed in %.3f seconds",
                llm_end - prompt_end,
            )

            logger.info("=" * 80)
            logger.info("LLM RESPONSE")
            logger.info("=" * 80)
            logger.info(answer)
            logger.info("=" * 80)

            logger.info(
                "Total request time: %.3f seconds",
                llm_end - start,
            )

            # ------------------------------------------------------------------
            # Sources
            # ------------------------------------------------------------------

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

            return ChatResponse(
                answer=answer,
                sources=sources,
            )

        except Exception:
            logger.exception("=" * 80)
            logger.exception("RAG PIPELINE FAILED")
            logger.exception("=" * 80)
            raise