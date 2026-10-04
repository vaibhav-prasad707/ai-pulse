import logging
from datetime import datetime, timedelta, timezone

from src.config import setup_logging
from src.sources import ArxivFetcher, HuggingFaceFetcher, RSSFetcher

logger = logging.getLogger(__name__)


def smoke_test_fetchers() -> dict[str, list]:
    """Run a quick smoke test against each data source and print counts."""
    setup_logging()

    since = datetime.now(timezone.utc) - timedelta(days=7)

    fetchers = {
        "arxiv": ArxivFetcher(),
        "huggingface": HuggingFaceFetcher(),
        "rss": RSSFetcher(),
    }

    results = {}
    for name, fetcher in fetchers.items():
        logger.info(f"Running smoke test for fetcher: {name}")
        items = fetcher.fetch(since=since)
        logger.info(f"Fetcher {name} returned {len(items)} items")

        results[name] = items

        for item in items[:3]:
            logger.info(
                f"Sample item: source={item.source}, title={item.title[:80]}, "
                f"url={item.url}, published_at={item.published_at}"
            )

    return results


if __name__ == "__main__":
    smoke_test_fetchers()
