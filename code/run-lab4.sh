#!/bin/bash
# Run Lab 4: Complete Solution with Tests

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/04-complete"

echo "🚀 Starting Lab 4: Complete Solution"
echo "====================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup..."
    cd "$SCRIPT_DIR"
    ./setup.sh
    cd "$SCRIPT_DIR/04-complete"
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "🌐 Starting FastAPI app on http://localhost:8000"
echo "   Swagger docs: http://localhost:8000/docs"
echo "   ReDoc: http://localhost:8000/redoc"
echo "   Health check: http://localhost:8000/health"
echo "   Orders API: http://localhost:8000/api/v1/orders"
echo ""
echo "💡 To run tests: ./test-lab4.sh"
echo "   Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --port 8000
