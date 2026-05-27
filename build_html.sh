#!/bin/bash
set -e
# Build standalone accessible HTML manuals (no mdbook required)

# Load DEPLOY_DIR from .env if present
if [ -f .env ]; then source .env; fi

OUTPUT_DIR="${DEPLOY_DIR:-dist}/html-manual"

echo "🔨 Building standalone HTML manuals..."
python3 build_html.py

if [ -n "$DEPLOY_DIR" ]; then
    echo "📦 Copying to deploy dir: $DEPLOY_DIR/html-manual"
    mkdir -p "$OUTPUT_DIR"
    cp -r html-manual/* "$OUTPUT_DIR/"
fi

echo ""
echo "✅ HTML manual built!"
echo "📁 Files: html-manual/index.html, html-manual/ru/, html-manual/en/"
echo "💻 Test: python3 -m http.server 8000 --directory html-manual"
