"""Focused display checks for the handout. Run after build.py.

    python3 handout/check_display.py [--out docs]

Python standard library only. Each block prints PASS or raises. The checks keep these guarantees
of handout/README.md:

- the Read-the-paper tab states the page counts, hashes and text date of the two PDFs it ships,
  as read from the files;
- every displayed number is the display of a slot registry row and carries its key and exact
  value; numbers inside formulas carry the same; no decimal is typed into the prose;
- the page ships only the locked faces (Archivo, STIX Two Text, Fira Mono, the symbol fallback) and makes
  no network request;
- neither the page nor the handout sources carry the rejected purple palette (the UCL hexes
  #361A54, #993BFF, #BA82FF or the --ucl-* tokens): the design is the ruled document of DESIGN.md.
"""
from __future__ import annotations

import argparse
import html
import importlib.util
import re
from pathlib import Path

import slot_data

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("handout_build", HERE / "build.py")
build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build)

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="docs")
out = ROOT / ap.parse_args().out
page = (out / "index.html").read_text(encoding="utf-8")

# ------------------------------------------------------------------ the published PDFs
for name in build.PAPERS:
    facts = build.pdf_facts(out / name)
    assert facts["pages"] > 0 and f'{facts["pages"]} pages' in page and facts["sha256"] in page, f"the paper tab misstates {name}"
main = build.pdf_facts(out / "paper.pdf")
assert f'Text revision of {main["created"]}' in page and f'Text revised {main["created"]}' in page
print(f"PASS the paper tab states {main['pages']} and {build.pdf_facts(out / 'comparison.pdf')['pages']} pages, "
      f"both hashes and the text date {main['created']}")

# ------------------------------------------------------------------ numbers
registry = slot_data.read_registry(ROOT)
body = page.split("<main", 1)[1]
n = 0
for m in re.finditer(r'<span class="q" data-q="([^"]+)" data-value="([^"]*)" title="[^"]*">([^<]*)</span>', page):
    key, value, text = m.groups()
    row = registry[key]
    assert html.unescape(value) == row["value"], f"{key}: value attribute differs from the registry"
    assert html.unescape(text) == build.shown_value(row), f"{key}: shows {text}; the registry display is {row['display']}"
    n += 1
assert n == len(re.findall(r'<span class="q"', page)), "a number span lacks its key or value"
k = 0
for m in re.finditer(r'<span class="q-math" data-q="([^"]+)" data-shown="([^"]*)" title="[^"]*">(.*?)</span>', page, re.S):
    keys, shown, math = m.group(1).split(), html.unescape(m.group(2)).split("|"), m.group(3)
    for key, s in zip(keys, shown, strict=True):
        assert build.shown_value(registry[key], in_math=True) == s, key
        assert s in html.unescape(math), f"{key}: the formula does not print {s}"
        k += 1
# No result is typed into the prose: outside number spans, mathematics, scripts and the build
# line, no decimal with two or more places may appear.
prose = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<span class=\"q[^\"]*\"[^>]*>.*?</span>"
               r"|\\\(.*?\\\)|\\\[.*?\\\]|<p class=\"build-meta\">.*?</p>|<code>.*?</code>|<pre\b.*?</pre>", " ", body, flags=re.S)
stray = re.findall(r"(?<![\w.])\d+\.\d{2,}(?![\w.])", re.sub(r"<[^>]+>", " ", prose))
assert not stray, f"unbound decimals in the prose: {stray[:8]}"
print(f"PASS {n} number spans and {k} numbers in formulas print their slot registry display; "
      "no decimal is typed into the prose")

# ------------------------------------------------------------------ faces, network
families = set(re.findall(r'@font-face \{ font-family: "([^"]+)"', page))
assert families == {"Archivo", "STIX Two Text", "Fira Mono", "CCC Symbols"}, families
assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "a network request"
print("PASS only Archivo, STIX Two Text, Fira Mono and the symbol fallback; no network request")

# ------------------------------------------------------------------ the rejected palette
# The ruled document (DESIGN.md at the repository root) has no chrome colour. The purple palette
# of the earlier "UCL family" design must not come back through any source or the built page.
PURPLE = re.compile(r"#(?:361A54|993BFF|BA82FF)\b|--ucl-(?:dark|bright|mid)\b", re.I)
sources = [out / "index.html"] + sorted(HERE.glob("*.html")) + sorted(HERE.glob("*.css")) + sorted(HERE.glob("*.js")) \
    + sorted((HERE / "sections").glob("*.html"))
hits = [f"{f.relative_to(ROOT)}:{m.group(0)}" for f in sources for m in PURPLE.finditer(f.read_text(encoding="utf-8"))]
assert not hits, f"the rejected purple palette appears: {hits[:6]}"
print(f"PASS no UCL purple hex or token in the page or in {len(sources) - 1} handout source files")
