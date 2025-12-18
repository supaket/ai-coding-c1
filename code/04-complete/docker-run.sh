#!/bin/bash
# =============================================================================
# Docker Run Script for Order Service API
# Runs the container standalone without docker-compose
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE_NAME="order-service"
CONTAINER_NAME="order-service-api"
PORT="${1:-8000}"

echo "========================================"
echo "Running Order Service Container"
echo "========================================"

# Stop and remove existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
fi

# Create data directory for SQLite
mkdir -p "$SCRIPT_DIR/data"

# Run the container
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:8000" \
    -e ENVIRONMENT=development \
    -e DATABASE_URL=sqlite+aiosqlite:///./data/orders.db \
    -v "$SCRIPT_DIR/data:/app/data" \
    --restart unless-stopped \
    "$IMAGE_NAME:latest"

echo ""
echo "✅ Container started!"
echo ""
echo "   Container: $CONTAINER_NAME"
echo "   Port:      $PORT"
echo ""
echo "📍 Access the API:"
echo "   Health:   http://localhost:$PORT/api/v1/health"
echo "   Docs:     http://localhost:$PORT/docs"
echo "   ReDoc:    http://localhost:$PORT/redoc"
echo ""
echo "📋 Useful commands:"
echo "   View logs:     docker logs -f $CONTAINER_NAME"
echo "   Stop:          docker stop $CONTAINER_NAME"
echo "   Remove:        docker rm $CONTAINER_NAME"
