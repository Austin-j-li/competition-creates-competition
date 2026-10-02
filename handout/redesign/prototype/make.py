"""Build the three design-direction mockups. Standard library only (plus fontTools for the
font report in make_index.py). Reads the live handout HTML, the registry, the Beamer deck and
the speaker script. Writes proposals/direction-{a,b,c}/ with everything needed offline.
"""
import csv, hashlib, html, json, re, shutil, subprocess
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROPOSALS = HERE.parent
WORK = PROPOSALS.parent
REPO = Path("/home/uctpiaj/work/Projects/competition-creates-competition")
INPUTS = WORK / "inputs"
FONTS = PROPOSALS / "_fonts"
SHARED = HERE / "shared"
SKINS = HERE / "skins"

LIVE = (INPUTS / "live_handout_stripped.html").read_text(encoding="utf-8")
DATA = json.loads((INPUTS / "live_handout_data.json").read_text(encoding="utf-8"))
REG = {r["name"]: r for r in csv.DictReader(open(REPO / "numerics/quantity_registry.csv", encoding="utf-8"))}
TALK = (REPO / "overleaf/talk/talk.tex").read_text(encoding="utf-8")
SCRIPT = (REPO / "overleaf/talk/script.tex").read_text(encoding="utf-8")

UCL = {"dark": "#361A54", "bright": "#993BFF", "mid": "#BA82FF"}
C_INFO, C_COST = "#AA4B00", "#006F50"


# ----------------------------------------------------------------------------- registry guard
def R(key: str, shown: str, pct: bool = False, check: str = None) -> str:
    """Return a span for a registry value. `shown` is the string the Beamer deck prints; it must
    round from the registry value, or the build stops. Nothing is re-rounded here.
    `check` gives a plain decimal form of `shown` when the shown string uses typographic marks."""
    r = REG[key]
    val = Decimal(r["value"]) if r["value"] not in ("n/a", "") else None
    disp = r["display"].replace("\\%", "%")
    ok = shown == disp
    if not ok and val is not None:
        try:
            s = Decimal((check or shown).replace("−", "-").replace(" pp", ""))
            target = val * 100 if pct else val
            # 3 significant digits of the registry value, or the displayed decimal itself
            digits = len(s.as_tuple().digits)
            ok = abs(s - target) <= Decimal(10) ** (s.as_tuple().exponent) / 2
        except Exception:
            ok = False
    if not ok:
        raise SystemExit(f"registry guard: {key} shown as {shown!r} but registry display is {disp!r} (value {r['value']})")
    title = f"{disp} · {r['status']} · {r['source_file']} · {r['source_row']}"
    return f'<span class="q" data-q="{key}" data-status="{r["status"]}" title="{html.escape(title)}">{shown}</span>'


def T(table: str, shown: str) -> str:
    """A value printed in a paper table file rather than the registry."""
    return f'<span class="q" data-q="{html.escape(table)}" data-status="analytical" title="{html.escape(shown + " · analytical · " + table)}">{shown}</span>'


# ----------------------------------------------------------------------------- live prose
def section(name: str) -> str:
    m = re.search(r'<section class="sec" id="sec-%s">(.*?)</section>' % name, LIVE, flags=re.S)
    return m.group(1)


def port_mechanism() -> str:
    s = section("mechanism")
    # Figure 1: replace the chart mount with our SVG host, keep the caption.
    s = re.sub(r'<p class="figure-scroll-hint">.*?</p>', "", s)
    s = s.replace('<div class="chart-mount" id="chart-fig1" role="img" aria-label="Target-payoff spread rising and challenger acquisition profits falling with incumbent strength"></div>',
                  '<div class="chart-mount" id="chart-fig1" tabindex="0" aria-label="Figure 1, interactive. Left and right arrow keys move the cursor."></div>')
    s = s.replace('Hover for values.', 'Hover, or focus the figure and use the arrow keys, for values.')
    # Explorer: labelled empty slot.
    s = s.replace('<div id="explorer" data-explorer tabindex="0"></div>',
                  '<div id="explorer" class="slot" role="note"><p><strong>Explorer slot.</strong> The live explorer mounts here (handout/explorer.js). It is a fixed-order calculation, not an equilibrium solver. Not rebuilt in this mockup.</p></div>')
    # Section time line becomes a kicker.
    s = s.replace('<p class="section-time">2 · The mechanism · 4 minutes</p>', '<p class="kicker section-time">2 · The mechanism · 4 minutes</p>')
    return s


def opening() -> dict:
    m = re.search(r'<aside class="opening-question"[^>]*>(.*?)</aside>', LIVE, flags=re.S)
    return {"aside": m.group(1).strip()}


def stub(name: str, title: str, time: str) -> str:
    return (f'<section class="sec stub" id="sec-{name}"><h2>{title}</h2><p class="kicker section-time">{time}</p>'
            f'<p class="muted">Live prose unchanged. Not rebuilt in this mockup; see <code>handout-reconciliation.md</code> for the proposed edits.</p></section>')


# ----------------------------------------------------------------------------- frames from talk.tex
PART_OF = {"F1": 1, "F2": 1, "F3": 1, "F4": 2, "F5": 3, "F6": 3, "F7": 4, "F8": 4, "F9": 5, "F10a": 6, "F10b": 6, "F11": 6,
           "F12": 7, "F13": 7, "F14": 7, "F15": 8, "F16": 8}
PARTS = [{"n": 1, "name": "Question"}, {"n": 2, "name": "Model"}, {"n": 3, "name": "Two claims"}, {"n": 4, "name": "Price"},
         {"n": 5, "name": "Theorem"}, {"n": 6, "name": "Numbers"}, {"n": 7, "name": "Boundaries"}, {"n": 8, "name": "Close"},
         {"n": "B", "name": "Backups"}]


def detex(s: str) -> str:
    s = re.sub(r"\\texorpdfstring\{([^{}]*)\}\{[^{}]*\}", r"\1", s)
    s = s.replace("\\\\[2pt]", " ").replace("\\\\", " ")
    s = re.sub(r"\$r_([012])\$", lambda m: "r" + "₀₁₂"[int(m.group(1))], s)
    s = re.sub(r"\$h>\\ell\$", "h > ℓ", s)
    s = s.replace("\\ell", "ℓ").replace("$", "").replace("~", " ").replace("\\&", "&")
    return re.sub(r"\s+", " ", s).strip()


def frames() -> list:
    out, main_targets = [], {}
    pattern = re.compile(r"\\begin\{frame\}(\[[^\]]*\])?(?:\{([^\n]*)\})?\n(.*?)\\end\{frame\}", re.S)
    in_appendix = False
    shown_num = 0
    for m in pattern.finditer(TALK):
        opts, title, body = m.group(1) or "", m.group(2) or "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders", m.group(3)
        label = re.search(r"label=([A-Za-z0-9]+)", opts).group(1)
        if label.startswith("A") and label != "A": in_appendix = True
        targets = re.findall(r"\\hypertarget\{((?:main|app):[a-z]+)\}", body)
        if not in_appendix:
            for t in targets: main_targets[t] = label
        if label == "F0": num = "0"
        elif not in_appendix:
            if "noframenumbering" not in opts: shown_num += 1
            num = str(shown_num)
        else:
            num = label
        if label == "F10b": num = "10 · r₂ column (build)"
        back = re.search(r"\\BackButton\{((?:main|app):[a-z]+)\}", body) or re.search(r"\\hyperlink\{((?:main|app):[a-z]+)\}\{\\beamerreturnbutton", body)
        out.append({"id": label.lower() if label not in ("F10a", "F10b") else "f10", "label": label, "num": num, "title": detex(title),
                    "backup": in_appendix, "part": "B" if in_appendix else PART_OF.get(label, ""), "targets": targets,
                    "back": back.group(1) if back else None})
    app_targets = {t: f["label"] for f in out if f["backup"] for t in f["targets"]}
    for f in out:
        if f["backup"]:
            f["origin"] = main_targets.get(f["back"]) or app_targets.get(f["back"]) or "?"
        f.pop("targets"); f.pop("back")
    assert len(out) == 47, len(out)
    return out


# ----------------------------------------------------------------------------- notes from script.tex
def notes() -> dict:
    blocks = {}
    for m in re.finditer(r"\\scriptframe\{(.+?)\}\{(.+?)\}\{%\n(.*?)\n\}\n", SCRIPT, flags=re.S):
        title, timing, body = m.group(1), m.group(2), m.group(3)
        blocks.setdefault(detex(title), []).append((timing, body))
    op = re.search(r"\\scriptopening\{(.+?)\}\{%\n(.*?)\n\}", SCRIPT, flags=re.S)

    def conv(body: str) -> str:
        srcs = re.findall(r"%\s*source:\s*(.+)", body)
        body = re.sub(r"^\s*%.*$", "", body, flags=re.M)
        body = re.sub(r"\\emph\{(.+?)\}", r"<em>\1</em>", body, flags=re.S)
        body = re.sub(r"\\textit\{(.+?)\}", r"<em>\1</em>", body, flags=re.S)
        body = re.sub(r"\\Cue\{(.+?)\}\s*$", r'<p class="cue">Live cue: \1</p>', body, flags=re.S)
        body = body.replace("\\Pause{}", "<em>[pause]</em>").replace("\\Pause", "<em>[pause]</em>").replace("\\Advance", "<em>[advance]</em>")
        body = body.replace("\\PaperTitle", "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders")
        body = re.sub(r"\$r_([012])\$", lambda m: "r" + "₀₁₂"[int(m.group(1))], body)
        body = body.replace("\\ell", "ℓ").replace("$", "").replace("~", " ").replace("\\&", "&").replace("\\%", "%")
        paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        out = "".join(p if p.startswith("<p") else f"<p>{p}</p>" for p in paras)
        if srcs: out += "<p class=\"small muted\">Number sources in the script: " + html.escape("; ".join(s.strip() for s in srcs)) + "</p>"
        return out
    res = {"f0": {"timing": op.group(1), "html": conv(op.group(2)), "source": "script.tex, Opening"}}
    for fid, title, k in [("f2", "This paper", 0), ("f6", "A stronger incumbent: spread up, profit down", 0),
                          ("f8", "Only good news makes expensive preparation pay", 0), ("a19", "Benchmark scale: declared, not calibrated", 0)]:
        t, b = blocks[title][k]
        res[fid] = {"timing": t, "html": conv(b), "source": f"script.tex, block “{title}”"}
    t1, b1 = blocks["At the benchmark, entry rises from 0.250 to 0.523"][0]
    t2, b2 = blocks["At the benchmark, entry rises from 0.250 to 0.523"][1]
    res["f10"] = {"timing": f"{t1}, then {t2} after the build", "html": conv(b1) + "<hr>" + conv(b2), "source": "script.tex, both blocks of frame 10"}
    return res


# ----------------------------------------------------------------------------- paper version
def pdf_info(path: Path) -> dict:
    out = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", out).group(1))
    date = re.search(r"CreationDate:\s+(.+)", out).group(1).strip()
    return {"pages": pages, "created": date, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}


def paper_version() -> dict:
    commit = subprocess.run(["git", "-C", str(REPO / "overleaf/paper"), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    v = {
        "source": "Overleaf working copy, overleaf/paper (project 6abd31b3b1fcb8e38afbb670)",
        "text_revision": "Peer-circulation revision, 6 September 2026",
        "overleaf_commit": commit,
        "main": {**pdf_info(REPO / "overleaf/paper/build/main.pdf"), "tex_sha256": hashlib.sha256((REPO / "overleaf/paper/main.tex").read_bytes()).hexdigest(), "file": "assets/main.pdf", "title": "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"},
        "online_appendix": {**pdf_info(REPO / "overleaf/paper/build/online_appendix.pdf"), "tex_sha256": hashlib.sha256((REPO / "overleaf/paper/online_appendix.tex").read_bytes()).hexdigest(), "file": "assets/online_appendix.pdf", "title": "Online Appendix"},
        "peer_release": {"main_sha256": hashlib.sha256((REPO / "peer_release/main.pdf").read_bytes()).hexdigest(), "online_appendix_sha256": hashlib.sha256((REPO / "peer_release/online_appendix.pdf").read_bytes()).hexdigest(), "tex_identical": True},
    }
    v["peer_release"]["tex_identical"] = (hashlib.sha256((REPO / "paper/main_filled.tex").read_bytes()).hexdigest() == v["main"]["tex_sha256"]
                                          and hashlib.sha256((REPO / "paper/online_appendix_filled.tex").read_bytes()).hexdigest() == v["online_appendix"]["tex_sha256"])
    return v


# ----------------------------------------------------------------------------- data.js
def data_js() -> str:
    keys = ["base_h", "base_ell", "base_p", "base_rho", "base_c_low", "base_c_high", "base_b", "base_k", "base_r_weak", "base_r_strong", "base_r_collapse",
            "base_entry_weak", "base_entry_strong", "base_entry_collapse", "base_profit_prior_weak", "base_profit_prior_strong", "base_spread_weak", "base_spread_strong",
            "base_ownership_weak", "base_ownership_strong", "base_entry_change_pp", "base_m", "base_M", "base_margin_strong_trade", "base_minimum_theorem_margin",
            "moderate_h", "moderate_ell", "moderate_p", "moderate_rho", "moderate_c_low", "moderate_c_high", "moderate_b", "moderate_k", "moderate_r_weak", "moderate_r_strong",
            "moderate_entry_weak", "moderate_entry_strong", "moderate_minimum_theorem_margin", "base_frozen_entry_weak", "base_frozen_entry_strong", "base_hidden_entry_weak", "base_hidden_entry_strong"]
    reg = {k: {"display": REG[k]["display"], "value": REG[k]["value"], "status": REG[k]["status"], "source_file": REG[k]["source_file"], "source_row": REG[k]["source_row"]} for k in keys}
    f = DATA["fig1"]
    payload = {"inputs": DATA["inputs"], "registry": reg, "fig1": {"r": f["r"], "Delta_T": f["Delta_T"], "B": f["B"], "mu_label": f["mu_label"]},
               "frames": frames(), "parts": PARTS,
               "meta": {"registry_sha256_prefix": DATA["meta"]["registry_hash"][:12], "sources": DATA["meta"]["sources"], "two_returns_rows": len(f["r"])}}
    return "window.CCC_DATA=" + json.dumps(payload, separators=(",", ":")) + ";\n"


# ----------------------------------------------------------------------------- fonts
UNICODE = {
    "latin": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
    "latin-ext": "U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF",
    "greek": "U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF",
}
FAMILIES = {
    "source-serif-4": {"name": "Source Serif 4", "variable": True, "range": "200 900", "styles": ["normal", "italic"]},
    "source-sans-3": {"name": "Source Sans 3", "variable": True, "range": "200 900", "styles": ["normal", "italic"]},
    "stix-two-text": {"name": "STIX Two Text", "variable": True, "range": "400 700", "styles": ["normal", "italic"]},
    "ibm-plex-sans": {"name": "IBM Plex Sans", "variable": False, "weights": [("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal")]},
    "ibm-plex-mono": {"name": "IBM Plex Mono", "variable": False, "weights": [("400", "normal"), ("500", "normal")]},
    "libertinus-serif": {"name": "Libertinus Serif", "variable": False, "weights": [("400", "normal"), ("400", "italic"), ("600", "normal"), ("700", "normal")]},
    "libertinus-sans": {"name": "Libertinus Sans", "variable": False, "weights": [("400", "normal"), ("400", "italic"), ("700", "normal")]},
    "inter": {"name": "Inter", "variable": True, "range": "100 900", "styles": ["normal", "italic"]},
    "inter-tight": {"name": "Inter Tight", "variable": True, "range": "100 900", "styles": ["normal", "italic"]},
    "jetbrains-mono": {"name": "JetBrains Mono", "variable": True, "range": "100 800", "styles": ["normal", "italic"]},
    "source-code-pro": {"name": "Source Code Pro", "variable": True, "range": "200 900", "styles": ["normal"]},
    "fira-sans": {"name": "Fira Sans", "variable": False, "weights": [("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal"), ("700", "normal")]},
    "fira-mono": {"name": "Fira Mono", "variable": False, "weights": [("400", "normal"), ("500", "normal"), ("700", "normal")]},
}
SYMBOLS = '"CCC Symbols"'
PAIRINGS = {
    "a": [
        {"id": "a1", "label": "Source Serif 4 + Source Sans 3", "text": "source-serif-4", "ui": "source-sans-3", "num": "source-serif-4", "display": "source-serif-4",
         "why": "One designer's serif and sans; the serif has a tnum feature, Greek and a true italic, and sits well beside KaTeX's Computer Modern."},
        {"id": "a2", "label": "STIX Two Text + IBM Plex Sans", "text": "stix-two-text", "ui": "ibm-plex-sans", "num": "ibm-plex-sans", "display": "stix-two-text",
         "why": "A Times-class face built for scientific text, the nearest to the paper PDF (newtx); Plex Sans gives equal-width digits for labels and tables."},
        {"id": "a3", "label": "Libertinus Serif + Libertinus Sans", "text": "libertinus-serif", "ui": "libertinus-sans", "num": "libertinus-sans", "display": "libertinus-serif",
         "why": "The TeX-world face with a math companion; warm and narrow, Greek and italic; digits are equal width by design."},
    ],
    "b": [
        {"id": "b1", "label": "Inter + JetBrains Mono", "text": "inter", "ui": "inter", "num": "jetbrains-mono", "display": "inter",
         "why": "A screen sans with tnum, Greek and an italic; the mono face carries every number and key so statistics line up."},
        {"id": "b2", "label": "IBM Plex Sans + IBM Plex Mono", "text": "ibm-plex-sans", "ui": "ibm-plex-sans", "num": "ibm-plex-mono", "display": "ibm-plex-sans",
         "why": "One family across sans and mono, drawn for data displays; digits are equal width by default; the mono subset has no Greek, so Greek stays in the sans."},
        {"id": "b3", "label": "Source Sans 3 + Source Code Pro", "text": "source-sans-3", "ui": "source-sans-3", "num": "source-code-pro", "display": "source-sans-3",
         "why": "A humanist sans that holds at 14 px; Greek included; the code face is quieter than JetBrains Mono at projector size."},
    ],
    "c": [
        {"id": "c1", "label": "Fira Sans + Fira Mono", "text": "fira-sans", "ui": "fira-sans", "num": "fira-mono", "display": "fira-sans",
         "why": "The Beamer deck's own face, so the web deck and the PDF deck are one family; tnum, Greek, italic; Fira Mono for numbers."},
        {"id": "c2", "label": "Inter Tight + Inter + JetBrains Mono", "text": "inter", "ui": "inter", "num": "jetbrains-mono", "display": "inter-tight",
         "why": "A tighter display cut for titles over the same text face; a grotesque feel near the UCL brand sans without a non-OFL font."},
        {"id": "c3", "label": "Source Serif 4 (titles) + Fira Sans + Fira Mono", "text": "fira-sans", "ui": "fira-sans", "num": "fira-mono", "display": "source-serif-4",
         "why": "Serif titles echo the deck's serif math; Fira Sans text keeps the PDF link; the serif has tnum for the title-slide numbers."},
    ],
}


def font_files(fam: str) -> list:
    return sorted(p for p in FONTS.glob(f"{fam}-*.woff2"))


def fonts_css(direction: str) -> str:
    fams = sorted({f for p in PAIRINGS[direction] for f in (p["text"], p["ui"], p["num"], p["display"])})
    css = []
    for fam in fams:
        spec = FAMILIES[fam]
        for p in font_files(fam):
            m = re.match(rf"{fam}-(latin-ext|latin|greek)-(wght|\d+)-(normal|italic)\.woff2", p.name)
            if not m: continue
            subset, weight, style = m.groups()
            w = spec["range"] if weight == "wght" else weight
            css.append(f'@font-face{{font-family:"{spec["name"]}";font-style:{style};font-weight:{w};font-display:swap;src:url("fonts/{p.name}") format("woff2");unicode-range:{UNICODE[subset]};}}')
    css.append(f'@font-face{{font-family:{SYMBOLS};font-style:normal;font-weight:400;font-display:swap;src:url("vendor/fonts/KaTeX_Main-Regular.woff2") format("woff2");unicode-range:U+2190-2193, U+2208, U+221E, U+2248, U+2264-2265;}}')
    for p in PAIRINGS[direction]:
        n = lambda k: f'"{FAMILIES[p[k]]["name"]}"'
        css.append(f'html[data-pairing="{p["id"]}"]{{--font-text:{n("text")}, {SYMBOLS}, Georgia, serif;--font-ui:{n("ui")}, {SYMBOLS}, Arial, sans-serif;--font-num:{n("num")}, {SYMBOLS}, monospace;--font-display:{n("display")}, {SYMBOLS}, serif;}}')
    return "\n".join(css) + "\n"


def copy_fonts(direction: str, out: Path):
    fams = sorted({f for p in PAIRINGS[direction] for f in (p["text"], p["ui"], p["num"], p["display"])})
    (out / "fonts").mkdir(parents=True, exist_ok=True)
    manifest = json.loads((FONTS / "manifest.json").read_text())
    lock = {}
    for fam in fams:
        for p in font_files(fam):
            if not re.match(rf"{fam}-(latin-ext|latin|greek)-", p.name): continue
            shutil.copy2(p, out / "fonts" / p.name)
            m = manifest["fetched"][p.name]
            lock[p.name] = {"family": FAMILIES[fam]["name"], "package": m["package"], "package_version": m["package_version"], "font_version": m["version"], "license": m["license"], "sha256": m["sha256"], "bytes": m["bytes"]}
        lic = FONTS / f"{fam}-LICENSE.txt"
        if lic.exists(): shutil.copy2(lic, out / "fonts" / lic.name)
    lock["KaTeX_Main-Regular.woff2 (CCC Symbols fallback)"] = {"family": "KaTeX_Main", "package": "KaTeX 0.18.5 (presentation/vendor)", "license": "MIT (code) / SIL OFL 1.1 (fonts)", "sha256": hashlib.sha256((REPO / "presentation/vendor/fonts/KaTeX_Main-Regular.woff2").read_bytes()).hexdigest()}
    (out / "fonts" / "fonts.lock.json").write_text(json.dumps(lock, indent=1))


# ----------------------------------------------------------------------------- html pieces
def pairing_switcher(direction: str, kind: str) -> str:
    btns = "".join(f'<button type="button" data-pairing-choice="{p["id"]}" aria-pressed="false" title="{html.escape(p["why"])}">{html.escape(p["label"])}</button>' for p in PAIRINGS[direction])
    why = "" if kind == "deck" else '<p class="pairing-why small muted" data-pairing-why aria-live="polite"></p>'
    return f'<div class="pairings" role="group" aria-label="Type pairing">{btns}</div>{why}'


def tabs(direction: str) -> str:
    return ('<div class="tabs" role="tablist" aria-label="Site sections">'
            '<a role="tab" data-tab="brief" href="#" aria-selected="true">Research brief</a>'
            '<a role="tab" data-tab="paper" href="#tab-paper" aria-selected="false">Read the paper</a>'
            '<a role="tab" data-tab="talk" href="#tab-talk" aria-selected="false">Seminar talk</a></div>')


def paper_panel(v: dict) -> str:
    def card(key, label):
        d = v[key]
        return (f'<article class="pdf-card"><h3>{html.escape(label)}</h3><p class="meta"><span class="num">{d["pages"]} pages</span> · <span class="num">{d["bytes"]//1024} KB</span> · PDF built {html.escape(d["created"])}</p>'
                f'<p class="hash"><span class="muted">sha256</span> <code>{d["sha256"]}</code></p>'
                f'<p class="actions"><a class="button primary" href="{d["file"]}" download>Download PDF</a> <a class="button" href="{d["file"]}" target="_blank" rel="noopener">Open in a new tab</a></p></article>')
    strip_main = "".join(f'<a href="assets/main.pdf#page={i}" target="_blank" rel="noopener"><img src="assets/pages/main-{i:02d}.jpg" alt="Page {i} of the manuscript" loading="lazy"></a>' for i in range(1, 9))
    strip_oa = "".join(f'<a href="assets/online_appendix.pdf#page={i}" target="_blank" rel="noopener"><img src="assets/pages/oa-{i:02d}.jpg" alt="Page {i} of the online appendix" loading="lazy"></a>' for i in range(1, 5))
    same = "identical" if v["peer_release"]["tex_identical"] else "different"
    return f'''
<div class="paper-head">
  <p class="kicker">Newest polished draft</p>
  <h2>Read the paper</h2>
  <p class="stamp" data-version-stamp>Source: {html.escape(v["source"])}. Text: {html.escape(v["text_revision"])}. PDF built {html.escape(v["main"]["created"])} (Overleaf commit <code>{v["overleaf_commit"]}</code>). {v["main"]["pages"]} + {v["online_appendix"]["pages"]} pages.</p>
</div>
<div class="pdf-cards">{card("main", "Manuscript")}{card("online_appendix", "Online appendix")}</div>
<h3>Page preview</h3>
<div class="page-strip" aria-label="Manuscript pages 1 to 8">{strip_main}</div>
<div class="page-strip" aria-label="Online appendix pages 1 to 4">{strip_oa}</div>
<h3>Inline viewer</h3>
<div class="viewer" data-viewer data-src="assets/main.pdf"></div>
<details class="fold"><summary>How this tab stays in step with the draft</summary>
<ol>
<li>A build step reads the chosen PDF pair and writes <code>assets/paper-version.js</code>: path, sha256, page count, PDF date, the sha256 of the <code>.tex</code> source and the Overleaf commit. Nothing on this tab is typed by hand.</li>
<li>The page renders the stamp, the cards and the page strip from that file.</li>
<li>The display check asserts that the copied PDF bytes hash to the recorded values and that the page counts match. A stale copy fails the build.</li>
<li>Today the <code>.tex</code> text is {same} to the peer-circulation revision of 6 September 2026 (main sha256 <code>{v["peer_release"]["main_sha256"][:12]}…</code>, appendix <code>{v["peer_release"]["online_appendix_sha256"][:12]}…</code>). Only the PDF bytes and the build date differ.</li>
</ol>
<pre class="small"><code>{html.escape(json.dumps({k: v[k] for k in ("source", "text_revision", "overleaf_commit")} | {"main": {k: v["main"][k] for k in ("pages", "created", "sha256", "tex_sha256")}, "online_appendix": {k: v["online_appendix"][k] for k in ("pages", "created", "sha256", "tex_sha256")}}, indent=1))}</code></pre>
</details>'''


def talk_panel() -> str:
    return ('<div class="paper-head"><p class="kicker">Interactive slides</p><h2>Seminar talk</h2>'
            '<p>The web deck carries all 47 frames of the Beamer deck in the same order and numbering. Open the mini-deck of this direction: <a class="button primary" href="slides.html">Open slides.html</a></p>'
            '<p class="muted">The published deck lives at /talk/. This mockup builds six of the frames; the overview inside it lists all 47.</p></div>')


def handout_html(direction: str, v: dict, op: dict, mech: str) -> str:
    d = direction
    skin = {"a": "Direction A · Journal", "b": "Direction B · Instrument", "c": "Direction C · UCL family"}[d]
    toc = ('<nav class="toc" id="toc" aria-label="Contents"><p class="kicker">Contents</p><ol class="toc-list">'
           '<li><a href="#sec-setting">Inside a takeover process</a></li><li><a href="#sec-mechanism" aria-current="true">Two returns to information</a></li>'
           '<li><a href="#sec-evidence">What the paper establishes</a></li><li><a href="#sec-implications">Implications and next steps</a></li></ol>'
           '<p class="legend"><span class="st st-analytical">analytical</span><span class="st st-computer">computer-assisted</span><span class="st st-diag">numerical diagnostic</span><span class="st st-open">open</span><span class="st st-input">input</span></p></nav>')
    controls = (f'<div class="controls"><button type="button" data-theme-toggle aria-pressed="false">Dark</button>{pairing_switcher(d, "handout")}</div>')
    status = (f'<p class="status-line"><span>Text revised 6 September 2026</span><span class="dot">·</span><span>PDF built 30 September 2026</span><span class="dot">·</span><span>Reading time 10–15 minutes</span><span class="dot">·</span><span>Theory working paper</span></p>')
    masthead = f'''
<header class="masthead">
  <div class="masthead-inner">
    <p class="mock-label">Mockup · {skin}</p>
    {status}
    <h1>Competition creates competition</h1>
    <p class="subtitle">Stock prices and the discovery of takeover bidders</p>
    <p class="byline">Austin Li · UCL School of Management</p>
    {tabs(d)}
    {controls}
  </div>
</header>'''
    brief = f'''
<div class="layout" role="tabpanel" data-tab="brief">
  {toc}
  <main id="main" tabindex="-1">
    <aside class="opening-question" aria-label="Research question and contribution">{op["aside"]}</aside>
    {stub("setting", "Inside a takeover process", "1 · The setting · 2–3 minutes")}
    <section class="sec" id="sec-mechanism">{mech}</section>
    {stub("evidence", "What the paper establishes", "3 · The result · 4 minutes")}
    {stub("implications", "Implications and next steps", "4 · Implications · 2–3 minutes")}
  </main>
</div>'''
    paper = f'<div class="layout paper" role="tabpanel" data-tab="paper" hidden><main class="paper-main">{paper_panel(v)}</main></div>'
    talk = f'<div class="layout paper" role="tabpanel" data-tab="talk" hidden><main class="paper-main">{talk_panel()}</main></div>'
    foot = f'''
<footer class="colophon">
  <p><a href="assets/main.pdf">Manuscript (PDF)</a><span class="dot">·</span><a href="assets/online_appendix.pdf">Online appendix (PDF)</a><span class="dot">·</span><a href="slides.html">Seminar talk (slides)</a></p>
  <p>Theory working paper · Text: peer-circulation revision, 6 September 2026 · PDF built 30 September 2026 from the Overleaf working copy.</p>
  <details class="fold"><summary>Sources and reproducibility</summary>
  <p>Figures use the paper's validated figure data (figures_data/two_returns.csv, {DATA["meta"]["sources"]["figures_data/two_returns.csv"][:12]}) and the release registry ({DATA["meta"]["registry_hash"][:12]}). Scalars keep their registry key, status and source on hover. The explorer slot is a fixed-order calculation, not an equilibrium solver.</p>
  <p>Type: self-hosted woff2 subsets, SIL Open Font License; see fonts/fonts.lock.json. Mathematics: KaTeX 0.18.5, local copy. No network request is made by this page.</p>
  </details>
</footer>'''
    return f'''<!doctype html>
<html lang="en" data-theme="{'dark' if d == 'b' else 'light'}" data-dir="dir-{d}" data-pairing="{PAIRINGS[d][0]["id"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Competition Creates Competition · {skin}</title>
<meta name="description" content="Research brief mockup: when can a stronger takeover bidder draw a second buyer into the sale?">
<link rel="icon" href="data:,">
<link rel="stylesheet" href="vendor/katex.min.css">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="skin.css">
<script>window.__errors=[];window.addEventListener('error',function(e){{window.__errors.push(String(e.message));}});</script>
</head>
<body class="handout">
<a class="skip-link" href="#main">Skip to the brief</a>
<div class="progress" data-progress aria-hidden="true"></div>
{masthead}
{brief}
{paper}
{talk}
{foot}
<noscript><p class="noscript">This page needs JavaScript for the rendered mathematics and the interactive figure. The prose is readable without it.</p></noscript>
<script src="assets/data.js"></script>
<script src="assets/paper-version.js"></script>
<script src="vendor/katex.min.js"></script>
<script src="closed.js"></script>
<script src="charts.js"></script>
<script src="handout.js"></script>
</body>
</html>'''


# ----------------------------------------------------------------------------- slides
def tex(s: str, display: bool = False) -> str:
    return f'<span class="tex" data-tex="{html.escape(s)}"{" data-display=\"true\"" if display else ""}></span>'


def slides_body() -> str:
    P = DATA["inputs"]
    f0 = f'''
<section class="slide title" id="f0" data-num="0" data-part="1" data-title="Title" data-minutes="0.25">
  <div class="slide-body">
    <p class="kicker">Austin Li · Department of Economics · University College London</p>
    <h1>Competition Creates Competition:<br>Stock Prices and the Discovery of Takeover Bidders</h1>
    <p class="hint">→ or Space to advance · O overview · N notes · T theme · ? help</p>
  </div>
</section>'''
    f2 = f'''
<section class="slide" id="f2" data-num="2" data-part="1" data-title="This paper" data-minutes="2.0">
  <header class="slide-head"><h2>This paper</h2></header>
  <div class="slide-body">
    <p class="lead">An informed investor trades the target's stock, which pays off from the sale price, before a challenger decides whether to pay to prepare a takeover bid; prices are rational, and trading and entry are solved in equilibrium.</p>
    <ul class="claims">
      <li data-step="0" class="shown"><span class="keyidea">Competition creates competition</span>: a stronger incumbent can turn an uninformative stock price into an informative one and raise entry
        <p class="bench">Benchmark: entry <b>{R("base_entry_weak", "0.250")} → {R("base_entry_strong", "0.523")}</b> while the challenger's profit before any news falls <b>{R("base_profit_prior_weak", "4.80")} → {R("base_profit_prior_strong", "4.29")}</b> <span class="st st-analytical">analytical</span></p></li>
      <li data-step="1"><b>Two possible outcomes of one auction</b>: a strong incumbent can beat a low-value challenger but not a high-value one, so the challenger keeps less while the sale price depends more on who shows up; informed trading puts that into the stock price, and good news justifies expensive preparation</li>
      <li data-step="2"><b>Information is the channel:</b> hold fixed what the price reveals, and a stronger incumbent cannot raise entry, as the textbook says <span class="st st-analytical">sign analytical, Prop. A.3</span></li>
    </ul>
    <p class="takeaway" data-step="3"><b>Implication:</b> when the target trades, a stronger rival is not a pure deterrent, because who competes depends on what the price reveals before anyone prepares.</p>
  </div>
  <footer class="slide-foot"><span class="source">Proposition 2; Proposition A.3</span></footer>
</section>'''
    f6 = f'''
<section class="slide" id="f6" data-num="6" data-part="3" data-title="A stronger incumbent: spread up, profit down" data-minutes="1.5">
  <header class="slide-head"><h2>A stronger incumbent: spread up, profit down</h2>
    <p class="sub">Declared benchmark; weak {tex("r_0=1.2")}, strong {tex("r_1=3")}; auction-stage payoffs, before trading and entry</p></header>
  <div class="slide-body">
    <div class="figure" id="x1" tabindex="0" aria-label="Figure X1, interactive. Arrow keys move the cursor."></div>
    <p class="stamp-line"><span class="st st-analytical">analytical (Proposition 1)</span> <span class="muted">Rebuilt from figures_data/two_returns.csv ({DATA["meta"]["sources"]["figures_data/two_returns.csv"][:12]})</span></p>
    <p class="takeaway">From {tex("r_0")} to {tex("r_1")} the <span class="info">spread</span> rises {R("base_spread_weak", "0.0167")} → {R("base_spread_strong", "0.667")} while profit at the prior (before any news) falls {R("base_profit_prior_weak", "4.80")} → {R("base_profit_prior_strong", "4.29")}: deterrence at every fixed belief, and more for the stock to reveal.</p>
  </div>
  <footer class="slide-foot"><span class="source">Proposition 1; figures_data/two_returns.csv</span></footer>
</section>'''
    f8 = f'''
<section class="slide" id="f8" data-num="8" data-part="4" data-title="Only good news makes expensive preparation pay" data-minutes="2.25">
  <header class="slide-head"><h2>Only good news makes expensive preparation pay</h2>
    <p class="sub">{tex(r"B_r(\mu)=g_L+\mu(g_H-g_L)")} at the worst, prior and best belief a price induces; {tex("c_L=1")} (prob. {tex(r"\rho=0.25")}), {tex("c_H=6")}</p></header>
  <div class="slide-body split">
    <div class="col">
      <div class="figure" id="x2" aria-label="Figure X2"></div>
      <div class="slider"><label for="x2-r">incumbent strength r</label><input type="range" id="x2-r" min="1.05" max="3.8" step="0.01" value="3"><output id="x2-r-value">3.00</output></div>
      <div id="x2-readout" class="readout"></div>
    </div>
    <div class="col text">
      <p data-step="0" class="shown"><span class="cost"><b>Low-cost floor</b></span> {tex("c_L<B_{r_1}(m)")}: a cheap challenger enters after any price, so entry {tex(r"\ge\rho")} (the bound used on the previous frame)</p>
      <p data-step="1"><span class="cost"><b>High-cost window</b></span> {tex("B_{r_0}(1/2)=4.80<c_H=6<B_{r_1}(M)")}: the expensive challenger stays out at the weak prior and enters after the best news against {tex("r_1")}. Beyond a ceiling strength, even the best price falls short ({tex("r_2")})</p>
      <p class="stamp-line"><span class="st st-analytical">analytical (Props. A.1, A.2, A.4); costs are inputs</span></p>
      <p class="nav"><button type="button" class="goto" disabled title="Not built in this mockup">Reading the price</button> <button type="button" class="goto" disabled title="Not built in this mockup">Why Laplace noise</button> <button type="button" class="goto" disabled title="Not built in this mockup">Is the floor doing the work?</button></p>
    </div>
  </div>
  <footer class="slide-foot"><span class="source">Propositions A.1, A.2, A.4; base_c_low, base_c_high, base_rho, base_profit_prior_weak</span></footer>
</section>'''
    f10 = f'''
<section class="slide" id="f10" data-num="10" data-part="6" data-title="At the benchmark, entry rises from 0.250 to 0.523" data-minutes="2.5">
  <header class="slide-head"><h2>At the benchmark, entry rises from {R("base_entry_weak", "0.250")} to {R("base_entry_strong", "0.523")}</h2>
    <p class="sub">Declared benchmark; units arbitrary (inputs in backup); unique equilibrium outcomes (analytical)</p></header>
  <div class="slide-body">
    <p class="small">Entry = Pr(challenger prepares); entry {tex(r"\rho=0.25")} = only the cheap challenger enters; high-value challenger ownership = Pr(high-value challenger acquires the target)</p>
    <table class="t3" id="t3">
      <thead><tr><th></th><th>weak<br>{tex("r_0=1.2")}</th><th class="strong">strong<br>{tex(r"\boldsymbol{{r_1=3}}")}</th><th class="r2">stronger still<br>{tex("r_2=3.6")}</th></tr></thead>
      <tbody>
        <tr><th>Challenger's profit at the prior {tex("B_r(1/2)")}</th><td>{R("base_profit_prior_weak", "4.80")}</td><td class="strong">{R("base_profit_prior_strong", "4.29")}</td><td class="r2 words">lower still</td></tr>
        <tr><th><span class="info">Target-payoff spread {tex(r"\Delta_T")}</span></th><td>{R("base_spread_weak", "0.0167")}</td><td class="strong">{R("base_spread_strong", "0.667")}</td><td class="r2 words">wider still</td></tr>
        <tr><th>Investor orders {tex("(q_H,q_L)")}</th><td>(0, 0)</td><td class="strong">(1, −1)</td><td class="r2">(1, −1)</td></tr>
        <tr><th>Price</th><td>uninformative</td><td class="strong">informative</td><td class="r2">informative</td></tr>
        <tr><th>Entry</th><td>{R("base_entry_weak", "0.250")}</td><td class="strong">{R("base_entry_strong", "0.523")}</td><td class="r2">{R("base_entry_collapse", "0.250")}</td></tr>
        <tr><th>High-value ownership</th><td>{R("base_ownership_weak", "0.125")}</td><td class="strong">{R("base_ownership_strong", "0.324")}</td><td class="r2">{T("tables/table2_equilibrium_controls.tex Panel A", "0.125")}</td></tr>
      </tbody>
    </table>
    <p class="takeaway takeaway-a">Entry rises {R("base_entry_change_pp", "27.28")} percentage points while the challenger's profit at the prior falls: the price, not the prize, brings it in.</p>
    <p class="takeaway takeaway-b" hidden>Rise, then fall: past a ceiling strength even the best price cannot cover {tex("c_H")}.</p>
    <p class="nav" hidden><button type="button" class="goto" data-goto="a19">Benchmark scale</button> <button type="button" class="goto" disabled title="Not built in this mockup">How entry is computed</button> <button type="button" class="goto" disabled title="Not built in this mockup">Which equilibrium?</button></p>
    <div data-step="1" class="build-marker" aria-hidden="true"></div>
  </div>
  <footer class="slide-foot"><span class="source">Table 1, Table 2 Panel A; registry base_* keys on hover</span></footer>
</section>'''
    a19 = f'''
<section class="slide backup" id="a19" data-num="A19" data-part="B" data-backup="true" data-origin="f10" data-title="Benchmark scale: declared, not calibrated">
  <header class="slide-head"><h2>Benchmark scale: declared, not calibrated</h2></header>
  <div class="slide-body split">
    <table class="t-inputs">
      <thead><tr><th>Input</th><th>Benchmark</th><th>Moderate</th></tr></thead>
      <tbody>
        <tr><th>{tex("h")}</th><td>{R("base_h", "10")}</td><td>{R("moderate_h", "2")}</td></tr>
        <tr><th>{tex(r"\ell")}</th><td>{R("base_ell", "1")}</td><td>{R("moderate_ell", "1")}</td></tr>
        <tr><th>{tex("p")}</th><td>{R("base_p", "0.5")}</td><td>{R("moderate_p", "0.5")}</td></tr>
        <tr><th>{tex(r"\rho")}</th><td>{R("base_rho", "0.25")}</td><td>{R("moderate_rho", "0.25")}</td></tr>
        <tr><th>{tex("c_L")}</th><td>{R("base_c_low", "1")}</td><td>{R("moderate_c_low", "0.3")}</td></tr>
        <tr><th>{tex("c_H")}</th><td>{R("base_c_high", "6")}</td><td>{R("moderate_c_high", "0.89")}</td></tr>
        <tr><th>{tex("b")}</th><td>{R("base_b", "2")}</td><td>{R("moderate_b", "2")}</td></tr>
        <tr><th>{tex("k")}</th><td>{R("base_k", "0.02")}</td><td>{R("moderate_k", "0.002")}</td></tr>
      </tbody>
    </table>
    <div class="col">
      <table class="t-outcomes">
        <thead><tr><th></th><th>Benchmark</th><th>Moderate</th></tr></thead>
        <tbody>
          <tr><th>Strengths</th><td>{R("base_r_weak", "1.2")} → {R("base_r_strong", "3")}</td><td>{R("moderate_r_weak", "1.05")} → {R("moderate_r_strong", "1.5")}</td></tr>
          <tr><th>Entry</th><td>{R("base_entry_weak", "0.250")} → {R("base_entry_strong", "0.523")}</td><td>{R("moderate_entry_weak", "0.250")} → {R("moderate_entry_strong", "0.527")}</td></tr>
          <tr><th>Minimum theorem margin</th><td>{R("base_minimum_theorem_margin", "0.00241")}</td><td>{R("moderate_minimum_theorem_margin", "8.01×10⁻⁴", check="8.01e-4")}</td></tr>
        </tbody>
      </table>
      <p class="muted">Units are arbitrary; magnitudes are not calibrated; the signs are the theorem; nonemptiness holds for every {tex(r"h>\ell")} (A17).</p>
      <p class="takeaway">A moderate economy with {tex("h=2")} gives a rise of similar size ({R("moderate_entry_weak", "0.250")} → {R("moderate_entry_strong", "0.527")}), so the benchmark scale is a declaration, not the mechanism.</p>
    </div>
  </div>
  <footer class="slide-foot"><span class="source">Appendix A.8 declarations; registry base_* and moderate_* keys</span><button type="button" class="goto back" data-back>← Back to 10</button></footer>
</section>'''
    return f0 + f2 + f6 + f8 + f10 + a19


def slides_html(direction: str) -> str:
    d = direction
    skin = {"a": "Direction A · Journal", "b": "Direction B · Instrument", "c": "Direction C · UCL family"}[d]
    return f'''<!doctype html>
<html lang="en" data-theme="{'dark' if d == 'b' else 'light'}" data-dir="dir-{d}" data-pairing="{PAIRINGS[d][0]["id"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Competition Creates Competition · slides · {skin}</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="vendor/katex.min.css">
<link rel="stylesheet" href="fonts.css">
<link rel="stylesheet" href="base.css">
<link rel="stylesheet" href="skin.css">
<script>window.__errors=[];window.addEventListener('error',function(e){{window.__errors.push(String(e.message));}});</script>
</head>
<body class="deck">
<a class="skip-link" href="#stage">Skip to the slides</a>
<main id="stage" tabindex="-1" aria-label="Presentation"><div id="deck">{slides_body()}</div></main>
<nav class="hud" aria-label="Presentation tools">
  <span class="mock-label">Mockup · {skin}</span>
  <button type="button" id="overview">Overview</button><button type="button" id="notes">Notes</button><button type="button" data-theme-toggle aria-pressed="false">Projector</button><button type="button" id="fullscreen">Fullscreen</button><button type="button" id="help" aria-label="Controls">?</button>
  {pairing_switcher(d, "deck")}
</nav>
<footer class="rail-bar">
  <ol id="rail" class="rail" aria-label="Parts of the talk"></ol>
  <div class="pager"><button type="button" id="return" hidden>← Back</button><button type="button" id="previous" aria-label="Previous">←</button><span id="counter" class="num"></span><button type="button" id="next" aria-label="Next">→</button><span id="progress-label" class="muted"></span></div>
</footer>
<dialog id="panel"><div class="panel-head"><h2 id="panel-title"></h2><button type="button" id="close-panel">Close</button></div><div id="panel-body"></div></dialog>
<div id="announcer" class="sr-only" aria-live="polite"></div>
<script src="assets/data.js"></script>
<script src="assets/notes.js"></script>
<script src="vendor/katex.min.js"></script>
<script src="closed.js"></script>
<script src="charts.js"></script>
<script src="deck.js"></script>
</body>
</html>'''


# ----------------------------------------------------------------------------- build
def build():
    v = paper_version()
    op = opening()
    mech = port_mechanism()
    nts = notes()
    for d in ("a", "b", "c"):
        out = PROPOSALS / f"direction-{d}"
        if out.exists(): shutil.rmtree(out)
        (out / "assets" / "pages").mkdir(parents=True)
        (out / "vendor" / "fonts").mkdir(parents=True)
        # vendor
        for name in ("katex.min.js", "katex.min.css"):
            shutil.copy2(REPO / "presentation/vendor" / name, out / "vendor" / name)
        for p in (REPO / "presentation/vendor/fonts").glob("*.woff2"):
            shutil.copy2(p, out / "vendor" / "fonts" / p.name)
        shutil.copy2(REPO / "presentation/vendor/licenses/KaTeX-LICENSE.txt", out / "vendor" / "KaTeX-LICENSE.txt")
        # assets
        shutil.copy2(REPO / "overleaf/paper/build/main.pdf", out / "assets" / "main.pdf")
        shutil.copy2(REPO / "overleaf/paper/build/online_appendix.pdf", out / "assets" / "online_appendix.pdf")
        for p in (INPUTS / "pages").glob("*.jpg"):
            shutil.copy2(p, out / "assets" / "pages" / p.name)
        (out / "assets" / "data.js").write_text(data_js(), encoding="utf-8")
        (out / "assets" / "paper-version.js").write_text("window.CCC_PAPER=" + json.dumps(v, indent=1) + ";\n", encoding="utf-8")
        (out / "assets" / "notes.js").write_text("window.CCC_NOTES=" + json.dumps(nts) + ";\n", encoding="utf-8")
        # shared code and styles
        for name in ("closed.js", "charts.js", "handout.js", "deck.js", "base.css"):
            shutil.copy2(SHARED / name, out / name)
        shutil.copy2(SKINS / f"{d}.css", out / "skin.css")
        copy_fonts(d, out)
        (out / "fonts.css").write_text(fonts_css(d), encoding="utf-8")
        (out / "handout.html").write_text(handout_html(d, v, op, mech), encoding="utf-8")
        (out / "slides.html").write_text(slides_html(d), encoding="utf-8")
        print("built", out)


if __name__ == "__main__":
    build()
