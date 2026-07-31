from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Knowledge Assistant"

    upload_folder: str = "uploads"
    max_upload_size: int = 10 * 1024 * 1024

    database_url: str = Field(alias="DATABASE_URL")

    lmstudio_base_url: str = Field(
        default="http://127.0.0.1:1234/v1",
        alias="LMSTUDIO_BASE_URL",
    )

    lmstudio_model: str = Field(
        default="google/gemma-4-e4b",
        alias="LMSTUDIO_MODEL",
    )

    openrouter_api_key: str = Field(
        default="",
        alias="OPENROUTER_API_KEY",
    )

    openrouter_base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        alias="OPENROUTER_BASE_URL",
    )

    openrouter_model: str = Field(
        default="deepseek/deepseek-chat-v3-0324",
        alias="OPENROUTER_MODEL",
    )

    llm_provider: str = Field(
        default="openrouter",
        alias="LLM_PROVIDER",
    )

    retrieval_limit: int = 5
    semantic_candidate_limit: int = 10
    semantic_similarity_threshold: float = 0.70
    rrf_k: int = 60
    max_context_chars: int = 6000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )


settings = Settings()

print("DATABASE_URL:", bool(settings.database_url))
print("OPENROUTER_API_KEY:", bool(settings.openrouter_api_key))
print("KEY LENGTH:", len(settings.openrouter_api_key))