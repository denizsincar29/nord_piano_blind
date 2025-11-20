#!/bin/bash
set -e

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
rm -rf book-ru/book book-en/book dist

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
mkdir -p dist
cp -r book-ru/book dist/book-ru
cp -r book-en/book dist/book-en
cp index.html dist/

echo ""
echo "✅ Build complete!"
echo ""
echo "📁 Distribution folder: ./dist/"
echo "   - dist/index.html (language selection)"
echo "   - dist/book-ru/ (Russian documentation)"
echo "   - dist/book-en/ (English documentation)"
echo ""
echo "🚀 To deploy, copy the entire 'dist' folder to your web server"
echo "💻 To test locally: python3 -m http.server 8000 --directory dist"
