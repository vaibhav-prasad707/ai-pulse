import logging
from typing import Optional

from src.database import Item, SourceTracking, get_session
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)


def get_source_last_fetched(source: str) -> Optional[datetime]:
    """Get the last fetch time for a given source."""
    session = get_session()
    try:
        tracking = session.query(SourceTracking).filter(SourceTracking.source == source).first()
        return tracking.last_fetched_at if tracking else None
    finally:
        session.close()


def update_source_last_fetched(source: str) -> None:
    """Update the last fetch time for a given source to now."""
    session = get_session()
    try:
        tracking = session.query(SourceTracking).filter(SourceTracking.source == source).first()
        if tracking:
            tracking.last_fetched_at = datetime.now(timezone.utc)
        else:
            tracking = SourceTracking(
                source=source,
                last_fetched_at=datetime.now(timezone.utc),
            )
            session.add(tracking)
        session.commit()
        logger.info(f"Updated last_fetched_at for source={source}")
    finally:
        session.close()


def item_exists_by_url(url: str) -> bool:
    """Check if an item with the given URL already exists."""
    session = get_session()
    try:
        count = session.query(Item).filter(Item.url == url).count()
        return count > 0
    finally:
        session.close()


def store_item(item: Item) -> Item:
    """Store an item in the database."""
    session = get_session()
    try:
        session.add(item)
        session.commit()
        session.refresh(item)
        logger.info(f"Stored item: id={item.id}, source={item.source}, url={item.url}")
        return item
    finally:
        session.close()


def get_recent_items(source: Optional[str] = None, hours: int = 24, limit: int = 100) -> list[Item]:
    """Get recently created items, optionally filtered by source."""
    session = get_session()
    try:
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        query = session.query(Item).filter(Item.created_at >= cutoff_time)
        if source:
            query = query.filter(Item.source == source)
        return query.order_by(Item.created_at.desc()).limit(limit).all()
    finally:
        session.close()
