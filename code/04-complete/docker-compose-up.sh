#!/bin/bash
# =============================================================================
# Docker Compose Up Script
# Starts all services defined in docker-compose.yml
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODE="${1:-up}"

echo "========================================"
echo "Order Service - Docker Compose"
echo "========================================"

case "$MODE" in
    up)
        echo "Starting services..."
        docker compose up -d --build
        echo ""
        echo "✅ Services started!"
        echo ""
        echo "📍 Access the API:"
        echo "   Health:   http://localhost:8000/api/v1/health"
        echo "   Docs:     http://localhost:8000/docs"
        echo "   ReDoc:    http://localhost:8000/redoc"
        echo ""
        echo "📋 Useful commands:"
        echo "   View logs:  docker compose logs -f"
        echo "   Stop:       ./docker-compose-up.sh down"
        echo "   Restart:    ./docker-compose-up.sh restart"
        ;;
    down)
        echo "Stopping services..."
        docker compose down
        echo "✅ Services stopped!"
        ;;
    restart)
        echo "Restarting services..."
        docker compose down
        docker compose up -d --build
        echo "✅ Services restarted!"
        ;;
    logs)
        docker compose logs -f
        ;;
    status)
        docker compose ps
        ;;
    *)
        echo "Usage: $0 {up|down|restart|logs|status}"
        echo ""
        echo "Commands:"
        echo "  up       - Start all services (default)"
        echo "  down     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  logs     - Follow logs"
        echo "  status   - Show service status"
        exit 1
        ;;
esac
