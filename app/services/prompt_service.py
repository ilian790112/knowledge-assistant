class PromptService:
    """
    Builds prompts for the language model.
    """

    def build_prompt(
        self,
        question: str,
        context: list[str],
    ) -> str:
        """
        Build a RAG prompt from the retrieved context.
        """

        joined_context = "\n\n".join(context)

        return f"""You are a helpful AI assistant.

Use ONLY the context below to answer the user's question.

If the answer cannot be found in the context, say that you don't know.

Context:
{joined_context}

Question:
{question}

Answer:
"""