#!/bin/bash
# p5.js Skill — Local Development Server
# Serves the current directory over HTTP for loading local assets (fonts, images)
#
# Usage:
#   bash scripts/serve.sh [port] [directory]
#
# Examples:
#   bash scripts/serve.sh                    # serve CWD on port 8080
#   bash scripts/serve.sh 3000               # serve CWD on port 3000
#   bash scripts/serve.sh 8080 ./my-project  # serve specific directory

PORT="${1:-8080}"
DIR="${2:-.}"

echo "=== p5.js Dev Server ==="
echo "Serving: $(cd "$DIR" && pwd)"
echo "URL:     http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""

if ! cd "$DIR"; then
	echo "Error: Cannot change to directory $DIR"
	exit 1
fi

if command -v uv &>/dev/null; then
	uv run python -m http.server "$PORT"
elif command -v npx &>/dev/null; then
	echo "uv not found. Falling back to Node.js..."
	npx serve -l "$PORT" "$DIR"
else
	echo "Error: Need uv or npx (Node.js) for local server"
	exit 1
fi
