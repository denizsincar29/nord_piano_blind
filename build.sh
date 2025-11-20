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

# Load from .env if BUILD_DIR not specified
if [ -z "$BUILD_DIR" ] && [ -f .env ]; then
    source .env
fi

# Use default 'dist' if still not specified
if [ -z "$BUILD_DIR" ]; then
    BUILD_DIR="dist"
fi

# If directory was specified via -d flag, save it to .env
if [ "$#" -gt 0 ] && [ "$1" = "-d" ]; then
    echo "BUILD_DIR=\"$BUILD_DIR\"" > .env
    echo "📝 Build directory saved to .env: $BUILD_DIR"
    echo "   Next time you don't need to specify the build directory."
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

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Distribution folder: $BUILD_DIR"
echo "   - $BUILD_DIR/index.html (language selection)"
echo "   - $BUILD_DIR/book-ru/ (Russian documentation)"
echo "   - $BUILD_DIR/book-en/ (English documentation)"
echo ""
echo "🚀 To deploy, copy the entire '$BUILD_DIR' folder to your web server"
echo "💻 To test locally: python3 -m http.server 8000 --directory $BUILD_DIR"
