"""Add the round-3 class exhibit and benchmark windows to the revised manuscript.

Run from the repository root with the project interpreter:

    .venv/bin/python audit/revision_v2_2026_10_21/scripts/round3.py            # writes the clone
    .venv/bin/python audit/revision_v2_2026_10_21/scripts/round3.py --check    # checks only

The script reads main.tex and online_appendix.tex at commit 1473673 of the revision clone
(the round-2 integration, git -C overleaf/paper-revision show 1473673:<file>) and applies,
in order:

  1. content edits to main.tex and online_appendix.tex, each an exact replacement with an
     expected count;
  2. one float move in main.tex: the robustness table (Table 3) goes from the end of
     Section 5.3 to the end of Section 5.1, so that it keeps its number and the class
     exhibit placed in Section 5.2 becomes Table 4;
  3. number substitution: \\NUM{name} takes the display of the registry row `name` of the
     numerical worktree, after two cross-checks (the reconciliation row of round 3 holds the
     same stored value, and the manifest display rule reproduces the display);
     \\INP{case.key} takes the exact declared input from numerics/manifests/c10_classes.json;
  4. checks: labels (including the label inside the class table), references, tags,
     citations against records, and no placeholder left;
  5. the write of both files and the copy of tables/table_class_exhibit.tex, after a check
     of its SHA-256 against the reconciliation record. No other table or figure is copied.

It stops with a message on any mismatch and writes nothing until every step has passed.
Print-only: it has no assertions.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REV = ROOT / "audit" / "revision_v2_2026_10_21"
CLONE = ROOT / "overleaf" / "paper-revision"
NUMERICS = Path("/home/uctpiaj/work/Projects/ccc-revision-numerics")
BASE_COMMIT = "1473673"
FILES = ("main.tex", "online_appendix.tex")
TABLE = "tables/table_class_exhibit.tex"
TABLE_RECON_NAME = "file.tables.table_class_exhibit.tex"
C10_FRAGMENT = REV / "integration" / "I04_oa_c10_classes.tex"


class Stop(Exception):
    pass


def stop(msg: str) -> None:
    raise Stop(msg)


def git_show(name: str) -> str:
    return subprocess.run(["git", "-C", str(CLONE), "show", f"{BASE_COMMIT}:{name}"],
                          check=True, capture_output=True, text=True).stdout


def replace(text: str, old: str, new: str, count: int, eid: str) -> str:
    n = text.count(old)
    if n != count:
        stop(f"{eid}: expected {count} of {old[:90]!r}, found {n}")
    return text.replace(old, new)


# --- main.tex texts ----------------------------------------------------------------------

INTRO_SENTENCE = (
    r"Dispersion within a class raises the option value of preparation: in an example in "
    r"\hyperref[sec-acquisition-values]{Section 5.2}, dispersed classes produce the reversal "
    r"and point-mass classes with the same means, costs, prior, and strengths do not. "
)

WINDOWS_PARAGRAPH = r"""At these strengths the spread ratio \(\Delta_T(r_0)/\Delta_T(r_1)\) is
\NUM{base_spread_ratio}, below the bound \((1-1/b)\rho m\) of
\NUM{base_spread_ratio_bound}, so the trading-cost window of
\eqref{eq:paper-cond-2} is nonempty. The window is
\((\NUM{base_trade_cost_lower},\NUM{base_trade_cost_upper})\), and it
contains \(k=\INP{benchmark.k}\). It depends on the prior through
\(\kappa(\pi)\), and at the benchmark strengths it is nonempty only for
priors in \((\NUM{base_prior_window_lower},\NUM{base_prior_window_upper})\).
With the other benchmark inputs fixed, the hypotheses of parts (i) and
(ii) of \hyperref[result-proposition-2]{Proposition 2} hold for priors in
\((\NUM{base_prior_prop2_lower},\NUM{base_prior_prop2_upper})\). The
hypotheses of all three parts hold for priors in
\((\NUM{base_prior_prop2_all_lower},\NUM{base_prior_prop2_all_upper})\).
Away from these priors the costs or strengths must change;
\hyperref[sec-acquisition-values]{Section 5.2} reports such vectors at
priors \INP{prior_03.fundamental_prior_H} and
\INP{prior_07.fundamental_prior_H}."""

EXHIBIT_PARAGRAPH = r"""Table~\ref{tab:oa-class-exhibit} reports four economies outside the
benchmark. Cases A, B, and C satisfy every hypothesis of
\hyperref[result-proposition-2]{Proposition 2}, including that of part
(iii), and its sufficient ownership condition. Cases A and B keep the
point masses and set the prior at \INP{prior_03.fundamental_prior_H} and
\INP{prior_07.fundamental_prior_H}, where the benchmark vector violates
these hypotheses and no trading cost satisfies \eqref{eq:paper-cond-2}
at the benchmark strengths
(\hyperref[sec-benchmark-and-information-controls]{Section 4.2}). Each
of the two cases therefore has its own high cost, trading cost, and weak
strength, and entry rises from \NUM{class_prior_03_r_0_E} to
\NUM{class_prior_03_r_1_E} in A and to \NUM{class_prior_07_r_1_E} in B.
Case C sets the prior at \INP{wide_07.fundamental_prior_H} and draws
values uniformly from \([\INP{wide_07.a_L},\INP{wide_07.b_L}]\) and
\([\INP{wide_07.a_H},\INP{wide_07.b_H}]\), wide classes above the
reserve with means \(\ell\) and \(h\). Its high class can lose to the
strong incumbent, so the ownership condition has content: at \(r_1\),
\(W_H\) falls to \NUM{class_wide_07_r_1_W_H}, and high-class ownership
still rises from \NUM{class_wide_07_r_0_O_H} to
\NUM{class_wide_07_r_1_O_H}. Case D puts point masses at the same means
and keeps the costs, prior, and strengths of C. C raises strong-economy
entry to \NUM{class_wide_07_r_1_E}, and D stays at
\NUM{class_matched_point_07_r_1_E}. Dispersion within a class raises the
challenger's option value of preparation. Preparation reveals the value,
and the challenger profits only when it wins, so its gross profit is
convex in the value; a spread around the same mean raises gross profit
at every belief. In C a favorable price lifts that profit above the high
cost, and in D even the largest feasible posterior does not. The class
model thus produces a reversal that the point-mass model with the same
means, costs, prior, and strengths cannot produce. D fails the upper
bound in \eqref{eq:paper-cond-1} at the strong strength, so its outcome
is not a counterexample to \hyperref[result-proposition-2]{Proposition 2}.

\setcounter{table}{3}
\input{tables/table_class_exhibit.tex}

"""

TABLE3_FLOAT = r"""\setcounter{table}{2}
\begin{table}[tbp]\begingroup\singlespacing\small\centering
\caption{Robustness and complementary private information.}\label{tab:3}
\input{tables/table3_extensions.tex}
\par\endgroup\end{table}

"""

SECTION7_OLD = (
    r"In the benchmark the preparation cost is independent of value, so at each price the "
    r"share of high-value buyers among those that prepare equals the price-implied posterior, "
    r"which rises with the price. A high-value buyer always outbids the incumbent; a low-value "
    r"buyer loses whenever the incumbent's value exceeds \(\ell\)."
)
SECTION7_NEW = (
    r"In the benchmark, a high-value buyer always outbids the incumbent, and a low-value buyer "
    r"loses whenever the incumbent's value exceeds \(\ell\). The preparation cost is "
    r"independent of value, so at each price the share of high-value buyers among those that "
    r"prepare equals the price-implied posterior, which rises with the price."
)


def main_edits() -> list[dict]:
    return [
        dict(id="m01", count=1, why="introduction: one sentence that announces the class exhibit; "
             "'It holds' becomes 'The reversal also holds' so the pronoun keeps its antecedent",
             old=r"both class supports lie above the reserve. It holds for every noise law",
             new=r"both class supports lie above the reserve. " + INTRO_SENTENCE
             + r"The reversal also holds for every noise law"),
        dict(id="m02", count=1, why="Section 4.2: benchmark ratio, trading-cost window, and the "
             "three prior intervals (referee rank 3 and M1)",
             old="0.125000 to 0.324192. At \\(r_2\\), entry returns to 0.250000.\n\n"
                 "\\setcounter{table}{0}",
             new="0.125000 to 0.324192. At \\(r_2\\), entry returns to 0.250000.\n\n"
                 + WINDOWS_PARAGRAPH + "\n\n\\setcounter{table}{0}"),
        dict(id="m03", count=1, why="Section 5.1: first citation of Table 3 (Panel A), whose float "
             "now ends Section 5.1",
             old=r"compared with 0.522757 under Laplace noise. The logistic flow threshold",
             new=r"compared with 0.522757 under Laplace noise (Table~\ref{tab:3}, Panel A). "
                 r"The logistic flow threshold"),
        dict(id="m05", count=1, why="Section 5.2: the class exhibit paragraph and the table "
             "(referee rank 1)",
             old="\\subsection{5.3 Complementary private\ninformation}",
             new=EXHIBIT_PARAGRAPH + "\\subsection{5.3 Complementary private\ninformation}"),
        dict(id="m06a", count=1, why="reserve comparisons become Table 5; label renamed to match",
             old="\\setcounter{table}{3}\n\\begin{table}[tbp]\\begingroup\\singlespacing\\small"
                 "\\centering\n\\caption{Reserve comparisons.}\\label{tab:4}",
             new="\\setcounter{table}{4}\n\\begin{table}[tbp]\\begingroup\\singlespacing\\small"
                 "\\centering\n\\caption{Reserve comparisons.}\\label{tab:5}"),
        dict(id="m06b", count=3, why="references to the reserve table follow the new label",
             old=r"\ref{tab:4}", new=r"\ref{tab:5}"),
        dict(id="m07", count=1, why="Section 7, referee minor 10: 'In the benchmark' governs the "
             "benchmark claims; cost independence is the reason, not the scoped clause",
             old=SECTION7_OLD, new=SECTION7_NEW),
        dict(id="m08", count=1, why="Figure 1 note, referee minor 13: drop the repeated prior",
             old=r"and \(b=2\), with prior \(1/2\). Values are per target share.",
             new=r"and \(b=2\). Values are per target share."),
        dict(id="m09", count=1, why="Appendix A.8: pointer to the four exhibit vectors "
             "(referee rank 1 asks for them there)",
             old=r"\(c_H\) otherwise. The prior is \(\pi=1/2\) in each vector.",
             new=r"\(c_H\) otherwise. The prior is \(\pi=1/2\) in each vector below. The four "
                 r"vectors of the class exhibit in \hyperref[sec-acquisition-values]{Section 5.2}, "
                 r"with priors \INP{prior_03.fundamental_prior_H} and "
                 r"\INP{prior_07.fundamental_prior_H}, are declared in the notes to "
                 r"Table~\ref{tab:oa-class-exhibit} and in Online Appendix C.10."),
    ]


def oa_edits(c10: str) -> list[dict]:
    return [
        dict(id="o01", count=1, why="new subsection C.10 from the worktree contract "
             "(integration/I04_oa_c10_classes.tex)",
             old="\\section{D. Institutional pilot and empirical design}\\label{oa-d}",
             new=c10 + "\\section{D. Institutional pilot and empirical design}\\label{oa-d}"),
        dict(id="o02", count=1, why="C.8: the registry now also takes C.10 outputs",
             old="the validated exercise outputs in C.1 to C.7 and C.9. The manifest specifies",
             new="the validated exercise outputs in C.1 to C.7, C.9, and C.10. The manifest "
                 "specifies"),
        dict(id="o03", count=1, why="C.8: two quantity families for C.10 (registry units)",
             old="Entry under additional noise laws at fixed orders & C.9 & probability \\\\\n",
             new="Entry under additional noise laws at fixed orders & C.9 & probability \\\\\n"
                 "Class exhibits: outcomes and margins & C.10 & probability; model units;\n"
                 "order units \\\\\n"
                 "Benchmark prior and trade-cost windows; four-law entry range & C.10 &\n"
                 "probability; model units \\\\\n"),
        dict(id="o03b", count=1, why="C.8: display rules of the C.10 rows (quantity manifest)",
             old="printed rather than rounding inward. Model units are the per-share\n"
                 "normalization of A.1.\n",
             new="printed rather than rounding inward. Model units are the per-share\n"
                 "normalization of A.1. The C.10 rows, margins included, use\n"
                 "\\texttt{decimal\\_6}, except the benchmark trade-cost bounds\n"
                 "(\\texttt{decimal\\_4}) and the spread ratio and its bound\n"
                 "(\\texttt{decimal\\_3}).\n"),
        dict(id="o04", count=1, why="E.1: the C.10 producer joins the run list",
             old="\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c9\\_revision.py}\n",
             new="\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c9\\_revision.py}\n"
                 "\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c10\\_classes.py}\n"),
        dict(id="o05", count=1, why="C.6: the reserve comparisons are now Table 5 of the paper",
             old="Feed: Table 4 and the sale-design discussion.",
             new="Feed: Table 5 and the sale-design discussion."),
    ]


def apply(text: str, edits: list[dict], label: str) -> str:
    for e in edits:
        text = replace(text, e["old"], e["new"], e["count"], e["id"])
        print(f"  {e['id']:5s} {label:4s} x{e['count']}  {e['why']}")
    return text


# --- stages -----------------------------------------------------------------------------

def load_c10_fragment() -> str:
    lines = C10_FRAGMENT.read_text().splitlines(keepends=True)
    body = [ln for ln in lines if not ln.startswith("%")]
    return "".join(body)


def stage_content(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 1. Content edits (expected counts must match)")
    print("=" * 78)
    text["main.tex"] = apply(text["main.tex"], main_edits(), "main")
    text["online_appendix.tex"] = apply(text["online_appendix.tex"], oa_edits(load_c10_fragment()),
                                        "OA")


def stage_move(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 2. Float move in main.tex")
    print("=" * 78)
    t = text["main.tex"]
    t = replace(t, TABLE3_FLOAT + "\\section{6. Welfare and sale terms}",
                "\\section{6. Welfare and sale terms}", 1, "m04 cut")
    t = replace(t, "\\subsection{5.2 Value classes}\\label{sec-acquisition-values}",
                TABLE3_FLOAT + "\\subsection{5.2 Value classes}\\label{sec-acquisition-values}",
                1, "m04 insert")
    print("  m04   main  Table 3 float moved from the end of Section 5.3 to the end of Section 5.1")
    i3 = t.find("\\label{tab:3}")
    i4 = t.find("\\input{tables/table_class_exhibit.tex}")
    i5 = t.find("\\label{tab:5}")
    print(f"  source order: Table 3 at {i3}, class exhibit at {i4}, reserve table at {i5}; "
          f"increasing: {'yes' if 0 < i3 < i4 < i5 else 'NO'}")
    if not 0 < i3 < i4 < i5:
        stop("table floats are not in source order 3, 4, 5")
    text["main.tex"] = t


def display(value: str, rule: str) -> str:
    m = re.fullmatch(r"decimal_(\d+)", rule)
    if not m:
        stop(f"display rule {rule} is not handled here")
    q = Decimal(1).scaleb(-int(m.group(1)))
    return format(Decimal(value).quantize(q, rounding=ROUND_HALF_EVEN), "f")


def load_numbers() -> tuple[dict, dict, dict]:
    recon: dict[str, list[dict]] = {}
    with open(REV / "reconciliation.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            recon.setdefault(row["name"], []).append(row)
    with open(NUMERICS / "paper" / "quantity_manifest.csv", newline="") as fh:
        manifest = {r["name"]: r for r in csv.DictReader(fh)}
    with open(NUMERICS / "numerics" / "quantity_registry.csv", newline="") as fh:
        registry = {r["name"]: r for r in csv.DictReader(fh)}
    return recon, manifest, registry


def load_inputs() -> dict[str, dict]:
    run = json.loads((NUMERICS / "numerics" / "manifests" / "c10_classes.json").read_text())
    cases = {c["case"]: c for c in run["inputs"]["cases"]}
    cases["benchmark"] = run["inputs"]["benchmark"]
    if run.get("passed") is not True:
        stop("c10_classes.json does not record a pass")
    return cases


def stage_numbers(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 3. Numbers and declared inputs")
    print("=" * 78)
    recon, manifest, registry = load_numbers()
    inputs = load_inputs()
    used: list[tuple] = []
    for name in FILES:
        def fill_num(m: re.Match) -> str:
            key = m.group(1)
            reg = registry.get(key)
            if reg is None:
                stop(f"{name}: \\NUM{{{key}}} is not a registry name")
            rows = [r for r in recon.get(key, []) if "new, round 3" in r["note"]]
            if len(rows) != 1:
                stop(f"{name}: {key} has {len(rows)} reconciliation rows marked 'new, round 3'")
            if Decimal(rows[0]["new_value"]) != Decimal(reg["value"]):
                stop(f"{name}: {key}: reconciliation {rows[0]['new_value']} differs from "
                     f"registry {reg['value']}")
            rule = manifest[key]["display"]
            shown = display(reg["value"], rule)
            if shown != reg["display"]:
                stop(f"{name}: {key}: rule {rule} gives {shown}, registry display {reg['display']}")
            used.append((name, f"\\NUM{{{key}}}", shown, f"{reg['value'][:24]}; {rule}; "
                         f"{reg['status']}; {reg['source_file']}"))
            return shown

        def fill_inp(m: re.Match) -> str:
            case, key = m.group(1), m.group(2)
            if case not in inputs or key not in inputs[case]:
                stop(f"{name}: \\INP{{{case}.{key}}} is not a declared input")
            shown = str(inputs[case][key])
            used.append((name, f"\\INP{{{case}.{key}}}", shown,
                         "exact input, numerics/manifests/c10_classes.json"))
            return shown

        text[name] = re.sub(r"\\NUM\{([^}]*)\}", fill_num, text[name])
        text[name] = re.sub(r"\\INP\{([^}.]*)\.([^}]*)\}", fill_inp, text[name])
        left = re.findall(r"\\(?:NUM|INP)\{[^}]*\}", text[name])
        if left:
            stop(f"{name}: placeholders left {left}")
    for name, ph, shown, src in used:
        print(f"  {name:20s} {ph:52s} -> {shown:10s} [{src}]")
    print(f"  {len(used)} substitutions; no placeholder left")


def bib_check(t: str, name: str) -> None:
    cited = set(re.findall(r"\\citeproc\{ref-([^}]+)\}", t))
    records = re.findall(r"\\bibitem\[\\citeproctext\]\{ref-([^}]+)\}", t)
    missing = sorted(cited - set(records))
    uncited = sorted(set(records) - cited)
    print(f"  {name}: {len(records)} records, {len(cited)} cited keys; "
          f"missing records {missing or 'none'}; uncited records {uncited or 'none'}")
    if missing or uncited:
        stop(f"{name}: citation and record sets differ")


def stage_checks(text: dict[str, str], base: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 4. Checks")
    print("=" * 78)
    table_labels = re.findall(r"\\label\{([^}]+)\}", (NUMERICS / TABLE).read_text())
    print(f"  labels inside {TABLE}: {table_labels}")
    for name in FILES:
        t = text[name]
        labels = re.findall(r"\\label\{([^}]+)\}", t)
        if name == "main.tex":
            labels += table_labels
        dup = sorted({x for x in labels if labels.count(x) > 1})
        if dup:
            stop(f"{name}: duplicate labels {dup}")
        refs = (set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", t))
                | set(re.findall(r"\\hyperref\[([^\]]+)\]", t)))
        undefined = sorted(refs - set(labels))
        old_labels = set(re.findall(r"\\label\{([^}]+)\}", base[name]))
        print(f"  {name}: {len(labels)} labels; removed {sorted(old_labels - set(labels))}; "
              f"added {sorted(set(labels) - old_labels)}")
        print(f"  {name}: references to undefined labels: {undefined or 'none'}")
        if undefined:
            stop(f"{name}: undefined references {undefined}")
        tags = re.findall(r"\\tag\{([^}]+)\}", t)
        base_tags = re.findall(r"\\tag\{([^}]+)\}", base[name])
        print(f"  {name}: tags unchanged: {'yes' if tags == base_tags else 'NO'} ({len(tags)})")
        if tags != base_tags:
            stop(f"{name}: tag list changed")
        counters = re.findall(r"\\setcounter\{table\}\{(\d+)\}", t)
        if name == "main.tex":
            print(f"  {name}: table counters in source order {counters}")
            if counters != ["0", "1", "2", "3", "4"]:
                stop(f"{name}: table counters are {counters}")
    bib_check(text["main.tex"], "main.tex")
    bib_check(text["online_appendix.tex"], "online_appendix.tex")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stage_artifact(write: bool) -> None:
    print("\n" + "=" * 78)
    print("STAGE 5. The class exhibit table")
    print("=" * 78)
    with open(REV / "reconciliation.csv", newline="") as fh:
        rows = [r for r in csv.DictReader(fh) if r["name"] == TABLE_RECON_NAME]
    if len(rows) != 1 or "new, round 3" not in rows[0]["note"]:
        stop(f"{TABLE_RECON_NAME}: expected one round-3 reconciliation row, found {len(rows)}")
    want = rows[0]["new_value"]
    src, dst = NUMERICS / TABLE, CLONE / TABLE
    h = sha(src)
    print(f"  worktree {TABLE}: sha256 {h}")
    print(f"  reconciliation record:            {want}")
    if h != want:
        stop(f"{TABLE}: worktree hash differs from the reconciliation record")
    if write:
        shutil.copyfile(src, dst)
        if sha(dst) != want:
            stop(f"{TABLE}: copied file hash differs")
        print(f"  copied to {dst}; hash matches")
    else:
        print("  --check: not copied")
    print("  no other table or figure is copied in this round")


def main() -> None:
    base = {name: git_show(name) for name in FILES}
    print(f"Base commit {BASE_COMMIT}: main.tex {base['main.tex'].count(chr(10))} lines, "
          f"online_appendix.tex {base['online_appendix.tex'].count(chr(10))} lines")
    text = dict(base)
    write = "--check" not in sys.argv
    try:
        stage_content(text)
        stage_move(text)
        stage_numbers(text)
        stage_checks(text, base)
        stage_artifact(write)
    except Stop as exc:
        print(f"\nSTOPPED: {exc}")
        sys.exit(1)
    if not write:
        print("\n--check: nothing written")
        return
    for name in FILES:
        (CLONE / name).write_text(text[name])
        print(f"  wrote {CLONE / name} ({text[name].count(chr(10))} lines)")
    print("\nDone.")


if __name__ == "__main__":
    main()
