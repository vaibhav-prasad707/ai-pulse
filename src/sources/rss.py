"""RSS feed fetcher for blogs/news."""

import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, List
import feedparser

from src.sources.base import BaseFetcher, FetchedItem
from src.config import get_settings

logger = logging.getLogger(__name__)


class RSSFetcher(BaseFetcher):
    """Fetches items from RSS feeds (e.g., company blogs, news sites)."""

    source_name = "rss"

    def __init__(self, feed_urls: Optional[List[str]] = None):
        """
        Initialize RSS fetcher.

        Args:
            feed_urls: List of RSS feed URLs to fetch from.
                      If None, uses default tech news feeds.
        """
        self.settings = get_settings()
        self.feed_urls = feed_urls or [
            "https://www.anthropic.com/feed.xml",  # Anthropic blog
            "https://openai.com/feed.xml",  # OpenAI blog
        ]

    def fetch(self, since: Optional[datetime] = None) -> list[FetchedItem]:
        """
        Fetch items from configured RSS feeds.

        Args:
            since: Only fetch entries published after this datetime.
                  If None, defaults to last 7 days.

        Returns:
            List of FetchedItem objects.
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=7)

        items = []

        for feed_url in self.feed_urls:
            try:
                logger.info(f"Fetching RSS feed: {feed_url}")
                feed = feedparser.parse(feed_url)

                if feed.bozo:
                    logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")

                for entry in feed.entries:
                    try:
                        title = entry.get("title", "Untitled").strip()
                        url = entry.get("link", "")
                        if not url:
                            continue

                        # Parse published date
                        published_at = None
                        if hasattr(entry, "published_parsed") and entry.published_parsed:
                            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                            published_at = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                        else:
                            published_at = datetime.now(timezone.utc)

                        # Skip items older than 'since'
                        if published_at < since:
                            continue

                        # Extract summary/description
                        summary = entry.get("summary", "") or entry.get("description", "")
                        summary = summary.strip()[:500]  # Limit to 500 chars

                        items.append(
                            FetchedItem(
                                source=self.source_name,
                                url=url,
                                title=title,
                                published_at=published_at,
                                raw_content=summary,
                                raw_metadata={
                                    "feed_url": feed_url,
                                    "author": entry.get("author", ""),
                                },
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error parsing RSS entry: {e}")
                        continue

                logger.info(f"Fetched {len([i for i in items if i.raw_metadata.get('feed_url') == feed_url])} entries from {feed_url}")

            except Exception as e:
                logger.error(f"Error fetching RSS feed {feed_url}: {e}")
                continue

        logger.info(f"Fetched {len(items)} total items from {len(self.feed_urls)} RSS feeds")
        return items
