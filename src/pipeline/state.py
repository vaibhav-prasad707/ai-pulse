from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class PipelineItemRecord:
    """Normalized item information as it flows through the pipeline."""

    source: str
    url: str
    title: str
    published_at: Optional[datetime] = None
    raw_content: Optional[str] = None
    raw_metadata: Optional[dict[str, Any]] = None
    category: Optional[str] = None
    summary: Optional[str] = None
    embedding: Optional[list[float]] = None
    dedup_key: Optional[str] = None


@dataclass
class PipelineState:
    """LangGraph-friendly pipeline state for ingestion."""

    raw_items: list[PipelineItemRecord] = field(default_factory=list)
    deduped_items: list[PipelineItemRecord] = field(default_factory=list)
    classified_items: list[PipelineItemRecord] = field(default_factory=list)
    summarized_items: list[PipelineItemRecord] = field(default_factory=list)
    stored_items: list[PipelineItemRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    last_run_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "raw_items": [item.__dict__ for item in self.raw_items],
            "deduped_items": [item.__dict__ for item in self.deduped_items],
            "classified_items": [item.__dict__ for item in self.classified_items],
            "summarized_items": [item.__dict__ for item in self.summarized_items],
            "stored_items": [item.__dict__ for item in self.stored_items],
            "errors": self.errors,
            "last_run_at": self.last_run_at,
        }
