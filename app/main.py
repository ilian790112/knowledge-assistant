from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Assistant",
    description="Enterprise AI Knowledge Assistant API",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "application": "AI Knowledge Assistant",
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }