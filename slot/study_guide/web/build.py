"""Build the complete HTML study guide from its LaTeX sources.

    python3 slot/study_guide/web/build.py

Requires Pandoc. All runtime assets are local. The PDF guide remains the source of
chapter order and cross-reference numbers; the registry remains the source of values.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GUIDE = HERE.parent
ROOT = HERE.parents[2]
HANDOUT = ROOT / "handout"
OUT = GUIDE / "index.html"
ASSETS = HERE / "assets"

sys.path.insert(0, str(HANDOUT))
import slot_data  # noqa: E402
from diagrams import render_diagram  # noqa: E402

MATH = re.compile(
    r"((?<!\\)\\\(.*?(?<!\\)\\\)|(?<!\\)\\\[.*?(?<!\\)\\\]|"
    r"\\begin\{(?:equation|align|gather|multline)\*?\}.*?"
    r"\\end\{(?:equation|align|gather|multline)\*?\})",
    re.S,
)
MACROS = r"""\newcommand{\E}{\mathbb{E}}
\newcommand{\1}{\mathbf{1}}
\newcommand{\DT}{\Delta_T}
\newcommand{\eu}{\mathrm{e}}
\newcommand{\Ent}{\mathsf{E}}
\newcommand{\Own}{\mathsf{O}}
\newcommand{\lb}{\bar\lambda}
\newcommand{\paper}[1]{\textsf{\small[paper #1]}}
"""
PARTS = {
    "The argument": ("argument", "Part I", "Words, intuition, and symbolic derivations"),
    "The numbers and the graphs": ("numbers", "Part II", "The benchmark and interactive evidence"),
    "The panel": ("panel", "Part III", "Whiteboard derivations and questions"),
    "Appendix": ("appendix", "Appendices", "Verification, parameters, and equation map"),
}
DIAGRAMS = {"fig:01_brief-chain", "fig:02_model-timing", "fig:03_auction-proceeds", "fig:08-map"}
CHARTS = {"fig:08-coexistence", "fig:09-research"}


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def pandoc(text: str, *, shift: int = 0) -> str:
    command = ["pandoc", "-f", "latex", "-t", "html", "--mathjax", "--wrap=none"]
    if shift:
        command.append(f"--shift-heading-level-by={shift}")
    done = subprocess.run(command, input=MACROS + text, text=True, capture_output=True, check=False)
    if done.returncode:
        raise RuntimeError(done.stderr.strip() or "Pandoc failed")
    if done.stderr.strip():
        raise RuntimeError(done.stderr.strip())
    return done.stdout.strip()


def read_aux() -> dict[str, str]:
    labels: dict[str, str] = {}
    aux = GUIDE / "main.aux"
    if not aux.exists():
        raise RuntimeError("slot/study_guide/main.aux is missing; build the PDF guide once with latexmk")
    for line in aux.read_text(encoding="utf-8").splitlines():
        match = re.match(r"\\newlabel\{([^}]+)\}\{\{([^{}]+)\}", line)
        if match and not match.group(1).endswith("@cref"):
            labels[match.group(1)] = match.group(2)
    return labels


def ref_text(label: str, labels: dict[str, str], *, cref: bool, eqref: bool = False) -> str:
    number = labels[label]
    if eqref:
        return f"({number})"
    if not cref:
        return number
    kind = {"sec": "Section", "fig": "Figure", "tab": "Table", "eq": "Equation"}.get(label.split(":", 1)[0], "")
    return f"{kind} {number}".strip()


def resolve_refs(text: str, labels: dict[str, str]) -> str:
    def one(match: re.Match) -> str:
        command, body = match.group(1), match.group(2)
        names = body.split(",")
        values = [ref_text(name.strip(), labels, cref=command == "Cref", eqref=command == "eqref") for name in names]
        if command == "Cref" and len(values) > 1:
            stem = values[0].split(" ", 1)[0] + "s"
            values = [stem + " " + values[0].split(" ", 1)[1]] + [v.split(" ", 1)[-1] for v in values[1:]]
        links = [f'<a href="#{html.escape(name.strip(), quote=True)}">{html.escape(value)}</a>'
                 for name, value in zip(names, values, strict=True)]
        return links[0] if len(links) == 1 else (", ".join(links[:-1]) + " and " + links[-1])

    return re.sub(r"\\(Cref|cref|eqref|ref)\{([^}]+)\}", one, text)


def shown_value(row: dict, in_math: bool) -> str:
    display = row["display"]
    if in_math:
        return re.sub(r"\\ensuremath\{(.*)\}", r"\1", display)
    return display


def resolve_registry(text: str, registry: dict, used: set[str]) -> str:
    def outside(match: re.Match) -> str:
        key = match.group(1)
        row = registry[key]
        used.add(key)
        return (f'<span class="q" data-q="{html.escape(key, quote=True)}" '
                f'data-value="{html.escape(row["value"], quote=True)}" '
                f'title="{html.escape(row["display"] + " | registry " + key + " | " + row["source_script"], quote=True)}">'
                f'{html.escape(shown_value(row, False))}</span>')

    def replace_math(segment: str) -> str:
        def inside(match: re.Match) -> str:
            key = match.group(1)
            used.add(key)
            return shown_value(registry[key], True)
        return re.sub(r"\\reg\{([^}]+)\}", inside, segment)

    pieces = MATH.split(text)
    for index, piece in enumerate(pieces):
        if index % 2:
            pieces[index] = replace_math(piece)
        else:
            pieces[index] = re.sub(r"\\reg\{([^}]+)\}", outside, piece)
    return "".join(pieces)


def normalize_boxes(text: str, box_types: list[tuple[str, str]]) -> str:
    pattern = re.compile(r"\\begin\{(intuition|panelnote|resultbox|caution)\}(?:\[([^]]*)\])?")

    def opening(match: re.Match) -> str:
        kind, title = match.group(1), match.group(2)
        box_types.append((kind, title or ""))
        name = {"intuition": "Intuition", "panelnote": "Panel note", "resultbox": "Result", "caution": "Caution"}[kind]
        heading = name + (f": {title}" if title else "")
        return "\\begin{quote}\\textbf{" + heading + "}\n"

    text = pattern.sub(opening, text)
    return re.sub(r"\\end\{(?:intuition|panelnote|resultbox|caution)\}", r"\\end{quote}", text)


def extract_exhibits(text: str, exhibits: dict[str, dict]) -> str:
    pattern = re.compile(r"\\begin\{figure\}(?:\[[^]]*\])?([\s\S]*?)\\end\{figure\}")

    def replace(match: re.Match) -> str:
        body = match.group(1)
        label_match = re.search(r"\\label\{([^}]+)\}", body)
        caption_match = re.search(r"\\caption\{([\s\S]*?)\}\s*\\label\{", body)
        if not label_match or not caption_match:
            raise RuntimeError("A figure lacks a caption or label")
        label = label_match.group(1)
        if label not in DIAGRAMS | CHARTS:
            raise RuntimeError(f"No web exhibit is defined for {label}")
        token = f"@@EXHIBIT-{len(exhibits)}@@"
        exhibits[token] = {"label": label, "caption": caption_match.group(1)}
        return "\n" + token + "\n"

    return pattern.sub(replace, text)


def prepare(text: str, registry: dict, labels: dict, used: set[str], exhibits: dict[str, dict],
            box_types: list[tuple[str, str]]) -> str:
    text = strip_comments(text)
    text = extract_exhibits(text, exhibits)
    text = text.replace(r"\begin{tabularx}{\linewidth}", r"\begin{tabular}")
    text = text.replace(r"\begin{tabularx}{\textwidth}", r"\begin{tabular}")
    text = text.replace(r"\end{tabularx}", r"\end{tabular}")
    text = re.sub(r"@\{[^}]*\}", "", text)
    text = re.sub(r">\{\\bfseries\}", "", text)
    text = re.sub(r"\bX(?=\})", "l", text)
    text = normalize_boxes(text, box_types)
    text = resolve_registry(text, registry, used)
    text = resolve_refs(text, labels)
    pieces = MATH.split(text)
    for index, piece in enumerate(pieces):
        if index % 2:
            pieces[index] = re.sub(r"\\label\{([^}]+)\}",
                                   lambda m: rf"\tag{{{labels[m.group(1)]}}}\htmlId{{{m.group(1)}}}{{}}", piece)
    text = "".join(pieces)
    text = re.sub(r"\\(?:centering|small|footnotesize|large|LARGE|bfseries|raggedright)\b", "", text)
    text = re.sub(r"\\(?:vspace|smallskip|medskip|bigskip)(?:\{[^}]*\})?", "", text)
    text = re.sub(r"\\(?:toprule|midrule|bottomrule)", "", text)
    text = text.replace("~", " ").replace("--", "-")
    return text


def restore_generated_html(fragment: str) -> str:
    fragment = re.sub(r'&lt;(span class="q"[\s\S]*?)&gt;', r'<\1>', fragment)
    fragment = fragment.replace("&lt;/span&gt;", "</span>")
    fragment = re.sub(r'&lt;a href="([^"]+)"&gt;([\s\S]*?)&lt;/a&gt;', r'<a href="\1">\2</a>', fragment)
    fragment = re.sub(r'(<span class="q"[^>]*>(?![^<]*</span>)[^<]+)', r'\1</span>', fragment)
    def equation_anchor(match: re.Match) -> str:
        identifier = re.search(r"\\htmlId\{([^}]+)\}\{\}", match.group(1))
        return (f'<span class="math display" id="{identifier.group(1)}">{match.group(1)}'
                if identifier else match.group(0))
    return re.sub(r'<span class="math display">(\\\[[\s\S]*?\\\]</span>)', equation_anchor, fragment)


def apply_boxes(fragment: str, box_types: list[tuple[str, str]]) -> str:
    pieces = re.split(r"(</?blockquote>)", fragment)
    index = 0
    out: list[str] = []
    for piece in pieces:
        if piece == "<blockquote>":
            kind, title = box_types[index]
            index += 1
            out.append(f'<aside class="note note-{kind}">')
        elif piece == "</blockquote>":
            out.append("</aside>")
        else:
            out.append(piece)
    if index != len(box_types):
        raise RuntimeError(f"Box conversion mismatch: {index} of {len(box_types)}")
    return "".join(out)


def strip_paragraph(fragment: str) -> str:
    return re.sub(r"^<p>([\s\S]*)</p>$", r"\1", fragment.strip())


def chart_exhibit(label: str, caption: str) -> str:
    if label == "fig:08-coexistence":
        return (f'<figure class="explorer-shell" id="{label}"><div id="explorer" data-explorer></div>'
                f'<figcaption><strong>Equilibrium entry.</strong> {caption}</figcaption></figure>')
    return (f'<figure class="chart" data-chart="research" tabindex="0" id="{label}">'
            '<div class="chart-mount" id="chart-research" role="img" '
            'aria-label="Research intensity and entry along the research branch"></div>'
            f'<figcaption><strong>Research and entry.</strong> {caption}</figcaption></figure>')


def additional_chart(kind: str) -> str:
    if kind == "payoffs":
        return ('<figure class="chart" data-chart="payoffs" tabindex="0" id="fig:benchmark-payoffs">'
                '<div class="chart-mount" id="chart-payoffs" role="img" aria-label="Target-payoff spread and gross profit against incumbent strength"></div>'
                '<figcaption><strong>The two returns.</strong> Panel (a) shows the target-payoff spread against the trading cost. '
                'Panel (b) shows gross profit at three beliefs against the high preparation cost. The curves evaluate the symbolic formulas at the benchmark.</figcaption></figure>')
    return ('<figure class="chart" data-chart="beliefs" tabindex="0" id="fig:benchmark-beliefs">'
            '<div class="chart-mount" id="chart-beliefs" role="img" aria-label="Preparation threshold and posterior bounds against incumbent strength"></div>'
            '<figcaption><strong>Beliefs and the entry ceiling.</strong> The threshold rises with incumbent strength while the posterior bounds stay fixed. '
            'A purchase recruits only where the top posterior reaches the threshold.</figcaption></figure>')


def convert_chapter(path: Path, registry: dict, labels: dict, used: set[str]) -> tuple[str, str, str]:
    source = path.read_text(encoding="utf-8")
    if path.name == "benchmark.tex":
        source = source.replace(r"\subsection{Benchmark numbers (Table 1 of the paper)}", "@@PAYOFFS@@\n" + r"\subsection{Benchmark numbers (Table 1 of the paper)}")
        source = source.replace(r"\subsection{The investor's orders at the benchmark}", "@@BELIEFS@@\n" + r"\subsection{The investor's orders at the benchmark}")
    exhibits: dict[str, dict] = {}
    box_types: list[tuple[str, str]] = []
    prepared = prepare(source, registry, labels, used, exhibits, box_types)
    fragment = restore_generated_html(pandoc(prepared, shift=1))
    fragment = apply_boxes(fragment, box_types)
    for token, exhibit in exhibits.items():
        caption = strip_paragraph(restore_generated_html(pandoc(prepare(exhibit["caption"], registry, labels, used, {}, []))))
        label = exhibit["label"]
        if label == "fig:01_brief-chain":
            caption = caption.replace("Blue:", "Orange:").replace("where blue wins", "where the information channel wins")
        rendered = render_diagram(label, caption, registry) if label in DIAGRAMS else chart_exhibit(label, caption)
        fragment = fragment.replace(f"<p>{token}</p>", rendered).replace(token, rendered)
    fragment = fragment.replace("<p>@@PAYOFFS@@</p>", additional_chart("payoffs"))
    fragment = fragment.replace("<p>@@BELIEFS@@</p>", additional_chart("beliefs"))
    fragment = re.sub(r"(<table\b[^>]*>[\s\S]*?</table>)", r'<div class="table-wrap">\1</div>', fragment)
    heading = re.search(r"<h2\b[^>]*id=\"([^\"]+)\"[^>]*>([\s\S]*?)</h2>", fragment)
    if not heading:
        raise RuntimeError(f"{path.name}: no chapter heading")
    chapter_id = heading.group(1)
    title = re.sub(r"<[^>]+>", "", heading.group(2)).strip()
    number = labels.get(chapter_id, "")
    fragment = fragment.replace(heading.group(0), heading.group(0).replace(heading.group(2),
        f'<span class="chapter-number">{html.escape(number)}</span><span>{html.escape(title)}</span>', 1), 1)
    return chapter_id, title, fragment


def font_faces(lock: dict) -> str:
    rules = []
    for name, value in lock.items():
        if value.get("kind") != "face":
            continue
        stretch = f' font-stretch: {value["stretch"]};' if value.get("stretch") else ""
        rules.append(f'@font-face {{ font-family: "{value["family"]}"; font-style: {value["style"]}; '
                     f'font-weight: {value["weight"]};{stretch} font-display: swap; '
                     f'src: url("web/assets/fonts/{name}") format("woff2"); unicode-range: {value["unicode_range"]}; }}')
    return "\n".join(rules)


def copy_assets() -> dict:
    if ASSETS.exists():
        shutil.rmtree(ASSETS)
    (ASSETS / "fonts").mkdir(parents=True)
    (ASSETS / "vendor").mkdir()
    fonts = json.loads((HANDOUT / "fonts.lock.json").read_text(encoding="utf-8"))
    for name, value in fonts.items():
        source = HANDOUT / "fonts" / name
        if hashlib.sha256(source.read_bytes()).hexdigest() != value["sha256"]:
            raise RuntimeError(f"Font hash mismatch: {name}")
        shutil.copy2(source, ASSETS / "fonts" / name)
    vendor = json.loads((HANDOUT / "vendor.lock.json").read_text(encoding="utf-8"))["katex"]["files"]
    for name, value in vendor.items():
        source = HANDOUT / "vendor" / name
        if hashlib.sha256(source.read_bytes()).hexdigest() != value["sha256"]:
            raise RuntimeError(f"KaTeX hash mismatch: {name}")
        target = ASSETS / "vendor" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for name in ("charts.js", "figures.js", "explorer.js"):
        shutil.copy2(HANDOUT / name, ASSETS / name)
    return fonts


def navigation(chapters: list[dict]) -> str:
    out = []
    for part in PARTS.values():
        members = [c for c in chapters if c["part"] == part[0]]
        if not members:
            continue
        out.append(f'<section class="toc-part" data-toc-part="{part[0]}"><h2>{part[1]}</h2><p>{part[2]}</p><ol>')
        for chapter in members:
            out.append(f'<li data-searchable="{html.escape(chapter["title"].lower(), quote=True)}">'
                       f'<a href="#{chapter["id"]}"><span>{html.escape(chapter["number"])}</span>{html.escape(chapter["title"])}</a></li>')
        out.append("</ol></section>")
    return "".join(out)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args()
    if shutil.which("pandoc") is None:
        raise RuntimeError("Pandoc is required")
    registry = slot_data.read_registry(ROOT)
    labels = read_aux()
    fonts = copy_assets()
    main_tex = (GUIDE / "main.tex").read_text(encoding="utf-8")
    tokens = re.findall(r"\\part\{([^}]+)\}|\\appendix|\\input\{chapters/([^}]+)\}", main_tex)
    current_part = ""
    chapters: list[dict] = []
    used: set[str] = set()
    for part_name, chapter_name in tokens:
        if part_name:
            current_part = PARTS[part_name][0]
            continue
        if not chapter_name or chapter_name == "00_front":
            if chapter_name == "00_front":
                continue
            current_part = current_part or "appendix"
        if not chapter_name:
            continue
        if chapter_name == "A_verification":
            current_part = "appendix"
        path = GUIDE / "chapters" / f"{chapter_name}.tex"
        chapter_id, title, fragment = convert_chapter(path, registry, labels, used)
        chapters.append({"id": chapter_id, "title": title, "number": labels[chapter_id], "part": current_part,
                         "file": chapter_name, "html": fragment})
    body = []
    active_part = None
    for index, chapter in enumerate(chapters):
        if chapter["part"] != active_part:
            if active_part is not None:
                body.append("</div>")
            active_part = chapter["part"]
            part = next(p for p in PARTS.values() if p[0] == active_part)
            body.append(f'<div class="part" id="part-{part[0]}" data-part="{part[0]}">'
                        f'<header class="part-heading"><span>{part[1]}</span><p>{part[2]}</p></header>')
        previous_link = (f'<a href="#{chapters[index - 1]["id"]}">Previous: {html.escape(chapters[index - 1]["title"])}</a>'
                         if index else "<span></span>")
        next_link = (f'<a href="#{chapters[index + 1]["id"]}">Next: {html.escape(chapters[index + 1]["title"])}</a>'
                     if index + 1 < len(chapters) else "<span></span>")
        body.append(f'<article class="chapter" id="chapter-{chapter["file"]}" data-chapter="{chapter["id"]}">'
                    f'{chapter["html"]}<nav class="chapter-nav" aria-label="Adjacent chapters">{previous_link}{next_link}</nav></article>')
    if active_part:
        body.append("</div>")
    data = slot_data.build_data(ROOT, registry)
    payload = slot_data.emit_js(data)
    template = (HERE / "template.html").read_text(encoding="utf-8")
    css = (HERE / "style.css").read_text(encoding="utf-8")
    app = (HERE / "app.js").read_text(encoding="utf-8")
    preface = restore_generated_html(pandoc(prepare((GUIDE / "chapters/00_front.tex").read_text(encoding="utf-8"),
                                                    registry, labels, used, {}, [])))
    preface = preface.replace('<div class="minipage">', '<aside class="preface" aria-label="How to use this guide">')
    preface = preface.replace("</div>", "</aside>", 1) if "</div>" in preface else preface + "</aside>"
    preface = preface.replace("Blue boxes give intuition. Orange boxes give notes for the panel. Green boxes state results. Red boxes mark common errors.",
                              "Orange rules give intuition. Dashed rules give panel notes. Heavy rules state results. Red rules mark common errors.")
    replacements = {
        "FONT_PRELOAD": '<link rel="preload" href="web/assets/fonts/stix-two-text-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
        "STYLE": "<style>\n" + font_faces(fonts) + css + "\n</style>",
        "NAVIGATION": navigation(chapters),
        "PREFACE": preface,
        "CONTENT": "\n".join(body),
        "DATA": "<script>window.CCC_DATA = " + payload + ";</script>",
        "APP": "<script>\n" + app + "\n</script>",
        "BUILD_META": (f'{len(chapters)} chapters; {len(used)} registry values; '
                       f'registry sha256 {slot_data.sha256(ROOT)[:12]}'),
    }
    page = template
    for key, value in replacements.items():
        page = page.replace(f"<!-- @@{key}@@ -->", value)
    if "@@" in page:
        raise RuntimeError("Unresolved template marker")
    seen_ids: dict[str, int] = {}
    def unique_id(match: re.Match) -> str:
        identifier = match.group(1)
        seen_ids[identifier] = seen_ids.get(identifier, 0) + 1
        suffix = f"-{seen_ids[identifier]}" if seen_ids[identifier] > 1 else ""
        return f' id="{identifier}{suffix}"'
    page = re.sub(r'\sid="([^"]+)"', unique_id, page)
    output = Path(args.out)
    output.write_text(page, encoding="utf-8")
    print(f"Built {output} ({len(page):,} characters, {len(chapters)} chapters, {len(used)} registry values)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
