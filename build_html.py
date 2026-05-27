#!/usr/bin/env python3
"""
Build standalone accessible HTML manuals from mdBook markdown sources.
Produces one self-contained HTML file per language.
"""
import os, re, json, markdown
from pathlib import Path

def parse_summary(summary_path):
    """Parse SUMMARY.md and return ordered list of (title, filename, is_part_header)."""
    chapters = []
    with open(summary_path, encoding='utf-8') as f:
        for line in f:
            # Part headers: # Part N: Title
            m = re.match(r'^#\s+(.+)$', line.strip())
            if m:
                chapters.append({'type': 'part', 'title': m.group(1)})
                continue
            # Chapter links: - [Title](file.md)
            m = re.match(r'^\s*-\s+\[(.+?)\]\((.+?)\)', line.strip())
            if m:
                chapters.append({'type': 'chapter', 'title': m.group(1), 'file': m.group(2)})
                continue
            # Intro link: [Title](file.md)
            m = re.match(r'^\[(.+?)\]\((.+?)\)', line.strip())
            if m:
                chapters.append({'type': 'intro', 'title': m.group(1), 'file': m.group(2)})
    return chapters

def md_to_html(text):
    """Convert markdown text to HTML."""
    return markdown.markdown(text, extensions=['tables', 'fenced_code', 'nl2br'])

def extract_button_info(chapters_data):
    """
    Extract button descriptions from chapter 01 (control types) and all chapters.
    Returns dict: button_name -> description text.
    """
    buttons = {}
    # Patterns to look for headings that describe specific buttons
    btn_pattern = re.compile(
        r'###\s+(.+?)\n(.*?)(?=\n###|\n##|\Z)', re.DOTALL
    )
    for ch in chapters_data:
        if ch.get('type') != 'chapter' and ch.get('type') != 'intro':
            continue
        content = ch.get('content', '')
        for m in btn_pattern.finditer(content):
            name = m.group(1).strip()
            desc = m.group(2).strip()
            if len(desc) > 20:
                # Store both the raw name and variants
                buttons[name.upper()] = {'name': name, 'desc': desc[:400]}
    return buttons

def build_manual(src_dir, out_path, lang, title):
    src = Path(src_dir)
    summary_path = src / 'SUMMARY.md'
    chapters = parse_summary(summary_path)

    # Load chapter content
    for ch in chapters:
        if 'file' in ch:
            fpath = src / ch['file']
            if fpath.exists():
                ch['content'] = fpath.read_text(encoding='utf-8')
                ch['html'] = md_to_html(ch['content'])
                # Generate an id-safe slug
                ch['id'] = re.sub(r'[^a-z0-9]+', '-', ch['file'].lower().replace('.md',''))
            else:
                ch['html'] = '<p><em>File not found.</em></p>'
                ch['id'] = 'missing'

    # Extract button info from chapter 01
    button_db = extract_button_info(chapters)

    # Build TOC JSON for JS
    toc_items = []
    for ch in chapters:
        if ch['type'] == 'part':
            toc_items.append({'type': 'part', 'title': ch['title']})
        elif ch['type'] in ('chapter', 'intro'):
            toc_items.append({'type': 'chapter', 'title': ch['title'], 'id': ch.get('id','')})

    toc_json = json.dumps(toc_items, ensure_ascii=False)
    btn_json = json.dumps(button_db, ensure_ascii=False)

    # Build chapter HTML sections
    sections_html = []
    for ch in chapters:
        if ch['type'] == 'part':
            continue
        cid = ch.get('id', '')
        ctitle = ch['title']
        chtml = ch.get('html', '')
        sections_html.append(f'<article id="{cid}" class="chapter" tabindex="-1">\n{chtml}\n</article>')

    all_sections = '\n'.join(sections_html)

    if lang == 'ru':
        skip_label = 'Перейти к содержимому'
        toc_label = 'Содержание'
        close_label = 'Закрыть'
        search_label = 'Поиск по руководству...'
        found_label = 'найдено результатов'
        no_results = 'Ничего не найдено'
        location_prefix = 'Расположение'
        close_popup = 'Закрыть (Escape)'
    else:
        skip_label = 'Skip to content'
        toc_label = 'Table of Contents'
        close_label = 'Close'
        search_label = 'Search the manual...'
        found_label = 'results found'
        no_results = 'No results found'
        location_prefix = 'Location'
        close_popup = 'Close (Escape)'

    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
/* ===== RESET & BASE ===== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
:root {{
  --bg: #1a1a1a;
  --surface: #242424;
  --surface2: #2e2e2e;
  --border: #3a3a3a;
  --text: #e8e8e8;
  --text-dim: #aaa;
  --accent: #e85c33;
  --accent2: #ff7a52;
  --link: #6cb4e4;
  --link-hover: #9dd0f5;
  --focus: #ffcc00;
  --toc-width: 320px;
  --header-height: 52px;
}}
html {{ scroll-behavior: smooth; }}
body {{
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.7;
  font-size: 1rem;
}}

/* ===== SKIP LINK ===== */
.skip-link {{
  position: absolute;
  top: -100px;
  left: 0;
  background: var(--focus);
  color: #000;
  padding: 10px 18px;
  font-weight: bold;
  z-index: 9999;
  text-decoration: none;
  border-radius: 0 0 6px 0;
}}
.skip-link:focus {{ top: 0; }}

/* ===== HEADER ===== */
header {{
  position: fixed;
  top: 0; left: 0; right: 0;
  height: var(--header-height);
  background: var(--surface);
  border-bottom: 2px solid var(--accent);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 16px;
  z-index: 200;
}}
#toc-toggle {{
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 6px 12px;
  font-size: 0.9rem;
  cursor: pointer;
  flex-shrink: 0;
}}
#toc-toggle:focus {{ outline: 3px solid var(--focus); }}
header h1 {{
  font-size: 1rem;
  font-weight: 600;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  color: var(--accent2);
}}
#search-input {{
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: 5px;
  padding: 5px 10px;
  font-size: 0.9rem;
  width: 200px;
}}
#search-input:focus {{ outline: 3px solid var(--focus); border-color: var(--focus); }}

/* ===== TOC PANEL ===== */
#toc-panel {{
  position: fixed;
  top: var(--header-height);
  left: 0;
  width: var(--toc-width);
  height: calc(100vh - var(--header-height));
  background: var(--surface);
  border-right: 1px solid var(--border);
  overflow-y: auto;
  z-index: 150;
  padding: 8px 0 32px;
  transform: translateX(0);
  transition: transform 0.2s ease;
}}
#toc-panel.hidden {{ transform: translateX(-100%); }}
#toc-panel nav {{ padding: 0; }}
#toc-panel h2 {{
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-dim);
  padding: 10px 16px 4px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 4px;
}}
.toc-part {{
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  padding: 10px 16px 2px;
  font-weight: 700;
  margin-top: 6px;
}}
.toc-link {{
  display: block;
  padding: 7px 16px 7px 24px;
  color: var(--text);
  text-decoration: none;
  font-size: 0.9rem;
  border-left: 3px solid transparent;
  transition: background 0.1s, border-color 0.1s;
}}
.toc-link:hover {{ background: var(--surface2); color: var(--link-hover); }}
.toc-link:focus {{ outline: 3px solid var(--focus); outline-offset: -3px; }}
.toc-link.active {{ border-left-color: var(--accent); color: var(--accent2); font-weight: 600; }}

/* ===== SEARCH RESULTS ===== */
#search-results {{
  position: fixed;
  top: var(--header-height);
  left: 0;
  right: 0;
  background: var(--surface);
  border-bottom: 2px solid var(--accent);
  z-index: 140;
  max-height: 50vh;
  overflow-y: auto;
  padding: 12px 16px;
  display: none;
}}
#search-results.visible {{ display: block; }}
#search-status {{ font-size: 0.85rem; color: var(--text-dim); margin-bottom: 8px; }}
.search-hit {{
  display: block;
  padding: 8px 12px;
  margin: 4px 0;
  background: var(--surface2);
  border-radius: 6px;
  color: var(--text);
  text-decoration: none;
  font-size: 0.9rem;
}}
.search-hit:focus, .search-hit:hover {{ background: var(--border); outline: 3px solid var(--focus); }}
.search-hit mark {{ background: var(--focus); color: #000; border-radius: 2px; padding: 0 2px; }}

/* ===== MAIN CONTENT ===== */
#main {{
  margin-left: var(--toc-width);
  margin-top: var(--header-height);
  padding: 32px 48px 80px;
  max-width: 900px;
  transition: margin-left 0.2s ease;
}}
#main.toc-hidden {{ margin-left: 0; }}
@media (max-width: 800px) {{
  #main {{ margin-left: 0; padding: 20px 16px 60px; }}
  #toc-panel {{ width: 280px; }}
  #search-input {{ width: 130px; }}
}}

/* ===== TYPOGRAPHY ===== */
.chapter {{ margin-bottom: 60px; padding-bottom: 40px; border-bottom: 1px solid var(--border); }}
.chapter:last-child {{ border-bottom: none; }}
.chapter h1 {{ font-size: 1.8rem; color: var(--accent2); margin-bottom: 24px; padding-bottom: 10px; border-bottom: 2px solid var(--accent); }}
.chapter h2 {{ font-size: 1.3rem; color: var(--text); margin: 28px 0 12px; padding-left: 10px; border-left: 4px solid var(--accent); }}
.chapter h3 {{ font-size: 1.05rem; color: var(--accent2); margin: 20px 0 8px; }}
.chapter h4 {{ font-size: 1rem; color: var(--text-dim); margin: 14px 0 6px; }}
.chapter p {{ margin: 10px 0; }}
.chapter ul, .chapter ol {{ padding-left: 1.8em; margin: 10px 0; }}
.chapter li {{ margin: 5px 0; }}
.chapter strong {{ color: var(--accent2); }}
.chapter em {{ color: var(--text-dim); }}
.chapter a {{ color: var(--link); text-decoration: underline; }}
.chapter a:hover {{ color: var(--link-hover); }}
.chapter a:focus {{ outline: 3px solid var(--focus); border-radius: 2px; }}
.chapter code {{ background: var(--surface2); padding: 1px 5px; border-radius: 3px; font-size: 0.9em; color: var(--accent2); }}
.chapter pre {{ background: var(--surface2); padding: 16px; border-radius: 6px; overflow-x: auto; margin: 14px 0; border: 1px solid var(--border); }}
.chapter blockquote {{ border-left: 4px solid var(--accent); padding: 8px 16px; background: var(--surface2); margin: 14px 0; border-radius: 0 6px 6px 0; color: var(--text-dim); font-style: italic; }}
.chapter table {{ width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.9rem; }}
.chapter th {{ background: var(--surface2); border: 1px solid var(--border); padding: 8px 12px; text-align: left; color: var(--accent2); }}
.chapter td {{ border: 1px solid var(--border); padding: 8px 12px; }}
.chapter tr:nth-child(even) td {{ background: var(--surface2); }}

/* ===== BUTTON LINKS (clickable button names) ===== */
.btn-ref {{
  display: inline;
  background: var(--surface2);
  border: 1px solid var(--accent);
  border-radius: 4px;
  padding: 1px 6px;
  color: var(--accent2);
  font-weight: 600;
  cursor: pointer;
  font-size: inherit;
  font-family: inherit;
  text-decoration: none;
  transition: background 0.15s;
}}
.btn-ref:hover {{ background: var(--accent); color: #fff; }}
.btn-ref:focus {{ outline: 3px solid var(--focus); outline-offset: 2px; }}

/* ===== POPUP ===== */
#btn-popup {{
  display: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--surface);
  border: 2px solid var(--accent);
  border-radius: 10px;
  padding: 24px 28px;
  z-index: 500;
  max-width: min(520px, 90vw);
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 40px rgba(0,0,0,0.7);
}}
#btn-popup.visible {{ display: block; }}
#btn-popup h3 {{ color: var(--accent2); margin-bottom: 12px; font-size: 1.1rem; }}
#btn-popup-body {{ color: var(--text); font-size: 0.95rem; line-height: 1.7; }}
#btn-popup-close {{
  margin-top: 18px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  font-size: 0.95rem;
  cursor: pointer;
  display: block;
  width: 100%;
}}
#btn-popup-close:focus {{ outline: 3px solid var(--focus); }}
#popup-overlay {{
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  z-index: 499;
}}
#popup-overlay.visible {{ display: block; }}
</style>
</head>
<body>
<a href="#main" class="skip-link">{skip_label}</a>

<header>
  <button id="toc-toggle" aria-expanded="true" aria-controls="toc-panel">☰ {toc_label}</button>
  <h1>{title}</h1>
  <input type="search" id="search-input" placeholder="{search_label}" aria-label="{search_label}" autocomplete="off">
</header>

<div id="search-results" role="region" aria-live="polite" aria-label="{search_label}">
  <div id="search-status"></div>
  <div id="search-hits"></div>
</div>

<nav id="toc-panel" aria-label="{toc_label}">
  <h2>{toc_label}</h2>
  <div id="toc-tree"></div>
</nav>

<div id="popup-overlay" aria-hidden="true"></div>
<div id="btn-popup" role="dialog" aria-modal="true" aria-labelledby="btn-popup-title" tabindex="-1">
  <h3 id="btn-popup-title"></h3>
  <div id="btn-popup-body"></div>
  <button id="btn-popup-close">{close_popup}</button>
</div>

<main id="main" tabindex="-1">
{all_sections}
</main>

<script>
(function() {{
  // ===== DATA =====
  const TOC = {toc_json};
  const BTNS = {btn_json};

  // ===== TOC TREE =====
  const tocTree = document.getElementById('toc-tree');
  TOC.forEach(item => {{
    if (item.type === 'part') {{
      const d = document.createElement('div');
      d.className = 'toc-part';
      d.textContent = item.title;
      tocTree.appendChild(d);
    }} else {{
      const a = document.createElement('a');
      a.className = 'toc-link';
      a.href = '#' + item.id;
      a.textContent = item.title;
      a.dataset.id = item.id;
      tocTree.appendChild(a);
    }}
  }});

  // ===== TOC TOGGLE =====
  const tocPanel = document.getElementById('toc-panel');
  const mainEl = document.getElementById('main');
  const tocBtn = document.getElementById('toc-toggle');
  let tocOpen = true;

  function setToc(open) {{
    tocOpen = open;
    tocPanel.classList.toggle('hidden', !open);
    mainEl.classList.toggle('toc-hidden', !open);
    tocBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }}

  tocBtn.addEventListener('click', () => setToc(!tocOpen));

  // ===== ACTIVE TOC LINK via IntersectionObserver =====
  const chapters = document.querySelectorAll('.chapter');
  const tocLinks = document.querySelectorAll('.toc-link');

  const observer = new IntersectionObserver(entries => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        const id = entry.target.id;
        tocLinks.forEach(l => l.classList.toggle('active', l.dataset.id === id));
      }}
    }});
  }}, {{ rootMargin: '-20% 0px -60% 0px' }});

  chapters.forEach(ch => observer.observe(ch));

  // ===== SEARCH =====
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const searchStatus = document.getElementById('search-status');
  const searchHits = document.getElementById('search-hits');

  // Build search index from chapter text content
  const searchIndex = [];
  chapters.forEach(ch => {{
    const headings = ch.querySelectorAll('h1,h2,h3');
    headings.forEach(h => {{
      searchIndex.push({{
        id: ch.id,
        heading: h.textContent,
        text: h.textContent,
        level: h.tagName
      }});
    }});
    // Also index paragraphs
    ch.querySelectorAll('p,li').forEach(p => {{
      const t = p.textContent.trim();
      if (t.length > 20) {{
        searchIndex.push({{ id: ch.id, heading: ch.querySelector('h1')?.textContent || '', text: t, level: 'P' }});
      }}
    }});
  }});

  function doSearch(q) {{
    if (!q || q.length < 2) {{
      searchResults.classList.remove('visible');
      return;
    }}
    const ql = q.toLowerCase();
    const hits = searchIndex.filter(item => item.text.toLowerCase().includes(ql)).slice(0, 30);
    searchHits.innerHTML = '';
    if (hits.length === 0) {{
      searchStatus.textContent = '{no_results}';
    }} else {{
      searchStatus.textContent = hits.length + ' {found_label}';
      const seen = new Set();
      hits.forEach(h => {{
        const key = h.id + '|' + h.text.slice(0,60);
        if (seen.has(key)) return;
        seen.add(key);
        const a = document.createElement('a');
        a.className = 'search-hit';
        a.href = '#' + h.id;
        // highlight
        const re = new RegExp('(' + q.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&') + ')', 'gi');
        const safe = h.text.replace(/</g,'&lt;').slice(0,160);
        a.innerHTML = '<strong>' + (h.heading||'').replace(/</g,'&lt;').slice(0,60) + '</strong>: ' +
          safe.replace(re, '<mark>$1</mark>') + (h.text.length > 160 ? '…' : '');
        a.addEventListener('click', () => {{
          searchResults.classList.remove('visible');
          searchInput.value = '';
        }});
        searchHits.appendChild(a);
      }});
    }}
    searchResults.classList.add('visible');
  }}

  searchInput.addEventListener('input', e => doSearch(e.target.value));
  searchInput.addEventListener('keydown', e => {{
    if (e.key === 'Escape') {{
      searchResults.classList.remove('visible');
      searchInput.value = '';
    }}
    if (e.key === 'ArrowDown') {{
      const first = searchHits.querySelector('.search-hit');
      if (first) {{ e.preventDefault(); first.focus(); }}
    }}
  }});

  // ===== BUTTON POPUP =====
  const popup = document.getElementById('btn-popup');
  const popupTitle = document.getElementById('btn-popup-title');
  const popupBody = document.getElementById('btn-popup-body');
  const popupClose = document.getElementById('btn-popup-close');
  const popupOverlay = document.getElementById('popup-overlay');
  let lastFocusedEl = null;

  function openPopup(name, data) {{
    lastFocusedEl = document.activeElement;
    popupTitle.textContent = name;
    // Convert simple markdown-like formatting
    let desc = data.desc
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/\n/g, '<br>');
    popupBody.innerHTML = desc;
    popup.classList.add('visible');
    popupOverlay.classList.add('visible');
    popupOverlay.setAttribute('aria-hidden', 'false');
    popup.focus();
  }}

  function closePopup() {{
    popup.classList.remove('visible');
    popupOverlay.classList.remove('visible');
    popupOverlay.setAttribute('aria-hidden', 'true');
    if (lastFocusedEl) {{
      lastFocusedEl.focus();
      // Scroll to the element's line
      lastFocusedEl.scrollIntoView({{ block: 'nearest', behavior: 'smooth' }});
    }}
  }}

  popupClose.addEventListener('click', closePopup);
  popupOverlay.addEventListener('click', closePopup);
  document.addEventListener('keydown', e => {{
    if (e.key === 'Escape' && popup.classList.contains('visible')) closePopup();
  }});

  // Trap focus inside popup
  popup.addEventListener('keydown', e => {{
    if (e.key === 'Tab') {{
      const focusable = popup.querySelectorAll('button, a, [tabindex]');
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {{ e.preventDefault(); last.focus(); }}
      else if (!e.shiftKey && document.activeElement === last) {{ e.preventDefault(); first.focus(); }}
    }}
  }});

  // ===== ANNOTATE BUTTON NAMES IN TEXT =====
  // Build a list of known button/control names sorted longest-first to avoid partial matches
  const btnNames = Object.keys(BTNS).sort((a,b) => b.length - a.length);

  // Walk text nodes and wrap known button names
  function annotateNode(node) {{
    if (node.nodeType === Node.TEXT_NODE) {{
      const text = node.textContent;
      if (!text.trim()) return;

      let result = null;

      for (const name of btnNames) {{
        // Only match bold text that exactly matches a button name
        // We'll handle this at element level instead
      }}
      return;
    }}
    if (node.nodeType === Node.ELEMENT_NODE) {{
      // Don't recurse into already-processed nodes, headings, or code
      if (node.classList?.contains('btn-ref') ||
          node.tagName === 'CODE' || node.tagName === 'PRE' ||
          node.tagName === 'SCRIPT' || node.tagName === 'STYLE') return;
      // Process <strong> tags that match a button name
      if (node.tagName === 'STRONG') {{
        const name = node.textContent.trim().toUpperCase();
        if (BTNS[name]) {{
          const btn = document.createElement('button');
          btn.className = 'btn-ref';
          btn.type = 'button';
          btn.textContent = node.textContent;
          btn.setAttribute('aria-label', node.textContent + ' — {location_prefix}');
          btn.addEventListener('click', () => openPopup(node.textContent, BTNS[name]));
          node.replaceWith(btn);
          return;
        }}
      }}
      Array.from(node.childNodes).forEach(annotateNode);
    }}
  }}

  document.querySelectorAll('.chapter').forEach(ch => annotateNode(ch));

  console.log('Nord manual loaded. Buttons annotated:', Object.keys(BTNS).length);
}})();
</script>
</body>
</html>'''

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    print(f"  Written: {out_path} ({out_path.stat().st_size // 1024} KB)")

if __name__ == '__main__':
    base = Path(__file__).parent
    build_manual(
        src_dir=base / 'book-ru' / 'src',
        out_path=base / 'html-manual' / 'ru' / 'index.html',
        lang='ru',
        title='Nord Piano 6 — Руководство для незрячих'
    )
    build_manual(
        src_dir=base / 'book-en' / 'src',
        out_path=base / 'html-manual' / 'en' / 'index.html',
        lang='en',
        title='Nord Piano 6 — Guide for Blind Users'
    )
    print("Done.")
