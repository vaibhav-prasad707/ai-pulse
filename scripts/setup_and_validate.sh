#!/bin/bash
# Quick setup and validation script for AI Pulse

set -e

echo "========================================"
echo "AI Pulse - Setup & Validation Script"
echo "========================================"

# Step 1: Check prerequisites
echo ""
echo "[1/6] Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed."; exit 1; }
echo "✓ Python 3, Docker, and Docker Compose are installed"

# Step 2: Create virtual environment
echo ""
echo "[2/6] Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

source venv/bin/activate
echo "✓ Virtual environment activated"

# Step 3: Install dependencies
echo ""
echo "[3/6] Installing Python dependencies..."
pip install -q -e .
echo "✓ Dependencies installed"

# Step 4: Start PostgreSQL container
echo ""
echo "[4/6] Starting PostgreSQL + pgvector container..."
docker-compose up -d
echo "✓ Container started"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 5
max_attempts=30
attempts=0
while [ $attempts -lt $max_attempts ]; do
    if docker-compose exec -T postgres pg_isready -U aiuser > /dev/null 2>&1; then
        echo "✓ PostgreSQL is ready"
        break
    fi
    attempts=$((attempts + 1))
    sleep 1
done

if [ $attempts -eq $max_attempts ]; then
    echo "✗ PostgreSQL did not become ready in time"
    exit 1
fi

# Step 5: Initialize database schema
echo ""
echo "[5/6] Initializing database schema..."
python -m scripts.validate_db
echo "✓ Database schema initialized"

# Step 6: Run fetcher smoke tests
echo ""
echo "[6/6] Running fetcher smoke tests..."
python -m scripts.smoke_test_fetchers
echo "✓ Fetcher smoke tests completed"

echo ""
echo "========================================"
echo "✓ All validation checks passed!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Review the logs above for any warnings"
echo "  2. Start the FastAPI backend: python -m src.api.main"
echo "  3. Start the Streamlit frontend: streamlit run src/frontend/app.py"
echo ""
echo "To stop the PostgreSQL container: docker-compose down"
echo ""
