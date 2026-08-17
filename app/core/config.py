from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = Field(
        default="AI Knowledge Assistant",
        alias="APP_NAME",
    )
    app_url: str = Field(
        default="http://localhost:8000",
        alias="APP_URL",
    )
    cors_origins: str = Field(
        default=(
            "http://localhost:5173,"
            "https://knowlegde-asistant-bot.up.railway.app"
        ),
        alias="CORS_ORIGINS",
    )

    upload_folder: str = Field(
        default="uploads",
        alias="UPLOAD_FOLDER",
    )
    max_upload_size: int = Field(
        default=10 * 1024 * 1024,
        alias="MAX_UPLOAD_SIZE",
    )

    database_url: str = Field(alias="DATABASE_URL")
    sql_echo: bool = Field(
        default=False,
        alias="SQL_ECHO",
    )

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
    semantic_similarity_threshold: float = 0.20
    rrf_k: int = 60
    max_context_chars: int = 6000

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,
        extra="ignore",
    )


settings = Settings()
