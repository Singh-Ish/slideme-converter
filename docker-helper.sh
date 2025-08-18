#!/bin/bash

# Slideme Converter Docker Helper Script
# This script provides convenient commands for Docker operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

show_help() {
    echo "Slideme Converter Docker Helper"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build the Docker image"
    echo "  run         Run the application with Docker Compose"
    echo "  dev         Run in development mode with volume mounting"
    echo "  prod        Run in production mode"
    echo "  stop        Stop all running containers"
    echo "  clean       Stop containers and remove images"
    echo "  logs        View application logs"
    echo "  shell       Access container shell"
    echo "  health      Check application health"
    echo "  help        Show this help message"
    echo ""
}

build() {
    echo "🔨 Building Docker image..."
    docker build -t slideme-converter .
    echo "✅ Build complete!"
}

run_dev() {
    echo "🚀 Starting in development mode..."
    docker-compose up -d
    echo "✅ Application running at http://localhost:8501"
    echo "📋 Use '$0 logs' to view logs"
}

run_prod() {
    echo "🚀 Starting in production mode..."
    docker-compose --profile production up -d slideme-converter-prod
    echo "✅ Application running at http://localhost:8501"
}

stop() {
    echo "🛑 Stopping containers..."
    docker-compose down
    echo "✅ Containers stopped"
}

clean() {
    echo "🧹 Cleaning up containers and images..."
    docker-compose down -v
    docker rmi slideme-converter 2>/dev/null || true
    echo "✅ Cleanup complete"
}

logs() {
    echo "📋 Viewing logs..."
    docker-compose logs -f
}

shell() {
    echo "🐚 Accessing container shell..."
    CONTAINER_ID=$(docker-compose ps -q slideme-converter)
    if [ -z "$CONTAINER_ID" ]; then
        echo "❌ No running container found. Start the application first."
        exit 1
    fi
    docker exec -it "$CONTAINER_ID" /bin/bash
}

health() {
    echo "🔍 Checking application health..."
    curl -f http://localhost:8501/_stcore/health && echo "✅ Application is healthy" || echo "❌ Application is not responding"
}

case "${1:-help}" in
    build)
        build
        ;;
    run|dev)
        run_dev
        ;;
    prod)
        run_prod
        ;;
    stop)
        stop
        ;;
    clean)
        clean
        ;;
    logs)
        logs
        ;;
    shell)
        shell
        ;;
    health)
        health
        ;;
    help|*)
        show_help
        ;;
esac
