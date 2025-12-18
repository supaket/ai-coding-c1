#!/bin/bash
# Run Lab 1: Legacy Flask Application

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/01-legacy-app"

echo "🚀 Starting Lab 1: Legacy Flask Application"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Running setup..."
    cd "$SCRIPT_DIR"
    ./setup.sh
    cd "$SCRIPT_DIR/01-legacy-app"
fi

# Activate virtual environment
source venv/bin/activate

# Seed database if it doesn't exist
if [ ! -f "shopfast.db" ]; then
    echo "📊 Seeding database..."
    python seed_data.py
    echo ""
fi

# Run the application
echo "🌐 Starting Flask app on http://localhost:5000"
echo "   API endpoint: http://localhost:5000/api/orders"
echo "   Press Ctrl+C to stop"
echo ""

python app.py
