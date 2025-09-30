#!/bin/bash
# =============================================================================
#  Filename: start_clean.sh
#
#  Short Description: Start server with clean logs (suppress WebSocket errors)
#
#  Creation date: 2025-01-27
#  Author: Priya
# =============================================================================

echo "🤖 Starting AI News Newsletter (Clean Mode)"
echo "=========================================="

# Kill any existing processes
pkill -f "python main.py" 2>/dev/null

# Start server with filtered logs
uv run python main.py 2>&1 | grep -v "WebSocket.*403\|connection rejected\|connection closed"
