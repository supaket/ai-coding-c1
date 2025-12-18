#!/bin/bash
# =============================================================================
# Docker Stop Script
# Stops all Order Service containers
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CONTAINER_NAME="order-service-api"

echo "========================================"
echo "Stopping Order Service Containers"
echo "========================================"

# Stop standalone container
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping standalone container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    echo "✅ Standalone container stopped"
fi

# Stop docker-compose services
if [ -f "docker-compose.yml" ]; then
    echo "Stopping docker-compose services..."
    docker-compose down 2>/dev/null || true
    echo "✅ Docker-compose services stopped"
fi

echo ""
echo "All containers stopped!"
