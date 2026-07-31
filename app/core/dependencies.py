from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.processors.chunk_processor import ChunkProcessor
from app.processors.document_processor import DocumentProcessor
from app.processors.embedding_processor import EmbeddingProcessor
from app.processors.indexing_processor import IndexingProcessor
from app.processors.ingestion_processor import IngestionProcessor
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.repositories.search_repository import SearchRepository
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService
from app.services.embedding_service import (
    embedding_service,
)
from app.services.llm_service import LLMService
from app.services.pdf_service import PDFService
from app.services.prompt_service import PromptService
from app.services.query_rewrite_service import (
    QueryRewriteService,
)
from app.services.rag_service import RAGService
from app.services.reindex_service import ReindexService
from app.services.retriever_service import RetrieverService
from app.services.search_service import SearchService
from app.storage.local_storage import LocalStorage


# Heavy services are created once.
llm_service = LLMService()
prompt_service = PromptService()
query_rewrite_service = QueryRewriteService(
    llm_service=llm_service,
)


def get_db() -> Generator[Session, None, None]:
    """
    Create a database session for each request.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_document_service(
    db: Session = Depends(get_db),
) -> DocumentService:
    """
    Create and wire all dependencies for the document pipeline.
    """

    document_repository = DocumentRepository(db)
    chunk_repository = DocumentChunkRepository(db)

    ingestion_processor = IngestionProcessor(
        storage=LocalStorage(),
        pdf_service=PDFService(),
    )

    chunk_processor = ChunkProcessor(
        chunk_service=ChunkService(),
    )

    embedding_processor = EmbeddingProcessor(
        embedding_service=embedding_service,
    )

    indexing_processor = IndexingProcessor(
        document_repository=document_repository,
        chunk_repository=chunk_repository,
    )

    processor = DocumentProcessor(
        ingestion_processor=ingestion_processor,
        chunk_processor=chunk_processor,
        embedding_processor=embedding_processor,
        indexing_processor=indexing_processor,
    )

    return DocumentService(
        processor=processor,
    )


def get_search_service(
    db: Session = Depends(get_db),
) -> SearchService:
    """
    Create and wire dependencies for search.
    """

    return SearchService(
        embedding_service=embedding_service,
        repository=SearchRepository(db),
    )


def get_reindex_service(
    db: Session = Depends(get_db),
) -> ReindexService:
    """
    Create and wire dependencies for embedding re-indexing.
    """

    return ReindexService(
        chunk_repository=DocumentChunkRepository(db),
        embedding_service=embedding_service,
    )


def get_retriever_service(
    db: Session = Depends(get_db),
) -> RetrieverService:
    """
    Create and wire dependencies for retrieval.
    """

    return RetrieverService(
        search_service=get_search_service(db),
    )


def get_rag_service(
    db: Session = Depends(get_db),
) -> RAGService:
    """
    Create and wire dependencies for the RAG pipeline.
    """

    return RAGService(
        retriever=get_retriever_service(db),
        prompt_service=prompt_service,
        llm_service=llm_service,
        query_rewriter=query_rewrite_service,
    )