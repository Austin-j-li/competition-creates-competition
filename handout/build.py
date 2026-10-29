"""Assemble docs/index.html from handout/ sources, the slot registry and the slot manuscript.

    python3 handout/build.py [--out docs] [--paper-cache DIR] [--verify-vendor] [--quiet]

Steps and checks follow handout/README.md. Every check prints ``PASS``/``FAIL``; the exit code is
nonzero if any check fails, and the output directory is then left unchanged. Stdlib only, apart
from latexmk, which builds the two PDFs outside the repository (``--paper-cache``, by default a
folder in the system temporary directory). The build never writes inside slot/manuscript/.
The page carries no timestamps, so rebuilds from unchanged inputs are byte-identical.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zlib
from base64 import b64encode
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import slot_data  # noqa: E402

PLACEHOLDER = re.compile(r"\[\[([A-Za-z0-9_]+)(?::([A-Za-z0-9_]+))?\]\]")
SLOT = re.compile(r"<!-- @@([A-Z_]+)@@ -->")
MATH = re.compile(r"((?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\\\[.*?(?<!\\)\\\])", re.S)
OPEN_INLINE, CLOSE_INLINE = re.compile(r"(?<!\\)\\\("), re.compile(r"(?<!\\)\\\)")
OPEN_DISPLAY, CLOSE_DISPLAY = re.compile(r"(?<!\\)\\\["), re.compile(r"(?<!\\)\\\]")
CHART_IDS = ("payoffs", "beliefs", "research")
SCRIPTS = (("APP", "app.js"), ("CHARTS", "charts.js"), ("FIGURES", "figures.js"), ("EXPLORER", "explorer.js"))
MANUSCRIPT = ROOT / "slot" / "manuscript"
# Published name -> LaTeX source in slot/manuscript/ (both pdfLaTeX, set in its latexmkrc).
PAPERS = {"paper.pdf": "main.tex", "comparison.pdf": "comparison.tex"}


class Report:
    def __init__(self, quiet: bool) -> None:
        self.quiet = quiet
        self.checks: dict[str, bool] = {}
        self.failures: list[str] = []
        self.placeholders_used: dict[str, str] = {}

    def check(self, cond: bool, msg: str) -> bool:
        print(("PASS " if cond else "FAIL ") + msg)
        self.checks[msg] = bool(cond)
        if not cond:
            self.failures.append(msg)
        return bool(cond)

    def note(self, msg: str) -> None:
        if not self.quiet:
            print("     " + msg)


# ----------------------------------------------------------------------------------------------
# Vendor, fonts and the paper files


def load_vendor(rep: Report, verify: bool) -> dict:
    """KaTeX is a local copy under handout/vendor. Every file must match its locked sha256, and the
    script and stylesheet must also match the upstream sha512 integrity recorded in the lock."""
    lock = json.loads((HERE / "vendor.lock.json").read_text(encoding="utf-8"))
    files = lock["katex"]["files"]
    for rel, v in files.items():
        path = HERE / "vendor" / rel
        body = path.read_bytes() if path.is_file() else b""
        ok = bool(body) and hashlib.sha256(body).hexdigest() == v["sha256"]
        if ok and "integrity" in v:
            ok = "sha512-" + b64encode(hashlib.sha512(body).digest()).decode() == v["integrity"]
        rep.check(ok, f"vendor {rel} present with locked hash")
    extra = sorted(q.relative_to(HERE / "vendor").as_posix() for q in (HERE / "vendor").rglob("*")
                   if q.is_file() and q.relative_to(HERE / "vendor").as_posix() not in files)
    rep.check(not extra, f"no unlocked files under handout/vendor ({len(extra)})")
    if verify:
        for rel, v in files.items():
            if not v.get("url", "").startswith("https://cdnjs."):
                continue
            try:
                with urllib.request.urlopen(v["url"], timeout=60) as resp:  # noqa: S310
                    body = resp.read()
                rep.check(hashlib.sha256(body).hexdigest() == v["sha256"], f"vendor {rel} matches {v['url']}")
            except Exception as exc:  # noqa: BLE001
                rep.check(False, f"vendor {rel} fetch: {exc}")
    return lock


def load_fonts(rep: Report) -> dict:
    """Self-hosted faces: every file in fonts.lock.json must exist under handout/fonts with its hash."""
    lock = json.loads((HERE / "fonts.lock.json").read_text(encoding="utf-8"))
    for name, v in lock.items():
        path = HERE / "fonts" / name
        ok = path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == v["sha256"]
        rep.check(ok, f"font {name} present with locked sha256")
    extra = sorted(q.name for q in (HERE / "fonts").glob("*") if q.name not in lock)
    rep.check(not extra, f"no unlocked files under handout/fonts ({len(extra)})")
    faces = {k: v for k, v in lock.items() if v.get("kind") == "face"}
    families = sorted({v["family"] for v in faces.values()})
    rep.check(families == ["Libertinus Math", "Libertinus Sans", "Libertinus Serif"],
              f"faces are Libertinus Serif, Libertinus Sans and Libertinus Math ({', '.join(families)})")
    rep.check(all(v.get("license_file") in lock for v in faces.values()), "every face names a locked licence file")
    return lock


def font_faces(lock: dict, prefix: str = "fonts/") -> str:
    """@font-face rules generated from the lock, so the stylesheet cannot drift from the files."""
    rules = []
    for name, v in lock.items():
        if v.get("kind") != "face":
            continue
        stretch = f' font-stretch: {v["stretch"]};' if v.get("stretch") else ""
        rules.append(f'@font-face {{ font-family: "{v["family"]}"; font-style: {v["style"]}; font-weight: {v["weight"]};{stretch} '
                     f'font-display: swap; src: url("{prefix}{name}") format("woff2"); unicode-range: {v["unicode_range"]}; }}')
    return "\n".join(rules) + "\n"


def katex_css(lock: dict) -> str:
    """The locked KaTeX stylesheet without the woff and ttf fallbacks, which are not shipped."""
    css = (HERE / "vendor" / "katex.min.css").read_text(encoding="utf-8")
    return re.sub(r',url\(fonts/[^)]+\.(?:woff|ttf)\) format\("[^"]+"\)', "", css)


def pdf_facts(path: Path) -> dict:
    """Page count, size, sha256 and creation date of a PDF, read with the standard library."""
    data = path.read_bytes()
    chunks = [data]
    for m in re.finditer(rb"stream\r?\n", data):
        end = data.find(b"endstream", m.end())
        if end < 0:
            continue
        try:
            chunks.append(zlib.decompress(data[m.end():end]))
        except zlib.error:
            pass
    counts = []
    for c in chunks:
        for m in re.finditer(rb"/Type\s*/Pages\b", c):
            lo, hi = c.rfind(b"<<", 0, m.start()), c.find(b">>", m.end())
            n = re.search(rb"/Count\s+(\d+)", c[lo:hi])
            if n:
                counts.append(int(n.group(1)))
    date = re.search(rb"/CreationDate\s*\(D:(\d{4})(\d{2})(\d{2})", data)
    months = ("January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December")
    created = f"{int(date.group(3))} {months[int(date.group(2)) - 1]} {int(date.group(1))}" if date else ""
    return {"pages": max(counts) if counts else 0, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(), "created": created}


def source_epoch() -> int:
    """The date the PDFs carry: the last commit that touched slot/manuscript/, or the newest
    modification time of its changed files when the working tree differs from that commit."""
    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    try:
        epoch = int(git("log", "-1", "--format=%ct", "--", "slot/manuscript"))
        changed = [line[3:] for line in git("status", "--porcelain", "--", "slot/manuscript").splitlines()]
        times = [int((ROOT / p).stat().st_mtime) for p in changed if (ROOT / p).is_file()]
        return max([epoch, *times])
    except (OSError, ValueError, subprocess.CalledProcessError):
        return int(Path(MANUSCRIPT / "main.tex").stat().st_mtime)


def build_papers(rep: Report, cache: Path) -> dict[str, Path]:
    """Run latexmk for each paper with its output directory outside the repository. The source
    date fixes the PDF dates and identifiers, so an unchanged manuscript gives the same bytes."""
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(source_epoch()), FORCE_SOURCE_DATE="1")
    built: dict[str, Path] = {}
    for name, tex in PAPERS.items():
        log = cache / (Path(tex).stem + ".latexmk.log")
        try:
            with log.open("w", encoding="utf-8") as fh:
                done = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                                       f"-outdir={cache}", tex], cwd=MANUSCRIPT, env=env, stdout=fh,
                                      stderr=subprocess.STDOUT, check=False)
            ok = done.returncode == 0
        except OSError as exc:
            ok = False
            rep.note(f"latexmk: {exc}")
        pdf = cache / (Path(tex).stem + ".pdf")
        if rep.check(ok and pdf.is_file(), f"latexmk built slot/manuscript/{tex} (log {log})"):
            built[name] = pdf
    return built


def paper_panel(facts: dict) -> str:
    """The Read-the-paper tab, written from the PDF facts. No date or count is typed by hand."""
    main, note = facts["paper.pdf"], facts["comparison.pdf"]

    def card(name: str, label: str, blurb: str, f: dict) -> str:
        return (f'<article class="pdf-card"><h3>{label}</h3><p>{blurb}</p>'
                f'<p class="meta"><span class="num">{f["pages"]} pages</span> · <span class="num">{round(f["bytes"] / 1024)} KB</span> · PDF</p>'
                f'<p class="hash"><span>sha256</span> <code>{f["sha256"]}</code></p>'
                f'<p class="actions"><a class="button primary" href="{name}" target="_blank" rel="noopener">Open the PDF</a> '
                f'<a class="button" href="{name}" download>Download</a></p></article>')
    return (f'<h2>Read the paper</h2>\n'
            f'<p class="stamp" data-version-stamp>Text revision of {main["created"]}. '
            f'Manuscript with appendix {main["pages"]} pages; comparison note {note["pages"]} pages.</p>\n'
            '<div class="pdf-cards">'
            + card("paper.pdf", "Manuscript", "The paper with its appendix: every result in full, with proofs.", main)
            + card("comparison.pdf", "Comparison note",
                   "The order slot of this version beside the Laplace order flow of the earlier version.", note)
            + '</div>\n'
            '<section class="viewer" data-viewer aria-label="Inline PDF viewer"><div class="viewer-bar" role="group" aria-label="Choose a document">'
            '<span class="viewer-label">Inline viewer</span>'
            '<button type="button" data-viewer-src="paper.pdf" data-viewer-title="Manuscript" aria-pressed="true">Manuscript</button>'
            '<button type="button" data-viewer-src="comparison.pdf" data-viewer-title="Comparison note" aria-pressed="false">Comparison note</button>'
            '</div><div class="viewer-frame"></div>'
            '<p class="viewer-note">Some phone browsers do not show a PDF inside a page. Use “Open the PDF” instead.</p></section>\n'
            '<p class="earlier"><a href="laplace/">Earlier version: Laplace order flow</a></p>')


# ----------------------------------------------------------------------------------------------
# Placeholders


def shown_value(row: dict, in_math: bool = False) -> str:
    """Display rule: the registry display, exactly as the manuscript prints it through \\reg{key}.
    Outside mathematics the one TeX escape in use, \\%, becomes a plain percent sign."""
    disp = row["display"]
    if in_math:
        return re.sub(r"\\ensuremath\{(.*)\}", r"\1", disp)
    return disp.replace("\\%", "%")


def resolve_placeholders(text: str, registry: dict, rep: Report, where: str) -> str:
    """Math-aware `[[key]]` substitution against the slot registry. Returns the new text and
    records failures on rep. Outside math a placeholder becomes a ``span.q`` with its key and exact
    value. Inside math it becomes the bare display, and the whole math segment is wrapped in a
    ``span.q-math`` that lists the keys and displays, so the binding survives rendering."""
    problems: list[str] = []

    def display_for(name: str, modifier: str | None, in_math: bool) -> str | None:
        row = registry.get(name)
        if row is None:
            problems.append(f"unknown registry key {name}")
            return None
        if modifier:
            problems.append(f"unknown placeholder modifier {name}:{modifier}")
            return None
        disp = shown_value(row, in_math)
        if "\\" in disp and not in_math:
            problems.append(f"TeX display outside math: {name} = {disp}")
            return None
        rep.placeholders_used[name] = row["source_script"]
        return disp

    def title_for(name: str) -> str:
        row = registry[name]
        return html.escape(f"{row['display']} · registry {name} · {row['source_script']}")

    def sub_text(m: re.Match) -> str:
        name = m.group(1)
        disp = display_for(name, m.group(2), False)
        if disp is None:
            return m.group(0)
        return (f'<span class="q" data-q="{name}" data-value="{html.escape(registry[name]["value"])}" '
                f'title="{title_for(name)}">{html.escape(disp)}</span>')

    def sub_math(segment: str) -> str:
        keys: list[str] = []
        shown: list[str] = []

        def one(m: re.Match) -> str:
            disp = display_for(m.group(1), m.group(2), True)
            if disp is None:
                return m.group(0)
            keys.append(m.group(1))
            shown.append(disp)
            return disp
        body = PLACEHOLDER.sub(one, segment)
        if not keys:
            return body
        title = html.escape(" ; ".join(f"{k} = {registry[k]['display']}" for k in keys))
        return (f'<span class="q-math" data-q="{" ".join(keys)}" data-shown="{html.escape("|".join(shown))}" '
                f'title="{title}">{body}</span>')

    parts = MATH.split(text)
    out = []
    for i, part in enumerate(parts):
        out.append(sub_math(part) if i % 2 == 1 else PLACEHOLDER.sub(sub_text, part))
    for p in sorted(set(problems)):
        rep.check(False, f"{where}: {p}")
    return "".join(out)


# ----------------------------------------------------------------------------------------------
# Fragment checks


def balanced(text: str, tag: str) -> tuple[int, int]:
    opens = len(re.findall(rf"<{tag}\b[^>]*>", text))
    closes = len(re.findall(rf"</{tag}\s*>", text))
    return opens, closes


def check_fragment(text: str, name: str, rep: Report, ids: dict[str, str]) -> None:
    for tag in ("details", "section", "figure", "table", "div", "ol", "ul", "dl"):
        o, c = balanced(text, tag)
        rep.check(o == c, f"{name}: <{tag}> balanced ({o} open, {c} close)")
    rep.check(len(OPEN_INLINE.findall(text)) == len(CLOSE_INLINE.findall(text)), f"{name}: inline math delimiters balanced")
    rep.check(len(OPEN_DISPLAY.findall(text)) == len(CLOSE_DISPLAY.findall(text)), f"{name}: display math delimiters balanced")
    no_code = re.sub(r"<code\b.*?</code>", "", text, flags=re.S)
    rep.check("$" not in no_code, f"{name}: no $ delimiters outside <code>")
    bad_lt = [m.group(0) for seg in MATH.findall(text) for m in re.finditer(r"<[A-Za-z]", seg)]
    rep.check(not bad_lt, f"{name}: no raw < before a letter inside math ({len(bad_lt)} found)")
    secs = re.findall(r'<section\s+class="sec"\s+id="(sec-[a-z0-9-]+)"', text)
    rep.check(len(secs) == 1, f"{name}: exactly one <section class=\"sec\" id=\"sec-…\"> ({len(secs)})")
    rep.check(len(re.findall(r"<h2\b", text)) == 1, f"{name}: exactly one <h2>")
    rep.check("<h1" not in text, f"{name}: no <h1>")
    rep.check("<script" not in text.lower(), f"{name}: no <script>")
    rep.check(re.search(r"\sstyle=", text) is None, f"{name}: no style= attributes")
    for m in re.finditer(r'\sid="([^"]+)"', text):
        i = m.group(1)
        if i in ids:
            rep.check(False, f"{name}: duplicate id {i} (also in {ids[i]})")
        ids[i] = name
    h3s = re.findall(r"<h3\b([^>]*)>", text)
    rep.check(all('id="' in a for a in h3s), f"{name}: every <h3> has an id ({len(h3s)} h3)")


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def build_toc(sections: list[str]) -> str:
    items = []
    for text in sections:
        sec = re.search(r'<section\s+class="sec"\s+id="([^"]+)"', text)
        h2 = re.search(r"<h2\b[^>]*>(.*?)</h2>", text, re.S)
        if not sec or not h2:
            continue
        items.append(f'<li><a href="#{sec.group(1)}">{strip_tags(h2.group(1))}</a></li>')
    return f'<ol class="toc-list">{"".join(items)}</ol>'


# ----------------------------------------------------------------------------------------------
# Main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs")
    ap.add_argument("--paper-cache", default=str(Path(tempfile.gettempdir()) / "ccc-slot-paper-build"),
                    help="latexmk output directory for the two PDFs (outside the repository)")
    ap.add_argument("--verify-vendor", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    rep = Report(args.quiet)
    out_dir = (ROOT / args.out).resolve()
    cache = Path(args.paper_cache).resolve()
    rep.check(ROOT not in cache.parents and cache != ROOT, f"paper build directory {cache} lies outside the repository")

    # (1) vendor and self-hosted fonts
    vendor = load_vendor(rep, args.verify_vendor)
    fonts = load_fonts(rep)

    # (2) the slot registry and the data script
    registry: dict = {}
    data_js = ""
    try:
        registry = slot_data.read_registry(ROOT)
        payload = slot_data.build_data(ROOT, registry)
        data_js = slot_data.emit_js(payload)
        json.loads(data_js)
        rep.check(True, f"slot registry read ({len(registry)} rows) and CCC_DATA built ({len(data_js.encode('utf-8'))} bytes)")
        rep.check(not re.search(r"\b(NaN|Infinity)\b", data_js) and "</script" not in data_js and "<!--" not in data_js,
                  "data script free of NaN, Infinity, </script, <!--")
    except (OSError, slot_data.DataError, ValueError, ZeroDivisionError) as exc:
        rep.check(False, f"slot registry and CCC_DATA: {exc}")

    # (3) the two PDFs
    built = build_papers(rep, cache)
    facts = {name: pdf_facts(path) for name, path in built.items()}
    ok = len(facts) == len(PAPERS) and all(f["pages"] > 0 and f["created"] for f in facts.values())
    rep.check(ok, "paper facts read from both PDFs (pages, bytes, sha256, date): "
              + ", ".join(f"{k} {v['pages']} pages" for k, v in facts.items()))

    # (4) fragments
    sec_dir = HERE / "sections"
    files = sorted(sec_dir.glob("*.html"))
    rep.check(len(files) >= 1, f"section fragments found ({len(files)})")
    sections: list[str] = []
    ids: dict[str, str] = {}
    chart_counts = {cid: 0 for cid in CHART_IDS}
    explorer_count = 0
    for path in files:
        text = resolve_placeholders(path.read_text(encoding="utf-8"), registry, rep, path.name)
        rep.check(PLACEHOLDER.search(text) is None, f"{path.name}: no placeholders left")
        rep.check("@@" not in text, f"{path.name}: no slot markers left")
        check_fragment(text, path.name, rep, ids)
        for cid in CHART_IDS:
            chart_counts[cid] += len(re.findall(rf'id="chart-{cid}"', text))
        explorer_count += len(re.findall(r'id="explorer"', text))
        sections.append(text)
    for cid in CHART_IDS:
        rep.check(chart_counts[cid] == 1, f"chart mount chart-{cid} appears exactly once ({chart_counts[cid]})")
    rep.check(explorer_count == 1, f"explorer mount appears exactly once ({explorer_count})")

    # (5) template assembly
    page = ""
    template_path = HERE / "template.html"
    if rep.check(template_path.exists(), "template.html present"):
        page = template_path.read_text(encoding="utf-8")
        css = (HERE / "style.css").read_text(encoding="utf-8") if (HERE / "style.css").exists() else ""
        rep.check(bool(css), "style.css present")
        rep.check("@font-face" not in css and "url(" not in css,
                  "style.css declares no font file; the faces come from fonts.lock.json")
        faces = font_faces(fonts)
        face_files = set(re.findall(r'url\("fonts/([^"]+)"\)', faces))
        rep.check(face_files == {k for k, v in fonts.items() if v.get("kind") == "face"},
                  f"generated @font-face rules match fonts.lock.json ({len(face_files)})")
        scripts = {}
        for slot, fname in SCRIPTS:
            p = HERE / fname
            scripts[slot] = p.read_text(encoding="utf-8") if p.exists() else ""
            rep.check(bool(scripts[slot]), f"{fname} present")
            rep.check("</script" not in scripts[slot], f"{fname} contains no </script")
        preload = "\n".join(f'<link rel="preload" href="fonts/{n}" as="font" type="font/woff2" crossorigin>'
                             for n in ("libertinus-serif-400-normal.woff2", "libertinus-sans-700-normal.woff2"))
        revision = facts["paper.pdf"]["created"] if ok else ""
        build_meta = ('<p class="build-meta">Sources (sha256, first 12 hex): '
                      f'registry {slot_data.sha256(ROOT)[:12] if registry else ""}; '
                      + "; ".join(f"{k} {v['sha256'][:12]}" for k, v in sorted(facts.items())) + ".</p>")
        fills = {
            "VENDOR_HEAD": '<link rel="stylesheet" href="vendor/katex.min.css">',
            "FONT_PRELOAD": preload,
            "STYLE": "<style>\n" + faces + css + "\n</style>",
            "PAPER": paper_panel(facts) if ok else "",
            "TEXT_REVISION": revision,
            "TOC": build_toc(sections),
            "SECTIONS": "\n".join(sections),
            "DATA": "<script>window.CCC_DATA = " + data_js + ";</script>",
            "VENDOR_SCRIPTS": '<script src="vendor/katex.min.js"></script>',
            "BUILD_META": build_meta,
        }
        fills.update({slot: "<script>\n" + scripts[slot] + "\n</script>" for slot, _ in SCRIPTS})
        present = set(SLOT.findall(page))
        for slot in fills:
            rep.check(slot in present, f"template has slot @@{slot}@@")
        page = SLOT.sub(lambda m: fills.get(m.group(1), m.group(0)), page)
        page = resolve_placeholders(page, registry, rep, "template.html")
        rep.check("@@" not in page, "no slot markers left in the page")

    # (6) validate the complete page before replacing artifacts
    if page and not rep.failures:
        rep.check(not PLACEHOLDER.search(page), "output has no [[key]] placeholders left")
        m = re.search(r"<script>window\.CCC_DATA = (.*?);</script>", page, re.S)
        parsed = False
        if m:
            try:
                json.loads(m.group(1))
                parsed = True
            except json.JSONDecodeError:
                parsed = False
        rep.check(parsed, "embedded CCC_DATA parses as JSON")
        remote = re.findall(r"<(?:script|link|img|iframe)\b[^>]*(?:src|href)=\"(?:https?:)?//[^>]*>", page)
        rep.check(not remote, f"no script, style, image or frame loads from the network ({len(remote)})")
        for cid in CHART_IDS:
            rep.check(page.count(f'id="chart-{cid}"') == 1, f"output has one chart-{cid} mount")
        rep.check(page.count('id="explorer"') == 1, "output has one explorer mount")
        rep.check(not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", page), "output carries no timestamps")
        rep.note(f"{args.out}/index.html: {len(page.encode('utf-8'))} bytes")

    if page and not rep.failures:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8", newline="\n")
        (out_dir / ".nojekyll").write_text("", encoding="utf-8")
        for name in ("main_filled.pdf", "online_appendix_filled.pdf"):
            (out_dir / name).unlink(missing_ok=True)  # the Laplace PDFs now live under /laplace/
        for name, src in built.items():
            shutil.copyfile(src, out_dir / name)
            rep.check((out_dir / name).read_bytes() == src.read_bytes(), f"copied {src.name} as {name}")
        if (out_dir / "fonts").is_dir():
            shutil.rmtree(out_dir / "fonts")
        (out_dir / "fonts").mkdir()
        for name in fonts:
            shutil.copyfile(HERE / "fonts" / name, out_dir / "fonts" / name)
        rep.check(all((out_dir / "fonts" / n).is_file() for n in fonts), f"copied {len(fonts)} font files")
        if (out_dir / "vendor").is_dir():
            shutil.rmtree(out_dir / "vendor")
        for rel in vendor["katex"]["files"]:
            target = out_dir / "vendor" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if rel == "katex.min.css":
                target.write_text(katex_css(vendor), encoding="utf-8", newline="\n")
            else:
                shutil.copyfile(HERE / "vendor" / rel, target)
        rep.check(all((out_dir / "vendor" / r).is_file() for r in vendor["katex"]["files"]),
                  f"copied {len(vendor['katex']['files'])} KaTeX files")

    # (7) run manifest
    passed = not rep.failures
    man_dir = ROOT / "numerics" / "manifests"
    man_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / "index.html"
    shown_out = out_html.relative_to(ROOT).as_posix() if ROOT in out_html.parents else str(out_html)
    manifest_obj = {
        "exercise": "handout",
        "timestamp_utc": None,  # omitted on purpose: the manifest is committed and must not churn
        "inputs": {slot_data.REGISTRY: slot_data.sha256(ROOT) if registry else None,
                   **{f"slot/manuscript/{PAPERS[k]} -> {k}": v["sha256"] for k, v in facts.items()}},
        "method": "handout build: slot registry placeholders, closed-form figure inputs, latexmk PDFs, template assembly",
        "tolerances": {},
        "software": {"python": sys.version.split()[0], "platform": platform.platform()},
        "outputs": {shown_out: hashlib.sha256(out_html.read_bytes()).hexdigest()} if passed and out_html.exists() else {},
        "checks": rep.checks,
        "passed": passed,
        "notes": ["vendor: KaTeX " + vendor["katex"]["version"] + " (local copy)",
                  "fonts: " + ", ".join(f"{k} sha256:{v['sha256'][:12]}" for k, v in fonts.items())],
    }
    (man_dir / "handout.json").write_text(json.dumps(manifest_obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    if not args.quiet and rep.placeholders_used:
        print(f"\nregistry keys used: {len(rep.placeholders_used)}")
    print("\nHANDOUT BUILD", "PASSED" if passed else f"FAILED ({len(rep.failures)} failures)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
