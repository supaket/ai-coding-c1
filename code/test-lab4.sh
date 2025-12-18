#!/bin/bash
# Run tests for Lab 4: Complete Solution

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/04-complete"

echo "🧪 Running Tests for Lab 4"
echo "=========================="
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

# Run pytest
echo "Running pytest with coverage..."
echo ""

pytest tests/ -v --cov=app --cov-report=term-missing

echo ""
echo "✅ Tests complete!"
