"""Focused display checks for the handout. Run after build.py.

    python3 handout/check_display.py [--out docs]

Python standard library only. Each block prints PASS or raises. The checks keep these guarantees
of handout/README.md:

- the Read-the-paper tab states the page counts, hashes and text date of the two PDFs it ships,
  as read from the files;
- every displayed number is the display of a slot registry row and carries its key and exact
  value; numbers inside formulas carry the same; no decimal is typed into the prose;
- the page ships only the locked faces (Libertinus Serif, Libertinus Sans, Libertinus Math) and makes
  no network request;
- the page and the handout styles use only the journal palette of DESIGN.md (white paper, ink,
  greys and the oxblood accent #7A1F1F, with the composed dark theme), and neither the page nor
  the handout sources carry the rejected purple palette (the UCL hexes #361A54, #993BFF, #BA82FF
  or the --ucl-* tokens).
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
assert families == {"Libertinus Serif", "Libertinus Sans", "Libertinus Math"}, families
assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "a network request"
print("PASS only Libertinus Serif, Libertinus Sans and Libertinus Math; no network request")

# ------------------------------------------------------------------ the journal palette
# The journal look (DESIGN.md at the repository root) has one chrome colour, the oxblood accent;
# everything else is white, ink or grey, with the composed dark theme. Every hex colour in the
# stylesheet, the template, the renderer and the built page's styles must be in that palette, and
# the accent token must be the oxblood of the Beamer deck.
JOURNAL = {
    "#ffffff", "#f2f2f2", "#1c1c1c", "#666666", "#c9c9c9", "#e6e6e6", "#7a1f1f",  # white paper
    "#171717", "#242424", "#ebebeb", "#a3a3a3", "#474747", "#2e2e2e", "#d4908f",  # the dark theme
    "#000000",  # print
}
HEX = re.compile(r"#[0-9a-f]{6}\b", re.I)
styled = [HERE / "style.css", HERE / "template.html", HERE / "charts.js"]
page_styles = "".join(re.findall(r"<style\b[^>]*>(.*?)</style>", page, re.S))
stray = sorted({f"{f.name}:{m.group(0)}" for f in styled for m in HEX.finditer(f.read_text(encoding="utf-8"))
                if m.group(0).lower() not in JOURNAL}
               | {f"index.html:{m.group(0)}" for m in HEX.finditer(page_styles) if m.group(0).lower() not in JOURNAL})
assert not stray, f"a colour outside the journal palette: {stray[:8]}"
light = re.search(r":root,\s*:root\[data-theme=\"light\"\]\s*\{([^}]*)\}", (HERE / "style.css").read_text(encoding="utf-8")).group(1)
assert re.search(r"--accent:\s*#7a1f1f\s*;", light, re.I), "the accent token is not the oxblood #7A1F1F"
assert re.search(r"--bg:\s*#ffffff\s*;", light, re.I), "the paper is not white"
print(f"PASS every hex colour in {len(styled)} styled sources and the page styles is in the journal palette; the accent is #7A1F1F on white")

# ------------------------------------------------------------------ the rejected palette
# The purple palette of the earlier "UCL family" design must not come back through any source or
# the built page.
PURPLE = re.compile(r"#(?:361A54|993BFF|BA82FF)\b|--ucl-(?:dark|bright|mid)\b", re.I)
sources = [out / "index.html"] + sorted(HERE.glob("*.html")) + sorted(HERE.glob("*.css")) + sorted(HERE.glob("*.js")) \
    + sorted((HERE / "sections").glob("*.html"))
hits = [f"{f.relative_to(ROOT)}:{m.group(0)}" for f in sources for m in PURPLE.finditer(f.read_text(encoding="utf-8"))]
assert not hits, f"the rejected purple palette appears: {hits[:6]}"
print(f"PASS no UCL purple hex or token in the page or in {len(sources) - 1} handout source files")
