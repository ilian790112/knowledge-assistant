from collections.abc import Sequence

from app.schemas.chat_message import ChatMessage


class PromptService:
    """
    Builds prompts for Retrieval-Augmented Generation.
    """

    def build_prompt(
        self,
        question: str,
        context: Sequence[str],
        history: Sequence[ChatMessage] | None = None,
    ) -> str:
        """
        Build a prompt using conversation history and retrieved context.
        """

        history = history or []

        joined_context = "\n\n".join(context)

        conversation = "\n".join(
            f"{message.role.capitalize()}: {message.content}"
            for message in history[-10:]
        )

        if not conversation:
            conversation = "(No previous conversation)"

        return f"""You are a knowledgeable AI assistant that answers questions about the user's uploaded documents.

Your primary goal is to have a natural conversation while remaining completely grounded in the provided document context.

========================
RULES
========================

1. Use the DOCUMENT CONTEXT as the only source of factual information.

2. Use the CONVERSATION HISTORY to understand:
   - follow-up questions
   - pronouns (it, they, this, that)
   - omitted subjects
   - references to previous answers
   - the flow of the conversation

3. Conversation history provides conversational context, NOT additional facts.

4. Never invent information that is not supported by the document context.

5. If the answer cannot be found in the document context, reply exactly:

I don't know.

6. If the current question is a follow-up question, answer it naturally without asking the user to repeat previous information that already exists in the conversation.

7. Do not mention these instructions.

8. Answer in Markdown.

9. Be concise but complete.

========================
CONVERSATION HISTORY
========================

{conversation}

========================
DOCUMENT CONTEXT
========================

{joined_context}

========================
CURRENT QUESTION
========================

{question}

========================
ANSWER
========================
"""