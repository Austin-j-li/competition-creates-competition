"""Build the offline slides (the /talk/ page) from talk/talk.tex content and validated data.

    python3 presentation/build.py

Steps: bind the research data through handout/data.py; render the 47 slide records of
content.js with presentation/render.mjs (KaTeX at build time, a registry guard on every number);
read the speaker notes from talk/script.tex; assemble dist/index.html with the locked Fira faces
and the local KaTeX copy of the handout; record source hashes; then run check_deck.mjs, which
compares the deck with talk/talk.tex. Any failure stops the build. Python and Node standard
libraries only.
"""
from __future__ import annotations

import hashlib
import html
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "handout"))
import data  # noqa: E402

_spec = importlib.util.spec_from_file_location("handout_build", ROOT / "handout" / "build.py")
handout_build = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(handout_build)

TABLE_FILES = ("table1_auction_primitives.tex", "table2_equilibrium_controls.tex", "table3_extensions.tex",
               "table4_reserve_comparisons.tex", "table_signal_grid.tex")
PARTS = [(1, "Question"), (2, "Model"), (3, "Two claims"), (4, "Price"), (5, "Theorem"), (6, "Numbers"),
         (7, "Boundaries"), (8, "Close"), ("B", "Backups")]
CHECKPOINTS = ("Checkpoints: frame 3 by 4.75 min; frame 5 by 9.5 min, else skip frame 6 and say its two "
               "numbers on frame 5; frame 9 by 18.5 min, else skip frames 12 and 14; frame 11 by 23.5 min, "
               "else skip frame 15 and give frame 13 as one sentence.")


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


# ------------------------------------------------------------------------------------------------
# Speaker notes from talk/script.tex


def balanced(text: str, i: int) -> tuple[str, int]:
    """The brace group that opens at text[i] == '{'; returns (content, index after it)."""
    assert text[i] == "{"
    depth, j = 0, i
    while True:
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j], j + 1
        j += 1


def note_html(body: str) -> str:
    sources = [s.strip() for s in re.findall(r"%\s*source:\s*(.+)", body)]
    body = re.sub(r"(?m)^\s*%.*$", "", body)
    body = re.sub(r"(?<!\\)%.*$", "", body, flags=re.M)
    cue = ""
    m = re.search(r"\\Cue\{", body)
    if m:
        content, end = balanced(body, m.end() - 1)
        cue = content
        body = body[:m.start()] + body[end:]
    for macro in ("emph", "textit"):
        while True:
            m = re.search(r"\\" + macro + r"\{", body)
            if not m:
                break
            content, end = balanced(body, m.end() - 1)
            body = body[:m.start()] + "<em>" + content + "</em>" + body[end:]

    def plain(s: str) -> str:
        s = s.replace(r"\PaperTitle", "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders")
        s = s.replace(r"\Pause{}", "[pause]").replace(r"\Pause", "[pause]").replace(r"\Advance", "[advance]")
        s = s.replace("~", " ").replace(r"\&", "&amp;").replace(r"\%", "%").replace("``", "“").replace("''", "”")
        s = s.replace("---", "—").replace("--", "–")
        s = re.sub(r"\$([^$]+)\$", lambda mm: '<span class="tex" data-tex="' + html.escape(mm.group(1)) + '"></span>', s)
        return s
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    out = "".join(f"<p>{plain(p)}</p>" for p in paras)
    if cue:
        out += f'<p class="cue"><b>Live cue:</b> {plain(cue)}</p>'
    if sources:
        out += '<p class="note-sources">Number sources in the script: ' + html.escape("; ".join(sources)) + "</p>"
    return out


def read_notes(frames: list[dict]) -> tuple[dict, list[str]]:
    script = (ROOT / "talk" / "script.tex").read_text(encoding="utf-8")
    notes: dict[str, dict] = {}
    m = re.search(r"\\scriptopening\{", script)
    timing, end = balanced(script, m.end() - 1)
    body, _ = balanced(script, end)
    notes["F0"] = {"timing": timing, "html": note_html(body), "source": "talk/script.tex, Opening"}
    mains = [f for f in frames if not f.get("backup")]
    used: set[str] = set()
    for m in re.finditer(r"\\scriptframe\{", script):
        title, i = balanced(script, m.end() - 1)
        timing, i = balanced(script, i)
        body, _ = balanced(script, i)
        backup = re.search(r"\(A(\d+)\)", timing)
        if backup:
            label = "A" + backup.group(1)
        else:
            hit = next((f for f in mains if f["title"] == title and f["label"] not in used), None)
            if hit is None:
                raise SystemExit(f"script.tex block without a frame: {title}")
            label = hit["label"]
        used.add(label)
        notes[label] = {"timing": timing, "html": note_html(body), "source": f"talk/script.tex, block “{title}”"}
    # Backups without a script block fall back to the structure plan (section 9).
    plan = (ROOT / "talk" / "structure-plan.md").read_text(encoding="utf-8")
    fallback = []
    for f in frames:
        if f["label"] in notes:
            continue
        row = re.search(r"^\| " + f["label"] + r" `[^`]+` \| [^|]+ \| ([^|]+) \|", plan, re.M)
        text = html.escape(row.group(1).strip()) if row else ""
        extra = ""
        if f["label"] == "A9":
            q = re.search(r"\\textit\{Why a second-price auction\? What about negotiation\?\}(.*?)\n\n", script, re.S)
            if q:
                extra = note_html(q.group(1))
        notes[f["label"]] = {"timing": "if asked (" + f["label"] + ")", "html": f"<p>{text}</p>" + extra,
                             "source": "talk/structure-plan.md, section 9 (no block in talk/script.tex)"}
        fallback.append(f["label"])
    return notes, fallback


# ------------------------------------------------------------------------------------------------
# Page assembly


def slide_html(f: dict) -> str:
    attrs = {
        "id": f["id"], "data-label": f["label"], "data-num": f["num"], "data-part": str(f["part"]),
        "data-title": re.sub(r"\$([^$]*)\$", r"\1", f["title"]), "data-minutes": str(f.get("minutes", 0)),
        "data-widget": f.get("widget", ""), "data-targets": " ".join(f.get("targets", [])),
    }
    if f.get("backup"):
        attrs["data-backup"] = "true"
        attrs["data-origin"] = f["origin"]
    attr = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
    cls = "slide" + (" title-slide" if f["id"] == "f0" else "") + (" backup" if f.get("backup") else "")
    if f["id"] == "f0":
        return f'<section class="{cls}" {attr} aria-label="Title">{f["body"]}</section>'
    sub = f'<p class="sub">{f["subtitleHtml"]}</p>' if f.get("subtitleHtml") else ""
    return (f'<section class="{cls}" {attr} aria-label="{html.escape(f["num"])}. {html.escape(attrs["data-title"])}">'
            f'<header class="slide-head"><h2>{f["titleHtml"]}</h2>{sub}</header>'
            f'<div class="slide-body">{f["body"]}</div>'
            f'<footer class="slide-foot"><span class="foot-title">Competition Creates Competition</span>'
            f'<span class="foot-num">{html.escape(f["num"])}</span></footer></section>')


def build() -> None:
    research, hashes = data.build_data(ROOT)
    out = HERE / "dist"
    if out.exists():
        for child in out.iterdir():
            if child.name in ("presentation.pdf",):
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    out.mkdir(exist_ok=True)

    # Fonts: the handout's locked Fira faces, symbol fallback and licences.
    fonts = json.loads((ROOT / "handout/fonts.lock.json").read_text())
    (out / "fonts").mkdir()
    for name, entry in fonts.items():
        body = (ROOT / "handout/fonts" / name).read_bytes()
        if digest(body) != entry["sha256"]:
            raise ValueError("Font hash mismatch: " + name)
        (out / "fonts" / name).write_bytes(body)
    faces = handout_build.font_faces(fonts, "fonts/")

    # KaTeX: the handout's locked local copy.
    vendor = json.loads((ROOT / "handout/vendor.lock.json").read_text())
    for rel, entry in vendor["katex"]["files"].items():
        body = (ROOT / "handout/vendor" / rel).read_bytes()
        if digest(body) != entry["sha256"]:
            raise ValueError("KaTeX hash mismatch: " + rel)
        target = out / "vendor" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel == "katex.min.css":
            target.write_text(handout_build.katex_css(vendor), encoding="utf-8")
        else:
            target.write_bytes(body)

    # Render the slide records; render.mjs guards every number.
    tables = {name: (ROOT / "tables" / name).read_text(encoding="utf-8") for name in TABLE_FILES}
    payload = json.dumps({"data": json.loads(data.emit_js(research)), "tables": tables})
    run = subprocess.run(["node", str(HERE / "render.mjs")], input=payload, capture_output=True, text=True)
    if run.returncode != 0:
        sys.stderr.write(run.stderr)
        raise SystemExit("Slide rendering failed: a number, a formula or a status word did not pass.")
    rendered = json.loads(run.stdout)
    frames = rendered["frames"]
    if len(frames) != 47:
        raise SystemExit(f"Expected 47 frames, found {len(frames)}")

    # Subtitles: render through the same helper output (content.js returns HTML already).
    for f in frames:
        f["subtitleHtml"] = f.get("subtitle", "")

    notes, fallback = read_notes(frames)
    for name, rel in handout_build.PDFS.items():
        shutil.copyfile(ROOT / rel, out / name)

    meta = {
        "frames": [{k: f.get(k) for k in ("id", "label", "num", "part", "minutes", "backup", "origin", "targets", "widget")}
                   | {"title": re.sub(r"<[^>]+>", "", f["titleHtml"]) if "katex" not in f["titleHtml"] else re.sub(r"\$([^$]*)\$", r"\1", f["title"])}
                   for f in frames],
        "parts": [{"n": n, "name": name} for n, name in PARTS],
        "notation": rendered["notation"],
        "checkpoints": CHECKPOINTS,
    }
    page = (HERE / "template.html").read_text(encoding="utf-8")
    fills = {
        "@@STYLE@@": faces + (HERE / "deck.css").read_text(encoding="utf-8"),
        "@@SLIDES@@": "\n".join(slide_html(f) for f in frames),
        "@@DATA@@": data.emit_js(research),
        "@@META@@": json.dumps(meta, ensure_ascii=False),
        "@@NOTES@@": json.dumps(notes, ensure_ascii=False),
        "@@CHARTS@@": (ROOT / "handout/charts.js").read_text(encoding="utf-8"),
        "@@FORMULAS@@": (ROOT / "handout/explorer.js").read_text(encoding="utf-8"),
        "@@APP@@": (HERE / "deck.js").read_text(encoding="utf-8"),
    }
    for slot, value in fills.items():
        if "</script" in value and slot not in ("@@SLIDES@@", "@@STYLE@@"):
            raise ValueError("A script slot contains </script: " + slot)
        page = page.replace(slot, value)
    if re.search(r"@@[A-Z]+@@", page):
        raise ValueError("Unresolved build slot")
    if re.search(r'<(?:script|link)\b[^>]*(?:src|href)="(?:https?:)?//', page):
        raise ValueError("The slides must not load anything from the network")
    (out / "index.html").write_text(page, encoding="utf-8")

    sources = dict(hashes)
    for name in ("talk/talk.tex", "talk/script.tex", "talk/structure-plan.md", "presentation/content.js",
                 "presentation/render.mjs", "presentation/deck.js", "presentation/deck.css", "presentation/template.html",
                 "presentation/check_deck.mjs", "handout/charts.js", "handout/explorer.js", "handout/fonts.lock.json",
                 "handout/vendor.lock.json", *("tables/" + t for t in TABLE_FILES)):
        sources[name] = digest((ROOT / name).read_bytes())
    (out / "provenance.json").write_text(json.dumps({
        "sources": sources,
        "frames": len(frames), "numbers_guarded": len(rendered["numbers"]),
        "notes_from_structure_plan": fallback,
        "scope": "Presentation build; existing passed-manifest outputs. No new equilibrium search or research release claim.",
    }, indent=2) + "\n")

    md = ["# Competition Creates Competition", "",
          "Speaker notes, 40-minute session: 18 main frames (F10a and F10b share number 10) and 29 backups.", "", CHECKPOINTS, ""]
    for f in frames:
        n = notes.get(f["label"], {})
        md.append(f"## {f['label']}. {re.sub(r'[$]', '', f['title'])}")
        md.append("")
        md.append(f"*{n.get('timing', '')}* · {n.get('source', '')}")
        md.append("")
        md.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r'<span class="tex" data-tex="([^"]*)"></span>', lambda m: html.unescape(m.group(1)), n.get("html", "")))).strip())
        md.append("")
    (out / "speaker-notes.md").write_text("\n".join(md), encoding="utf-8")

    check = subprocess.run(["node", str(HERE / "check_deck.mjs")], cwd=ROOT, capture_output=True, text=True)
    sys.stdout.write(check.stdout)
    if check.returncode != 0:
        sys.stderr.write(check.stderr)
        raise SystemExit("The deck differs from talk/talk.tex or breaks the deck contract.")
    print(f"Built {out / 'index.html'} ({len(page):,} characters); {len(hashes)} research sources verified; "
          f"{len(frames)} frames; {len(rendered['numbers'])} numbers guarded; notes from the structure plan for {', '.join(fallback)}.")


if __name__ == "__main__":
    build()
