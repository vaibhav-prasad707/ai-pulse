# AI Pulse 🚀

An emerging AI tool update dashboard that aggregates AI news, model releases, and tool launches from multiple sources, summarizes them with Claude, and provides both a digest UI and RAG-based chat interface.

## Features

- **Automated Ingestion**: Fetches updates from arXiv, Hugging Face, and RSS feeds on a schedule
- **Smart Deduplication**: Fuzzy-matches items to avoid duplicate entries
- **LLM-Powered Summarization**: Classifies and summarizes each item using Claude
- **Vector Search**: Stores embeddings for semantic search over aggregated content
- **Digest Dashboard**: View daily/weekly summaries grouped by category (Streamlit)
- **RAG Chat Interface**: Query the corpus with grounded answers and citations
- **FastAPI Backend**: RESTful API for all operations

## Tech Stack

- **Runtime**: Python 3.11+
- **Backend**: FastAPI
- **Database**: PostgreSQL + pgvector
- **Pipeline**: LangGraph
- **LLM**: Claude (Anthropic)
- **Embeddings**: OpenAI text-embedding-3-small
- **Scheduling**: APScheduler
- **Frontend**: Streamlit (MVP)

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Anthropic API key
- OpenAI API key (for embeddings)

### Setup

1. **Clone and install**:
   ```bash
   git clone https://github.com/vaibhav-prasad707/ai-pulse.git
   cd ai-pulse
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database settings
   ```

3. **Start PostgreSQL + pgvector**:
   ```bash
   docker-compose up -d
   ```

4. **Run the ingestion pipeline** (manual trigger for now):
   ```bash
   python -m src.pipeline.orchestrator
   ```

5. **Start the FastAPI backend** (coming next):
   ```bash
   python -m src.api.main
   ```

6. **Launch the Streamlit dashboard** (coming next):
   ```bash
   streamlit run src/frontend/app.py
   ```

## Project Structure

```
ai-pulse/
├── src/
│   ├── config.py              # Settings and environment config
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py      # DB session management
│   │   └── models.py          # SQLAlchemy ORM models
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── base.py            # Base fetcher class
│   │   ├── arxiv.py           # arXiv fetcher
│   │   ├── huggingface.py     # Hugging Face fetcher
│   │   └── rss.py             # RSS feed fetcher
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── orchestrator.py    # LangGraph pipeline definition
│   │   ├── nodes.py           # Individual pipeline nodes
│   │   └── state.py           # Pipeline state schema
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm.py             # LLM interactions (Claude)
│   │   ├── embeddings.py      # Embedding generation
│   │   ├── dedup.py           # Deduplication logic
│   │   └── search.py          # Vector similarity search
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app
│   │   ├── routes/
│   │   │   ├── digest.py
│   │   │   ├── items.py
│   │   │   ├── chat.py
│   │   │   └── ingest.py
│   │   └── schemas.py         # Pydantic models
│   └── frontend/
│       ├── app.py             # Streamlit main
│       ├── pages/
│       │   ├── digest.py
│       │   ├── chat.py
│       │   └── settings.py
│       └── utils.py
├── tests/
├── docker-compose.yml
├── init-pgvector.sql
├── pyproject.toml
├── .env.example
└── README.md
```

## Development

### Running Tests

```bash
pytest
```

### Formatting & Linting

```bash
black src/
ruff check src/
```

## Roadmap

- [x] Project scaffolding
- [x] Docker Compose setup
- [ ] Fetchers (arXiv, Hugging Face, RSS)
- [ ] LangGraph pipeline (fetch → dedupe → classify → summarize → embed)
- [ ] FastAPI backend with `/digest` and `/items` endpoints
- [ ] Streamlit digest page
- [ ] FastAPI `/chat` endpoint with RAG
- [ ] Streamlit chat page with citations
- [ ] Scheduling (APScheduler)
- [ ] Advanced: Trend detection, alerting, React upgrade

## License

MIT
