"""Base fetcher class for data sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class FetchedItem:
    """Represents a raw item fetched from a data source."""

    source: str  # 'arxiv', 'huggingface', 'rss', etc.
    url: str
    title: str
    published_at: Optional[datetime] = None
    raw_content: Optional[str] = None
    raw_metadata: Optional[dict] = None  # Source-specific metadata


class BaseFetcher(ABC):
    """Abstract base class for data source fetchers."""

    source_name: str

    @abstractmethod
    def fetch(self, since: Optional[datetime] = None) -> list[FetchedItem]:
        """
        Fetch items from the data source.

        Args:
            since: Only fetch items published after this datetime.
                  If None, fetch recent items (implementation-dependent).

        Returns:
            List of FetchedItem objects.
        """
        pass
