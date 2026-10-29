"""Build the offline slides (the /talk/ page) from the order-slot talk and the slot registry.

    python3 presentation/build.py

Steps: read the slot registry (audit/slot_manuscript_2026_10_23/registry/registry.csv); render the
slide records of content.js with presentation/render.mjs (KaTeX at build time; every number is the
registry display of its key, as \\reg{key} prints it in slot/manuscript/slides.tex); compute the
figure curves with presentation/figdata.py; read the speaker notes from the spoken script
slot/manuscript/slides_script.md (one block per main frame; a prepared answer goes to the backup it
names); assemble dist/index.html with the locked faces and the local KaTeX copy of the handout;
record source hashes; then run check_deck.mjs, which compares the deck with slot/manuscript/slides.tex
and the script. Any failure stops the build. Python and Node standard libraries only.
"""
from __future__ import annotations

import base64
import csv
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import figdata  # noqa: E402

REGISTRY = ROOT / "audit/slot_manuscript_2026_10_23/registry/registry.csv"
SLIDES_TEX = ROOT / "slot/manuscript/slides.tex"
SCRIPT = ROOT / "slot/manuscript/slides_script.md"
# The parts follow the roadmap line of frame 4: Model, Mechanism and main result, Fixed-information
# control, Extensions and prediction.
PARTS = [(1, "Question"), (2, "Model"), (3, "Mechanism and main result"), (4, "Fixed-information control"),
         (5, "Extensions and prediction"), (6, "Conclusion"), ("B", "Backups")]


def digest(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def read_registry() -> dict[str, dict[str, str]]:
    with REGISTRY.open(newline="", encoding="utf-8") as fh:
        return {r["key"]: {"value": r["value"], "display": r["display"]} for r in csv.DictReader(fh)}


# ------------------------------------------------------------------------------------------------
# Locked static files (the handout's fonts and KaTeX)


def font_faces(lock: dict) -> str:
    """@font-face rules generated from the lock, so the stylesheet cannot drift from the files."""
    rules = []
    for name, v in lock.items():
        if v.get("kind") != "face":
            continue
        data = base64.b64encode((HERE / "fonts" / name).read_bytes()).decode("ascii")
        stretch = f' font-stretch: {v["stretch"]};' if v.get("stretch") else ""
        rules.append(f'@font-face {{ font-family: "{v["family"]}"; font-style: {v["style"]}; font-weight: {v["weight"]};{stretch} '
                     f'font-display: swap; src: url("data:font/woff2;base64,{data}") format("woff2"); unicode-range: {v["unicode_range"]}; }}')
    return "\n".join(rules) + "\n"


def katex_css() -> str:
    """The locked KaTeX stylesheet without the woff and ttf fallbacks, which are not shipped."""
    css = (ROOT / "handout/vendor/katex.min.css").read_text(encoding="utf-8")
    return re.sub(r',url\(fonts/[^)]+\.(?:woff|ttf)\) format\("[^"]+"\)', "", css)


# ------------------------------------------------------------------------------------------------
# Speaker notes from slot/manuscript/slides_script.md


def note_html(body: str) -> str:
    def plain(s: str) -> str:
        s = html.escape(s, quote=False)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
        s = re.sub(r"\$([^$]+)\$", lambda mm: '<span class="tex" data-tex="' + html.escape(mm.group(1).replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")) + '"></span>', s)
        return s
    return "".join(f"<p>{plain(p)}</p>" for p in [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", body) if p.strip()])


def read_notes(frames: list[dict]) -> dict:
    """The spoken text of each main frame (## Title, ## Frame N) with its timing line, and the prepared
    answers (### question — Bn) on the first page of the backup each names; answers that name no backup
    go to the last main frame."""
    text = SCRIPT.read_text(encoding="utf-8")
    notes: dict[str, dict] = {}
    labels = {f["label"] for f in frames}
    last_main = [f["label"] for f in frames if not f.get("backup")][-1]
    answers, _, prepared = text.partition("\n## Prepared answers")
    for block in re.split(r"(?m)^## ", answers)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"(Title|Frame (\d+)) — ", head)
        if not m:
            continue
        label = "S" + (m.group(2) or "0")
        tm = re.match(r"\s*\*([^*]+)\*\s*\n", body)
        timing = tm.group(1).strip() if tm else ""
        notes[label] = {"timing": timing, "html": note_html(body[tm.end():] if tm else body), "source": "slot/manuscript/slides_script.md"}
    for block in re.split(r"(?m)^### ", prepared)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"(.+?)(?: — (B\d+))?\s*$", head.strip())
        question, target = m.group(1), m.group(2) or last_main
        entry = notes.setdefault(target, {"timing": "prepared answer", "html": "", "source": "slot/manuscript/slides_script.md"})
        entry["html"] += f'<p class="cue"><b>Prepared answer: {html.escape(question)}</b></p>' + note_html(body)
    missing = [f["label"] for f in frames if not f.get("backup") and f["label"] not in notes]
    extra = [k for k in notes if k not in labels]
    if missing or extra:
        raise SystemExit(f"slides_script.md: main frames without a block: {missing}; blocks without a frame: {extra}")
    return notes


# ------------------------------------------------------------------------------------------------
# Page assembly


def slide_html(f: dict) -> str:
    plain_title = re.sub(r"\$([^$]*)\$", r"\1", f["title"]) or f["short"]
    attrs = {
        "id": f["id"], "data-label": f["label"], "data-num": f["num"], "data-part": str(f["part"]),
        "data-title": plain_title, "data-minutes": str(f.get("minutes", 0)),
        "data-widget": f.get("widget", ""), "data-targets": " ".join(f.get("targets", [])),
    }
    if f.get("backup"):
        attrs["data-backup"] = "true"
        attrs["data-origin"] = f["origin"]
    attr = " ".join(f'{k}="{html.escape(v)}"' for k, v in attrs.items())
    cls = ("slide" + (" title-slide" if f["id"] == "f0" else "") + (" backup" if f.get("backup") else "")
           + (" nohead" if not f["title"] and f["id"] != "f0" else "") + (" " + f["cls"] if f.get("cls") else ""))
    label = f'{html.escape(f["num"])}. {html.escape(plain_title)}'
    if f["id"] == "f0":
        return f'<section class="{cls}" {attr} aria-label="Title">{f["body"]}</section>'
    foot = (f'<footer class="slide-foot"><span class="foot-title">Competition Creates Competition</span>'
            f'<span class="foot-num">{html.escape(f["num"])}</span></footer>')
    if not f["title"]:
        return f'<section class="{cls}" {attr} aria-label="{label}"><div class="slide-body">{f["body"]}</div>{foot}</section>'
    sub = f'<p class="sub">{f["subtitle"]}</p>' if f.get("subtitle") else ""
    return (f'<section class="{cls}" {attr} aria-label="{label}">'
            f'<header class="slide-head"><h2>{f["titleHtml"]}</h2>{sub}</header>'
            f'<div class="slide-body">{f["body"]}</div>{foot}</section>')


def build() -> None:
    registry = read_registry()
    out = HERE / "dist"
    if out.exists():
        for child in out.iterdir():
            if child.name in ("presentation.pdf",):
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    out.mkdir(exist_ok=True)

    # Fonts: the deck's locked faces, symbol fallback and licences. The brief's locked files also
    # ship under /talk/fonts/ because the publisher stages one shared list for both pages.
    deck_fonts = json.loads((HERE / "fonts.lock.json").read_text())
    brief_fonts = json.loads((ROOT / "handout/fonts.lock.json").read_text())
    (out / "fonts").mkdir()
    for name, entry in deck_fonts.items():
        body = (HERE / "fonts" / name).read_bytes()
        if digest(body) != entry["sha256"]:
            raise ValueError("Font hash mismatch: " + name)
        (out / "fonts" / name).write_bytes(body)
    for name, entry in brief_fonts.items():
        body = (ROOT / "handout/fonts" / name).read_bytes()
        if digest(body) != entry["sha256"]:
            raise ValueError("Font hash mismatch: " + name)
        (out / "fonts" / name).write_bytes(body)
    faces = font_faces(deck_fonts)

    # KaTeX: the handout's locked local copy.
    vendor = json.loads((ROOT / "handout/vendor.lock.json").read_text())
    for rel, entry in vendor["katex"]["files"].items():
        body = (ROOT / "handout/vendor" / rel).read_bytes()
        if digest(body) != entry["sha256"]:
            raise ValueError("KaTeX hash mismatch: " + rel)
        target = out / "vendor" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel == "katex.min.css":
            target.write_text(katex_css(), encoding="utf-8")
        else:
            target.write_bytes(body)

    # Render the slide records; render.mjs resolves every registry key.
    run = subprocess.run(["node", str(HERE / "render.mjs")], input=json.dumps({"registry": registry}),
                         capture_output=True, text=True)
    if run.returncode != 0:
        sys.stderr.write(run.stderr)
        raise SystemExit("Slide rendering failed: a registry key or a formula did not pass.")
    rendered = json.loads(run.stdout)
    frames = rendered["frames"]
    for f in frames:
        f.setdefault("subtitle", "")

    notes = read_notes(frames)
    figures = figdata.build(registry)
    used = {k: registry[k] for k in rendered["used"]}
    # Keys the figures print or place at runtime (frame 14, B3, B12).
    for key in ("rA", "rF_B", "rN", "rJ", "rS_B", "rC_B", "res_rR", "res_rcap", "res_rN", "res_rQ", "res_rC",
                "res_lambda_floor_rQ", "prim_r0", "prim_r1", "prim_r2", "prim_pi", "res_cap", "tau_r1", "tau_r2", "M_half_B",
                "str_r155", "str_r160", "str_r165", "res_lambda_r155", "res_lambda_r160", "res_lambda_r165",
                "res_entry_r155", "res_entry_r160", "res_entry_r165"):
        used[key] = registry[key]
    total = max(int(f["num"]) for f in frames if not f.get("backup"))
    minutes = sum(f["minutes"] for f in frames if not f.get("backup"))
    planned = re.search(r"^Prepared speech: .*$", SCRIPT.read_text(encoding="utf-8"), re.M)
    checkpoints = planned.group(0) if planned else ""

    meta = {
        "frames": [{k: f.get(k) for k in ("id", "label", "num", "part", "minutes", "backup", "origin", "targets", "widget")}
                   | {"title": re.sub(r"\$([^$]*)\$", r"\1", f["title"]) or f["short"]} for f in frames],
        "parts": [{"n": n, "name": name} for n, name in PARTS],
        "notation": rendered["notation"],
        "total": total,
        "minutes": minutes,
        "checkpoints": checkpoints,
    }
    page = (HERE / "template.html").read_text(encoding="utf-8")
    fills = {
        "@@STYLE@@": faces + (HERE / "deck.css").read_text(encoding="utf-8"),
        "@@SLIDES@@": "\n".join(slide_html(f) for f in frames),
        "@@DATA@@": json.dumps({"registry": used, "fig": figures}, ensure_ascii=False, separators=(",", ":")),
        "@@META@@": json.dumps(meta, ensure_ascii=False),
        "@@NOTES@@": json.dumps(notes, ensure_ascii=False),
        "@@CHARTS@@": (HERE / "charts.js").read_text(encoding="utf-8"),
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

    sources = {}
    for name in ("audit/slot_manuscript_2026_10_23/registry/registry.csv", "slot/manuscript/slides.tex",
                 "slot/manuscript/slides_script.md",
                 "presentation/content.js", "presentation/render.mjs", "presentation/figdata.py",
                 "presentation/deck.js", "presentation/deck.css", "presentation/template.html", "presentation/check_deck.mjs",
                 "presentation/charts.js", "presentation/fonts.lock.json", "handout/fonts.lock.json", "handout/vendor.lock.json"):
        sources[name] = digest((ROOT / name).read_bytes())
    (out / "provenance.json").write_text(json.dumps({
        "sources": sources, "frames": len(frames), "registry_keys_used": len(rendered["used"]),
        "numbers_printed": len(rendered["numbers"]),
    }, indent=2) + "\n")

    md = ["# Competition Creates Competition", "",
          f"Speaker notes: {len([f for f in frames if not f.get('backup')])} main frames "
          f"({minutes:g} planned minutes) and {len([f for f in frames if f.get('backup')])} backup pages.", "", checkpoints, ""]
    for f in frames:
        if f["label"] not in notes:
            continue
        n = notes[f["label"]]
        md.append(f"## {f['label']}. {re.sub(r'[$]', '', f['title']) or f['short']}")
        md.append("")
        md.append(f"*{n['timing']}*")
        md.append("")
        md.append(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r'<span class="tex" data-tex="([^"]*)"></span>', lambda m: html.unescape(m.group(1)), n["html"]))).strip())
        md.append("")
    (out / "speaker-notes.md").write_text("\n".join(md), encoding="utf-8")

    check = subprocess.run(["node", str(HERE / "check_deck.mjs")], cwd=ROOT, capture_output=True, text=True)
    sys.stdout.write(check.stdout)
    if check.returncode != 0:
        sys.stderr.write(check.stderr)
        raise SystemExit("The deck differs from slides.tex or breaks the deck contract.")
    print(f"Built {out / 'index.html'} ({len(page):,} characters); {len(frames)} frames; "
          f"{len(rendered['used'])} registry keys, {len(rendered['numbers'])} numbers printed.")


if __name__ == "__main__":
    build()
