from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.
    """

    app_name: str = "AI Knowledge Assistant"

    upload_folder: str = "uploads"

    max_upload_size: int = 10 * 1024 * 1024

    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/knowledge_assistant"
    )

    # LM Studio
    lmstudio_base_url: str = "http://127.0.0.1:1234/v1"
    lmstudio_model: str = "google/gemma-4-e4b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()