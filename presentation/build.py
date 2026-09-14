"""Build the offline presentation from locked assets and manifest-bound research data."""
from pathlib import Path
import base64
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / 'handout'))
import data


def digest(body):
    return hashlib.sha256(body).hexdigest()


def fetch(url):
    with urllib.request.urlopen(url, timeout=45) as response:
        return response.read()


def build():
    research, hashes = data.build_data(ROOT)
    vendor = HERE / 'vendor'
    lock_path = vendor / 'lock.json'
    lock = json.loads(lock_path.read_text()) if lock_path.exists() else {}
    upstream = json.loads((ROOT / 'handout/vendor.lock.json').read_text())
    for key, filename in [('katex_js', 'katex.min.js'), ('katex_css', 'katex.min.css')]:
        path = vendor / filename
        body = path.read_bytes() if path.exists() else fetch(upstream[key]['url'])
        integrity = 'sha512-' + base64.b64encode(hashlib.sha512(body).digest()).decode()
        if integrity != upstream[key]['integrity']:
            raise ValueError('KaTeX integrity mismatch: ' + filename)
        path.write_bytes(body)
        lock[filename] = {'sha256': digest(body), 'url': upstream[key]['url']}
    font_urls = {rel for rel in re.findall(r'url\((fonts/[^)]+)\)', (vendor / 'katex.min.css').read_text()) if rel.endswith('.woff2')}
    def font(rel):
        path = vendor / rel
        url = upstream['katex_css']['url'].rsplit('/', 1)[0] + '/' + rel
        body = path.read_bytes() if path.exists() else fetch(url)
        if rel in lock and digest(body) != lock[rel]['sha256']:
            raise ValueError('Font integrity mismatch: ' + rel)
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(body)
        return rel, {'sha256': digest(body), 'url': url}
    with ThreadPoolExecutor(max_workers=8) as pool:
        lock.update(dict(pool.map(font, sorted(font_urls))))
    lock_path.write_text(json.dumps(lock, indent=2, sort_keys=True) + '\n')
    out = HERE / 'dist'
    out.mkdir(exist_ok=True)
    shutil.copytree(vendor, out / 'vendor', dirs_exist_ok=True)
    # Chromium and current browsers use WOFF2; remove unused upstream fallback URLs.
    css_path = out / 'vendor/katex.min.css'
    css_path.write_text(re.sub(r',url\(fonts/[^)]+\.(?:woff|ttf)\) format\("[^"]+"\)', '', css_path.read_text()))
    fonts = json.loads((ROOT / 'handout/fonts.lock.json').read_text())
    for name in ['LibreFranklin-normal-300-900.woff2', 'CourierPrime-normal-400.woff2']:
        body = (ROOT / 'handout/fonts' / name).read_bytes()
        if digest(body) != fonts[name]['sha256']:
            raise ValueError('Project font hash mismatch: ' + name)
        (out / name).write_bytes(body)
    uifonts = HERE / 'vendor/uifonts'
    uilock = json.loads((uifonts / 'lock.json').read_text())
    (out / 'uifonts').mkdir(exist_ok=True)
    for name, entry in uilock.items():
        body = (uifonts / name).read_bytes()
        if digest(body) != entry['sha256']:
            raise ValueError('Deck font hash mismatch: ' + name)
        (out / 'uifonts' / name).write_bytes(body)
    for name in ['main_filled.pdf', 'online_appendix_filled.pdf']:
        shutil.copyfile(ROOT / 'paper' / name, out / name)
    html = (HERE / 'template.html').read_text()
    replacements = {
        '@@STYLE@@': (HERE / 'deck.css').read_text(),
        '@@DATA@@': data.emit_js(research),
        '@@FORMULAS@@': (ROOT / 'handout/explorer.js').read_text(),
        '@@CONTENT@@': (HERE / 'content.js').read_text(),
        '@@APP@@': (HERE / 'deck.js').read_text(),
    }
    for key, value in replacements.items():
        html = html.replace(key, value)
    if re.search(r'@@[A-Z]+@@', html):
        raise ValueError('Unresolved build slot')
    (out / 'index.html').write_text(html)
    sources = dict(hashes)
    for name in ['paper/main.md', 'paper/online_appendix.md', 'handout/explorer.js', 'presentation/content.js', 'presentation/deck.js', 'presentation/deck.css', 'presentation/template.html']:
        sources[name] = digest((ROOT / name).read_bytes())
    (out / 'provenance.json').write_text(json.dumps({'sources': sources, 'scope': 'Presentation build; existing passed-manifest outputs. No new equilibrium search or research release claim.'}, indent=2) + '\n')
    notes = subprocess.run(['node', str(HERE / 'notes.mjs')], input=data.emit_js(research), capture_output=True, text=True, check=True).stdout
    (out / 'speaker-notes.md').write_text(notes)
    print(f'Built {out / "index.html"} ({len(html):,} characters); {len(hashes)} research sources verified.')


if __name__ == '__main__':
    build()
