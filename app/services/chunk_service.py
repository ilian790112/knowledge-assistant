from collections.abc import Iterator


class ChunkService:
    """
    Splits text into overlapping chunks for semantic retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(
        self,
        text: str,
    ) -> Iterator[str]:
        """
        Yield chunks one at a time instead of returning a list.
        """

        if not text:
            return

        step = self.chunk_size - self.overlap

        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]

            if chunk.strip():
                yield chunk