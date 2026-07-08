from fastapi import FastAPI

from app.api.documents import router as documents_router

app = FastAPI(
    title="AI Knowledge Assistant",
    version="0.1.0"
)

app.include_router(documents_router)


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