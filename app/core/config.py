from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.
    """

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "AI Knowledge Assistant"

    upload_folder: str = "uploads"

    max_upload_size: int = 10 * 1024 * 1024

    # ------------------------------------------------------------------
    # Database
    # ------------------------------------------------------------------

    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/knowledge_assistant"
    )

    # ------------------------------------------------------------------
    # Language Model
    # ------------------------------------------------------------------

    lmstudio_base_url: str = "http://127.0.0.1:1234/v1"

    lmstudio_model: str = "google/gemma-4-e4b"

    # OpenRouter
    openrouter_api_key: str = ""

    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    openrouter_model: str = "deepseek/deepseek-chat-v3-0324"

    llm_provider: str = "openrouter"

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    retrieval_limit: int = 5

    semantic_candidate_limit: int = 10

    semantic_similarity_threshold: float = 0.70

    rrf_k: int = 60

    max_context_chars: int = 6000

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()