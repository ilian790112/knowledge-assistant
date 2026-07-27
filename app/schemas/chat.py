from pydantic import BaseModel, Field

from app.schemas.chat_message import ChatMessage


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        examples=["What is FastAPI?"],
    )

    history: list[ChatMessage] = Field(
        default_factory=list,
    )