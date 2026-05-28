#!/usr/bin/env python3
"""
build.py — unified build script for Nord Piano 6 documentation.

Usage:
    python build.py              # build HTML manual only (no mdbook needed)
    python build.py --mdbook     # also build mdBook versions (requires mdbook)
    python build.py -d /var/www  # set deploy dir and save to .env
    python build.py --serve      # build then start a local HTTP server

.env keys:
    DEPLOY_DIR   — output directory (default: dist)
"""
import argparse
import os
import re
import json
import shutil
import subprocess
import sys
from pathlib import Path

# ── Deps ────────────────────────────────────────────────────────────────────────
try:
    from dotenv import load_dotenv, set_key
except ImportError:
    print("❌  python-dotenv not found. Run:  uv sync  or  pip install python-dotenv")
    sys.exit(1)

try:
    import markdown
except ImportError:
    print("❌  markdown not found. Run:  uv sync  or  pip install markdown")
    sys.exit(1)

# ── Constants ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
ENV_FILE = ROOT / ".env"
BOOK_LANGS = [
    {"src": ROOT / "book-ru" / "src", "lang": "ru",
     "title": "Nord Piano 6 — Руководство для незрячих"},
    {"src": ROOT / "book-en" / "src", "lang": "en",
     "title": "Nord Piano 6 — Guide for Blind Users"},
]
HTML_OUT = ROOT / "html-manual"

# ── CLI ──────────────────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-d", "--deploy-dir", metavar="DIR",
                   help="Output directory (saved to .env as DEPLOY_DIR)")
    p.add_argument("--mdbook", action="store_true",
                   help="Also build mdBook versions (requires mdbook in PATH)")
    p.add_argument("--serve", action="store_true",
                   help="Start a local HTTP server after building")
    p.add_argument("--port", type=int, default=8000,
                   help="Port for --serve (default 8000)")
    return p.parse_args()

# ── .env helpers ─────────────────────────────────────────────────────────────────
def load_env():
    load_dotenv(ENV_FILE)

def get_deploy_dir(cli_dir: str | None) -> Path:
    if cli_dir:
        deploy = Path(cli_dir).expanduser().resolve()
        # Persist to .env
        ENV_FILE.touch(exist_ok=True)
        set_key(str(ENV_FILE), "DEPLOY_DIR", str(deploy))
        print(f"📝 Deploy directory saved to .env: {deploy}")
        return deploy
    # Read from env (already loaded by load_dotenv)
    env_val = os.getenv("DEPLOY_DIR") or os.getenv("BUILD_DIR")
    if env_val:
        return Path(env_val).expanduser().resolve()
    return ROOT / "dist"

# ── Markdown helpers ─────────────────────────────────────────────────────────────
def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])

def parse_summary(summary_path: Path) -> list[dict]:
    chapters = []
    for line in summary_path.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"^#\s+(.+)$", line.strip()):
            chapters.append({"type": "part", "title": m.group(1)})
        elif m := re.match(r"^\s*-\s+\[(.+?)\]\((.+?)\)", line.strip()):
            chapters.append({"type": "chapter", "title": m.group(1), "file": m.group(2)})
        elif m := re.match(r"^\[(.+?)\]\((.+?)\)", line.strip()):
            chapters.append({"type": "intro", "title": m.group(1), "file": m.group(2)})
    return chapters

def slug(filename: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", filename.lower().replace(".md", ""))

# ── Button DB ────────────────────────────────────────────────────────────────────
def extract_button_db(chapters: list[dict]) -> dict:
    """
    Build a dict of uppercase_name -> {name, desc} from all ### headings
    that have substantial body text — used to power the in-page button popups.
    """
    db = {}
    section_re = re.compile(r"###\s+(.+?)\n(.*?)(?=\n###|\n##|\Z)", re.DOTALL)
    for ch in chapters:
        content = ch.get("content", "")
        for m in section_re.finditer(content):
            name = m.group(1).strip()
            desc = m.group(2).strip()
            if len(desc) > 20:
                db[name.upper()] = {"name": name, "desc": desc[:500]}
    return db

# ── HTML builder ─────────────────────────────────────────────────────────────────
def build_html_manual(src_dir: Path, out_path: Path, lang: str, title: str):
    chapters = parse_summary(src_dir / "SUMMARY.md")
    for ch in chapters:
        if "file" not in ch:
            continue
        fpath = src_dir / ch["file"]
        ch["content"] = fpath.read_text(encoding="utf-8") if fpath.exists() else ""
        ch["html"] = md_to_html(ch["content"])
        ch["id"] = slug(ch["file"])

    button_db = extract_button_db(chapters)

    toc_items = [
        {"type": ch["type"], "title": ch["title"],
         **( {"id": ch["id"]} if "id" in ch else {} )}
        for ch in chapters if ch["type"] != "part" or True
    ]

    sections_html = "\n".join(
        f'<article id="{ch["id"]}" class="chapter" tabindex="-1">\n{ch["html"]}\n</article>'
        for ch in chapters if ch.get("type") in ("chapter", "intro") and "html" in ch
    )

    i18n = {
        "ru": {
            "skip": "Перейти к содержимому",
            "toc": "Содержание",
            "search": "Поиск по руководству…",
            "found": "найдено",
            "none": "Ничего не найдено",
            "location": "Расположение",
            "close": "Закрыть (Escape)",
        },
        "en": {
            "skip": "Skip to content",
            "toc": "Table of Contents",
            "search": "Search the manual…",
            "found": "results found",
            "none": "No results found",
            "location": "Location",
            "close": "Close (Escape)",
        },
    }[lang]

    toc_json = json.dumps(toc_items, ensure_ascii=False)
    btn_json = json.dumps(button_db, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#1a1a1a;--surface:#242424;--surface2:#2e2e2e;--border:#3a3a3a;
  --text:#e8e8e8;--dim:#aaa;--accent:#e85c33;--accent2:#ff7a52;
  --link:#6cb4e4;--link-h:#9dd0f5;--focus:#ffcc00;
  --toc-w:320px;--hdr:52px;
}}
html{{scroll-behavior:smooth}}
body{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--text);line-height:1.7;font-size:1rem}}

.skip-link{{position:absolute;top:-100px;left:0;background:var(--focus);color:#000;padding:10px 18px;font-weight:700;z-index:9999;text-decoration:none;border-radius:0 0 6px 0}}
.skip-link:focus{{top:0}}

header{{position:fixed;top:0;left:0;right:0;height:var(--hdr);background:var(--surface);border-bottom:2px solid var(--accent);display:flex;align-items:center;gap:12px;padding:0 16px;z-index:200}}
#toc-toggle{{background:var(--accent);color:#fff;border:none;border-radius:5px;padding:6px 12px;font-size:.9rem;cursor:pointer;flex-shrink:0}}
#toc-toggle:focus{{outline:3px solid var(--focus)}}
header h1{{font-size:1rem;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--accent2)}}
#search-input{{background:var(--surface2);border:1px solid var(--border);color:var(--text);border-radius:5px;padding:5px 10px;font-size:.9rem;width:200px}}
#search-input:focus{{outline:3px solid var(--focus);border-color:var(--focus)}}

#toc-panel{{position:fixed;top:var(--hdr);left:0;width:var(--toc-w);height:calc(100vh - var(--hdr));background:var(--surface);border-right:1px solid var(--border);overflow-y:auto;z-index:150;padding:8px 0 32px;transition:transform .2s ease}}
#toc-panel.hidden{{transform:translateX(-100%)}}
#toc-panel h2{{font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dim);padding:10px 16px 4px;border-bottom:1px solid var(--border);margin-bottom:4px}}
.toc-part{{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);padding:10px 16px 2px;font-weight:700;margin-top:6px}}
.toc-link{{display:block;padding:7px 16px 7px 24px;color:var(--text);text-decoration:none;font-size:.9rem;border-left:3px solid transparent;transition:background .1s,border-color .1s}}
.toc-link:hover{{background:var(--surface2);color:var(--link-h)}}
.toc-link:focus{{outline:3px solid var(--focus);outline-offset:-3px}}
.toc-link.active{{border-left-color:var(--accent);color:var(--accent2);font-weight:600}}

#search-results{{position:fixed;top:var(--hdr);left:0;right:0;background:var(--surface);border-bottom:2px solid var(--accent);z-index:140;max-height:50vh;overflow-y:auto;padding:12px 16px;display:none}}
#search-results.visible{{display:block}}
#search-status{{font-size:.85rem;color:var(--dim);margin-bottom:8px}}
.search-hit{{display:block;padding:8px 12px;margin:4px 0;background:var(--surface2);border-radius:6px;color:var(--text);text-decoration:none;font-size:.9rem}}
.search-hit:focus,.search-hit:hover{{background:var(--border);outline:3px solid var(--focus)}}
.search-hit mark{{background:var(--focus);color:#000;border-radius:2px;padding:0 2px}}

#main{{margin-left:var(--toc-w);margin-top:var(--hdr);padding:32px 48px 80px;max-width:900px;transition:margin-left .2s ease}}
#main.toc-hidden{{margin-left:0}}
@media(max-width:800px){{#main{{margin-left:0;padding:20px 16px 60px}}#toc-panel{{width:280px}}#search-input{{width:130px}}}}

.chapter{{margin-bottom:60px;padding-bottom:40px;border-bottom:1px solid var(--border)}}
.chapter:last-child{{border-bottom:none}}
.chapter h1{{font-size:1.8rem;color:var(--accent2);margin-bottom:24px;padding-bottom:10px;border-bottom:2px solid var(--accent)}}
.chapter h2{{font-size:1.3rem;color:var(--text);margin:28px 0 12px;padding-left:10px;border-left:4px solid var(--accent)}}
.chapter h3{{font-size:1.05rem;color:var(--accent2);margin:20px 0 8px}}
.chapter h4{{font-size:1rem;color:var(--dim);margin:14px 0 6px}}
.chapter p{{margin:10px 0}}
.chapter ul,.chapter ol{{padding-left:1.8em;margin:10px 0}}
.chapter li{{margin:5px 0}}
.chapter strong{{color:var(--accent2)}}
.chapter em{{color:var(--dim)}}
.chapter a{{color:var(--link);text-decoration:underline}}
.chapter a:hover{{color:var(--link-h)}}
.chapter a:focus{{outline:3px solid var(--focus);border-radius:2px}}
.chapter code{{background:var(--surface2);padding:1px 5px;border-radius:3px;font-size:.9em;color:var(--accent2)}}
.chapter pre{{background:var(--surface2);padding:16px;border-radius:6px;overflow-x:auto;margin:14px 0;border:1px solid var(--border)}}
.chapter blockquote{{border-left:4px solid var(--accent);padding:8px 16px;background:var(--surface2);margin:14px 0;border-radius:0 6px 6px 0;color:var(--dim);font-style:italic}}
.chapter table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.9rem}}
.chapter th{{background:var(--surface2);border:1px solid var(--border);padding:8px 12px;text-align:left;color:var(--accent2)}}
.chapter td{{border:1px solid var(--border);padding:8px 12px}}
.chapter tr:nth-child(even) td{{background:var(--surface2)}}

.btn-ref{{display:inline;background:var(--surface2);border:1px solid var(--accent);border-radius:4px;padding:1px 6px;color:var(--accent2);font-weight:600;cursor:pointer;font-size:inherit;font-family:inherit;text-decoration:none;transition:background .15s}}
.btn-ref:hover{{background:var(--accent);color:#fff}}
.btn-ref:focus{{outline:3px solid var(--focus);outline-offset:2px}}

#popup-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:499}}
#popup-overlay.visible{{display:block}}
#btn-popup{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--surface);border:2px solid var(--accent);border-radius:10px;padding:24px 28px;z-index:500;max-width:min(520px,90vw);max-height:80vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,.7)}}
#btn-popup.visible{{display:block}}
#btn-popup h3{{color:var(--accent2);margin-bottom:12px;font-size:1.1rem}}
#btn-popup-body{{color:var(--text);font-size:.95rem;line-height:1.7}}
#btn-popup-close{{margin-top:18px;background:var(--accent);color:#fff;border:none;border-radius:6px;padding:8px 20px;font-size:.95rem;cursor:pointer;display:block;width:100%}}
#btn-popup-close:focus{{outline:3px solid var(--focus)}}
</style>
</head>
<body>
<a href="#main" class="skip-link">{i18n["skip"]}</a>

<header>
  <button id="toc-toggle" aria-expanded="true" aria-controls="toc-panel">&#9776; {i18n["toc"]}</button>
  <h1>{title}</h1>
  <input type="search" id="search-input" placeholder="{i18n["search"]}" aria-label="{i18n["search"]}" autocomplete="off">
</header>

<div id="search-results" role="region" aria-live="polite">
  <div id="search-status"></div>
  <div id="search-hits"></div>
</div>

<nav id="toc-panel" aria-label="{i18n["toc"]}">
  <h2>{i18n["toc"]}</h2>
  <div id="toc-tree"></div>
</nav>

<div id="popup-overlay" aria-hidden="true"></div>
<div id="btn-popup" role="dialog" aria-modal="true" aria-labelledby="btn-popup-title" tabindex="-1">
  <h3 id="btn-popup-title"></h3>
  <div id="btn-popup-body"></div>
  <button id="btn-popup-close">{i18n["close"]}</button>
</div>

<main id="main" tabindex="-1">
{sections_html}
</main>

<script>
(function(){{
const TOC={toc_json};
const BTNS={btn_json};

// TOC tree
const tree=document.getElementById('toc-tree');
TOC.forEach(item=>{{
  if(item.type==='part'){{
    const d=document.createElement('div');
    d.className='toc-part';d.textContent=item.title;tree.appendChild(d);
  }} else if(item.id){{
    const a=document.createElement('a');
    a.className='toc-link';a.href='#'+item.id;
    a.textContent=item.title;a.dataset.id=item.id;
    tree.appendChild(a);
  }}
}});

// TOC toggle
const tocPanel=document.getElementById('toc-panel');
const mainEl=document.getElementById('main');
const tocBtn=document.getElementById('toc-toggle');
let tocOpen=window.innerWidth>800;
function setToc(open){{
  tocOpen=open;
  tocPanel.classList.toggle('hidden',!open);
  mainEl.classList.toggle('toc-hidden',!open);
  tocBtn.setAttribute('aria-expanded',open?'true':'false');
}}
setToc(tocOpen);
tocBtn.addEventListener('click',()=>setToc(!tocOpen));

// Active chapter tracking
const chapters=document.querySelectorAll('.chapter');
const tocLinks=document.querySelectorAll('.toc-link');
new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{
    if(e.isIntersecting){{
      const id=e.target.id;
      tocLinks.forEach(l=>l.classList.toggle('active',l.dataset.id===id));
    }}
  }});
}},{{rootMargin:'-20% 0px -60% 0px'}}).observe && chapters.forEach(ch=>{{
  new IntersectionObserver(entries=>{{
    entries.forEach(e=>{{
      if(e.isIntersecting) tocLinks.forEach(l=>l.classList.toggle('active',l.dataset.id===e.target.id));
    }});
  }},{{rootMargin:'-20% 0px -60% 0px'}}).observe(ch);
}});

// Search
const si=document.getElementById('search-input');
const sr=document.getElementById('search-results');
const ss=document.getElementById('search-status');
const sh=document.getElementById('search-hits');
const idx=[];
chapters.forEach(ch=>{{
  const h1=ch.querySelector('h1');
  ch.querySelectorAll('h1,h2,h3').forEach(h=>idx.push({{id:ch.id,section:h1?.textContent||'',text:h.textContent,level:h.tagName}}));
  ch.querySelectorAll('p,li').forEach(p=>{{
    const t=p.textContent.trim();
    if(t.length>20) idx.push({{id:ch.id,section:h1?.textContent||'',text:t,level:'P'}});
  }});
}});

function doSearch(q){{
  if(!q||q.length<2){{sr.classList.remove('visible');return;}}
  const ql=q.toLowerCase();
  const hits=[...new Map(
    idx.filter(i=>i.text.toLowerCase().includes(ql)).slice(0,40)
       .map(i=>[i.id+'|'+i.text.slice(0,50),i])
  ).values()].slice(0,25);
  sh.innerHTML='';
  ss.textContent=hits.length?hits.length+' {i18n["found"]}':'{i18n["none"]}';
  const re=new RegExp('('+q.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&')+')','gi');
  hits.forEach(h=>{{
    const a=document.createElement('a');
    a.className='search-hit';a.href='#'+h.id;
    const safe=h.text.replace(/</g,'&lt;').slice(0,160);
    a.innerHTML='<strong>'+h.section.replace(/</g,'&lt;').slice(0,50)+'</strong>: '+safe.replace(re,'<mark>$1</mark>')+(h.text.length>160?'…':'');
    a.addEventListener('click',()=>{{sr.classList.remove('visible');si.value=''}});
    sh.appendChild(a);
  }});
  sr.classList.add('visible');
}}
si.addEventListener('input',e=>doSearch(e.target.value));
si.addEventListener('keydown',e=>{{
  if(e.key==='Escape'){{sr.classList.remove('visible');si.value='';}}
  if(e.key==='ArrowDown'){{const f=sh.querySelector('.search-hit');if(f){{e.preventDefault();f.focus();}}}}
}});

// Popup
const popup=document.getElementById('btn-popup');
const pTitle=document.getElementById('btn-popup-title');
const pBody=document.getElementById('btn-popup-body');
const pClose=document.getElementById('btn-popup-close');
const overlay=document.getElementById('popup-overlay');
let lastFocus=null;

function openPopup(name,data){{
  lastFocus=document.activeElement;
  pTitle.textContent=name;
  pBody.innerHTML=data.desc
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>')
    .replace(/\\*(.+?)\\*/g,'<em>$1</em>')
    .replace(/\\n/g,'<br>');
  popup.classList.add('visible');overlay.classList.add('visible');
  overlay.setAttribute('aria-hidden','false');popup.focus();
}}
function closePopup(){{
  popup.classList.remove('visible');overlay.classList.remove('visible');
  overlay.setAttribute('aria-hidden','true');
  if(lastFocus){{lastFocus.focus();lastFocus.scrollIntoView({{block:'nearest',behavior:'smooth'}});}}
}}
pClose.addEventListener('click',closePopup);
overlay.addEventListener('click',closePopup);
document.addEventListener('keydown',e=>{{if(e.key==='Escape'&&popup.classList.contains('visible'))closePopup();}});
popup.addEventListener('keydown',e=>{{
  if(e.key!=='Tab') return;
  const f=popup.querySelectorAll('button,[tabindex]');
  const first=f[0],last=f[f.length-1];
  if(e.shiftKey&&document.activeElement===first){{e.preventDefault();last.focus();}}
  else if(!e.shiftKey&&document.activeElement===last){{e.preventDefault();first.focus();}}
}});

// Annotate bold button names
const btnNames=Object.keys(BTNS).sort((a,b)=>b.length-a.length);
document.querySelectorAll('.chapter strong').forEach(el=>{{
  const name=el.textContent.trim().toUpperCase();
  if(BTNS[name]){{
    const btn=document.createElement('button');
    btn.className='btn-ref';btn.type='button';btn.textContent=el.textContent;
    btn.setAttribute('aria-label',el.textContent+' — {i18n["location"]}');
    btn.addEventListener('click',()=>openPopup(el.textContent,BTNS[name]));
    el.replaceWith(btn);
  }}
}});
}})();
</script>
</body>
</html>"""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    size = out_path.stat().st_size // 1024
    print(f"  ✅ {out_path.relative_to(ROOT)}  ({size} KB)")


# ── mdBook builder ────────────────────────────────────────────────────────────────
def find_mdbook() -> str | None:
    # Check ~/.cargo/bin first (common install location)
    cargo_bin = Path.home() / ".cargo" / "bin" / "mdbook"
    if cargo_bin.exists():
        return str(cargo_bin)
    return shutil.which("mdbook")

def build_mdbook(deploy_dir: Path):
    mdbook = find_mdbook()
    if not mdbook:
        print("❌  mdbook not found. Install with:  cargo install mdbook")
        sys.exit(1)

    for lang in ("ru", "en"):
        book_dir = ROOT / f"book-{lang}"
        out_dir = book_dir / "book"
        if out_dir.exists():
            shutil.rmtree(out_dir)
        print(f"  📚 Building book-{lang}…")
        subprocess.run([mdbook, "build"], cwd=book_dir, check=True)
        dest = deploy_dir / f"book-{lang}"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(out_dir, dest)
        print(f"     → {dest.relative_to(ROOT)}")

    # Copy language-selector index
    index = ROOT / "index.html"
    if index.exists():
        shutil.copy(index, deploy_dir / "index.html")


# ── Landing page ─────────────────────────────────────────────────────────────────
LANDING_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nord Piano 6 Manual</title>
<style>
body{background:#1a1a1a;color:#e8e8e8;font-family:system-ui,sans-serif;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:100vh;gap:24px;margin:0}
h1{color:#ff7a52;font-size:1.6rem;text-align:center}
.langs{display:flex;gap:20px;flex-wrap:wrap;justify-content:center}
a{display:block;background:#2e2e2e;border:2px solid #e85c33;border-radius:10px;
  padding:24px 40px;color:#e8e8e8;text-decoration:none;font-size:1.2rem;text-align:center}
a:hover,a:focus{background:#e85c33;outline:3px solid #ffcc00}
</style>
</head>
<body>
<h1>Nord Piano 6 Manual</h1>
<div class="langs">
  <a href="ru/index.html">&#127479;&#127482; &#1056;&#1091;&#1089;&#1089;&#1082;&#1072;&#1103; &#1074;&#1077;&#1088;&#1089;&#1080;&#1103;</a>
  <a href="en/index.html">&#127468;&#127463; English Version</a>
</div>
</body>
</html>
"""

# ── Main ─────────────────────────────────────────────────────────────────────────
def main():
    load_env()
    args = parse_args()
    deploy_dir = get_deploy_dir(args.deploy_dir)

    print(f"\n🔨  Building Nord Piano 6 documentation")
    print(f"    Deploy dir: {deploy_dir}\n")

    # Always build HTML manual
    html_out = HTML_OUT
    html_out.mkdir(parents=True, exist_ok=True)
    (html_out / "index.html").write_text(LANDING_HTML, encoding="utf-8")

    for book in BOOK_LANGS:
        build_html_manual(
            src_dir=book["src"],
            out_path=html_out / book["lang"] / "index.html",
            lang=book["lang"],
            title=book["title"],
        )

    # Copy html-manual to deploy dir
    dest_html = deploy_dir / "html-manual"
    if dest_html.exists():
        shutil.rmtree(dest_html)
    shutil.copytree(html_out, dest_html)

    # Optionally build mdBook
    if args.mdbook:
        print("\n📚  Building mdBook versions…")
        build_mdbook(deploy_dir)

    print(f"\n✅  Done!  Output in: {deploy_dir}")
    print(f"    html-manual/  — standalone accessible HTML (no mdBook needed)")
    if args.mdbook:
        print(f"    book-ru/  book-en/  — mdBook output")

    if args.serve:
        import http.server
        import threading
        os.chdir(deploy_dir / "html-manual")
        port = args.port
        handler = http.server.SimpleHTTPRequestHandler
        httpd = http.server.HTTPServer(("", port), handler)
        print(f"\n🌐  Serving at http://localhost:{port}/")
        print(f"    Press Ctrl+C to stop.\n")
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    main()
