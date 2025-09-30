#!/bin/bash
# =============================================================================
#  Filename: start.sh
#
#  Short Description: Startup script for AI News Newsletter
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

echo "🤖 Starting AI News Newsletter..."
echo "📦 Installing dependencies..."

# Install dependencies
uv sync

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your API keys before running again."
    echo "   Required: OPENAI_API_KEY"
    echo "   Optional: SERPAPI_API_KEY"
    exit 1
fi

echo "🚀 Starting server..."
echo "📡 Server will be available at http://localhost:8080"
echo "📚 API documentation at http://localhost:8080/docs"
echo "🔄 Cache TTL: 10 minutes"
echo "-" * 50

# Start the application
uv run python main.py
