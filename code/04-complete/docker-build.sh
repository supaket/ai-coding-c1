#!/bin/bash
# =============================================================================
# Docker Build Script for Order Service API
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE_NAME="order-service"
TAG="${1:-latest}"

echo "========================================"
echo "Building Docker Image: $IMAGE_NAME:$TAG"
echo "========================================"

# Build the Docker image
docker build -t "$IMAGE_NAME:$TAG" .

echo ""
echo "✅ Build complete!"
echo "   Image: $IMAGE_NAME:$TAG"
echo ""
echo "To run the container:"
echo "   ./docker-run.sh"
echo ""
echo "Or use docker-compose:"
echo "   ./docker-compose-up.sh"
