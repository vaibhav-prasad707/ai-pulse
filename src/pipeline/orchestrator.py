#!/usr/bin/env python
"""Main orchestrator for the AI Pulse ingestion pipeline.

This is a placeholder for the full LangGraph pipeline that will:
1. Fetch items from multiple sources
2. Deduplicate entries
3. Classify items
4. Summarize content
5. Generate embeddings and store in the database

For now, it just validates that the pipeline state and node structure work.
"""

import logging
from datetime import datetime, timezone

from src.config import setup_logging
from src.pipeline import PipelineState, PipelineItemRecord, run_pipeline_step

logger = logging.getLogger(__name__)


def run_orchestrator() -> None:
    """Run the complete ingestion pipeline."""
    setup_logging()

    logger.info("Starting AI Pulse ingestion pipeline...")

    # Initialize pipeline state
    state = PipelineState(last_run_at=datetime.now(timezone.utc))

    # For now, just run placeholder nodes to verify structure
    nodes_to_run = ["fetch", "dedupe", "classify", "summarize", "embed_and_store"]

    for node_name in nodes_to_run:
        try:
            logger.info(f"Running node: {node_name}")
            state = run_pipeline_step(node_name, state)
            logger.info(f"Node {node_name} completed successfully")
        except Exception as e:
            logger.exception(f"Error running node {node_name}: {e}")
            state.errors.append(f"Node {node_name} failed: {str(e)}")

    logger.info(f"Pipeline run completed with {len(state.errors)} errors")
    if state.errors:
        logger.warning(f"Errors occurred: {state.errors}")


if __name__ == "__main__":
    run_orchestrator()
