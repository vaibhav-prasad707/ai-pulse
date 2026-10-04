import logging
from typing import Any

from src.pipeline.state import PipelineState, PipelineItemRecord

logger = logging.getLogger(__name__)


def fetch_node(state: PipelineState) -> PipelineState:
    """Placeholder fetch node for future pipeline implementation."""
    logger.info("fetch_node invoked")
    return state


def dedupe_node(state: PipelineState) -> PipelineState:
    """Placeholder dedupe node for future pipeline implementation."""
    logger.info("dedupe_node invoked")
    return state


def classify_node(state: PipelineState) -> PipelineState:
    """Placeholder classify node for future pipeline implementation."""
    logger.info("classify_node invoked")
    return state


def summarize_node(state: PipelineState) -> PipelineState:
    """Placeholder summarize node for future pipeline implementation."""
    logger.info("summarize_node invoked")
    return state


def embed_and_store_node(state: PipelineState) -> PipelineState:
    """Placeholder embed/store node for future pipeline implementation."""
    logger.info("embed_and_store_node invoked")
    return state


def run_pipeline_step(node_name: str, state: PipelineState) -> PipelineState:
    """Simple dispatch helper for pipeline node execution."""
    dispatch = {
        "fetch": fetch_node,
        "dedupe": dedupe_node,
        "classify": classify_node,
        "summarize": summarize_node,
        "embed_and_store": embed_and_store_node,
    }

    func = dispatch.get(node_name)
    if func is None:
        raise ValueError(f"Unknown pipeline node: {node_name}")

    return func(state)
