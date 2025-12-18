#!/bin/bash
# =============================================================================
# Docker Clean Script
# Removes containers, images, and optionally data volumes
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE_NAME="order-service"
CONTAINER_NAME="order-service-api"
CLEAN_DATA="${1:-no}"

echo "========================================"
echo "Cleaning Docker Resources"
echo "========================================"

# Stop and remove containers
echo "Stopping containers..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true
docker-compose down 2>/dev/null || true

# Remove image
echo "Removing image: $IMAGE_NAME"
docker rmi "$IMAGE_NAME:latest" 2>/dev/null || true

# Remove volumes (optional)
if [ "$CLEAN_DATA" = "all" ] || [ "$CLEAN_DATA" = "--all" ]; then
    echo "Removing data volumes..."
    docker volume rm 04-complete_order-data 2>/dev/null || true
    rm -rf "$SCRIPT_DIR/data" 2>/dev/null || true
    echo "✅ Data volumes removed"
fi

# Prune dangling images
echo "Pruning dangling images..."
docker image prune -f 2>/dev/null || true

echo ""
echo "✅ Cleanup complete!"
echo ""
if [ "$CLEAN_DATA" != "all" ] && [ "$CLEAN_DATA" != "--all" ]; then
    echo "Note: Data volumes preserved. To remove all data:"
    echo "   ./docker-clean.sh --all"
fi
