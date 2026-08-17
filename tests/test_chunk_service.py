import unittest

from app.services.chunk_service import ChunkService


class ChunkServiceTests(unittest.TestCase):
    def test_empty_text_yields_no_chunks(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)

        self.assertEqual(list(service.chunk_text("")), [])

    def test_chunks_overlap(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)
        chunks = list(service.chunk_text("abcdefghijklmnopqrst"))

        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1][:2], chunks[0][-2:])

    def test_invalid_overlap_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ChunkService(chunk_size=10, overlap=10)


if __name__ == "__main__":
    unittest.main()
