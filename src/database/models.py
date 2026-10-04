from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
import uuid

Base = declarative_base()


class Item(Base):
    """ORM model for aggregated items (news, papers, releases, etc.)."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, index=True)  # 'arxiv', 'huggingface', 'rss'
    url = Column(String(2048), nullable=False, unique=True, index=True)
    title = Column(Text, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True, index=True)
    category = Column(String(50), nullable=True, index=True)  # 'model_release', 'paper', etc.
    summary = Column(Text, nullable=True)
    raw_content = Column(Text, nullable=True)  # For full text storage if needed
    raw_metadata = Column(JSONB, nullable=True)  # For flexible extra fields per source
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Item(id={self.id}, source={self.source}, title={self.title[:50]}...)>"


class Embedding(Base):
    """ORM model for item embeddings (vector representations)."""

    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    embedding = Column(Vector(1536), nullable=False)  # For text-embedding-3-small
    embedding_model = Column(String(100), default="text-embedding-3-small", nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Embedding(id={self.id}, item_id={self.item_id}, model={self.embedding_model})>"


class SourceTracking(Base):
    """ORM model to track the last fetch time for each data source."""

    __tablename__ = "source_tracking"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, unique=True, index=True)
    last_fetched_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<SourceTracking(source={self.source}, last_fetched_at={self.last_fetched_at})>"
