#!/bin/bash
set -e
# Build standalone accessible HTML manuals (no mdbook required)

# Load DEPLOY_DIR from .env if present
if [ -f .env ]; then source .env; fi

OUTPUT_DIR="${DEPLOY_DIR:-dist}/html-manual"

# ── Detect Python ──────────────────────────────────────────────────────────────
# Priority: uv run python > uv run python3 > python3 > python
find_python() {
    # uv: run python inside the uv-managed environment
    if command -v uv &>/dev/null; then
        if uv run python --version &>/dev/null 2>&1; then
            echo "uv run python"
            return
        fi
        if uv run python3 --version &>/dev/null 2>&1; then
            echo "uv run python3"
            return
        fi
    fi
    # Standalone python3
    if command -v python3 &>/dev/null; then
        echo "python3"
        return
    fi
    # Standalone python (might be 3.x)
    if command -v python &>/dev/null; then
        local ver
        ver=$(python --version 2>&1)
        if [[ "$ver" == Python\ 3* ]]; then
            echo "python"
            return
        fi
    fi
    echo ""
}

PYTHON=$(find_python)
if [ -z "$PYTHON" ]; then
    echo "❌ Python 3 not found. Tried: uv run python, uv run python3, python3, python"
    echo "   Install uv (https://docs.astral.sh/uv/) or Python 3 directly."
    exit 1
fi
echo "🐍 Using Python: $PYTHON"

# ── Build ──────────────────────────────────────────────────────────────────────
echo "🔨 Building standalone HTML manuals..."
$PYTHON build_html.py

if [ -n "$DEPLOY_DIR" ]; then
    echo "📦 Copying to deploy dir: $DEPLOY_DIR/html-manual"
    mkdir -p "$OUTPUT_DIR"
    cp -r html-manual/* "$OUTPUT_DIR/"
fi

echo ""
echo "✅ HTML manual built!"
echo "📁 Files: html-manual/index.html, html-manual/ru/, html-manual/en/"
echo "💻 Test: $PYTHON -m http.server 8000 --directory html-manual"
