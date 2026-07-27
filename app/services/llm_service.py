from app.core.config import settings
from app.services.lmstudio_service import LMStudioService
from app.services.openrouter_service import OpenRouterService


class LLMService:
    """
    Provides a unified interface for LLM providers.
    """

    def __init__(self) -> None:
        if settings.llm_provider == "openrouter":
            self.provider = OpenRouterService()

        elif settings.llm_provider == "lmstudio":
            self.provider = LMStudioService()

        else:
            raise ValueError(
                f"Unsupported LLM provider: {settings.llm_provider}"
            )

    def generate(
        self,
        prompt: str,
    ) -> str:
        return self.provider.generate(prompt)