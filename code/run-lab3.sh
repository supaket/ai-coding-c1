#!/bin/bash
# Run Lab 3: Business Logic Implementation

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/03-business-logic"

echo "🚀 Starting Lab 3: Business Logic Implementation"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup..."
    cd "$SCRIPT_DIR"
    ./setup.sh
    cd "$SCRIPT_DIR/03-business-logic"
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "🌐 Starting FastAPI app on http://localhost:8000"
echo "   Swagger docs: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Health check: http://localhost:8000/health"
echo "   Orders API: http://localhost:8000/api/v1/orders"
echo "   Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --port 8000
