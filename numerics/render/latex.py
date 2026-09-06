"""LaTeX conversion of the filled manuscript and online appendix (deliverable 5).

The filled Markdown copies are generated files. Figure and table positions are marked in the
manuscript by

    <!-- FIGURE 1: figures/two_returns.pdf -->
    > **Figure 1.** Caption text, possibly over several blockquote lines.

and likewise `<!-- TABLE 2: tables/table2_equilibrium_controls.tex -->` with a `> **Table 2.**`
caption. The caption is the author's text and is converted with pandoc before insertion. The
older instruction blockquotes (`> **Figure N placeholder — ...**`) still work as a fallback with
the default captions below. Compilation uses pandoc (citeproc, references.bib) and latexmk.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT  # noqa: E402

FALLBACK_FIGS = {
    2: ("figures/equilibrium_correspondence.pdf",
        r"The equilibrium correspondence at the benchmark primitives. Panel (a): total entry $\mathsf{E}$ against incumbent strength $r$ for every accepted branch. Shaded regions are analytically established uniqueness regions; the gray band marks strengths at which several equilibria were found. Dotted verticals mark $r_N$, $r_U$, and $r_C$. Certified points carry interval enclosures. Panel (b): order magnitudes along the informative branches, with full orders as the boundary."),
    1: ("figures/two_returns.pdf",
        r"Incumbent strength raises the sensitivity of target proceeds while reducing challenger acquisition profit at every displayed belief. Panel (a): $\Delta_T(r)$. Panel (b): $B_r(\mu)$ for $\mu\in\{m,1/2,M\}$. Benchmark primitives; values per target share."),
    3: ("figures/posterior_tail_entry.pdf",
        r"The upper tail of price information under full orders at the strong benchmark strength and scale $b=2$. Panel (a): $\Pr(\mu_X\ge\tau)$ against the threshold distance $M-\tau$. Panel (b): implied total entry. At $M-\tau=0$ the Laplace plateau enters under the tie rule (filled dot) while the logistic mass is zero (open circle)."),
    4: ("figures/bargaining_weight.pdf",
        r"Bargaining and the division of information-sensitive returns in the verifiable-value institution with zero reserve, benchmark $h=10$, $\ell=1$, and uniform incumbents with $r=1.2$ (weak) and $r=3$ (strong). Panel (a): $\Delta_\eta$ against the seller weight $\eta$. Panel (b): challenger profits $G_{H,\eta}$ and $G_{L,\eta}$ on a log scale."),
}
FALLBACK_TABS = {
    1: ("tables/table1_auction_primitives.tex", "Auction primitives at the benchmark specification."),
    2: ("tables/table2_equilibrium_controls.tex", "Equilibrium outcomes, information controls, and gains from access to prices."),
    3: ("tables/table3_extensions.tex", "Extensions and information complementarities."),
    4: ("tables/table4_reserve_comparisons.tex", "Sale terms and discovery."),
}

NEW_MARKER = re.compile(r"^<!-- (FIGURE|TABLE) (\d+): (\S+) -->[ \t]*\n((?:>.*(?:\n|$))+)", re.M)
OLD_MARKER = re.compile(r"^> \*\*(Figure|Table) (\d) placeholder — .*?$", re.M)
CAPTION_PREFIX = re.compile(r"^\*\*(Figure|Table) \d+\.\*\*\s*")

HEADER_META = {
    "documentclass": "article",
    "fontsize": "12pt",
    "geometry": "margin=1in",
    "linestretch": "2",
    "fontfamily": "newtxtext",
    "colorlinks": "true",
    "linkcolor": "paperlink",
    "citecolor": "paperlink",
    "urlcolor": "paperlink",
}
HEADER_INCLUDES = [
    r"\usepackage{amsmath,amssymb,amsthm}",
    r"\usepackage{newtxmath}",
    r"\usepackage{booktabs}",
    r"\usepackage{threeparttable}",
    r"\usepackage{graphicx}",
    r"\usepackage{float}",
    r"\usepackage{pdflscape}",
    r"\usepackage{needspace}",
    r"\usepackage{setspace}",
    r"\usepackage{etoolbox}",
    r"\usepackage[font=small,labelfont=bf,labelsep=period]{caption}",
    r"\usepackage[section]{placeins}",
    r"\definecolor{paperlink}{RGB}{31,59,115}",
    r"\allowdisplaybreaks",
    r"\setlength{\parskip}{0pt}",
    r"\setlength{\parindent}{1.5em}",
    r"\AtBeginEnvironment{CSLReferences}{\interlinepenalty=10000}",
]


def md_to_latex_fragment(md: str) -> str:
    """Convert a caption written in Markdown (with $math$) to a LaTeX fragment."""
    r = subprocess.run(["pandoc", "-f", "markdown+tex_math_dollars", "-t", "latex"], input=md, capture_output=True, text=True, check=True)
    return r.stdout.strip()


def figure_env(num: int, path: str, caption_tex: str, notes_tex: str = "") -> str:
    notes = (r"\par\medskip\begin{minipage}{\linewidth}\footnotesize\singlespacing\noindent "
             + r"\textit{Notes.} " + notes_tex + r"\end{minipage}" + "\n") if notes_tex else ""
    return ("```{=latex}\n" + f"\\setcounter{{figure}}{{{num - 1}}}\n" + r"\begin{figure}[tbp]\centering\begingroup\singlespacing" + "\n"
            + f"\\includegraphics[width=\\linewidth]{{{path}}}\n" + f"\\caption{{{caption_tex}}}\\label{{fig:{num}}}\n"
            + notes + r"\endgroup\end{figure}" + "\n```")


def table_env(num: int, path: str, caption_tex: str) -> str:
    return ("```{=latex}\n" + f"\\setcounter{{table}}{{{num - 1}}}\n" + r"\begin{table}[tbp]\begingroup\singlespacing\small\centering" + "\n"
            + f"\\caption{{{caption_tex}}}\\label{{tab:{num}}}\n" + f"\\input{{{path}}}\n" + r"\par\endgroup\end{table}" + "\n```")


def replace_markers(text: str) -> str:
    def new_repl(m: re.Match) -> str:
        kind, num, path, block = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        cap = " ".join(line.lstrip("> ").rstrip() for line in block.strip().splitlines())
        cap = CAPTION_PREFIX.sub("", cap).strip()
        cap, _, notes = cap.partition("**Notes.**")
        cap_tex = md_to_latex_fragment(cap) if cap else ""
        notes_tex = md_to_latex_fragment(notes.strip()) if notes.strip() else ""
        return (figure_env(num, path, cap_tex, notes_tex) if kind == "FIGURE" else table_env(num, path, cap_tex)) + "\n"

    def old_repl(m: re.Match) -> str:
        kind, num = m.group(1), int(m.group(2))
        if kind == "Figure":
            path, cap = FALLBACK_FIGS[num]
            return figure_env(num, path, cap)
        path, cap = FALLBACK_TABS[num]
        return table_env(num, path, cap)

    text = NEW_MARKER.sub(new_repl, text)
    return OLD_MARKER.sub(old_repl, text)


APPENDIX_INCLUDES = [
    # Long numerical schemas wrap; ordinary inline code keeps LaTeX's escaping intact.
    r"\usepackage{fvextra}",
    r"\fvset{breaklines=true,breakanywhere=true}",
    r"\DefineVerbatimEnvironment{verbatim}{Verbatim}{breaklines=true,breakanywhere=true}",
    r"\AtBeginEnvironment{longtable}{\footnotesize}",
]


def build_front_matter(existing: str, overrides: dict | None = None, extra_includes: list[str] | None = None) -> str:
    lines = ["---"]
    meta = {**HEADER_META, **(overrides or {})}
    for k, v in meta.items():
        lines.append(f"{k}: {v}")
    lines.append("header-includes:")
    for inc in HEADER_INCLUDES + (extra_includes or []):
        lines.append(f"  - '{inc}'" if "'" not in inc else f'  - "{inc}"')
    if existing.strip():
        lines.append(existing.strip())
    lines.append("---")
    return "\n".join(lines) + "\n"


def convert(md_path: str, tex_path: str, pdf: bool, meta_overrides: dict | None = None,
            extra_includes: list[str] | None = None) -> bool:
    text = (ROOT / md_path).read_text(encoding="utf-8")
    # Reserve room for a formal statement's opening and first conditions.
    text = re.sub(r"(?m)^(?:(#{2,6} [^\n]+\n\n))?(\[?\*\*(?:Proposition|Lemma|Theorem)\s)",
                  lambda match: "```{=latex}\n\\Needspace{" + ("10" if match[1] else "8")
                  + "\\baselineskip}\n```\n\n" + (match[1] or "") + match[2], text)
    text = re.sub(r"(?m)^(\*\*Input declaration:[^\n]+)",
                  lambda match: "```{=latex}\n\\Needspace{5\\baselineskip}\n```\n\n" + match[1], text)
    text = replace_markers(text)
    # cross-document links (main <-> online appendix) become plain text in the compiled PDFs
    text = re.sub(r"\[([^\]]+)\]\((?:online_appendix|main)\.md#[^)]+\)", r"\1", text)
    existing = ""
    if text.startswith("---"):
        end = text.index("\n---", 3)
        existing = text[4:end]
        text = text[end + 4:]
    text = build_front_matter(existing, meta_overrides, extra_includes) + text
    src = ROOT / (tex_path + ".md")
    src.write_text(text, encoding="utf-8")
    cmd = ["pandoc", str(src), "-o", str(ROOT / tex_path), "--standalone", "--citeproc", "--bibliography", str(ROOT / "references.bib"),
           "--resource-path", str(ROOT), "-f", "markdown+tex_math_dollars+raw_attribute", "--shift-heading-level-by=-1"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr)
        return False
    if pdf:
        r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-output-directory=paper/build", tex_path],
                           cwd=ROOT, capture_output=True, text=True, errors="replace")
        if r.returncode != 0:
            print(r.stdout[-3000:])
            return False
        built = ROOT / "paper/build" / (Path(tex_path).stem + ".pdf")
        built.replace(ROOT / (Path(tex_path).with_suffix(".pdf")))
    return True


def main() -> int:
    ok = convert("paper/main_filled.md", "paper/main_filled.tex", pdf=True,
                 extra_includes=[r"\AfterEndEnvironment{abstract}{\clearpage}"])
    # the online appendix is proof-heavy; 11pt and near-single spacing keep long displays inside the text width
    ok &= convert("paper/online_appendix_filled.md", "paper/online_appendix_filled.tex", pdf=True,
                  meta_overrides={"fontsize": "11pt", "linestretch": "1.15"}, extra_includes=APPENDIX_INCLUDES)
    print("LaTeX build", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
