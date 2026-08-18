import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

from fastapi import HTTPException


# DocumentService imports DocumentProcessor only for its type annotation.
# Replace that module during this unit test so document-service tests stay
# independent from optional/heavy infrastructure such as pgvector,
# SQLAlchemy models, and sentence-transformers.
if "app.processors.document_processor" not in sys.modules:
    document_processor_stub = ModuleType("app.processors.document_processor")

    class DocumentProcessor:  # noqa: D101
        pass

    document_processor_stub.DocumentProcessor = DocumentProcessor
    sys.modules["app.processors.document_processor"] = document_processor_stub


from app.services.document_service import DocumentService


class DocumentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.processor = MagicMock()
        self.service = DocumentService(self.processor)

    def test_rejects_non_pdf_before_processing(self) -> None:
        with self.assertRaises(HTTPException) as context:
            self.service.upload_document(
                temp_path="/tmp/example.txt",
                filename="example.txt",
                content_type="text/plain",
            )

        self.assertEqual(context.exception.status_code, 400)
        self.processor.process.assert_not_called()

    def test_upload_processing_removes_temporary_file(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = tmp.name

        self.processor.process.return_value = MagicMock()

        result = self.service.upload_document(
            temp_path=temp_path,
            filename="example.pdf",
            content_type="application/pdf",
        )

        self.assertIsNotNone(result)
        self.assertFalse(Path(temp_path).exists())
        self.processor.process.assert_called_once_with(
            temp_path=temp_path,
            filename="example.pdf",
            content_type="application/pdf",
        )

    def test_processing_error_is_reraised_and_temp_file_is_removed(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = tmp.name

        error = RuntimeError("processing failed")
        self.processor.process.side_effect = error

        with self.assertRaises(RuntimeError) as context:
            self.service.upload_document(
                temp_path=temp_path,
                filename="example.pdf",
                content_type="application/pdf",
            )

        self.assertIs(context.exception, error)
        self.assertFalse(Path(temp_path).exists())

    def test_delete_missing_document_returns_false(self) -> None:
        self.processor.indexing_processor.document_repository.get_by_id.return_value = None

        self.assertFalse(self.service.delete_document(123))
        self.processor.indexing_processor.chunk_repository.delete_by_document_id.assert_not_called()

    def test_delete_document_removes_chunks_file_and_record(self) -> None:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            pdf_path = tmp.name

        document = MagicMock(id=123, path=pdf_path)
        document_repository = self.processor.indexing_processor.document_repository
        chunk_repository = self.processor.indexing_processor.chunk_repository
        document_repository.get_by_id.return_value = document

        self.assertTrue(self.service.delete_document(123))

        self.assertFalse(Path(pdf_path).exists())
        chunk_repository.delete_by_document_id.assert_called_once_with(123)
        document_repository.delete.assert_called_once_with(document)


if __name__ == "__main__":
    unittest.main()
