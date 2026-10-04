import logging
from typing import Optional
from datetime import timedelta

from pydantic_settings import BaseSettings
from pydantic import Field

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    postgres_user: str = Field(default="aiuser", alias="POSTGRES_USER")
    postgres_password: str = Field(default="aipassword", alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="ai_pulse", alias="POSTGRES_DB")
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")

    # LLM & Embeddings
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    embedding_model: str = Field(default="text-embedding-3-small", alias="EMBEDDING_MODEL")
    llm_model: str = Field(default="claude-3-5-sonnet-20241022", alias="LLM_MODEL")

    # Application
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    schedule_interval_hours: int = Field(default=24, alias="SCHEDULE_INTERVAL_HOURS")
    vector_search_top_k: int = Field(default=5, alias="VECTOR_SEARCH_TOP_K")
    embedding_dimension: int = Field(default=1536)  # For text-embedding-3-small

    # API
    fastapi_host: str = Field(default="0.0.0.0", alias="FASTAPI_HOST")
    fastapi_port: int = Field(default=8000, alias="FASTAPI_PORT")

    # Streamlit
    streamlit_port: int = Field(default=8501, alias="STREAMLIT_PORT")

    # Fetcher settings
    arxiv_max_results: int = Field(default=50)
    huggingface_max_results: int = Field(default=50)
    dedup_threshold: float = Field(default=0.85)  # Fuzzy match threshold for deduplication

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

    @property
    def sqlalchemy_database_url(self) -> str:
        """Construct SQLAlchemy database URL."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()


def setup_logging(settings: Optional[Settings] = None) -> None:
    """Configure logging for the application."""
    if settings is None:
        settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
