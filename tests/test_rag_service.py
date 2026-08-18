import unittest
from unittest.mock import MagicMock

from app.schemas.chat_message import ChatMessage
from app.services.rag_service import RAGService


class RAGServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.retriever = MagicMock()
        self.prompt_service = MagicMock()
        self.llm_service = MagicMock()
        self.query_rewriter = MagicMock()

        self.service = RAGService(
            retriever=self.retriever,
            prompt_service=self.prompt_service,
            llm_service=self.llm_service,
            query_rewriter=self.query_rewriter,
        )

    def test_returns_grounded_fallback_when_no_context_is_retrieved(self) -> None:
        self.query_rewriter.rewrite.return_value = "rewritten question"
        self.retriever.retrieve.return_value = []

        response = self.service.answer("What is this?")

        self.assertEqual(response.answer, "I don't know.")
        self.assertEqual(response.sources, [])
        self.llm_service.generate.assert_not_called()
        self.prompt_service.build_prompt.assert_not_called()

    def test_rewrites_question_with_conversation_history(self) -> None:
        self.query_rewriter.rewrite.return_value = "rewritten question"
        self.retriever.retrieve.return_value = []

        history = [
            ChatMessage(role="user", content="Tell me about chapter one."),
            ChatMessage(role="assistant", content="Chapter one discusses X."),
        ]

        self.service.answer("What about chapter two?", history=history)

        self.query_rewriter.rewrite.assert_called_once_with(
            question="What about chapter two?",
            history=[
                {"role": "user", "content": "Tell me about chapter one."},
                {"role": "assistant", "content": "Chapter one discusses X."},
            ],
        )

    def test_generates_answer_from_retrieved_context(self) -> None:
        self.query_rewriter.rewrite.return_value = "rewritten question"
        self.llm_service.generate.return_value = "Grounded answer"

        chunk = MagicMock(
            document_id=7,
            filename="book.pdf",
            chunk_id=42,
            chunk_index=3,
            content="Relevant document content.",
            score=0.91,
        )
        self.retriever.retrieve.return_value = [chunk]
        self.prompt_service.build_prompt.return_value = "prompt"

        response = self.service.answer("What does the document say?")

        self.assertEqual(response.answer, "Grounded answer")
        self.assertEqual(len(response.sources), 1)
        self.assertEqual(response.sources[0].document_id, 7)
        self.assertEqual(response.sources[0].filename, "book.pdf")
        self.assertEqual(response.sources[0].chunk_id, 42)
        self.assertEqual(response.sources[0].chunk_index, 3)
        self.assertEqual(response.sources[0].score, 0.91)
        self.assertEqual(
            response.sources[0].preview,
            "Relevant document content.",
        )

        self.prompt_service.build_prompt.assert_called_once()
        self.llm_service.generate.assert_called_once_with("prompt")

    def test_limits_context_to_configured_maximum(self) -> None:
        self.query_rewriter.rewrite.return_value = "rewritten question"
        self.llm_service.generate.return_value = "answer"
        self.prompt_service.build_prompt.return_value = "prompt"

        first = MagicMock(
            document_id=1,
            filename="first.pdf",
            chunk_id=1,
            chunk_index=0,
            content="A" * 5000,
            score=0.9,
        )
        second = MagicMock(
            document_id=2,
            filename="second.pdf",
            chunk_id=2,
            chunk_index=1,
            content="B" * 5000,
            score=0.8,
        )
        self.retriever.retrieve.return_value = [first, second]

        self.service.answer("Question")

        context = self.prompt_service.build_prompt.call_args.kwargs["context"]
        combined = "\n".join(context)

        self.assertLessEqual(len(combined), 6000 + 100)
        self.assertIn("[Source: first.pdf, chunk 0]", combined)
        self.assertIn("[Source: second.pdf, chunk 1]", combined)


if __name__ == "__main__":
    unittest.main()
