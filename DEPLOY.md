# Deployment Instructions

## Building the Documentation

To build the complete bilingual documentation website, run:

```bash
./build.sh
```

This script will:
1. Clean previous builds
2. Build the Russian version (`book-ru/`)
3. Build the English version (`book-en/`)
4. Create a `dist/` folder with all compiled HTML
5. Copy the language selection page (`index.html`)

## Distribution Folder Structure

After building, the `dist/` folder contains everything needed for deployment:

```
dist/
├── index.html           # Language selection landing page
├── book-ru/            # Complete Russian documentation
│   ├── index.html
│   ├── 01-control-types.html
│   ├── ... (all chapters)
│   └── (all assets: CSS, JS, fonts)
└── book-en/            # Complete English documentation
    ├── index.html
    ├── 01-control-types.html
    ├── ... (all chapters)
    └── (all assets: CSS, JS, fonts)
```

## Deploying to a Web Server

### Option 1: Copy to Web Server

Simply copy the entire `dist/` folder to your web server:

```bash
# Example: copy to Apache web root
sudo cp -r dist/* /var/www/html/nord-piano-docs/

# Example: copy via SCP to remote server
scp -r dist/* user@server:/path/to/webroot/
```

### Option 2: Static Hosting Services

The `dist/` folder can be deployed to any static hosting service:

- **GitHub Pages**: Push `dist/` contents to `gh-pages` branch
- **Netlify**: Drag and drop the `dist/` folder
- **Vercel**: Deploy the `dist/` folder
- **AWS S3**: Upload `dist/` contents to S3 bucket

### Option 3: Test Locally

To test the documentation locally before deploying:

```bash
# Start a local web server
python3 -m http.server 8000 --directory dist

# Or use npx
npx serve dist

# Then open: http://localhost:8000
```

## Requirements

- **mdBook** must be installed to build the documentation:
  ```bash
  cargo install mdbook
  ```

## Building from Source

If you need to modify the documentation:

1. Edit markdown files in `book-ru/src/` (Russian) or `book-en/src/` (English)
2. Run `./build.sh` to rebuild
3. The updated HTML will be in `dist/`

## Notes

- The `dist/` folder is self-contained and includes all necessary assets
- No server-side processing is required - it's pure static HTML/CSS/JS
- The documentation is responsive and works on mobile devices
- Full-text search is included in each language version
- Original `.txt` files are preserved in `Описание PIANO - папка с текстовыми файлами/`
