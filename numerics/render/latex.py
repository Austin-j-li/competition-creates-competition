"""LaTeX conversion of the filled manuscript and online appendix (deliverable 5).

The filled Markdown copies are generated files; the figure/table placeholder blockquotes in them
are replaced by LaTeX float environments that include the rendered files. The author's prose is
untouched. Compilation uses pandoc (with citeproc and references.bib) and latexmk.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from numerics.io import ROOT  # noqa: E402

FIGS = {
    "Figure 1": ("figures/equilibrium_correspondence.pdf", "fig:correspondence",
                 r"The equilibrium correspondence at the benchmark primitives. Panel (a): total entry $\mathsf E$ against incumbent strength $r$ for every accepted branch: pooling (no trade), full orders, the asymmetric family $(q_H,q_L)=(1,-v)$ by numerical continuation, and any other pure or mixed profiles found. Shaded regions are analytically established uniqueness regions (no trade below $\mathfrak r(k)$; full orders above $r_U$). Dashed verticals mark $r_N$ (exact pooling-existence boundary), $r_U$ (sufficient full-order uniqueness boundary), and $r_C$ (expensive-entry feasibility boundary). Certified points carry interval enclosures. Lines are broken at unresolved nodes or branch changes; a missing branch is not a uniqueness label. Panel (b): the unfavorable-state order magnitude $v$ along asymmetric candidates, with full orders as the boundary."),
    "Figure 2": ("figures/two_returns.pdf", "fig:two_returns",
                 r"Incumbent strength raises the sensitivity of target proceeds while reducing challenger acquisition profit at every displayed belief. Panel (a): $\Delta_T(r)$. Panel (b): $B_r(\mu)$ for $\mu\in\{m,1/2,M\}$. All other primitives at the benchmark specification; values per target share."),
    "Figure 3": ("figures/posterior_tail_entry.pdf", "fig:posterior_tail",
                 r"The upper tail of price information under full orders at the strong benchmark strength and scale $b=2$. Panel (a): $\Pr(\mu_X\ge\tau)$ against the threshold distance $M-\tau$ for Laplace and logistic noise. Panel (b): implied total entry $\rho+(1-\rho)\Pr(\mu_X\ge\tau)$ and the conditional favorable-flow probabilities $\alpha_H,\alpha_L$. At $M-\tau=0$ the Laplace plateau enters under the tie rule (dot) while the logistic mass is zero (cross). These are fixed-profile information diagnostics; the accompanying data file records for each threshold whether the equilibrium interpretation with the implied high cost is validated."),
    "Figure 4": ("figures/bargaining_weight.pdf", "fig:bargaining",
                 r"Bargaining and the division of information-sensitive returns in the verifiable-value institution with zero reserve, benchmark $h=10$, $\ell=1$, and uniform incumbents with $r=1.2$ (weak) and $r=3$ (strong). Panel (a): $\Delta_\eta$ against the seller weight $\eta$; the strength ordering reverses at $\eta=1/2$. Panel (b): challenger profits $G_{H,\eta}$ and $G_{L,\eta}$ (log scale). These are acquisition-stage comparisons, not equilibrium entry predictions."),
}
TABS = {"Table 1": "tables/table1_auction_primitives.tex", "Table 2": "tables/table2_equilibrium_controls.tex",
        "Table 3": "tables/table3_extensions.tex", "Table 4": "tables/table4_reserve_comparisons.tex"}

PLACEHOLDER_RE = re.compile(r"^> \*\*(Figure \d|Table \d) placeholder — .*?$", re.M)
HEADER = r"""---
documentclass: article
classoption: 11pt
geometry: margin=1in
header-includes:
  - \usepackage{amsmath,amssymb,amsthm}
  - \usepackage{booktabs}
  - \usepackage{graphicx}
  - \usepackage{float}
  - \usepackage{hyperref}
  - \allowdisplaybreaks
---
"""


def convert(md_path: str, tex_path: str, pdf: bool) -> bool:
    text = (ROOT / md_path).read_text(encoding="utf-8")

    def repl(m: re.Match) -> str:
        key = m.group(1)
        num = int(key.split()[1])
        if key in FIGS:
            f, lab, cap = FIGS[key]
            return ("```{=latex}\n\\setcounter{figure}{" + str(num - 1) + "}\\begin{figure}[H]\\centering\\includegraphics[width=\\linewidth]{" + f + "}\n"
                    f"\\caption{{{cap}}}\\label{{{lab}}}\\end{{figure}}\n```")
        return "```{=latex}\n\\setcounter{table}{" + str(num - 1) + "}\\input{" + TABS[key] + "}\n```"

    text = PLACEHOLDER_RE.sub(repl, text)
    # cross-document links (main <-> online appendix) become plain text in the compiled PDFs
    text = re.sub(r"\[([^\]]+)\]\((?:online_appendix|main)\.md#[^)]+\)", r"\1", text)
    # YAML front matter: keep the author's (bibliography) and add LaTeX packages
    if text.startswith("---"):
        end = text.index("\n---", 3)
        front = text[4:end]
        text = HEADER.rstrip("-\n") + "\n" + front + "\n---" + text[end + 4:]
    else:
        text = HEADER + text
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
                           cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-3000:])
            return False
        built = ROOT / "paper/build" / (Path(tex_path).stem + ".pdf")
        built.replace(ROOT / (Path(tex_path).with_suffix(".pdf")))
    return True


def main() -> int:
    ok = convert("paper/main_filled.md", "paper/main_filled.tex", pdf=True)
    ok &= convert("paper/online_appendix_filled.md", "paper/online_appendix_filled.tex", pdf=True)
    print("LaTeX build", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
