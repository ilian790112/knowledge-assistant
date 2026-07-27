from app.services.llm_service import LLMService


class QueryRewriteService:
    """
    Rewrites follow-up questions into standalone questions.
    """

    def __init__(
        self,
        llm_service: LLMService,
    ) -> None:
        self.llm_service = llm_service

    def rewrite(
        self,
        question: str,
        history: list[dict[str, str]],
    ) -> str:
        if not history:
            return question

        conversation = "\n".join(
            f"{message['role'].capitalize()}: {message['content']}"
            for message in history
        )

        prompt = f"""
You rewrite follow-up questions.

Given the conversation below, rewrite the LAST user question into a standalone question.

Rules:
- Do NOT answer the question.
- Preserve the original intent.
- Replace pronouns like "it", "they", "this", "that" with their actual meaning.
- Return ONLY the rewritten question.

Conversation:

{conversation}

Last user question:

{question}

Standalone question:
"""

        return self.llm_service.generate(prompt).strip()