from collections.abc import Iterator


class ChunkService:
    """
    Splits text into overlapping chunks for semantic retrieval.
    """

    def __init__(
        self,
        chunk_size: int = 1200,
        overlap: int = 200,
    ) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(
        self,
        text: str,
    ) -> Iterator[str]:
        """
        Yield overlapping chunks without keeping all chunks in memory.
        """

        if not text:
            return

        step = self.chunk_size - self.overlap

        for start in range(0, len(text), step):
            chunk = text[start:start + self.chunk_size]

            if chunk.strip():
                yield chunk
