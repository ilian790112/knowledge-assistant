import unittest

from app.schemas.chat_message import ChatMessage
from app.services.prompt_service import PromptService


class PromptServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.service = PromptService()

    def test_prompt_contains_question_and_document_context(self) -> None:
        prompt = self.service.build_prompt(
            question="What is the main idea?",
            context=["The document explains retrieval-augmented generation."],
        )

        self.assertIn("What is the main idea?", prompt)
        self.assertIn(
            "The document explains retrieval-augmented generation.",
            prompt,
        )
        self.assertIn("I don't know.", prompt)

    def test_prompt_marks_missing_conversation_history(self) -> None:
        prompt = self.service.build_prompt(
            question="What does this mean?",
            context=["A fact from the document."],
        )

        self.assertIn("(No previous conversation)", prompt)

    def test_prompt_formats_conversation_history(self) -> None:
        history = [
            ChatMessage(role="user", content="What is RAG?"),
            ChatMessage(role="assistant", content="It retrieves context."),
        ]

        prompt = self.service.build_prompt(
            question="Explain it again.",
            context=["RAG retrieves relevant document context."],
            history=history,
        )

        self.assertIn("User: What is RAG?", prompt)
        self.assertIn("Assistant: It retrieves context.", prompt)
        self.assertNotIn("(No previous conversation)", prompt)

    def test_prompt_uses_only_the_last_ten_history_messages(self) -> None:
        history = [
            ChatMessage(role="user", content=f"message-{index}")
            for index in range(12)
        ]

        prompt = self.service.build_prompt(
            question="Follow up",
            context=["Document fact"],
            history=history,
        )

        self.assertNotIn("message-0", prompt)
        self.assertNotIn("message-1", prompt)
        self.assertIn("message-2", prompt)
        self.assertIn("message-11", prompt)


if __name__ == "__main__":
    unittest.main()
