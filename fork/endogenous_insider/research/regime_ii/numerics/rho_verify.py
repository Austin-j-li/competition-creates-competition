"""Equilibria at high rho (adversary's request): list every equilibrium the cutoff scan finds at rho in {0.5154, 0.6, 0.75}
and c_L in {2.4, 3.0} (r1 = 3, k = 0.02), write them to rho_check_eq.csv, and let verify_csv.py check each by
independent quadrature.  Status of the engine rows: numerical diagnostic; accepted rows: computer-assisted.
"""
from __future__ import annotations

from engine import make_econ
from run_sweep import CH, EQ_COLS, R0, write_csv
from scan import row_of, scan_point
from pathlib import Path

HERE = Path(__file__).resolve().parent

if __name__ == "__main__":
    rows = []
    for rho in (0.5154, 0.6, 0.75):
        for cL in (2.4, 3.0):
            ec = make_econ(3.0, rho, cL, CH)
            ecw = make_econ(R0, rho, cL, CH)
            res = scan_point(ec, step=0.05)
            rows += [row_of(ec, c, ecw) for c in res.members]
    write_csv(HERE / "rho_check_eq.csv", EQ_COLS, rows)
    print("rho_check_eq.csv", len(rows))
