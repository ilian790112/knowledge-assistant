from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        examples=[
            "What is FastAPI?"
        ],
    )