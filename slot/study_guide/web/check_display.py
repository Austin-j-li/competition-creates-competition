"""Static checks for the built HTML study guide. Standard library only."""
from __future__ import annotations

import html
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDE = HERE.parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "handout"))
import slot_data  # noqa: E402


def main() -> int:
    output = GUIDE / "index.html"
    page = output.read_text(encoding="utf-8")
    registry = slot_data.read_registry(ROOT)

    assert len(re.findall(r'<article class="chapter"', page)) == 17, "expected all 17 chapters"
    assert len(re.findall(r'<aside class="preface"', page)) == 1, "expected the complete guide preface"
    assert "Decimal displays are rounded" in page and "maps the paper to this guide" in page, "incomplete preface"
    assert len(re.findall(r'<div class="part"', page)) == 4, "expected three parts and appendices"
    assert len(re.findall(r"<table\b", page)) == 33, "expected all 33 source tables"
    assert len(re.findall(r'<aside class="note ', page)) == 77, "expected all 77 teaching notes"
    assert len(re.findall(r'<figure class="diagram ', page)) == 4, "expected four symbolic diagrams"
    assert len(re.findall(r'data-chart="', page)) == 3, "expected payoffs, beliefs, and research charts"
    assert len(re.findall(r'id="explorer" data-explorer', page)) == 1, "expected one benchmark explorer"
    print("PASS 17 chapters, 33 tables, 77 notes, four diagrams, three charts, and one explorer")

    identifiers = re.findall(r'\sid="([^"]+)"', page)
    duplicates = [key for key, count in Counter(identifiers).items() if count > 1]
    assert not duplicates, f"duplicate IDs: {duplicates}"
    missing = sorted({href for href in re.findall(r'href="#([^"]+)"', page) if href not in identifiers})
    assert not missing, f"broken local links: {missing}"
    assert "\\reg{" not in page and "@@" not in page, "unresolved registry or build marker"
    assert "&lt;a href" not in page and '&lt;span class="q"' not in page, "escaped generated HTML"
    assert "—" not in page and "–" not in page, "unwanted typographic dash"
    print(f"PASS {len(identifiers)} unique IDs and every local link resolves; no unresolved build markers")

    number_spans = re.findall(r'<span class="q" data-q="([^"]+)" data-value="([^"]*)" title="[^"]*">([^<]*)</span>', page)
    assert len(number_spans) == len(re.findall(r'<span class="q"', page)), "incomplete registry provenance span"
    assert len(number_spans) >= 250, "registry provenance spans are missing"
    for key, value, shown in number_spans:
        row = registry[key]
        assert html.unescape(value) == row["value"], f"{key}: exact value differs from registry"
        assert html.unescape(shown) == row["display"].replace(r"\%", "%"), f"{key}: display differs from registry"
    print(f"PASS {len(number_spans)} displayed values match their registry keys and exact values")

    assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "external asset request"
    for relative in (
        "web/assets/vendor/katex.min.js", "web/assets/vendor/katex.min.css", "web/assets/charts.js",
        "web/assets/figures.js", "web/assets/explorer.js", "Competition_Creates_Competition_Study_Guide_Slot.pdf",
    ):
        assert (GUIDE / relative).is_file(), f"missing local asset: {relative}"
    assert "web/assets/vendor/katex.min.css" in page, "KaTeX stylesheet is not loaded"
    print("PASS all runtime assets are local and the PDF fallback exists")
    print(f"PASS {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
