"""Assemble docs/index.html from handout/ sources and the repo's validated CSVs.

    python3 handout/build.py [--out docs] [--verify-vendor] [--allow-missing-pdf] [--quiet]

Steps and checks follow handout/README.md. Every check prints ``PASS``/``FAIL`` like
numerics/verify.py; the exit code is nonzero if any check fails. Stdlib only, no numerics imports.
The output carries no timestamps, so rebuilds from unchanged inputs are byte-identical.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import sys
from decimal import Decimal
import urllib.request
from base64 import b64encode
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import data as data_mod  # noqa: E402
import tables_html  # noqa: E402

PLACEHOLDER = re.compile(r"\[\[([A-Za-z0-9_]+)(?::(percent))?\]\]")
TABLE_SLOT = re.compile(r"^[ \t]*<!-- @@TABLE:([a-z_]+)@@ -->[ \t]*$", re.M)
SLOT = re.compile(r"<!-- @@([A-Z_]+)@@ -->")
MATH = re.compile(r"((?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\\\[.*?(?<!\\)\\\])", re.S)
OPEN_INLINE, CLOSE_INLINE = re.compile(r"(?<!\\)\\\("), re.compile(r"(?<!\\)\\\)")
OPEN_DISPLAY, CLOSE_DISPLAY = re.compile(r"(?<!\\)\\\["), re.compile(r"(?<!\\)\\\]")
SECTION_ORDER_LAST = "appendix.html"
CHART_IDS = ("fig1", "fig2", "fig3", "fig4")
PDFS = ("paper/main_filled.pdf", "paper/online_appendix_filled.pdf")


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
# Vendor


def load_vendor(rep: Report, verify: bool) -> dict:
    lock = json.loads((HERE / "vendor.lock.json").read_text(encoding="utf-8"))
    ok = all({"url", "version", "integrity", "as"} <= set(v) for v in lock.values())
    rep.check(ok, "vendor lock complete (url, version, integrity, as)")
    if verify:
        for name, v in lock.items():
            try:
                with urllib.request.urlopen(v["url"], timeout=60) as resp:  # noqa: S310
                    body = resp.read()
                digest = "sha512-" + b64encode(hashlib.sha512(body).digest()).decode()
                rep.check(digest == v["integrity"], f"vendor {name} integrity matches {v['url']}")
            except Exception as exc:  # noqa: BLE001
                rep.check(False, f"vendor {name} fetch: {exc}")
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
    return lock


# ----------------------------------------------------------------------------------------------
# Placeholders


def resolve_placeholders(text: str, registry: dict, manifest: dict, rep: Report, where: str) -> str:
    """Math-aware `[[name]]` substitution. Returns the new text; records failures on rep."""
    problems: list[str] = []

    def display_for(name: str, in_math: bool) -> str | None:
        if name not in manifest:
            problems.append(f"unknown placeholder {name}")
            return None
        row = registry.get(name)
        if row is None or row["status"] == "open" or row["display"] == "[[unresolved]]":
            problems.append(f"unresolved placeholder {name}")
            return None
        disp = row["display"]
        if "\\" in disp and not in_math:
            problems.append(f"TeX display outside math: {name} = {disp}")
            return None
        rep.placeholders_used[name] = row["source_file"]
        return disp

    def sub_math(m: re.Match) -> str:
        disp = display_for(m.group(1), True)
        return disp if disp is not None else m.group(0)

    def sub_text(m: re.Match) -> str:
        name = m.group(1)
        disp = display_for(name, False)
        if disp is None:
            return m.group(0)
        row = registry[name]
        exact = disp
        if m.group(2) == "percent":
            value = Decimal(row["value"])
            if not value.is_finite() or not 0 <= value <= 1:
                raise ValueError(f"invalid probability: {name}")
            disp = f"{value * 100:.1f}%"
        title = f"{exact} · {row['status']} · {row['source_file']} · {row['source_row']}".replace('"', "&quot;")
        return (f'<span class="q" data-q="{name}" data-status="{row["status"]}" title="{title}">'
                f"{disp}</span>")

    parts = MATH.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(PLACEHOLDER.sub(sub_math, part))
        else:
            out.append(PLACEHOLDER.sub(sub_text, part))
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
    ap.add_argument("--verify-vendor", action="store_true")
    ap.add_argument("--allow-missing-pdf", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    rep = Report(args.quiet)
    out_dir = ROOT / args.out

    # (1) vendor and self-hosted fonts
    vendor = load_vendor(rep, args.verify_vendor)
    fonts = load_fonts(rep)

    # (2) registry and manifest
    registry = {r["name"]: r for r in data_mod.read_csv(ROOT, "numerics/quantity_registry.csv")}
    manifest = {m["name"]: m for m in data_mod.read_csv(ROOT, "paper/quantity_manifest.csv")}
    rep.check(len(registry) > 0 and len(manifest) > 0, f"registry ({len(registry)}) and manifest ({len(manifest)}) loaded")

    # (3) crosscheck
    try:
        import crosscheck  # noqa: PLC0415
        res = crosscheck.run(verbose=not args.quiet)
        ok = bool(res[0]) if isinstance(res, tuple) else bool(res)
        rep.check(ok, "crosscheck: closed forms agree with CSV rows (1e-9)")
    except ImportError as exc:
        rep.check(False, f"crosscheck module missing: {exc}")
    except Exception as exc:  # noqa: BLE001
        rep.check(False, f"crosscheck raised: {exc}")

    # (4) data
    data_js = ""
    hashes: dict[str, str] = {}
    try:
        payload, hashes = data_mod.build_data(ROOT, vendor)
        data_js = data_mod.emit_js(payload)
        json.loads(data_js)
        rep.check(True, f"CCC_DATA built ({len(data_js.encode('utf-8'))} bytes)")
        b = payload["fig2"]["branches"]
        rep.note("fig2 accepted rows per branch: " + ", ".join(f"{k}={len(v['r'])}" for k, v in b.items()))
        for fig in ("fig1", "fig2", "fig3", "fig4"):
            rep.check(bool(payload[fig]), f"{fig} slice nonempty")
        rep.check(not re.search(r"\b(NaN|Infinity)\b", data_js) and "</script" not in data_js and "<!--" not in data_js,
                  "data script free of NaN, Infinity, </script, <!--")
    except Exception as exc:  # noqa: BLE001
        rep.check(False, f"CCC_DATA build: {exc}")

    # (5) tables
    tables: dict[str, str] = {}
    try:
        tables, _tokens = tables_html.render_tables(ROOT)
        rep.check(len(tables) == len(tables_html.GENERATORS), f"tables rendered ({len(tables)})")
    except Exception as exc:  # noqa: BLE001
        rep.check(False, f"table rendering: {exc}")

    # (6) fragments
    sec_dir = HERE / "sections"
    files = sorted(p for p in sec_dir.glob("*.html") if p.name != SECTION_ORDER_LAST)
    if (sec_dir / SECTION_ORDER_LAST).exists():
        files.append(sec_dir / SECTION_ORDER_LAST)
    rep.check(len(files) >= 1, f"section fragments found ({len(files)})")
    sections: list[str] = []
    ids: dict[str, str] = {}
    chart_counts = {cid: 0 for cid in CHART_IDS}
    explorer_count = 0
    for path in files:
        text = path.read_text(encoding="utf-8")

        def sub_table(m: re.Match) -> str:
            name = m.group(1)
            if name not in tables:
                rep.check(False, f"{path.name}: no table generator for @@TABLE:{name}@@")
                return m.group(0)
            return tables[name]

        text = TABLE_SLOT.sub(sub_table, text)
        text = resolve_placeholders(text, registry, manifest, rep, path.name)
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

    # (7) template assembly
    template_path = HERE / "template.html"
    page = ""
    if not rep.check(template_path.exists(), "template.html present"):
        page = ""
    else:
        page = template_path.read_text(encoding="utf-8")
        css = (HERE / "style.css").read_text(encoding="utf-8") if (HERE / "style.css").exists() else ""
        rep.check(bool(css), "style.css present")
        css_fonts = set(re.findall(r'url\("fonts/([^"]+)"\)', css))
        rep.check(css_fonts == set(fonts), f"style.css @font-face files match fonts.lock.json ({len(css_fonts)})")
        scripts = {}
        for slot, fname in (("APP", "app.js"), ("CHARTS", "charts.js"), ("EXPLORER", "explorer.js")):
            p = HERE / fname
            scripts[slot] = p.read_text(encoding="utf-8") if p.exists() else ""
            rep.check(bool(scripts[slot]), f"{fname} present")
            rep.check("</script" not in scripts[slot], f"{fname} contains no </script")
        k_css = vendor["katex_css"]
        vendor_head = (f'<link rel="stylesheet" href="{k_css["url"]}" integrity="{k_css["integrity"]}" '
                       f'crossorigin="anonymous">')
        vendor_scripts = "\n".join(
            f'<script defer src="{vendor[n]["url"]}" integrity="{vendor[n]["integrity"]}" crossorigin="anonymous"></script>'
            for n in ("katex_js", "katex_auto_render", "plotly"))
        meta_items = [f"registry {hashes.get('numerics/quantity_registry.csv', '')[:12]}"] + [
            f"{k} {v[:12]}" for k, v in sorted(hashes.items()) if k != "numerics/quantity_registry.csv"]
        build_meta = '<p class="build-meta">Sources (sha256, first 12 hex): ' + "; ".join(meta_items) + ".</p>"
        fills = {
            "VENDOR_HEAD": vendor_head,
            "THEME_BOOT": "",
            "STYLE": "<style>\n" + css + "\n</style>",
            "TOC": build_toc(sections),
            "SECTIONS": "\n".join(sections),
            "DATA": "<script>window.CCC_DATA = " + data_js + ";</script>",
            "APP": "<script>\n" + scripts["APP"] + "\n</script>",
            "CHARTS": "<script>\n" + scripts["CHARTS"] + "\n</script>",
            "EXPLORER": "<script>\n" + scripts["EXPLORER"] + "\n</script>",
            "VENDOR_SCRIPTS": vendor_scripts,
            "BUILD_META": build_meta,
        }
        present = set(SLOT.findall(page))
        if "THEME_BOOT" not in present:
            fills.pop("THEME_BOOT")
        for slot in ("VENDOR_HEAD", "STYLE", "TOC", "SECTIONS", "DATA", "APP", "CHARTS", "EXPLORER", "VENDOR_SCRIPTS", "BUILD_META"):
            rep.check(slot in present, f"template has slot @@{slot}@@")

        def fill(m: re.Match) -> str:
            return fills.get(m.group(1), m.group(0))

        page = SLOT.sub(fill, page)
        page = resolve_placeholders(page, registry, manifest, rep, "template.html")
        rep.check("@@" not in page, "no slot markers left in the page")

    # (8) validate the complete page before replacing artifacts
    if page and not rep.failures:
        rep.check(not PLACEHOLDER.search(page), "output has no [[name]] placeholders left")
        m = re.search(r"<script>window\.CCC_DATA = (.*?);</script>", page, re.S)
        ok = False
        if m:
            try:
                json.loads(m.group(1))
                ok = True
            except json.JSONDecodeError:
                ok = False
        rep.check(ok, "embedded CCC_DATA parses as JSON")
        tags = re.findall(r"<(?:script|link)\b[^>]*cdnjs\.cloudflare\.com[^>]*>", page)
        rep.check(len(tags) == 4 and all("integrity=" in t and 'crossorigin="anonymous"' in t for t in tags),
                  f"four vendor tags carry integrity and crossorigin ({len(tags)})")
        for cid in CHART_IDS:
            rep.check(page.count(f'id="chart-{cid}"') == 1, f"output has one chart-{cid} mount")
        rep.check(page.count('id="explorer"') == 1, "output has one explorer mount")
        rep.check(not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", page), "output carries no timestamps")
        rep.note(f"docs/index.html: {len(page.encode('utf-8'))} bytes")

    for rel in PDFS:
        rep.check(args.allow_missing_pdf or (ROOT / rel).is_file(), f"{rel} present for copying")
    if page and not rep.failures:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8", newline="\n")
        (out_dir / ".nojekyll").write_text("", encoding="utf-8")
        for rel in PDFS:
            src = ROOT / rel
            if src.exists():
                shutil.copyfile(src, out_dir / src.name)
                rep.check((out_dir / src.name).stat().st_size > 0, f"copied {src.name}")
        (out_dir / "fonts").mkdir(exist_ok=True)
        for name in fonts:
            shutil.copyfile(HERE / "fonts" / name, out_dir / "fonts" / name)
        rep.check(all((out_dir / "fonts" / n).is_file() for n in fonts), f"copied {len(fonts)} font files")

    # (10) manifest
    passed = not rep.failures
    man_dir = ROOT / "numerics" / "manifests"
    man_dir.mkdir(parents=True, exist_ok=True)
    out_html = out_dir / "index.html"
    manifest_obj = {
        "exercise": "handout",
        "timestamp_utc": None,  # omitted on purpose: the manifest is committed and must not churn
        "inputs": hashes,
        "method": "handout build: CSV to inline JSON, registry placeholders, table rendering, template assembly",
        "tolerances": {"crosscheck_abs": 1e-9},
        "software": {"python": sys.version.split()[0], "platform": platform.platform()},
        "outputs": {f"{args.out}/index.html": hashlib.sha256(out_html.read_bytes()).hexdigest()} if out_html.exists() else {},
        "checks": rep.checks,
        "passed": passed,
        "notes": ["vendor: " + ", ".join(f"{k} {v['version']}" for k, v in vendor.items()),
                  "fonts: " + ", ".join(f"{k} sha256:{v['sha256'][:12]}" for k, v in fonts.items())],
    }
    (man_dir / "handout.json").write_text(json.dumps(manifest_obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    if not args.quiet and rep.placeholders_used:
        print("\nplaceholders used:")
        for name in sorted(rep.placeholders_used):
            print(f"  {name:40s} {rep.placeholders_used[name]}")
    print("\nHANDOUT BUILD", "PASSED" if passed else f"FAILED ({len(rep.failures)} failures)")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
