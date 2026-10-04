import logging
import os
from pathlib import Path

from src.config import get_settings, setup_logging
from src.database import init_database

logger = logging.getLogger(__name__)


def validate_database_bootstrap() -> bool:
    """Validate that the database connection and schemas initialize correctly."""
    setup_logging()
    settings = get_settings()

    logger.info("Validating database bootstrap...")
    logger.info(f"Postgres settings: host={settings.postgres_host}, db={settings.postgres_db}, port={settings.postgres_port}")

    try:
        init_database()
        logger.info("Database bootstrap succeeded")
        return True
    except Exception as e:
        logger.exception(f"Database bootstrap failed: {e}")
        return False


if __name__ == "__main__":
    validate_database_bootstrap()
