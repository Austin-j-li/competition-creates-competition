"""Write registry/W1.csv: the benchmark primitives and two gross profits at the prior.

Usage (from the repository root):
    .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/W1/w1_registry.py

Every value is an exact rational. The script prints each row and writes a run log beside itself.
"""
import csv
import pathlib
from fractions import Fraction as Fr

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
OUT = TEAM / "registry" / "W1.csv"
LOG = HERE / "w1_registry.log"
SCRIPT = "scripts/W1/w1_registry.py"
RUNLOG = "scripts/W1/w1_registry.log"

h, ell, p, rho, cH, k, pi = Fr(10), Fr(1), Fr(1, 2), Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)


def gross_profit(r: Fr, mu: Fr) -> Fr:
    """B_r(mu) = g_L + mu (g_H - g_L) for point masses h, ell and R ~ U[0, r], p < ell < r < h."""
    g_H = h - r / 2 - p * p / (2 * r)
    g_L = (ell * ell - p * p) / (2 * r)
    return g_L + mu * (g_H - g_L)


def exact(x: Fr) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


rows = [
    ("prim_h", h, exact(h), "input", "benchmark high value h"),
    ("prim_ell", ell, exact(ell), "input", "benchmark low value ell (unit of money)"),
    ("prim_p", p, exact(p), "input", "benchmark reserve p"),
    ("prim_rho", rho, exact(rho), "input", "probability of the zero preparation cost"),
    ("prim_cH", cH, exact(cH), "input", "high preparation cost c_H"),
    ("prim_k", k, exact(k), "input", "trading cost k"),
    ("prim_pi", pi, exact(pi), "input", "benchmark prior on class H"),
    ("prim_r0", r0, exact(r0), "input", "weak incumbent strength r_0"),
    ("prim_r1", r1, exact(r1), "input", "strong incumbent strength r_1"),
    ("prim_r2", r2, exact(r2), "input", "very strong incumbent strength r_2"),
    ("Bprior_r0", gross_profit(r0, pi), f"{float(gross_profit(r0, pi)):.6f}", "analytical",
     "B_{r_0}(1/2) = 1153/240; gross acquisition profit at the prior, weak incumbent"),
    ("Bprior_r1_B", gross_profit(r1, pi), f"{float(gross_profit(r1, pi)):.6f}", "analytical",
     "B_{r_1}(1/2) = 103/24; gross acquisition profit at the prior, strong incumbent; free of the slot"),
    ("B_r1_half", gross_profit(r1, pi), exact(gross_profit(r1, pi)), "analytical",
     "B_{3}(1/2) as an exact fraction"),
    ("Bprior_r2", gross_profit(r2, pi), f"{float(gross_profit(r2, pi)):.6f}", "analytical",
     "B_{r_2}(1/2); gross acquisition profit at the prior, very strong incumbent; free of the slot"),
    # Strengths at which the manuscript reports values on a branch (same values as the P1, P3 and P5 keys).
    ("str_r140", Fr(7, 5), "1.40", "input", "strength 1.40 on the mixed-purchase branch (entry_mb_r140_B)"),
    ("str_r145", Fr(29, 20), "1.45", "input", "strength 1.45 on the mixed-purchase branch (entry_mb_r145_B)"),
    ("str_r155", Fr(31, 20), "1.55", "input", "intermediate strength 31/20 (research and threshold keys)"),
    ("str_r160", Fr(8, 5), "1.60", "input", "intermediate strength 8/5 (research and threshold keys)"),
    ("str_r165", Fr(33, 20), "1.65", "input", "intermediate strength 33/20 (research and threshold keys)"),
    # Proposition region (b): the right side of (H2) at r_1 is u < 19/3 (u_kstrong in P1_core).
    ("u_kstrong_frac", Fr(19, 3), "19/3", "analytical", "right side of (H2) at r_1 and prior 1/2: u < 19/3"),
    # Atomless costs (P4 R7): H_C = (1/4) U[0, L] + (3/4) U[c_H - eps, c_H + eps].
    ("atom_L", Fr(1, 5), "1/5", "input", "upper end L of the zero-cost component (P4 p4_input_low_upper)"),
    ("atom_eps", Fr(1, 10), "1/10", "input", "half-width of the high-cost band (P4 p4_input_epsilon)"),
    ("atom_eps_small", Fr(1, 1000), "1/1000", "input", "half-width that keeps all three parts (P4 p4_atomless_small_width)"),
    # The signal economy S(B) (P4 R8) and the pair that works at the benchmark.
    ("sig_rho", Fr(17, 20), "0.85", "input", "S(B): probability of the zero cost (P4 p4_input_s_rho)"),
    ("sig_cH", Fr(357, 50), "7.14", "input", "S(B): high cost (P4 p4_input_s_cost)"),
    ("sig_k", Fr(3, 200), "0.015", "input", "S(B): trading cost (P4 p4_input_s_fee)"),
    ("sig_r0", Fr(11, 10), "1.1", "input", "S(B): weak strength (P4 p4_input_s_r0)"),
    ("sig_r1", Fr(23, 10), "2.3", "input", "S(B): strong strength (P4 p4_input_s_r1)"),
    ("sig_aT", Fr(7, 10), "0.70", "input", "investor signal accuracy (P4 p4_input_signal_a)"),
    ("sig_d", Fr(3, 4), "0.75", "input", "challenger signal accuracy (P4 p4_input_signal_d)"),
    ("sig_comp_aT", Fr(47, 50), "0.94", "input", "investor accuracy of the complementary pair at B (P4 p4_input_comp_a)"),
    ("sig_comp_d", Fr(101, 200), "0.505", "input", "challenger accuracy of the complementary pair at B (P4 p4_input_comp_d)"),
    # Sale terms (P2 R9).
    ("access_out_cH", Fr(12, 5), "12/5", "input", "high cost outside the recruiting region (P2 Section 4.2)"),
    ("pay_gap_coef", Fr(13, 20), "13/20", "analytical",
     "Delta_omega(r_1) - Delta_omega(r_0) = (13/20)(1 - 2 omega); E[(R - ell)_+] = (r - ell)^2/(2r)"),
    ("rsv_points_excl", Fr(101, 100), "101/100", "input", "exclusion reserve, point-mass classes (P2 prop:exclude)"),
    ("rsv_bands_excl", Fr(11, 10), "11/10", "input", "exclusion reserve, narrow uniform classes (P2 prop:exclude)"),
    ("rsv_deter", Fr(31, 20), "31/20", "input", "reserve that restores strict deterrence (P2 prop:deter)"),
    # The four-class economy of Proposition A.6 (P2 derive.py, the block after "Four separated classes").
    ("four_v1", Fr(1), "1", "input", "four-class economy: low-group value 1 (P2 derive.py vals[0])"),
    ("four_v2", Fr(1001, 1000), "1001/1000", "input", "four-class economy: low-group value 1001/1000 (P2 derive.py vals[1])"),
    ("four_v3", Fr(9999, 1000), "9999/1000", "input", "four-class economy: high-group value 9999/1000 (P2 derive.py vals[2])"),
    ("four_v4", Fr(10), "10", "input", "four-class economy: high-group value 10 (P2 derive.py vals[3])"),
    ("four_prior", Fr(1, 4), "1/4", "input", "four-class economy: prior of each class (P2 derive.py divides by 4)"),
]

def mean_excess(r: Fr) -> Fr:
    """E[(R - ell)_+] for R ~ U[0, r], r > ell."""
    return (r - ell) ** 2 / (2 * r)


assert_free_check = mean_excess(r1) - mean_excess(r0)
lines = [f"check: E[(R-ell)_+] at r_1 minus at r_0 = {exact(assert_free_check)}"]
with OUT.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["key", "value", "display", "status", "source_script", "run_log", "note"])
    for key, value, display, status, note in rows:
        w.writerow([key, exact(value), display, status, SCRIPT, RUNLOG, note])
        lines.append(f"{key}: value {exact(value)}, display {display}, status {status}")
lines.append(f"rows written: {len(rows)} to {OUT.relative_to(TEAM)}")
text = "\n".join(lines) + "\n"
LOG.write_text(text)
print(text, end="")
