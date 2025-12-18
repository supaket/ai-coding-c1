#!/bin/bash
# Run Lab 2: FastAPI Scaffold

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/02-scaffold"

echo "🚀 Starting Lab 2: FastAPI Scaffold"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup..."
    cd "$SCRIPT_DIR"
    ./setup.sh
    cd "$SCRIPT_DIR/02-scaffold"
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "🌐 Starting FastAPI app on http://localhost:8000"
echo "   Swagger docs: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --port 8000
