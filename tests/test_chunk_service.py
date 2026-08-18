import unittest

from app.services.chunk_service import ChunkService


class ChunkServiceTests(unittest.TestCase):
    def test_empty_text_yields_no_chunks(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)

        self.assertEqual(list(service.chunk_text("")), [])

    def test_chunk_text_returns_a_lazy_iterator(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)

        chunks = service.chunk_text("abcdefghijklmnopqrst")

        self.assertTrue(hasattr(chunks, "__iter__"))
        self.assertEqual(next(chunks), "abcdefghij")

    def test_chunks_overlap(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)
        chunks = list(service.chunk_text("abcdefghijklmnopqrst"))

        self.assertEqual(chunks[0], "abcdefghij")
        self.assertEqual(chunks[1], "ijklmnopqr")
        self.assertEqual(chunks[0][-2:], chunks[1][:2])

    def test_short_text_produces_one_chunk(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)

        self.assertEqual(
            list(service.chunk_text("hello")),
            ["hello"],
        )

    def test_whitespace_only_text_produces_no_chunks(self) -> None:
        service = ChunkService(chunk_size=10, overlap=2)

        self.assertEqual(
            list(service.chunk_text("   \n\t   ")),
            [],
        )

    def test_invalid_chunk_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ChunkService(chunk_size=0, overlap=0)

        with self.assertRaises(ValueError):
            ChunkService(chunk_size=-1, overlap=0)

    def test_negative_overlap_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ChunkService(chunk_size=10, overlap=-1)

    def test_overlap_equal_to_chunk_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ChunkService(chunk_size=10, overlap=10)

    def test_overlap_greater_than_chunk_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ChunkService(chunk_size=10, overlap=11)


if __name__ == "__main__":
    unittest.main()
