#!/usr/bin/env python3
"""Assemble the seminar talk into ONE self-contained HTML file.

    python3 build.py [--out dist/index.html] [--src src]
                     [--pages p00,p03,p13 --allow-missing] [--all-katex-fonts]

Reads src/ (template, stage CSS, engine, pages, figures, data, looks), fills every
<span data-num="ID"></span> in a page with src/data.json numbers[ID].text (an unknown ID stops
the build), includes every src/figs/*.css and src/figs/*.js, renders every
\\( ... \\) and \\[ ... \\] in the pages and every entry of src/figs/labels.json with the local
KaTeX at build time (Node), inlines the KaTeX CSS with only the font faces the rendered math
uses, verifies the site's locked fonts and inlines them as base64, and writes one file that opens from file:// with no
network. Standard library and Node only.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import base64
import json
import re
import subprocess
import sys
from html import escape as html_escape, unescape as html_unescape
from html.parser import HTMLParser
from pathlib import Path

DEMO = Path(__file__).resolve().parent
REPO = DEMO.parents[0]
VENDOR = REPO / 'handout' / 'vendor'
PAGE_ORDER = (['p%02d' % i for i in range(0, 21)]          # the title and main pages 1 to 20
              + ['b%02d' % i for i in range(22, 62)]        # backups B1 to B17, keyed by PowerPoint show position
              + ['b74'])                                    # B18: the formal Proposition 2 page only
# Import the site's face generator and hash checks without running its build.
_spec = importlib.util.spec_from_file_location('site_handout_build', REPO / 'handout/build.py')
site_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(site_build)

MATH_RE = re.compile(r'\\\((.+?)\\\)|\\\[(.+?)\\\]', re.S)
NUM_RE = re.compile(r'<span(\s(?:[^>]*\s)?)data-num="([^"]+)"([^>]*)>\s*</span>')


def kb(n: int) -> str:
    return f'{n / 1024:,.1f} KB'


def unescape_tex(tex: str) -> str:
    return tex.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').strip()


def render_tex(items: list[dict]) -> list[str]:
    if not items:
        return []
    payload = json.dumps({'katex': str(VENDOR / 'katex.min.js'), 'items': items})
    proc = subprocess.run(['node', str(DEMO / 'render_math.mjs')], input=payload,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit('build stopped: KaTeX could not render the TeX above')
    return json.loads(proc.stdout)['html']


TRIANGLE = {'\u25b8': 'tri tri-r', '\u25c2': 'tri tri-l'}
SVG_RE = re.compile(r'<svg\b.*?</svg>', re.S)


def triangles(html: str) -> str:
    """The small pointing triangles of the links are not in the locked faces; outside SVG they are
    drawn by CSS, so they look the same on every machine and in the PDF."""
    out, last = [], 0
    for m in SVG_RE.finditer(html):
        out.append(re.sub('[\u25b8\u25c2]', lambda t: f'<span class="{TRIANGLE[t.group(0)]}" aria-hidden="true"></span>', html[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(re.sub('[\u25b8\u25c2]', lambda t: f'<span class="{TRIANGLE[t.group(0)]}" aria-hidden="true"></span>', html[last:]))
    return ''.join(out)


def script_safe(text: str) -> str:
    """Make text safe to sit inside a <script> element."""
    return text.replace('</script', '<\\/script').replace('<!--', '<\\!--')


def json_for_script(obj) -> str:
    return json.dumps(obj, ensure_ascii=False).replace('</', '<\\/')


# ---------------------------------------------------------------- KaTeX CSS and its fonts

def katex_faces(css: str) -> list[dict]:
    faces = []
    for m in re.finditer(r'@font-face\{([^}]*)\}', css):
        body = m.group(1)
        fam = re.search(r'font-family:([^;]+)', body).group(1).strip()
        style = re.search(r'font-style:([^;]+)', body).group(1).strip()
        weight = re.search(r'font-weight:([^;]+)', body).group(1).strip()
        weight = '700' if weight in ('700', 'bold') else '400'
        woff2 = re.search(r'url\(([^)]+\.woff2)\)', body).group(1)
        faces.append({'rule': m.group(0), 'family': fam, 'style': style, 'weight': weight,
                      'file': woff2})
    return faces


def katex_class_fonts(css: str) -> dict[str, set[tuple[str, str, str]]]:
    """Map each KaTeX class to the font faces (family, weight, style) its rules ask for."""
    out: dict[str, set[tuple[str, str, str]]] = {}
    for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', css):
        sel, body = m.group(1), m.group(2)
        if sel.strip().startswith('@'):
            continue
        fam = re.search(r'font-family:\s*(KaTeX_[A-Za-z0-9]+)', body)
        wt = re.search(r'font-weight:\s*(\w+)', body)
        st = re.search(r'font-style:\s*(\w+)', body)
        if not (fam or (wt and wt.group(1) in ('700', 'bold')) or (st and st.group(1) == 'italic')):
            continue
        family = fam.group(1) if fam else 'KaTeX_Main'
        weight = '700' if (wt and wt.group(1) in ('700', 'bold')) else '400'
        style = 'italic' if (st and st.group(1) == 'italic') else 'normal'
        for part in sel.split(','):
            # the last compound selector that names a class decides which element gets the font
            compounds = [c for c in re.split(r'[\s>+~]+', part.strip()) if c]
            classes: list[str] = []
            for comp in reversed(compounds):
                classes = [c for c in re.findall(r'\.([A-Za-z0-9_-]+)', comp) if c != 'katex']
                if classes:
                    break
            if not classes:
                continue
            key = '.'.join(sorted(classes))
            out.setdefault(key, set()).add((family, weight, style))
    return out


def katex_css(rendered_html: str, all_fonts: bool) -> tuple[str, list[str]]:
    css = (VENDOR / 'katex.min.css').read_text()
    faces = katex_faces(css)
    used: set[tuple[str, str, str]] = set()
    if rendered_html:
        used.add(('KaTeX_Main', '400', 'normal'))
        class_sets = [set(m.group(1).split()) for m in re.finditer(r'class="([^"]+)"', rendered_html)]
        present = set().union(*class_sets) if class_sets else set()
        for key, fonts in katex_class_fonts(css).items():
            need = set(key.split('.'))
            if need <= present and any(need <= cs for cs in class_sets):
                used |= fonts
    kept = []
    for face in faces:
        rule = face['rule']
        if all_fonts or (face['family'], face['weight'], face['style']) in used:
            path = VENDOR / face['file']
            data = base64.b64encode(path.read_bytes()).decode()
            new_src = f'src:url(data:font/woff2;base64,{data}) format("woff2")'
            new_rule = re.sub(r'src:[^}]*', new_src, rule)
            css = css.replace(rule, new_rule)
            kept.append(Path(face['file']).name)
        else:
            css = css.replace(rule, '')
    return css, kept


# ---------------------------------------------------------------- shipping guards and locked fonts

def display_palette() -> tuple[set[str], re.Pattern]:
    """Read the display check's constants without running its CLI or PDF checks."""
    tree = ast.parse((REPO / 'handout/check_display.py').read_text())
    values = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ('PALETTE', 'COLOUR') for t in node.targets):
            value = eval(compile(ast.Expression(node.value), '<display palette>', 'eval'), {'re': re})
            values[node.targets[0].id] = value
    return values['PALETTE'], values['COLOUR']


def locked_fonts() -> tuple[str, str, dict]:
    report = site_build.Report(quiet=True)
    lock = site_build.load_fonts(report)
    for name, row in lock.items():
        report.check((REPO / 'handout/fonts' / name).stat().st_size == row['bytes'],
                     f'font {name} has locked byte count')
    if report.failures:
        sys.exit('build stopped: locked fonts failed verification')
    css = site_build.font_faces(lock)
    for name, row in lock.items():
        if row.get('kind') == 'face':
            encoded = base64.b64encode((REPO / 'handout/fonts' / name).read_bytes()).decode()
            css = css.replace(f'url("fonts/{name}")', f'url("data:font/woff2;base64,{encoded}")')
    licenses = '\n\n'.join(name + '\n' + (REPO / 'handout/fonts' / name).read_text()
                            for name, row in lock.items() if row.get('kind') == 'license')
    return css, licenses, lock


# SHA256 fingerprints of sentences of at least 12 words in the master's five note blocks,
# from the 15 November text dumps, excluding sentences also printed on the pages. The 17 November
# master's notes (show positions 8 to 12) give the same set.
# Only fingerprints are retained, so audit/ is not a build input.
NOTE_SENTENCES = {12: ['416c38ca084781169ce1d0329a859f66a43d497f2614674fafe51754bec1e93c'],
 13: ['9906c658318324534e51661829973cff4e21fdcbb3a4676015c871652876d9c0'],
 14: ['43fe0deb06c484265e8b65222eeb69b8d71c21cb847fd1f9f3641b6201e9726f',
      'e3be8c23f41685ef32090d4245e67844ac602dc404964a31621f3025990073d6',
      'f45dfe4c38649cea98c8de08ebd9db39595d9b3d5f8a2d17570514a4050e9ca8'],
 15: ['7c82bc2977bde91ecb725d7ba28c8db331e479ee24ec1fe58e15443efb58c4e7',
      'cdd6fca2ac17949df1e6e5990db9f68b0e50235bb2a911f9330fa0f7f290b77d'],
 16: ['1133c8e0968a9d848a334b540b96cf0862dc7bb27a71c56fe211426ac87e1332',
      '5da2cf0bd3c0a26d77096cbc95a47dbdd649591b8df072385c6248a40b14d248'],
 17: ['71eca89f9fbb30a1402b6ee8e64030cc7faa2ace8aba0e8de85b78de1176c71b'],
 18: ['1db8f2f1cc8d095490a1f2ee62bb958517de93e0dbf2b8a396a4a55731af81cb',
      '4a680982078802a88a864d7e138aa98df760cfeb48641810243687269b1663be',
      '5b2dbdeaa6185cd127516488ab5d1d23d763e29af61a917cd5b0f174f2075de8',
      '89c285777f6cd2e7962c80f5f0d6ac9eb458f734937c09572871a307c0674c4b'],
 19: ['4e87a29245f701c7e5e8a0877a8a20c113e9869ac7a59ada37bbbfefc034defa',
      '8cf05e6303afd64d9b2ed8cb9ffad3214c94919f391e023ced9a7db0abff0cc8',
      'e3cbb6bd3e6d311205f67b5f8be43204d3c38d448312c73ed6ab69a7e24dfbcd'],
 20: ['16f6d3eb72d9d33412b8fa74c81583cd0c2e1b316c47a6c571a1e659f81a8e71',
      '2710287380b5997deb116733d641bd5b3e0572fb4ca9087aa5300aa1b5f28c82',
      'c39f9c6db6e1a60cf181c507912772064ccd0acaa5687bc750d334c3b9417bc2'],
 21: ['ac316505d22bf89152f46651b228b87bb6beeea4463f32e38e5d9378a9893033',
      'c95d31bbaf2e4310ee97a9f4c0189cfe16822a9abd35d66af8497277534965cc',
      'fc8741de951139a23e46eb838d4ba34cdd46ad6b4f33665b25541020a923b7a6'],
 22: ['cacb38ed6eb74825e599083047dba34b2e0c436f9c9bfef69abf194c8f83aac2'],
 23: ['b2b7a4e6547479041bdf3c8905a7c060cfc1db3e5d403591c2240bc50f2a0c8e',
      'ec620218ebb1074f4621ac9d479d0632fc104d08fc27fc9868b3340a58951af9'],
 24: ['d5c674fe3e6314e125fa407da894f9e3c7bb4314d0161b6de7123ed78b22d239'],
 26: ['7aecda5e47aae740640444f5e833bb8b719c24079330ac1a0448b0aebe721d65'],
 28: ['580f2f3656affe51ab98413d1cb5ea1c5f173c3ebcd7b14695072c3e78eeefe0'],
 31: ['5e2e82e2756dfc9b1c5c183c05f8442b55bf349cc43448f9b9142e5ddb926241']}


class ShippingPage(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.pages = []
        self.styles = []
        self.text = []
        self.number_depth = None
        self.depth = 0
        self.number_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.styles.append(attrs.get('style', ''))
        if tag.lower() == 'notes' or any(
            re.search(r'^(?:data-)?(?:speaker[-_])?notes$', k, re.I)
            or (k in ('id', 'class', 'name') and any(x.lower() in ('notes', 'speaker-notes', 'speaker_notes') for x in (v or '').split()))
            for k, v in attrs.items()
        ):
            sys.exit('build stopped: a notes element or attribute is present')
        if tag in ('script', 'link', 'img', 'iframe'):
            for key in ('src', 'href', 'srcset'):
                if key in attrs and not (attrs[key] or '').startswith(('data:', '#')):
                    sys.exit(f'build stopped: external resource on {tag}[{key}]')
        if tag == 'section' and 'page' in attrs.get('class', '').split():
            self.pages.append(attrs.get('id'))
        if 'data-num' in attrs:
            if tag != 'span' or self.number_depth is not None:
                sys.exit('build stopped: malformed data-num')
            self.number_depth = self.depth
            self.number_text = []
        if tag not in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            self.depth += 1

    def handle_endtag(self, tag):
        self.depth -= 1
        if self.number_depth == self.depth:
            if not ''.join(self.number_text).strip():
                sys.exit('build stopped: unfilled data-num')
            self.number_depth = None

    def handle_data(self, data):
        self.text.append(data)
        if self.number_depth is not None:
            self.number_text.append(data)


def shipping_guards(html: str, allow_missing: bool, face_css: str) -> None:
    parsed = ShippingPage()
    parsed.feed(html)
    if len(parsed.pages) != len(set(parsed.pages)) or set(parsed.pages) - set(PAGE_ORDER):
        sys.exit('build stopped: duplicate or unknown page keys')
    if not allow_missing and parsed.pages != PAGE_ORDER:
        sys.exit('build stopped: missing pages: ' + ' '.join(k for k in PAGE_ORDER if k not in parsed.pages))
    if parsed.number_depth is not None:
        sys.exit('build stopped: unclosed data-num')
    # URLs in SVG namespace declarations are identifiers, not network requests.
    css = '\n'.join(re.findall(r'<style\b[^>]*>(.*?)</style>', html, re.S) + parsed.styles)
    if re.search(r'@import\b|\bfetch\s*\(', html, re.I):
        sys.exit('build stopped: @import or fetch is present')
    for ref in re.findall(r'url\(\s*([^)]*)\)', css, re.I):
        if not ref.strip(' \"\'').startswith(('data:', '#')):
            sys.exit('build stopped: non-inline URL: ' + ref[:100])
    if re.search(r'["\'](?:speaker[-_])?notes["\']\s*:', html, re.I):
        sys.exit('build stopped: notes data is present')
    words = re.findall(r'\w+', ' '.join(parsed.text).lower())
    for length, hashes in NOTE_SENTENCES.items():
        forbidden = set(hashes)
        for i in range(len(words) - length + 1):
            if hashlib.sha256(' '.join(words[i:i + length]).encode()).hexdigest() in forbidden:
                sys.exit('build stopped: master speaker note text is present')
    palette, colour = display_palette()
    # Scan styles, inline attributes, SVG and scripts; comments and embedded binary data are not paint.
    # JSON records include colour descriptions from the source slides, not painted colours.
    paint = re.sub(r'<script\b[^>]*type="(?:application/json|text/plain)"[^>]*>.*?</script>', '', html, flags=re.S)
    paint = re.sub(r'/\*.*?\*/|<!--.*?-->', '', paint, flags=re.S)
    paint = re.sub(r'#[pb]\d{2}\b', '', paint)
    paint = re.sub(r'data:[^;\s"\']+;base64,[A-Za-z0-9+/=]+', '', paint)
    paint = re.sub(r'url\(#[^)]*\)|href=["\']#[^"\']*["\']|\bid=["\'][^"\']*["\']', '', paint)
    stray = {re.sub(r'\s+', ' ', m.group().lower()) for m in colour.finditer(paint)} - palette
    if stray:
        sys.exit('build stopped: colour outside shared palette: ' + repr(sorted(stray)))
    faces = re.findall(r'@font-face\s*\{[^}]*\}', css)
    site_faces = [f for f in faces if not re.search(r'font-family:\s*["\']?KaTeX_', f)]
    if site_faces != re.findall(r'@font-face\s*\{[^}]*\}', face_css):
        sys.exit('build stopped: faces differ from fonts.lock.json')
    print(f'PASS shipping guards: {len(parsed.pages)}/{len(PAGE_ORDER)} pages; every data-num filled; no network reference; '
          'no notes markup, data or master note sentences; shared palette; locked faces')


# ---------------------------------------------------------------- build

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', default='dist/index.html')
    ap.add_argument('--src', default='src')
    ap.add_argument('--pages', default='', help='comma list of working page keys (requires --allow-missing)')
    ap.add_argument('--allow-missing', action='store_true', help='permit an incomplete working copy')
    ap.add_argument('--all-katex-fonts', action='store_true', help='inline every KaTeX font (for checking the subset)')
    args = ap.parse_args()

    src = (DEMO / args.src).resolve() if not Path(args.src).is_absolute() else Path(args.src)
    out = Path(args.out)
    if not out.is_absolute():
        out = (DEMO / out).resolve()        # relative to this folder, wherever it is run from
    report: list[str] = []

    # pages
    want_pages = [p for p in args.pages.split(',') if p] or PAGE_ORDER
    if set(want_pages) - set(PAGE_ORDER):
        sys.exit('build stopped: unknown --pages key')
    pages = []
    for key in PAGE_ORDER:
        if key not in want_pages:
            continue
        f = src / 'pages' / f'{key}.html'
        if f.exists():
            pages.append((key, f.read_text()))
    if not pages:
        sys.exit('build stopped: no page found in ' + str(src / 'pages'))
    report.append('pages: ' + ' '.join(k for k, _ in pages)
                  + ('' if len(pages) == len(want_pages) else
                     '   (missing: ' + ' '.join(k for k in want_pages if k not in dict(pages)) + ')'))

    # printed numbers: <span data-num="ID"></span> takes data.json numbers[ID].text
    data_path = src / 'data.json'
    data = json.loads(data_path.read_text()) if data_path.exists() else None
    numbers = dict((data or {}).get('numbers', {}))
    # further data files, one per owner: src/data_<name>.json. Their "numbers" join the table
    # (an id may not be defined twice); the rest is exposed to figures as TALK.data.extra[name].
    for extra in sorted(src.glob('data_*.json')):
        content = json.loads(extra.read_text())
        for ident, row in content.get('numbers', {}).items():
            if ident in numbers:
                sys.exit(f'build stopped: number id {ident!r} is defined twice ({extra.name})')
            numbers[ident] = row
        if data is None:
            data = {}
        data.setdefault('extra', {})[extra.stem[len('data_'):]] = content
    if data is not None:
        data['numbers'] = numbers
        # Build commentary is private, even when a data script records it.
        def without_notes(value):
            if isinstance(value, dict):
                return {k: without_notes(v) for k, v in value.items() if k.lower() not in ('notes', 'speaker-notes', 'speaker_notes')}
            if isinstance(value, list):
                return [without_notes(v) for v in value]
            return value
        data = without_notes(data)
    n_nums = 0
    filled_pages = []
    for key, html in pages:
        def fill(m: re.Match, key: str = key) -> str:
            nonlocal n_nums
            ident = m.group(2)
            if ident not in numbers:
                sys.exit(f'build stopped: pages/{key}.html asks for number {ident!r}, '
                         f'which src/data.json "numbers" does not have')
            n_nums += 1
            text = html_escape(str(numbers[ident]['text']), quote=False)
            return f'<span{m.group(1)}data-num="{ident}"{m.group(3)}>{text}</span>'
        out_html = NUM_RE.sub(fill, html)
        left = len(re.findall(r'data-num=', html)) - len(NUM_RE.findall(html))
        if left:
            sys.exit(f'build stopped: pages/{key}.html has {left} data-num span(s) not written as '
                     f'<span data-num="ID"></span> (empty, double quotes)')
        filled_pages.append((key, out_html))
    pages = filled_pages
    report.append(f'numbers: {n_nums} filled from data.json')

    # math in pages and figure labels: one Node call
    items: list[dict] = []
    for key, html in pages:
        for m in MATH_RE.finditer(html):
            tex = m.group(1) if m.group(1) is not None else m.group(2)
            items.append({'tex': unescape_tex(tex), 'display': m.group(2) is not None,
                          'where': f'pages/{key}.html'})
    # figure labels: figs/labels.json and one file per group of pages, figs/labels_<name>.json
    labels = {}
    for labels_path in sorted((src / 'figs').glob('labels*.json')):
        for k, v in json.loads(labels_path.read_text()).items():
            if k in labels:
                sys.exit(f'build stopped: figure label {k!r} is defined twice ({labels_path.name})')
            labels[k] = v
    label_keys = list(labels)
    for k in label_keys:
        items.append({'tex': labels[k], 'display': False, 'where': f'figs/labels.json [{k}]'})
    rendered = render_tex(items)
    it = iter(rendered)
    page_html = []
    for key, html in pages:
        page_html.append(triangles(MATH_RE.sub(lambda m: next(it), html)))
    math = {k: next(it) for k in label_keys}
    n_page_math = len(items) - len(label_keys)
    report.append(f'math: {n_page_math} in pages, {len(label_keys)} figure labels')

    # KaTeX CSS with the fonts that the rendered math uses
    kcss, kfonts = katex_css(''.join(rendered), args.all_katex_fonts)
    report.append('KaTeX fonts: ' + (', '.join(kfonts) if kfonts else 'none'))

    # The author's one look. Shared design tokens precede the plate stylesheet.
    token_path = REPO / 'design' / 'tokens.css'
    tokens = token_path.read_text()
    f = src / 'looks' / 'plate.css'
    if not f.exists():
        sys.exit('build stopped: plate.css is missing')
    face_css, licenses, lock = locked_fonts()
    css = face_css + f.read_text()
    js_path = f.with_suffix('.js')
    looks = [('plate', css, js_path.read_text() if js_path.exists() else '')]
    report.append('look: plate; fonts from handout/fonts.lock.json (14 faces)')

    # figures and data
    figs = sorted((src / 'figs').glob('*.js')) if (src / 'figs').exists() else []
    # every figure stylesheet, the common figs.css first
    css_files = sorted((src / 'figs').glob('*.css'), key=lambda f: (f.name != 'figs.css', f.name)) \
        if (src / 'figs').exists() else []
    figs_css = '\n'.join(f'<style data-src="figs/{f.name}">\n{f.read_text()}\n</style>' for f in css_files)
    # page stylesheets, one per group of pages, in src/css
    own_css = sorted((src / 'css').glob('*.css')) if (src / 'css').exists() else []
    figs_css += '\n' + '\n'.join(f'<style data-src="css/{f.name}">\n{f.read_text()}\n</style>' for f in own_css)
    report.append('figures: ' + (' '.join(f.name for f in figs) or 'none')
                  + ('; styles ' + ' '.join(f.name for f in css_files) if css_files else ''))
    report.append('data: ' + ('data.json' if data is not None else 'none'))

    # assemble
    template = (src / 'template.html').read_text()
    template = template.replace('</head>', '<script type="text/plain" id="font-licenses">' + script_safe(licenses) + '</script>\n</head>')
    stage_css = (src / 'stage.css').read_text()
    engine_js = (src / 'engine.js').read_text()

    fig_scripts = '\n'.join(
        f'<script data-src="figs/{f.name}">\n{script_safe(f.read_text())}\n</script>' for f in figs)
    look_styles = '\n'.join(f'<style data-look-css="{n}">\n{c}\n</style>' for n, c, _ in looks)
    look_scripts = '\n'.join(f'<script data-src="looks/{n}.js">\n{script_safe(j)}\n</script>'
                             for n, _, j in looks if j)
    boot = {'pages': [k for k, _ in pages]}

    parts = {
        '{{KATEX_CSS}}': f'<style data-src="katex">{kcss}</style>',
        '{{STAGE_CSS}}': f'<style data-src="stage.css">\n{stage_css}\n</style>',
        '{{FIGS_CSS}}': figs_css,
        '{{LOOKS_CSS}}': look_styles,
        '{{TOKENS_CSS}}': f'<style data-src="design/tokens.css">\n{tokens}\n</style>',
        '{{PAGES}}': '\n'.join(page_html),
        '{{DATA}}': (f'<script type="application/json" id="talk-data">{json_for_script(data)}</script>'
                     if data is not None else ''),
        '{{MATH}}': f'<script type="application/json" id="talk-math">{json_for_script(math)}</script>',
        '{{BOOT}}': f'<script type="application/json" id="talk-boot">{json_for_script(boot)}</script>',
        '{{ENGINE_JS}}': f'<script data-src="engine.js">\n{script_safe(engine_js)}\n</script>',
        '{{FIG_JS}}': fig_scripts,
        '{{LOOK_JS}}': look_scripts,
    }
    for k in parts:
        if k not in template:
            sys.exit(f'build stopped: template has no {k}')
    html = re.sub(r'\{\{[A-Z_]+\}\}', lambda m: parts.get(m.group(0), m.group(0)), template)

    # Thumbnails keep page-specific layout without duplicating page IDs.
    html = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)',
                  lambda m: m[1] + re.sub(r'#([pb]\d{2})\b',
                      lambda n: f':is(#{n[1]}, [data-thumb-page="{n[1]}"])', re.sub(r'#stage (?=[^\s{,])', ':is(#stage, #overview, #sheet) ', m[2])) + m[3],
                  html, flags=re.S)
    shipping_guards(html, args.allow_missing, face_css)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Preserve the HTML date when its bytes are unchanged, so a fresh PDF stays eligible.
    changed = not out.is_file() or out.read_text() != html
    if changed:
        out.write_text(html)
    report.append('shared tokens: design/tokens.css')
    report.append(f"{'wrote' if changed else 'unchanged'} {out}  {kb(out.stat().st_size)}")
    print('\n'.join(report))


if __name__ == '__main__':
    main()
