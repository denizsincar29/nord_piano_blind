#!/usr/bin/env python3
"""
build.py — build the Nord Piano 6 accessible HTML manual.

Usage:
    python build.py              # build into html-manual/
    python build.py -d /var/www  # set deploy dir, saved to .env
    python build.py --serve      # build then start a local HTTP server
    python build.py --serve --port 9000

.env key:
    DEPLOY_DIR   — where to copy the finished manual (default: html-manual/)
"""
import argparse
import os
import re
import json
import shutil
import sys
from pathlib import Path

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
ROOT     = Path(__file__).parent
ENV_FILE = ROOT / ".env"
HTML_OUT = ROOT / "html-manual"
BOOKS = [
    {"src": ROOT / "book-ru" / "src", "lang": "ru",
     "title": "Nord Piano 6 — Руководство для незрячих"},
    {"src": ROOT / "book-en" / "src", "lang": "en",
     "title": "Nord Piano 6 — Guide for Blind Users"},
]

# ── CLI ──────────────────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-d", "--deploy-dir", metavar="DIR",
                   help="Copy output here and save path to .env as DEPLOY_DIR")
    p.add_argument("--serve", action="store_true",
                   help="Start a local HTTP server after building")
    p.add_argument("--port", type=int, default=8000,
                   help="Port for --serve (default: 8000)")
    return p.parse_args()

# ── .env ─────────────────────────────────────────────────────────────────────────
def get_deploy_dir(cli_dir: str | None) -> Path | None:
    load_dotenv(ENV_FILE)
    if cli_dir:
        deploy = Path(cli_dir).expanduser().resolve()
        ENV_FILE.touch(exist_ok=True)
        set_key(str(ENV_FILE), "DEPLOY_DIR", str(deploy))
        print(f"📝 Saved DEPLOY_DIR={deploy} to .env")
        return deploy
    val = os.getenv("DEPLOY_DIR")
    return Path(val).expanduser().resolve() if val else None

# ── Markdown ─────────────────────────────────────────────────────────────────────
def md_to_html(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code", "nl2br"])

def parse_summary(path: Path) -> list[dict]:
    chapters = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if m := re.match(r"^#\s+(.+)$", line.strip()):
            chapters.append({"type": "part", "title": m.group(1)})
        elif m := re.match(r"^\s*[-*]\s+\[(.+?)\]\((.+?)\)", line.strip()):
            chapters.append({"type": "chapter", "title": m.group(1), "file": m.group(2)})
        elif m := re.match(r"^\[(.+?)\]\((.+?)\)", line.strip()):
            chapters.append({"type": "intro",   "title": m.group(1), "file": m.group(2)})
    return chapters

def slug(filename: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", filename.lower().replace(".md", ""))

def extract_button_db(chapters: list[dict]) -> dict:
    db = {}
    pat = re.compile(r"###\s+(.+?)\n(.*?)(?=\n###|\n##|\Z)", re.DOTALL)
    for ch in chapters:
        for m in pat.finditer(ch.get("content", "")):
            name, desc = m.group(1).strip(), m.group(2).strip()
            if len(desc) > 20:
                db[name.upper()] = {"name": name, "desc": desc[:500]}
    return db

# ── HTML template ─────────────────────────────────────────────────────────────────
I18N = {
    "ru": {
        "skip": "Перейти к содержимому",
        "toc":  "Содержание",
        "search": "Поиск по руководству…",
        "found":  "найдено",
        "none":   "Ничего не найдено",
        "loc":    "Расположение",
        "close":  "Закрыть (Escape)",
    },
    "en": {
        "skip": "Skip to content",
        "toc":  "Table of Contents",
        "search": "Search the manual…",
        "found":  "results found",
        "none":   "No results found",
        "loc":    "Location",
        "close":  "Close (Escape)",
    },
}

LANDING_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
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
  <a href="ru/index.html">🇷🇺 Русская версия</a>
  <a href="en/index.html">🇬🇧 English Version</a>
</div>
</body>
</html>
"""

def build_manual(src_dir: Path, out_path: Path, lang: str, title: str):
    t = I18N[lang]
    chapters = parse_summary(src_dir / "SUMMARY.md")
    for ch in chapters:
        if "file" not in ch:
            continue
        fp = src_dir / ch["file"]
        ch["content"] = fp.read_text(encoding="utf-8") if fp.exists() else ""
        ch["html"]    = md_to_html(ch["content"])
        ch["id"]      = slug(ch["file"])

    btn_db = extract_button_db(chapters)
    toc_items = [
        {"type": ch["type"], "title": ch["title"],
         **( {"id": ch["id"]} if "id" in ch else {})}
        for ch in chapters
    ]
    sections = "\n".join(
        f'<article id="{ch["id"]}" class="chapter" tabindex="-1">\n{ch["html"]}\n</article>'
        for ch in chapters if ch.get("type") in ("chapter", "intro") and "html" in ch
    )
    toc_json = json.dumps(toc_items, ensure_ascii=False)
    btn_json = json.dumps(btn_db,   ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#1a1a1a;--surf:#242424;--surf2:#2e2e2e;--bord:#3a3a3a;
  --txt:#e8e8e8;--dim:#aaa;--acc:#e85c33;--acc2:#ff7a52;
  --lnk:#6cb4e4;--lnkh:#9dd0f5;--foc:#ffcc00;--toc:320px;--hdr:52px}}
html{{scroll-behavior:smooth}}
body{{font-family:system-ui,-apple-system,"Segoe UI",sans-serif;background:var(--bg);color:var(--txt);line-height:1.7}}

/* skip link */
.skip{{position:absolute;top:-100px;left:0;background:var(--foc);color:#000;padding:10px 18px;font-weight:700;z-index:9999;text-decoration:none;border-radius:0 0 6px 0}}
.skip:focus{{top:0}}

/* header */
header{{position:fixed;inset:0 0 auto;height:var(--hdr);background:var(--surf);border-bottom:2px solid var(--acc);display:flex;align-items:center;gap:12px;padding:0 16px;z-index:200}}
#tog{{background:var(--acc);color:#fff;border:none;border-radius:5px;padding:6px 12px;font-size:.9rem;cursor:pointer;flex-shrink:0}}
#tog:focus{{outline:3px solid var(--foc)}}
header h1{{font-size:1rem;font-weight:600;flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--acc2)}}
#si{{background:var(--surf2);border:1px solid var(--bord);color:var(--txt);border-radius:5px;padding:5px 10px;font-size:.9rem;width:200px}}
#si:focus{{outline:3px solid var(--foc);border-color:var(--foc)}}

/* toc */
#toc{{position:fixed;top:var(--hdr);left:0;width:var(--toc);height:calc(100vh - var(--hdr));background:var(--surf);border-right:1px solid var(--bord);overflow-y:auto;z-index:150;padding:8px 0 32px;transition:transform .2s}}
#toc.hide{{transform:translateX(-100%)}}
#toc h2{{font-size:.78rem;text-transform:uppercase;letter-spacing:.1em;color:var(--dim);padding:10px 16px 4px;border-bottom:1px solid var(--bord);margin-bottom:4px}}
.tp{{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--acc);padding:10px 16px 2px;font-weight:700;margin-top:6px}}
.tl{{display:block;padding:7px 16px 7px 24px;color:var(--txt);text-decoration:none;font-size:.9rem;border-left:3px solid transparent;transition:background .1s,border-color .1s}}
.tl:hover{{background:var(--surf2);color:var(--lnkh)}}
.tl:focus{{outline:3px solid var(--foc);outline-offset:-3px}}
.tl.on{{border-left-color:var(--acc);color:var(--acc2);font-weight:600}}

/* search results */
#sr{{position:fixed;top:var(--hdr);left:0;right:0;background:var(--surf);border-bottom:2px solid var(--acc);z-index:140;max-height:50vh;overflow-y:auto;padding:12px 16px;display:none}}
#sr.show{{display:block}}
#ss{{font-size:.85rem;color:var(--dim);margin-bottom:8px}}
.sh{{display:block;padding:8px 12px;margin:4px 0;background:var(--surf2);border-radius:6px;color:var(--txt);text-decoration:none;font-size:.9rem}}
.sh:focus,.sh:hover{{background:var(--bord);outline:3px solid var(--foc)}}
.sh mark{{background:var(--foc);color:#000;border-radius:2px;padding:0 2px}}

/* main */
#main{{margin-left:var(--toc);margin-top:var(--hdr);padding:32px 48px 80px;max-width:900px;transition:margin-left .2s}}
#main.wide{{margin-left:0}}
@media(max-width:800px){{#main{{margin-left:0;padding:20px 16px 60px}}#toc{{width:280px}}#si{{width:130px}}}}

/* typography */
.chapter{{margin-bottom:60px;padding-bottom:40px;border-bottom:1px solid var(--bord)}}
.chapter:last-child{{border-bottom:none}}
.chapter h1{{font-size:1.8rem;color:var(--acc2);margin-bottom:24px;padding-bottom:10px;border-bottom:2px solid var(--acc)}}
.chapter h2{{font-size:1.3rem;color:var(--txt);margin:28px 0 12px;padding-left:10px;border-left:4px solid var(--acc)}}
.chapter h3{{font-size:1.05rem;color:var(--acc2);margin:20px 0 8px}}
.chapter h4{{font-size:1rem;color:var(--dim);margin:14px 0 6px}}
.chapter p{{margin:10px 0}}
.chapter ul,.chapter ol{{padding-left:1.8em;margin:10px 0}}
.chapter li{{margin:5px 0}}
.chapter strong{{color:var(--acc2)}}
.chapter em{{color:var(--dim)}}
.chapter a{{color:var(--lnk);text-decoration:underline}}
.chapter a:hover{{color:var(--lnkh)}}
.chapter a:focus{{outline:3px solid var(--foc);border-radius:2px}}
.chapter code{{background:var(--surf2);padding:1px 5px;border-radius:3px;font-size:.9em;color:var(--acc2)}}
.chapter pre{{background:var(--surf2);padding:16px;border-radius:6px;overflow-x:auto;margin:14px 0;border:1px solid var(--bord)}}
.chapter blockquote{{border-left:4px solid var(--acc);padding:8px 16px;background:var(--surf2);margin:14px 0;border-radius:0 6px 6px 0;color:var(--dim);font-style:italic}}
.chapter table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:.9rem}}
.chapter th{{background:var(--surf2);border:1px solid var(--bord);padding:8px 12px;text-align:left;color:var(--acc2)}}
.chapter td{{border:1px solid var(--bord);padding:8px 12px}}
.chapter tr:nth-child(even) td{{background:var(--surf2)}}

/* button refs */
.br{{display:inline;background:var(--surf2);border:1px solid var(--acc);border-radius:4px;padding:1px 6px;color:var(--acc2);font-weight:600;cursor:pointer;font-size:inherit;font-family:inherit;transition:background .15s}}
.br:hover{{background:var(--acc);color:#fff}}
.br:focus{{outline:3px solid var(--foc);outline-offset:2px}}

/* popup */
#ov{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:499}}
#ov.show{{display:block}}
#pop{{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:var(--surf);border:2px solid var(--acc);border-radius:10px;padding:24px 28px;z-index:500;max-width:min(520px,90vw);max-height:80vh;overflow-y:auto;box-shadow:0 8px 40px rgba(0,0,0,.7)}}
#pop.show{{display:block}}
#pop h3{{color:var(--acc2);margin-bottom:12px;font-size:1.1rem}}
#pb{{color:var(--txt);font-size:.95rem;line-height:1.7}}
#pc{{margin-top:18px;background:var(--acc);color:#fff;border:none;border-radius:6px;padding:8px 20px;font-size:.95rem;cursor:pointer;display:block;width:100%}}
#pc:focus{{outline:3px solid var(--foc)}}
</style>
</head>
<body>
<a href="#main" class="skip">{t["skip"]}</a>

<header>
  <button id="tog" aria-expanded="true" aria-controls="toc">&#9776; {t["toc"]}</button>
  <h1>{title}</h1>
  <input type="search" id="si" placeholder="{t["search"]}" aria-label="{t["search"]}" autocomplete="off">
</header>

<div id="sr" role="region" aria-live="polite" aria-label="{t["search"]}">
  <div id="ss"></div>
  <div id="sh"></div>
</div>

<nav id="toc" aria-label="{t["toc"]}">
  <h2>{t["toc"]}</h2>
  <div id="tt"></div>
</nav>

<div id="ov" aria-hidden="true"></div>
<div id="pop" role="dialog" aria-modal="true" aria-labelledby="pt" tabindex="-1">
  <h3 id="pt"></h3>
  <div id="pb"></div>
  <button id="pc">{t["close"]}</button>
</div>

<main id="main" tabindex="-1">
{sections}
</main>

<script>
(function(){{
const TOC={toc_json};
const DB={btn_json};

// ── TOC tree ──
const tt=document.getElementById('tt');
TOC.forEach(item=>{{
  if(item.type==='part'){{
    const d=document.createElement('div');d.className='tp';d.textContent=item.title;tt.appendChild(d);
  }}else if(item.id){{
    const a=document.createElement('a');
    a.className='tl';a.href='#'+item.id;a.textContent=item.title;a.dataset.id=item.id;
    tt.appendChild(a);
  }}
}});

// ── TOC toggle ──
const toc=document.getElementById('toc'),main=document.getElementById('main'),tog=document.getElementById('tog');
let open=window.innerWidth>800;
function setToc(v){{open=v;toc.classList.toggle('hide',!v);main.classList.toggle('wide',!v);tog.setAttribute('aria-expanded',v);}}
setToc(open);tog.addEventListener('click',()=>setToc(!open));

// ── Active chapter ──
document.querySelectorAll('.chapter').forEach(ch=>{{
  new IntersectionObserver(es=>es.forEach(e=>{{
    if(e.isIntersecting) document.querySelectorAll('.tl').forEach(l=>l.classList.toggle('on',l.dataset.id===e.target.id));
  }}),{{rootMargin:'-20% 0px -60% 0px'}}).observe(ch);
}});

// ── Search ──
const si=document.getElementById('si'),sr=document.getElementById('sr'),
      ss=document.getElementById('ss'),sh=document.getElementById('sh');
const idx=[];
document.querySelectorAll('.chapter').forEach(ch=>{{
  const h1txt=ch.querySelector('h1')?.textContent||'';
  ch.querySelectorAll('h1,h2,h3').forEach(h=>idx.push({{id:ch.id,sec:h1txt,txt:h.textContent}}));
  ch.querySelectorAll('p,li').forEach(p=>{{const t=p.textContent.trim();if(t.length>20)idx.push({{id:ch.id,sec:h1txt,txt:t}});}});
}});
function search(q){{
  if(!q||q.length<2){{sr.classList.remove('show');return;}}
  const ql=q.toLowerCase();
  const seen=new Set();
  const hits=idx.filter(i=>i.txt.toLowerCase().includes(ql)).filter(i=>{{const k=i.id+'|'+i.txt.slice(0,50);return seen.has(k)?false:(seen.add(k),true);}}).slice(0,25);
  sh.innerHTML='';
  ss.textContent=hits.length?hits.length+' {t["found"]}':'{t["none"]}';
  const re=new RegExp('('+q.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&')+')','gi');
  hits.forEach(h=>{{
    const a=document.createElement('a');a.className='sh';a.href='#'+h.id;
    a.innerHTML='<strong>'+h.sec.replace(/</g,'&lt;').slice(0,50)+'</strong>: '+h.txt.replace(/</g,'&lt;').slice(0,150).replace(re,'<mark>$1</mark>')+(h.txt.length>150?'…':'');
    a.addEventListener('click',()=>{{sr.classList.remove('show');si.value='';}});
    sh.appendChild(a);
  }});
  sr.classList.add('show');
}}
si.addEventListener('input',e=>search(e.target.value));
si.addEventListener('keydown',e=>{{
  if(e.key==='Escape'){{sr.classList.remove('show');si.value='';}}
  if(e.key==='ArrowDown'){{const f=sh.querySelector('.sh');if(f){{e.preventDefault();f.focus();}}}}
}});

// ── Popup ──
const pop=document.getElementById('pop'),pt=document.getElementById('pt'),
      pb=document.getElementById('pb'),pc=document.getElementById('pc'),
      ov=document.getElementById('ov');
let lf=null;
function open_pop(name,data){{
  lf=document.activeElement;pt.textContent=name;
  pb.innerHTML=data.desc.replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/\\*\\*(.+?)\\*\\*/g,'<strong>$1</strong>')
    .replace(/\\*(.+?)\\*/g,'<em>$1</em>').replace(/\\n/g,'<br>');
  pop.classList.add('show');ov.classList.add('show');ov.setAttribute('aria-hidden','false');pop.focus();
}}
function close_pop(){{
  pop.classList.remove('show');ov.classList.remove('show');ov.setAttribute('aria-hidden','true');
  if(lf){{lf.focus();lf.scrollIntoView({{block:'nearest',behavior:'smooth'}});}}
}}
pc.addEventListener('click',close_pop);ov.addEventListener('click',close_pop);
document.addEventListener('keydown',e=>{{if(e.key==='Escape'&&pop.classList.contains('show'))close_pop();}});
pop.addEventListener('keydown',e=>{{
  if(e.key!=='Tab')return;
  const f=[...pop.querySelectorAll('button,[tabindex="0"]')];
  if(!f.length)return;
  if(e.shiftKey&&document.activeElement===f[0]){{e.preventDefault();f[f.length-1].focus();}}
  else if(!e.shiftKey&&document.activeElement===f[f.length-1]){{e.preventDefault();f[0].focus();}}
}});

// ── Annotate button names ──
document.querySelectorAll('.chapter strong').forEach(el=>{{
  const key=el.textContent.trim().toUpperCase();
  if(!DB[key])return;
  const btn=document.createElement('button');
  btn.className='br';btn.type='button';btn.textContent=el.textContent;
  btn.setAttribute('aria-label',el.textContent+' — {t["loc"]}');
  btn.addEventListener('click',()=>open_pop(el.textContent,DB[key]));
  el.replaceWith(btn);
}});
}})();
</script>
</body>
</html>"""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✅ {out_path.relative_to(ROOT)}  ({out_path.stat().st_size // 1024} KB)")

# ── Main ─────────────────────────────────────────────────────────────────────────
def main():
    args = parse_args()
    deploy_dir = get_deploy_dir(args.deploy_dir)

    print(f"\n🔨  Building Nord Piano 6 HTML manual\n")

    HTML_OUT.mkdir(parents=True, exist_ok=True)
    (HTML_OUT / "index.html").write_text(LANDING_HTML, encoding="utf-8")

    for book in BOOKS:
        build_manual(src_dir=book["src"], out_path=HTML_OUT / book["lang"] / "index.html",
                     lang=book["lang"], title=book["title"])

    if deploy_dir:
        dest = deploy_dir / "html-manual"
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(HTML_OUT, dest)
        print(f"\n📦 Copied to {dest}")

    print(f"\n✅  Done!  Manual is in: {HTML_OUT}")

    if args.serve:
        import http.server, threading
        os.chdir(HTML_OUT)
        httpd = http.server.HTTPServer(("", args.port), http.server.SimpleHTTPRequestHandler)
        print(f"\n🌐  http://localhost:{args.port}/  — Ctrl+C to stop\n")
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")

if __name__ == "__main__":
    main()
