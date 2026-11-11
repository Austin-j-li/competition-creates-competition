"""Focused display checks for the handout. Run after build.py.

    python3 handout/check_display.py [--out docs]

Python standard library only. Each block prints PASS or raises. The checks keep these guarantees
of handout/README.md:

- the Read-the-paper tab states the page counts, hashes and text date of the two PDFs it ships,
  as read from the files;
- every displayed number is the display of a slot registry row and carries its key and exact
  value; numbers inside formulas carry the same; no decimal is typed into the prose;
- the page ships only the locked faces (Libertinus Serif, DM Sans, Libertinus Math) and makes
  no network request;
- the page and the handout styles use only the palette of DESIGN.md (white paper, ink, greys,
  dark purple #361A54 for coloured text and bright purple #993BFF for rules, with the dark
  theme on dark purple), each UCL colour on the ground that UCL permits;
- neither the page nor the handout sources carry a retired look: the oxblood accent of the look
  of 29 October 2026, the --ucl-* tokens of the template of 3 October 2026, or the marks of that
  template (a gradient, a shadow, a rounded box or pill).
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
assert families == {"Libertinus Serif", "DM Sans", "Libertinus Math"}, families
assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "a network request"
print("PASS only Libertinus Serif, DM Sans and Libertinus Math; no network request")

# ------------------------------------------------------------------ the palette
# The look of 11 November 2026 (DESIGN.md at the repository root): white paper, ink and greys, with
# the official UCL colours in fixed roles. Dark purple is coloured text (--accent); bright purple is
# every rule, bullet and mark (--rule). The dark theme is dark purple paper with heritage blue for
# coloured text and mid purple for rules; three tones derived from dark purple give its hairlines,
# grid and tooltip ground. Every hex colour in the stylesheet, the template, the renderer and the
# built page's styles must be in that palette.
PALETTE = {
    "#ffffff", "#f2f2f2", "#1c1c1c", "#666666", "#c9c9c9", "#e6e6e6",  # white paper, ink, greys
    "#361a54", "#993bff", "#ba82ff", "#30d6ff", "#fafafa",  # UCL: dark, bright and mid purple, heritage blue, screen white
    "#6a4e8a", "#4a2d6c", "#422464",  # derived from dark purple for the dark theme; not UCL colours
    "#000000",  # print
}
HEX = re.compile(r"#[0-9a-f]{6}\b", re.I)
styled = [HERE / "style.css", HERE / "template.html", HERE / "charts.js"]
page_styles = "".join(re.findall(r"<style\b[^>]*>(.*?)</style>", page, re.S))
stray = sorted({f"{f.name}:{m.group(0)}" for f in styled for m in HEX.finditer(f.read_text(encoding="utf-8"))
                if m.group(0).lower() not in PALETTE}
               | {f"index.html:{m.group(0)}" for m in HEX.finditer(page_styles) if m.group(0).lower() not in PALETTE})
assert not stray, f"a colour outside the palette: {stray[:8]}"
css = (HERE / "style.css").read_text(encoding="utf-8")
light = re.search(r":root,\s*:root\[data-theme=\"light\"\]\s*\{([^}]*)\}", css).group(1)
dark = re.search(r":root\[data-theme=\"dark\"\]\s*\{([^}]*)\}", css).group(1)
for block, name, value in ((light, "--bg", "#ffffff"), (light, "--accent", "#361a54"), (light, "--rule", "#993bff"),
                           (dark, "--bg", "#361a54"), (dark, "--accent", "#30d6ff"), (dark, "--rule", "#ba82ff")):
    assert re.search(rf"{name}:\s*{value}\s*;", block, re.I), f"the token {name} is not {value}"
# UCL's pairing rules: bright purple is for white grounds only; heritage blue and mid purple are for
# dark purple grounds only.
assert not re.search(r"#993bff", dark, re.I), "bright purple on the dark purple ground"
assert not re.search(r"#(?:30d6ff|ba82ff)", light, re.I), "heritage blue or mid purple on the white ground"
print(f"PASS every hex colour in {len(styled)} styled sources and the page styles is in the palette; "
      "dark purple text and bright purple rules on white, heritage blue and mid purple on dark purple")

# ------------------------------------------------------------------ the retired looks
# Neither retired look may come back through a source or the built page: the oxblood accent of the
# look of 29 October 2026 (as a hex or inside rgba()), and the template of 3 October 2026, which the
# author rejected. That template used the same UCL hexes as the present look, so its marks identify
# it: the --ucl-* tokens, a gradient, a shadow, and a rounded box or pill (a radius above 2 px).
RETIRED = re.compile(r"#(?:7A1F1F|D4908F)\b|rgba\(\s*(?:122,\s*31,\s*31|212,\s*144,\s*143)\b|--ucl-(?:dark|bright|mid)\b"
                     r"|\b(?:linear|radial|conic)-gradient\b|\bbox-shadow\b|\bborder-radius:\s*(?!\s|0\s*[;}]|2px\b)", re.I)
sources = [out / "index.html"] + sorted(HERE.glob("*.html")) + sorted(HERE.glob("*.css")) + sorted(HERE.glob("*.js")) \
    + sorted((HERE / "sections").glob("*.html"))
hits = [f"{f.relative_to(ROOT)}:{m.group(0)}" for f in sources for m in RETIRED.finditer(f.read_text(encoding="utf-8"))]
assert not hits, f"a mark of a retired look appears: {hits[:6]}"
print(f"PASS no oxblood, no --ucl-* token, no gradient, shadow or rounded box in the page or in {len(sources) - 1} handout source files")
