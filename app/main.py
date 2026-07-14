from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.routes.search import router as search_router
from app.api.routes.reindex import router as reindex_router
from app.api.routes.chat import router as chat_router

app = FastAPI(
    title="AI Knowledge Assistant",
    version="0.1.0"
)

app.include_router(documents_router)
app.include_router(search_router)
app.include_router(reindex_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "application": "AI Knowledge Assistant",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }