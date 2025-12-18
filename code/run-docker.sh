#!/bin/bash
# Run Lab 4 using Docker Compose

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/04-complete"

echo "🐳 Starting Lab 4 with Docker Compose"
echo "======================================"
echo ""

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    exit 1
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up --build

echo ""
echo "🌐 Application available at:"
echo "   FastAPI: http://localhost:8000"
echo "   Swagger docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
