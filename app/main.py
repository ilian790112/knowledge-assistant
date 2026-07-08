from fastapi import FastAPI

app = FastAPI(
    title="AI Knowledge Assistant",
    description="Enterprise AI Knowledge Assistant API",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "AI Knowledge Assistant API"
    }