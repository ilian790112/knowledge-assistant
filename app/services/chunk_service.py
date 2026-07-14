class ChunkService:
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def chunk_text(self, text: str) -> list[str]:
        """
        Splits text into fixed-size chunks.
        """

        chunks = []

        for i in range(0, len(text), self.chunk_size):
            chunks.append(text[i:i + self.chunk_size])

        return chunks