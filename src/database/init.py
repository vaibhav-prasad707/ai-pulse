"""Database initialization and schema setup script."""

import logging
from sqlalchemy import text

from src.config import setup_logging, get_settings
from src.database import init_database, get_session, Base, Item, Embedding, SourceTracking

logger = logging.getLogger(__name__)


def init_schema() -> None:
    """Create all tables and indexes in the database."""
    setup_logging()
    settings = get_settings()

    logger.info(f"Initializing database schema at {settings.postgres_host}:{settings.postgres_port}")

    init_database()

    # Create all tables
    Base.metadata.create_all(bind=None)  # Uses engine from module scope
    logger.info("Created all tables")

    # Manually create pgvector index if it doesn't exist
    session = get_session()
    try:
        # Enable pgvector
        session.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        session.commit()
        logger.info("pgvector extension created/verified")

        # Create IVFFLAT index on embeddings if not exists
        try:
            session.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS idx_embeddings_vector 
                    ON embeddings USING ivfflat (embedding vector_cosine_ops) 
                    WITH (lists = 100);
                    """
                )
            )
            session.commit()
            logger.info("Vector index created/verified")
        except Exception as e:
            logger.warning(f"Could not create vector index: {e}")

    except Exception as e:
        logger.error(f"Error initializing schema: {e}")
        raise
    finally:
        session.close()

    logger.info("Database schema initialization complete")


if __name__ == "__main__":
    init_schema()
