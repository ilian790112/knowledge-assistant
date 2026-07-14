from openai import OpenAI

from app.core.config import settings
from app.services.llm_service import LLMService


class LMStudioService(LLMService):
    """
    Service for interacting with a local LM Studio server.
    """

    def __init__(self) -> None:
        self.client = OpenAI(
            base_url=settings.lmstudio_base_url,
            api_key="lm-studio",
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response using the configured LM Studio model.
        """

        response = self.client.chat.completions.create(
            model=settings.lmstudio_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content