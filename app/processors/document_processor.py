from fastapi import UploadFile

from app.processors.chunk_processor import ChunkProcessor
from app.processors.embedding_processor import EmbeddingProcessor
from app.processors.indexing_processor import IndexingProcessor
from app.processors.ingestion_processor import IngestionProcessor
from app.schemas.processing import ProcessingResult


class DocumentProcessor:
    """
    Coordinates the complete document processing pipeline.

    Pipeline:
        Upload File
            ↓
        Save File
            ↓
        Extract Text
            ↓
        Chunk Text
            ↓
        Generate Embeddings
            ↓
        Store in Database
    """

    def __init__(
        self,
        ingestion_processor: IngestionProcessor,
        chunk_processor: ChunkProcessor,
        embedding_processor: EmbeddingProcessor,
        indexing_processor: IndexingProcessor,
    ):
        self.ingestion_processor = ingestion_processor
        self.chunk_processor = chunk_processor
        self.embedding_processor = embedding_processor
        self.indexing_processor = indexing_processor

    def process(
        self,
        uploaded_file: UploadFile,
    ):
        """
        Execute the complete AI document processing pipeline.
        """

        # Step 1 - Save file & extract text
        saved_path, cleaned_text = self.ingestion_processor.ingest(
            uploaded_file
        )

        # Step 2 - Split text into chunks
        chunks = self.chunk_processor.process(cleaned_text)

        # Step 3 - Generate embeddings
        embedding_results = self.embedding_processor.process(chunks)

        # Step 4 - Build processing metadata
        result = ProcessingResult(
            filename=uploaded_file.filename,
            content_type=uploaded_file.content_type,
            path=str(saved_path),
            status="processed",
            characters=len(cleaned_text),
            chunks=len(chunks),
            embedding_dimensions=(
                len(embedding_results[0].embedding)
                if embedding_results
                else 0
            ),
            embedding_preview=(
                embedding_results[0].embedding[:10]
                if embedding_results
                else []
            ),
            preview=(
                embedding_results[0].content[:500]
                if embedding_results
                else ""
            ),
        )

        # Step 5 - Persist document, chunks, and embeddings
        return self.indexing_processor.process(
            result=result,
            embedding_results=embedding_results,
        )