#!/bin/bash
# Script quản lý Docker cho Captcha OCR API

case "$1" in
    start)
        echo "🚀 Starting Captcha OCR API with Docker Compose (daemon mode)..."
        docker compose up -d
        echo "✅ API started in background at http://localhost:8086"
        echo "🔍 Check status: bash docker.sh status"
        echo "📋 View logs: bash docker.sh logs"
        ;;
    stop)
        echo "🛑 Stopping Captcha OCR API..."
        docker compose down
        echo "✅ API stopped"
        ;;
    restart)
        echo "🔄 Restarting Captcha OCR API..."
        docker compose down
        docker compose up -d
        echo "✅ API restarted"
        ;;
    logs)
        echo "📋 Captcha OCR API logs:"
        docker compose logs -f
        ;;
    status)
        echo "📊 Captcha OCR API status:"
        docker compose ps
        ;;
    test)
        echo "🧪 Testing Captcha OCR API..."
        sleep 3
        curl -X GET http://localhost:8086/api/health || echo "❌ API not responding"
        ;;
    clean)
        echo "🧹 Cleaning up Docker resources..."
        docker compose down -v
        docker system prune -f
        echo "✅ Cleanup completed"
        ;;
    *)
        echo "🐳 Docker Commands for Captcha OCR API:"
        echo ""
        echo "🚀 Main Commands:"
        echo "  bash docker.sh start    - Start API (daemon mode)"
        echo "  bash docker.sh stop     - Stop API"
        echo "  bash docker.sh restart  - Restart API"
        echo ""
        echo "📋 Monitor:"
        echo "  bash docker.sh status   - Check status"
        echo "  bash docker.sh logs     - View logs"
        echo "  bash docker.sh test     - Test API"
        echo ""
        echo "🧹 Cleanup:"
        echo "  bash docker.sh clean    - Clean up all resources"
        echo ""
        echo "🎯 Quick Start:"
        echo "  bash docker.sh start    # Start API in background"
        echo "  bash docker.sh test     # Test API"
        ;;
esac
