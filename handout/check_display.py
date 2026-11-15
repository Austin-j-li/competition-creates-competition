"""Focused display checks for the handout. Run after build.py.

    python3 handout/check_display.py [--out docs]

Python standard library only. Each block prints PASS or raises. The checks keep these guarantees
of handout/README.md:

- the Read-the-paper tab states the page counts, hashes and text date of the two PDFs it ships,
  as read from the files;
- every displayed number is the display of a slot registry row and carries its key and exact
  value; numbers inside formulas carry the same; no decimal is typed into the prose;
- the page ships only the locked faces (Jost and STIX Two Text) and makes no network request;
- every colour literal in the page's styles, the look's tokens (design/tokens.css), the handout
  stylesheet, the template and the figure scripts is in the palette of the two-colour plate:
  white stock, black ink, a dark grey for secondary text, the press green, white type on a band,
  and three light greys for line screens and a comparison trace; the green is spent on one meaning
  only, the price bringing in the costly rival; there is one theme and no dark-theme hook;
- neither the page nor the handout sources carry a retired look: the purple look of 11 November
  2026 that the plate replaces (its UCL hexes and its dark-theme derivatives), the oxblood accent
  of 29 October 2026, the --ucl-* tokens of the template of 3 October 2026, or the marks of that
  template (a gradient, a shadow, a rounded box or pill). The one gradient allowed is the line
  screen that design/tokens.css declares as --tint-fill.
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
assert families == {"Jost", "STIX Two Text"}, families
assert not re.search(r'<(?:script|link|img|iframe)\b[^>]*(?:src|href)="(?:https?:)?//', page), "a network request"
print("PASS only Jost and STIX Two Text; no network request")

# ------------------------------------------------------------------ the palette
# The two-colour plate (talk/LOOK_plate.md; tokens in design/tokens.css): bright white stock, black
# ink, a dark grey for secondary text at 7:1 or better, one press green, white type on the black
# band or the green, and light greys that only draw line screens and the talk's comparison trace.
# Every colour literal (hex, oklch(), rgb(), hsl()) in these sources must be one of them.
PALETTE = {
    "oklch(0.985 0.002 250)",  # --ground: white stock
    "oklch(0.20 0.01 260)",    # --ink: black ink, every keyline
    "oklch(0.40 0.012 260)",   # --ink-2: secondary text (8.8:1 on the ground)
    "oklch(0.50 0.15 150)",    # --accent / --fig-accent: press green, the one meaning
    "#ffffff",                 # --accent-ink / --band-ink: white type on the band or the green
    "oklch(0.62 0.008 260)",   # --scr-page: the lines of a screen in a figure
    "oklch(0.70 0.008 260)",   # --trace-grey: the talk's trace of the full model
    "oklch(0.80 0.006 260)",   # the talk's broad trace stroke
}
COLOUR = re.compile(r"#[0-9a-f]{8}\b|#[0-9a-f]{6}\b|#[0-9a-f]{3}\b(?![-\w])|\b(?:oklch|oklab|rgba?|hsla?|lab|lch)\([^)]*\)", re.I)
TOKENS = ROOT / "design" / "tokens.css"
styled = [TOKENS, HERE / "style.css", HERE / "template.html", HERE / "charts.js", HERE / "figures.js", HERE / "explorer.js"]
page_styles = "".join(re.findall(r"<style\b[^>]*>(.*?)</style>", page, re.S))


def colours(text: str) -> set[str]:
    # an id reference such as url(#scr-a) or href="#tab-paper" is not a colour
    text = re.sub(r"url\(#[^)]*\)|href=\"#[^\"]*\"|\bid=\"[^\"]*\"", " ", text)
    return {re.sub(r"\s+", " ", m.group(0).lower()) for m in COLOUR.finditer(text)}


stray = sorted({f"{f.name}:{c}" for f in styled for c in colours(f.read_text(encoding="utf-8")) if c not in PALETTE}
               | {f"index.html:{c}" for c in colours(page_styles) if c not in PALETTE})
assert not stray, f"a colour outside the palette: {stray[:8]}"
tokens = TOKENS.read_text(encoding="utf-8")
for name, value in (("--ground", "oklch(0.985 0.002 250)"), ("--ink", "oklch(0.20 0.01 260)"),
                    ("--ink-2", "oklch(0.40 0.012 260)"), ("--accent", "oklch(0.50 0.15 150)"),
                    ("--fig-accent", "oklch(0.50 0.15 150)")):
    assert re.search(rf"{name}:\s*{re.escape(value)}\s*;", tokens), f"the token {name} is not {value}"
css = (HERE / "style.css").read_text(encoding="utf-8")
# Green means one thing: every rule of the stylesheet that spends it names that meaning (a recruit
# class); focus, links, tabs and the current contents entry are black.
for sel, body_ in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
    if re.search(r"var\(--(?:accent|fig-accent)\)", body_):
        assert all("recruit" in part for part in sel.split(",")), f"green outside its meaning: {sel.strip()}"
assert re.search(r"--focus-ring:\s*var\(--ink\)", tokens) and not re.search(r"--focus-ring:", css), "the focus ring is not black"
for f in (HERE / "figures.js", HERE / "explorer.js"):
    # the figure scripts reach the green only through the renderer's recruit token
    assert not re.search(r"--(?:fig-)?accent|oklch\(0\.50 0\.15 150\)", f.read_text(encoding="utf-8")), f"{f.name} names the green directly"
# One theme: no dark theme, no theme toggle, no stored theme.
theme = [f"{f.name}" for f in [HERE / "style.css", HERE / "template.html", HERE / "app.js", HERE / "charts.js"]
         if re.search(r"data-theme|theme-toggle|ccc-theme|themechange|prefers-color-scheme", f.read_text(encoding="utf-8"))]
assert not theme and "data-theme" not in page and "theme-toggle" not in page, f"a theme hook remains: {theme}"
print(f"PASS every colour in {len(styled)} styled sources and the page styles is in the plate's palette; "
      "green only on the recruit marks; black focus; one theme")

# ------------------------------------------------------------------ the retired looks
# No retired look may come back through a source or the built page: the purple look of 11 November
# 2026 (the UCL hexes #361A54, #993BFF, #BA82FF, #30D6FF and its dark-theme tones #6A4E8A, #4A2D6C,
# #422464, and the rgba() forms of the purples and the blue), the oxblood accent of 29 October 2026
# (as a hex or inside rgba()), and the template of 3 October 2026, whose marks identify it: the
# --ucl-* tokens, a gradient, a shadow, and a rounded box or pill (a radius above 2 px). The one
# gradient allowed is the line screen declared as --tint-fill in design/tokens.css (repeating thin
# lines with hard stops); it is removed before the scan and nothing else is.
RETIRED = re.compile(r"#(?:7A1F1F|D4908F|361A54|993BFF|BA82FF|30D6FF|6A4E8A|4A2D6C|422464)\b"
                     r"|rgba\(\s*(?:122,\s*31,\s*31|212,\s*144,\s*143|153,\s*59,\s*255|48,\s*214,\s*255|54,\s*26,\s*84|186,\s*130,\s*255)\b"
                     r"|--ucl-(?:dark|bright|mid)\b"
                     r"|\b(?:linear|radial|conic)-gradient\b|\bbox-shadow\b|\bborder-radius:\s*(?!\s|0\s*[;}]|2px\b)", re.I)


def without_screen(text: str) -> tuple[str, int]:
    """Remove each `--tint-fill: repeating-linear-gradient(...)` declaration (balanced parentheses)."""
    n = 0
    while (m := re.search(r"--tint-fill:\s*repeating-linear-gradient\(", text)):
        depth, i = 1, m.end()
        while depth and i < len(text):
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            i += 1
        text = text[:m.start()] + "--tint-fill: screen" + text[i:]
        n += 1
    return text, n


assert without_screen(tokens)[1] == 1, "design/tokens.css no longer declares the one line-screen gradient"
sources = [out / "index.html", TOKENS] + sorted(HERE.glob("*.html")) + sorted(HERE.glob("*.css")) + sorted(HERE.glob("*.js")) \
    + sorted((HERE / "sections").glob("*.html"))
hits = [f"{f.relative_to(ROOT)}:{m.group(0)}" for f in sources
        for m in RETIRED.finditer(without_screen(f.read_text(encoding="utf-8"))[0])]
assert not hits, f"a mark of a retired look appears: {hits[:6]}"
print(f"PASS no purple, no oxblood, no --ucl-* token, no gradient other than the tokens' line screen, "
      f"no shadow or rounded box in the page or in {len(sources) - 1} source files")
