from app.services.chunk_service import ChunkService


class ChunkProcessor:
    """
    Responsible for splitting text into chunks.
    """

    def __init__(self, chunk_service: ChunkService):
        self.chunk_service = chunk_service

    def process(
        self,
        text: str,
    ) -> list[str]:

        return self.chunk_service.chunk_text(text)