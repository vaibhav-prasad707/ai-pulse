"""arXiv paper fetcher."""

import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

from src.sources.base import BaseFetcher, FetchedItem
from src.config import get_settings

logger = logging.getLogger(__name__)


class ArxivFetcher(BaseFetcher):
    """Fetches recent papers from arXiv in AI/ML categories."""

    source_name = "arxiv"
    ARXIV_API_URL = "http://export.arxiv.org/api/query?"
    CATEGORIES = ["cat:cs.AI", "cat:cs.CL", "cat:cs.LG"]  # AI, NLP, Machine Learning

    def __init__(self):
        self.settings = get_settings()
        self.max_results = self.settings.arxiv_max_results

    def fetch(self, since: Optional[datetime] = None) -> list[FetchedItem]:
        """
        Fetch recent arXiv papers.

        Args:
            since: Fetch papers submitted after this date.
                  If None, defaults to last 7 days.

        Returns:
            List of FetchedItem objects.
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=7)

        items = []
        # arXiv query format: (cat:cs.AI OR cat:cs.CL OR cat:cs.LG) AND submittedDate:[date TO now]
        query = (
            f"({' OR '.join(self.CATEGORIES)}) "
            f"AND submittedDate:[{since.strftime('%Y%m%d%H%M%S')}Z TO now]"
        )

        params = {
            "search_query": query,
            "start": 0,
            "max_results": self.max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        try:
            logger.info(f"Fetching arXiv papers since {since} (max {self.max_results})")
            response = requests.get(self.ARXIV_API_URL, params=params, timeout=30)
            response.raise_for_status()

            import xml.etree.ElementTree as ET

            root = ET.fromstring(response.content)
            namespace = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", namespace):
                try:
                    title = entry.findtext("atom:title", namespace="").strip()
                    arxiv_id = entry.findtext("atom:id", namespace="").strip().split("/abs/")[1]
                    url = f"https://arxiv.org/abs/{arxiv_id}"
                    published_str = entry.findtext("atom:published", namespace="")
                    published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))

                    # Extract summary
                    summary = entry.findtext("atom:summary", namespace="").strip()

                    items.append(
                        FetchedItem(
                            source=self.source_name,
                            url=url,
                            title=title,
                            published_at=published_at,
                            raw_content=summary,
                            raw_metadata={
                                "arxiv_id": arxiv_id,
                                "authors": [
                                    a.findtext("{http://www.w3.org/2005/Atom}name")
                                    for a in entry.findall("atom:author", namespace)
                                ],
                            },
                        )
                    )
                except Exception as e:
                    logger.warning(f"Error parsing arXiv entry: {e}")
                    continue

            logger.info(f"Fetched {len(items)} papers from arXiv")
            return items

        except requests.RequestException as e:
            logger.error(f"Error fetching from arXiv: {e}")
            return []
