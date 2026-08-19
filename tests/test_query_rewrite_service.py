import unittest
from unittest.mock import MagicMock

from app.services.query_rewrite_service import QueryRewriteService


class QueryRewriteServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.llm_service = MagicMock()
        self.service = QueryRewriteService(self.llm_service)

    def test_returns_original_question_without_history(self) -> None:
        question = "What is RAG?"

        result = self.service.rewrite(question=question, history=[])

        self.assertEqual(result, question)
        self.llm_service.generate.assert_not_called()

    def test_rewrites_question_using_conversation_history(self) -> None:
        self.llm_service.generate.return_value = "What does RAG mean in this project?"
        history = [
            {"role": "user", "content": "Tell me about retrieval."},
            {"role": "assistant", "content": "It finds relevant chunks."},
        ]

        result = self.service.rewrite(
            question="What does it do?",
            history=history,
        )

        self.assertEqual(result, "What does RAG mean in this project?")
        self.llm_service.generate.assert_called_once()
        prompt = self.llm_service.generate.call_args.args[0]
        self.assertIn("User: Tell me about retrieval.", prompt)
        self.assertIn("Assistant: It finds relevant chunks.", prompt)
        self.assertIn("What does it do?", prompt)
        self.assertIn("Return ONLY the rewritten question.", prompt)

    def test_strips_llm_whitespace(self) -> None:
        self.llm_service.generate.return_value = "  Standalone question  \n"

        result = self.service.rewrite(
            question="What about it?",
            history=[{"role": "user", "content": "Explain X."}],
        )

        self.assertEqual(result, "Standalone question")


if __name__ == "__main__":
    unittest.main()
