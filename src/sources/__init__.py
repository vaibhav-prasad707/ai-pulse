"""Sources module."""

from src.sources.base import BaseFetcher, FetchedItem
from src.sources.arxiv import ArxivFetcher
from src.sources.huggingface import HuggingFaceFetcher
from src.sources.rss import RSSFetcher

__all__ = [
    "BaseFetcher",
    "FetchedItem",
    "ArxivFetcher",
    "HuggingFaceFetcher",
    "RSSFetcher",
]
