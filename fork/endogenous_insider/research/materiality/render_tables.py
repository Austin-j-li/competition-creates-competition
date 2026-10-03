"""Render Markdown tables from the materiality CSVs. Reads CSV only; never solves."""
from __future__ import annotations

import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(name: str) -> list[dict[str, str]]:
    with (HERE / name).open() as fh:
        return list(csv.DictReader(fh))


def num(s: str, d: int = 4) -> str:
    try:
        return f"{float(s):.{d}f}"
    except ValueError:
        return s


def table(rows: list[dict[str, str]], cols: list[tuple[str, str, int]]) -> str:
    head = "| " + " | ".join(c[1] for c in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    body = ["| " + " | ".join(num(r[c[0]], c[2]) if c[2] >= 0 else r[c[0]] for c in cols) + " |" for r in rows]
    return "\n".join([head, sep, *body])


def main() -> None:
    out = []
    branch = read("materiality_branch.csv")
    keep = {"1.2", "1.5", "1.66", "1.8", "2.0", "2.05", "2.5", "3.0", "3.5", "3.5926", "3.5927", "3.6"}
    sel = [r for r in branch if r["r"] in keep]
    out.append("### Table 1. Materiality index on the minimal-pool full-order branch\n")
    out.append(table(sel, [("r", "$r$", 4), ("Delta_T", "$\\Delta_T$", 4), ("E", "$\\mathsf E$", 4), ("mat", "$\\mathfrak M=\\mathsf E\\Delta_T$", 4),
                           ("mat_H", "$\\mathfrak M_H$", 4), ("mat_L", "$\\mathfrak M_L$", 4), ("J", "$J$", 4), ("resid_H", "$J/\\mathfrak M_H$", 3),
                           ("suff_margin", "$(1-1/b)J-k$", 4), ("mat_bench", "benchmark index", 4), ("region", "region", -1), ("status", "status", -1)]))
    fam = read("materiality_family.csv")
    out.append("\n### Table 2. The cutoff family at $r=3$: materiality and the own-order probability\n")
    out.append(table(fam, [("x_prime", "$x'$", 3), ("e_H", "$e_H$", 4), ("e_L", "$e_L$", 4), ("mat", "$\\mathfrak M$", 4),
                           ("prob_H_s0", "$\\Pr(A\\mid H,s=0)$", 4), ("prob_H_s1", "$\\Pr(A\\mid H,s=1)$", 4),
                           ("prob_L_s0", "$\\Pr(A\\mid L,s=0)$", 4), ("prob_L_s1", "$\\Pr(A\\mid L,s=1)$", 4),
                           ("suff_margin", "$(1-1/b)J-k$", 4)]))
    dev = read("materiality_deviation.csv")
    out.append("\n### Table 3. Gross value of trading against the fixed schedule, by own order size\n")
    out.append(table(dev, [("r", "$r$", 2), ("s", "$s$", 2), ("prob_H", "$\\Pr(A\\mid H,s)$", 4), ("gross_H", "$F_H(s)$", 4), ("bound_H", "$\\Delta_T\\Pr(A\\mid H,s)$", 4),
                           ("prob_L", "$\\Pr(A\\mid L,-s)$", 4), ("gross_L", "$F_L(s)$", 4), ("bound_L", "$\\Delta_T\\Pr(A\\mid L,-s)$", 4), ("U_H", "$U_H(s)$", 4), ("U_L", "$U_L(s)$", 4)]))
    fork = (HERE.parent.parent / "branches.csv")
    if fork.exists():
        with fork.open() as fh:
            live = [r for r in csv.DictReader(fh) if r["branch"] == "live"]
        for r in live:
            r["mat"] = str(float(r["E"]) * float(r["DeltaT"]))
            r["mat_H"] = str(float(r["eH"]) * float(r["DeltaT"]))
            r["mat_L"] = str(float(r["eL"]) * float(r["DeltaT"]))
        sel = [r for r in live if float(r["r"]) <= 2.05 or r["r"] in {"3", "3.5926"}]
        out.append("\n### Table 3b. Materiality index on the fork's own live branch (`branches.csv`, numerical diagnostic), including interior orders\n")
        out.append(table(sel, [("r", "$r$", 4), ("qH", "$q_H$", 2), ("qL", "$q_L$", 2), ("E", "$\\mathsf E$", 4), ("DeltaT", "$\\Delta_T$", 4),
                               ("mat", "$\\mathfrak M$", 4), ("mat_H", "$\\mathfrak M_H$", 4), ("mat_L", "$\\mathfrak M_L$", 4), ("U_H", "$U_H$", 4), ("U_L", "$U_L$", 4)]))
    thr = read("materiality_thresholds.csv")
    out.append("\n### Table 4. Boundaries\n")
    out.append(table(thr, [("boundary", "object", -1), ("value", "value", 4), ("definition", "definition", -1), ("status", "status", -1)]))
    (HERE / "tables.md").write_text("\n".join(out) + "\n")
    print((HERE / "tables.md").read_text())


if __name__ == "__main__":
    main()
