#!/bin/bash
set -e

# Parse command line arguments
BUILD_DIR=""
while getopts "d:" opt; do
  case $opt in
    d)
      BUILD_DIR="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      echo "Usage: $0 [-d directory]"
      exit 1
      ;;
  esac
done

# Load from .env if BUILD_DIR not specified via flag
# Supports both DEPLOY_DIR and BUILD_DIR variable names in .env
if [ -z "$BUILD_DIR" ] && [ -f .env ]; then
    source .env
    # Prefer DEPLOY_DIR if set, fall back to BUILD_DIR
    if [ -n "$DEPLOY_DIR" ]; then
        BUILD_DIR="$DEPLOY_DIR"
    fi
fi

# Use default 'dist' if still not specified
if [ -z "$BUILD_DIR" ]; then
    BUILD_DIR="dist"
fi

# If directory was specified via -d flag, save it to .env as DEPLOY_DIR
if [ -n "$OPTARG" ] || { [ "$#" -ge 2 ] && [ "$1" = "-d" ]; }; then
    echo "DEPLOY_DIR=\"$BUILD_DIR\"" > .env
    echo "📝 Deploy directory saved to .env: $BUILD_DIR"
    echo "   Next time you don't need to specify the deploy directory."
    echo ""
fi

echo "🔨 Building Nord Piano 6 Documentation..."
echo ""

# Ensure mdbook is in PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Check if mdbook is installed
if ! command -v mdbook &> /dev/null; then
    echo "❌ mdbook not found. Please install it first:"
    echo "   cargo install mdbook"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf book-ru/book book-en/book "$BUILD_DIR"

# Build Russian version
echo "📚 Building Russian version..."
cd book-ru
mdbook build
cd ..

# Build English version
echo "📚 Building English version..."
cd book-en
mdbook build
cd ..

# Create distribution folder
echo "📦 Creating distribution folder..."
mkdir -p "$BUILD_DIR"
cp -r book-ru/book "$BUILD_DIR/book-ru"
cp -r book-en/book "$BUILD_DIR/book-en"
cp index.html "$BUILD_DIR/"

# Optionally build standalone HTML manual (no mdbook needed, Python only)
# Detect Python: uv run python > uv run python3 > python3 > python
if [ -f build_html.py ]; then
    PYTHON=""
    if command -v uv &>/dev/null; then
        uv run python --version &>/dev/null 2>&1  && PYTHON="uv run python"
        [ -z "$PYTHON" ] && uv run python3 --version &>/dev/null 2>&1 && PYTHON="uv run python3"
    fi
    [ -z "$PYTHON" ] && command -v python3 &>/dev/null && PYTHON="python3"
    if [ -z "$PYTHON" ] && command -v python &>/dev/null; then
        [[ "$(python --version 2>&1)" == Python\ 3* ]] && PYTHON="python"
    fi

    if [ -n "$PYTHON" ]; then
        echo "📚 Building standalone HTML manual (using $PYTHON)..."
        $PYTHON build_html.py
        mkdir -p "$BUILD_DIR/html-manual"
        cp -r html-manual/* "$BUILD_DIR/html-manual/"
    else
        echo "⚠️  Python 3 not found — skipping HTML manual build."
        echo "   Install uv or Python 3 to enable it."
    fi
fi

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Distribution folder: $BUILD_DIR"
echo "   - $BUILD_DIR/index.html (language selection)"
echo "   - $BUILD_DIR/book-ru/ (Russian mdBook documentation)"
echo "   - $BUILD_DIR/book-en/ (English mdBook documentation)"
echo "   - $BUILD_DIR/html-manual/ (standalone accessible HTML, no mdBook needed)"
echo ""
echo "🚀 To deploy, copy the entire '$BUILD_DIR' folder to your web server"
echo "💻 To test locally: python3 -m http.server 8000 --directory $BUILD_DIR  (or: uv run python -m http.server 8000)"
