import logging
from typing import Generator

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from src.config import get_settings

logger = logging.getLogger(__name__)

# Global engine and session factory
engine = None
SessionLocal = None


def init_database() -> None:
    """Initialize database engine and session factory."""
    global engine, SessionLocal

    settings = get_settings()
    database_url = settings.sqlalchemy_database_url

    logger.info(f"Connecting to database at {settings.postgres_host}:{settings.postgres_port}")

    engine = create_engine(
        database_url,
        poolclass=NullPool,  # Useful for serverless/testing
        echo=settings.log_level == "DEBUG",
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test connection
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

    # Enable pgvector extension
    try:
        with SessionLocal() as session:
            session.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            session.commit()
            logger.info("pgvector extension enabled")
    except Exception as e:
        logger.warning(f"pgvector extension already exists or error: {e}")


def get_db() -> Generator[Session, None, None]:
    """Dependency for FastAPI to get a database session."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session() -> Session:
    """Get a database session for non-FastAPI contexts."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return SessionLocal()


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()
