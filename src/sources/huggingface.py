"""Hugging Face models/spaces fetcher."""

import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
import requests

from src.sources.base import BaseFetcher, FetchedItem
from src.config import get_settings

logger = logging.getLogger(__name__)


class HuggingFaceFetcher(BaseFetcher):
    """Fetches recently updated models and spaces from Hugging Face Hub."""

    source_name = "huggingface"
    HF_API_URL = "https://huggingface.co/api"

    def __init__(self):
        self.settings = get_settings()
        self.max_results = self.settings.huggingface_max_results

    def fetch(self, since: Optional[datetime] = None) -> list[FetchedItem]:
        """
        Fetch recent models from Hugging Face.

        Args:
            since: Fetch models updated after this date.
                  If None, defaults to last 7 days.

        Returns:
            List of FetchedItem objects.
        """
        if since is None:
            since = datetime.now(timezone.utc) - timedelta(days=7)

        items = []
        try:
            logger.info(f"Fetching Hugging Face models updated since {since}")

            # Fetch models sorted by last_modified
            url = f"{self.HF_API_URL}/models"
            params = {
                "sort": "last_modified",
                "direction": -1,
                "limit": self.max_results,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            models = response.json()
            if not isinstance(models, list):
                models = models.get("models", []) if isinstance(models, dict) else []

            for model in models:
                try:
                    # Parse model metadata
                    model_id = model.get("id", "")
                    if not model_id:
                        continue

                    url_str = f"https://huggingface.co/{model_id}"
                    title = model_id  # Use model ID as title
                    description = model.get("description", "") or ""

                    # Parse last_modified timestamp
                    last_modified_str = model.get("lastModified")
                    if last_modified_str:
                        published_at = datetime.fromisoformat(last_modified_str.replace("Z", "+00:00"))
                        if published_at < since:
                            continue  # Skip items older than 'since'
                    else:
                        published_at = datetime.now(timezone.utc)

                    items.append(
                        FetchedItem(
                            source=self.source_name,
                            url=url_str,
                            title=title,
                            published_at=published_at,
                            raw_content=description,
                            raw_metadata={
                                "model_id": model_id,
                                "tags": model.get("tags", []),
                                "downloads": model.get("downloads", 0),
                                "likes": model.get("likes", 0),
                            },
                        )
                    )
                except Exception as e:
                    logger.warning(f"Error parsing Hugging Face model: {e}")
                    continue

            logger.info(f"Fetched {len(items)} models from Hugging Face")
            return items

        except requests.RequestException as e:
            logger.error(f"Error fetching from Hugging Face: {e}")
            return []
