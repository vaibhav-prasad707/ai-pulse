# Quick Setup & Validation Guide

## Prerequisites

Before running the validation, ensure you have:

- **Python 3.11+** installed
- **Docker** and **Docker Compose** installed
- **API Keys** in your `.env` file:
  - `ANTHROPIC_API_KEY` (for Claude LLM)
  - `OPENAI_API_KEY` (for embeddings)

## Quick Start (Automated)

The easiest way to validate everything is to run the automated setup script:

### On macOS/Linux:

```bash
# Navigate to the project root
cd ai-pulse

# Make the script executable
chmod +x scripts/setup_and_validate.sh

# Run the setup and validation
./scripts/setup_and_validate.sh
```

### On Windows (PowerShell):

```powershell
cd ai-pulse

# Run Python to set up
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .

# Start containers
docker-compose up -d

# Wait a few seconds, then initialize DB
Start-Sleep -Seconds 5
python -m scripts.validate_db

# Run smoke tests
python -m scripts.smoke_test_fetchers
```

## Manual Step-by-Step Setup

If you prefer to run commands individually:

### 1. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -e .
```

### 3. Set up environment

```bash
cp .env.example .env
# Edit .env and add your API keys
```

### 4. Start PostgreSQL + pgvector

```bash
docker-compose up -d
```

### 5. Verify PostgreSQL is running

```bash
docker-compose ps
```

You should see the `ai_pulse_postgres` container running.

### 6. Validate database initialization

```bash
python -m scripts.validate_db
```

Expected output:
```
...
INFO:src.database.connection:Connecting to database at localhost:5432
INFO:src.database.connection:Database connection successful
INFO:src.database.connection:pgvector extension enabled
INFO:src.database.init:Database schema initialization complete
```

### 7. Run fetcher smoke tests

```bash
python -m scripts.smoke_test_fetchers
```

Expected output:
```
INFO:scripts.smoke_test_fetchers:Running smoke test for fetcher: arxiv
INFO:src.sources.arxiv:Fetching arXiv papers since 2026-09-27 12:34:56+00:00 (max 50)
INFO:src.sources.arxiv:Fetched X papers from arXiv
INFO:scripts.smoke_test_fetchers:Fetcher arxiv returned X items
INFO:scripts.smoke_test_fetchers:Sample item: source=arxiv, title=..., url=..., published_at=...
...
```

## Troubleshooting

### PostgreSQL Connection Error

**Error**: `Error connecting to database at localhost:5432`

**Solution**:
1. Check if Docker is running: `docker ps`
2. Start containers: `docker-compose up -d`
3. Wait a few seconds and try again: `docker-compose logs postgres`

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
1. Ensure you're in the project root directory
2. Ensure virtual environment is activated: `source venv/bin/activate`
3. Reinstall dependencies: `pip install -e .`

### Missing API Keys

**Error**: `ANTHROPIC_API_KEY not set` or similar

**Solution**:
1. Copy `.env.example` to `.env`: `cp .env.example .env`
2. Edit `.env` and add your API keys
3. Note: The fetcher smoke tests don't require these keys (they test fetching only)

### Fetcher Failures

**Error**: `Error fetching from arXiv` or similar

**Solution**:
1. Check your internet connection
2. The APIs may have rate limits; wait a few minutes and retry
3. Check logs for specific error messages
4. For RSS feeds, verify the URLs are accessible

### Docker Compose Issues

**Error**: `Error response from daemon: port is already allocated`

**Solution**:
1. Stop existing containers: `docker-compose down`
2. Or change the port in `docker-compose.yml`
3. Restart: `docker-compose up -d`

## What Gets Validated

The validation script checks:

✓ Python 3.11+ installation  
✓ Docker and Docker Compose installation  
✓ Virtual environment setup  
✓ Python dependencies installation  
✓ PostgreSQL container startup  
✓ Database connection  
✓ pgvector extension enablement  
✓ Database schema creation  
✓ arXiv fetcher functionality  
✓ Hugging Face fetcher functionality  
✓ RSS fetcher functionality  
✓ Item normalization across all fetchers  

## Next Steps After Validation

Once validation passes, you can:

1. **Continue development** on the pipeline nodes (dedupe, classify, summarize)
2. **Build the FastAPI backend** with digest and chat endpoints
3. **Create the Streamlit frontend** dashboard and chat interface
4. **Add scheduling** via APScheduler for automated ingestion

## Cleanup

To stop the database and clean up:

```bash
# Stop containers
docker-compose down

# Remove the virtual environment
rm -rf venv
```
