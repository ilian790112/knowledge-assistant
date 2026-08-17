# AI Knowledge Assistant

> A production-oriented Retrieval-Augmented Generation (RAG) application for uploading PDFs, indexing their contents, and asking grounded questions over a personal knowledge base.

[![CI](https://github.com/ilian790112/knowledge-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/ilian790112/knowledge-assistant/actions/workflows/ci.yml)

## What it demonstrates

This project is designed as a portfolio-quality example of an end-to-end AI application rather than a simple chatbot. It combines:

- **FastAPI** REST APIs and dependency injection
- **PostgreSQL + pgvector** for vector similarity search
- **PostgreSQL full-text search** for keyword retrieval
- **Hybrid retrieval with Reciprocal Rank Fusion (RRF)**
- **Sentence Transformers** for local document/query embeddings
- **OpenRouter-compatible LLM generation**
- **RAG prompt grounding** with explicit source context
- **PDF ingestion and text cleaning**
- **Streaming document processing** to reduce memory pressure
- **Alembic** database migrations
- **React + TypeScript + MUI** frontend
- **Docker Compose** development infrastructure
- **GitHub Actions** repository checks

## Architecture

```mermaid
flowchart LR
    UI[React + TypeScript UI]
    API[FastAPI API]
    INGEST[PDF ingestion]
    CHUNK[Lazy chunking]
    EMBED[Sentence Transformer]
    DB[(PostgreSQL + pgvector)]
    SEARCH[Hybrid search]
    RAG[RAG service]
    LLM[OpenRouter LLM]

    UI -->|upload / chat| API
    API --> INGEST
    INGEST --> CHUNK
    CHUNK --> EMBED
    EMBED --> DB

    API --> RAG
    RAG --> SEARCH
    SEARCH --> DB
    RAG --> LLM
    LLM --> API
    API --> UI
```

## Document ingestion flow

1. The client uploads a PDF.
2. FastAPI streams the request into a temporary file with a configurable size limit.
3. The ingestion layer moves the file into local storage using a sanitized, collision-resistant filename.
4. PyMuPDF extracts text and the cleaner normalizes it.
5. `ChunkService` yields overlapping chunks instead of building a large list.
6. `EmbeddingProcessor` embeds small batches and yields results incrementally.
7. `IndexingProcessor` writes chunks to PostgreSQL in bounded batches.
8. The document status moves from `processing` to `processed`, or `failed` if indexing raises an exception.

## Retrieval and RAG flow

1. The chat endpoint receives a question and optional conversation history.
2. The query rewriter creates a standalone question for retrieval.
3. The query is embedded with the same Sentence Transformer used during ingestion.
4. PostgreSQL performs semantic vector search and full-text search.
5. The results are combined with Reciprocal Rank Fusion.
6. A bounded context is assembled from the highest-ranked chunks.
7. The LLM receives the question, recent conversation history, and retrieved document context.
8. If no relevant context is found, the service returns the grounded fallback `I don't know.` without making an unnecessary LLM request.
9. The API returns both the answer and source metadata for transparency.

## Project structure

```text
knowledge-assistant/
├── app/
│   ├── api/             # HTTP routes
│   ├── core/            # configuration, database, dependencies, logging
│   ├── models/          # SQLAlchemy models
│   ├── processors/      # ingestion / chunking / embedding / indexing pipeline
│   ├── repositories/    # database access layer
│   ├── schemas/         # Pydantic request/response models
│   ├── services/        # RAG, retrieval, embeddings, LLM and domain services
│   ├── storage/         # local document storage
│   └── main.py          # FastAPI application entry point
├── alembic/             # database migrations
├── frontend/            # React + TypeScript client
├── docker-compose.yml   # local PostgreSQL infrastructure
├── Procfile             # production web process
├── tests/               # lightweight backend tests
└── requirements.txt     # Python dependencies
```

## Production-minded details

The ingestion pipeline was deliberately designed around bounded memory usage. Large intermediate collections are avoided where practical: chunks and embeddings are streamed, embeddings are generated in small batches, and database writes are grouped into bounded transactions.

The upload endpoint also streams incoming files rather than calling `read()` on the entire request body. Database SQL echo is disabled by default and can be enabled explicitly with `SQL_ECHO=true` when debugging.

Uploaded filenames are sanitized and prefixed with a UUID, preventing path traversal and accidental overwrites.

## Configuration

Copy `.env.example` to `.env` and provide your database and LLM credentials. Important production variables include:

```env
DATABASE_URL=postgresql+psycopg2://user:password@host:5432/knowledge_assistant
OPENROUTER_API_KEY=your_api_key
LLM_PROVIDER=openrouter
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324
APP_URL=https://your-api.example.com
CORS_ORIGINS=https://your-frontend.example.com
MAX_UPLOAD_SIZE=10485760
SQL_ECHO=false
```

The application also supports LM Studio configuration for local-compatible LLM deployments.

## Running with Docker Compose

```bash
docker compose up --build
```

The frontend and backend can also be run independently when developing locally.

## API surface

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/documents/` | List uploaded documents |
| `POST` | `/documents/upload` | Upload and process a PDF asynchronously |
| `DELETE` | `/documents/{document_id}` | Delete a document and its chunks |
| `POST` | `/chat/` | Ask a question against the knowledge base |
| `POST` | `/search/` | Run hybrid document search |
| `POST` | `/retrieve/` | Inspect retrieval results |
| `POST` | `/reindex/embeddings` | Rebuild missing embeddings |

FastAPI also exposes interactive OpenAPI documentation through its standard docs endpoints.

## Why hybrid retrieval?

Vector search is strong at semantic similarity, while PostgreSQL full-text search is useful for exact terminology, names, and phrases. Combining both rankings with RRF gives the application two complementary retrieval signals instead of depending on one search strategy.

## Current trade-offs

This repository intentionally keeps the infrastructure understandable:

- Local filesystem storage is used for PDFs rather than object storage.
- FastAPI background tasks are used instead of a dedicated job queue.
- The embedding model runs on CPU, which keeps deployment requirements simple but makes large ingestion jobs slower.
- PostgreSQL is both the relational store and vector/full-text search engine.

These choices make the project easy to understand while leaving clear paths for future scaling.

## Roadmap

- [ ] Dedicated durable job queue for document processing
- [ ] Object storage for uploaded PDFs
- [ ] Streaming chat responses
- [ ] Authentication and per-user knowledge bases
- [ ] Retrieval/evaluation test set with measurable RAG metrics
- [ ] Observability for ingestion and retrieval latency
- [ ] Automated deployment environment

## License

MIT
