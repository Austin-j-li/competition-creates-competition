"""Write registry/W3_laplace.csv: the Laplace-manuscript numbers that the comparison note prints.

Each row takes its value from the independent outward intervals of scripts/XLA/independent_intervals.csv
(exact rationals, or the lower endpoint to 20 decimals with the full enclosure in the note), or from a table
of the pinned manuscript (overleaf/paper at 01bd5d6), named in source_script. Prints the rows it writes.
"""
import csv
import pathlib
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[4]
TEAM = ROOT / "audit/slot_manuscript_2026_10_23"
XLA = TEAM / "scripts/XLA/independent_intervals.csv"
OUT = TEAM / "registry/W3_laplace.csv"
XLA_SCRIPT = "scripts/XLA/independent_intervals.py"
XLA_LOG = "scripts/XLA/independent_intervals_run.log"
PIN = "git -C overleaf/paper show 01bd5d6:"

xla = {}
with XLA.open(newline="") as fh:
    for row in csv.DictReader(fh):
        xla[row["key"]] = row


def six(x: str) -> str:
    return f"{float(Fraction(x)):.6f}"


def from_xla(key, xla_key, display=None, status=None, note=""):
    row = xla[xla_key]
    lo, hi = row["lower"], row["upper"]
    if "/" in lo or lo == hi:
        value = lo
        disp = display or (lo if "/" in lo and display is None else six(lo))
        st = status or "analytical"
        enc = f"exact {lo}"
    else:
        value = lo[: lo.index(".") + 21]
        disp = display or six(lo)
        st = status or "computer-assisted"
        enc = f"outward enclosure [{lo}, {hi}]"
    return dict(key=key, value=value, display=disp, status=st, source_script=XLA_SCRIPT, run_log=XLA_LOG,
                note=f"{note}; {enc}".strip("; "))


def from_table(key, value, display, status, table, note=""):
    return dict(key=key, value=value, display=display, status=status, source_script=PIN + table, run_log="",
                note=note)


rows = [
    dict(key="lap_b", value="2", display="2", status="input", source_script=PIN + "main.tex",
         run_log="", note="Laplace scale b, benchmark vector (A.48)"),
    from_xla("lap_m_half", "m", note="m(1/2)=1/(1+e)"),
    from_xla("lap_M_half", "M", note="M(1/2)=e/(1+e); the slot's M_half_B is the same number"),
    from_xla("lap_tau_r0", "r0_tau", display="0.633117", note="tau(1.2)=195/308"),
    from_xla("lap_tau_r1", "r1_tau", display="0.705000", note="tau(3)=141/200"),
    from_xla("lap_tau_r2", "r2_tau", display="0.731392", note="tau(3.6)=4245/5804"),
    from_xla("lap_Delta_r0", "r0_D", display="0.016667", note="Delta_T(1.2)=1/60"),
    from_xla("lap_Delta_r1", "r1_D", display="0.666667", note="Delta_T(3)=2/3"),
    from_xla("lap_Delta_r2", "r2_D", display="0.938889", note="Delta_T(3.6)=169/180"),
    from_xla("lap_gH_r2", "r2_gH", display="5879/720", note="g_H(3.6)"),
    from_xla("lap_gL_r2", "r2_gL", display="5/48", note="g_L(3.6)"),
    from_xla("lap_margin_A1_lower", "A1_lower", display="1.195833", note="c_H-B_{1.2}(1/2)=287/240"),
    from_xla("lap_margin_A1_upper", "A1_upper", note="B_3(M)-c_H"),
    from_xla("lap_margin_A2_lower", "A2_lower", display="0.003333", note="k-Delta_T(1.2)=1/300"),
    from_xla("lap_margin_A2_upper", "A2_upper", note="(1-1/b)rho m Delta_T(3)-k; the smallest Prop. 2 margin in cost units"),
    from_xla("lap_margin_ownership", "ownership_sufficient_margin", display="3/4", note="(1+rho)-2rho"),
    from_xla("lap_return_cost", "return_cost_margin", note="c_H-B_{3.6}(M); not printed in the pinned manuscript"),
    from_xla("lap_return_post", "return_posterior_margin", note="tau(3.6)-M"),
    from_xla("lap_return_trade", "return_trade_margin", note="(1-1/b)rho m Delta_T(3.6)-k"),
    from_xla("lap_spread_increase", "spread_increase", display="0.272222", note="Delta_T(3.6)-Delta_T(3)=49/180"),
    from_xla("lap_rC", "rC", note="ceiling, Prop. A.4 (A.11)"),
    from_xla("lap_r2_minus_rC", "r2_minus_rC", note="3.6-r_C"),
    from_xla("lap_rN", "rN", note="no-trade existence boundary, Prop. A.4"),
    from_xla("lap_rU", "rU", note="sufficient full-order uniqueness bound, Prop. A.4"),
    from_xla("lap_r_unique_zero", "r_unique_zero", note="sufficient no-trade uniqueness bound r(k), Prop. A.4"),
    from_xla("lap_prior_lo", "prior_lower", note="prior window, lower end (binds B_3(M(pi))=c_H)"),
    from_xla("lap_prior_hi", "prior_upper", note="prior window for all three parts, upper end (binds B_{3.6}(M(pi))=c_H)"),
    from_xla("lap_prior_ii_hi", "prior_ii_upper", note="prior window for parts (i)-(ii), upper end"),
    from_xla("lap_cH_lo", "return_cH_lower", note="c_H window, lower end B_{3.6}(M)"),
    from_xla("lap_cH_hi", "return_cH_upper", note="c_H window, upper end B_3(M)"),
    from_xla("lap_xstar_r1", "strong_xstar", note="threshold flow at r=3, eq. (12)"),
    from_xla("lap_entry_r1", "strong_entry", note="entry at r=3, Prop. 2(ii)"),
    from_xla("lap_own_r1", "strong_ownership", note="high-class ownership at r=3"),
    from_xla("lap_frozen_r0_entry", "frozen_weak_entry",
             note="full orders imposed at r=1.2, challenger reoptimizes; pinned Table 2 labels the row numerical diagnostic; closed form"),
    from_xla("lap_frozen_r1_entry", "strong_entry", note="full orders imposed at r=3; equals the equilibrium entry"),
    from_xla("lap_access_proceeds_gain", "proceeds_gain", note="Prop. A.9 at r=3"),
    from_xla("lap_access_surplus_gain", "surplus_gain", note="Prop. A.9 at r=3"),
    from_xla("lap_hidden_surplus", "hidden_surplus", display="2.552083", note="net surplus, price hidden, 245/96"),
    from_xla("lap_access_surplus", "feedback_surplus", note="net surplus with price access at r=3"),
    from_xla("lap_stake_omegaU", "stake_omegaU", note="stake bound Omega_U, OA A.12"),
    from_xla("lap_A6_strong_entry_margin", "A6_strong_entry", note="B_3(M)-(c_H+0.1), Prop. A.6"),
    from_xla("lap_logistic_entry", "logistic_entry", note="entry at r=3 under logistic noise, Table 3"),
    from_xla("lap_caseD_A1_upper", "caseD_A1_upper", note="Table 4 case D fails (A1) upper by this amount"),
    from_xla("lap_moderate_A2_upper", "moderate_A2_upper", note="moderate-value vector (A.49), strong trade margin"),
    from_xla("lap_P3_entry_r155", "P3_1.55_entry", note="Prop. 3 entry enclosure at r=1.55 (independent)"),
    from_xla("lap_P3_entry_r160", "P3_1.60_entry", note="Prop. 3 entry enclosure at r=1.60 (independent)"),
    from_xla("lap_P3_entry_r165", "P3_1.65_entry", note="Prop. 3 entry enclosure at r=1.65 (independent)"),
    from_xla("lap_P3_GammaH_r155", "P3_1.55_Gamma_H", display=r"\ensuremath{7.6\times10^{-5}}",
             note="high-type global lower bound Gamma_H at 1.55"),
    from_xla("lap_P3_GammaH_r160", "P3_1.60_Gamma_H", display="0.002753", note="Gamma_H at 1.60"),
    from_xla("lap_P3_GammaH_r165", "P3_1.65_Gamma_H", display="0.005492", note="Gamma_H at 1.65"),
    from_xla("lap_P3_pool_r155", "P3_1.55_pooling_margin", display="0.007802", note="k-rho Delta_T/2 at 1.55 = 387/49600"),
    from_xla("lap_P3_pool_r160", "P3_1.60_pooling_margin", display="0.005938", note="19/3200"),
    from_xla("lap_P3_pool_r165", "P3_1.65_pooling_margin", display="0.003996", note="211/52800"),
    from_xla("lap_P3_psi_left_r155", "P3_1.55_Psi_left", display=r"\ensuremath{1.1\times10^{-10}}",
             note="Psi at the left end of the root bracket, 1.55"),
    from_xla("lap_P3_psi_right_r155", "P3_1.55_Psi_right", display=r"\ensuremath{-9.6\times10^{-11}}",
             note="Psi at the right end of the root bracket, 1.55"),
    from_xla("lap_P3_thr_r155", "P3_1.55_threshold_margin", display="0.028042", note="M_v-tau over the bracket, 1.55"),
    from_table("lap_P3_v_r155", "0.46031618", "0.460316", "computer-assisted", "main.tex",
               "sale magnitude v at 1.55, eq. (13) bracket [0.46031618, 0.46031620]"),
    from_table("lap_P3_v_r160", "0.70747537", "0.707475", "computer-assisted", "main.tex",
               "sale magnitude v at 1.60, eq. (13) bracket [0.70747537, 0.70747539]"),
    from_table("lap_P3_v_r165", "0.90333198", "0.903332", "computer-assisted", "main.tex",
               "sale magnitude v at 1.65, eq. (13) bracket [0.90333198, 0.90333201]"),
    from_table("lap_mixture_entry_r1", "0.522715", "0.522715", "analytical", "tables/table3_extensions.tex",
               "Laplace, cost mixture half-width 0.1, entry at r=3 (manuscript label)"),
    from_table("lap_signal_entry_r0", "0.85", "0.850000", "analytical", "tables/table3_extensions.tex",
               "complementary signals vector (A.50), weak entry"),
    from_table("lap_signal_entry_r1", "0.879438", "0.879438", "analytical", "tables/table3_extensions.tex",
               "complementary signals vector (A.50), strong entry"),
    from_table("lap_moderate_entry_r1", "0.526805", "0.526805", "analytical", "tables/table3_extensions.tex",
               "moderate-value vector (A.49), strong entry"),
    from_table("lap_reserve_excl_p", "101/100", "1.01", "input", "tables/table4_reserve_comparisons.tex",
               "reserve that excludes the low class, Table 5 Panel A"),
    from_table("lap_reserve_excl_r0_entry", "0.543573", "0.543573", "analytical", "tables/table4_reserve_comparisons.tex",
               "preparation at r=1.2, p=1.01, Table 5; unique continuation by the global bound"),
    from_table("lap_reserve_excl_r1_entry", "0.513373", "0.513373", "analytical", "tables/table4_reserve_comparisons.tex",
               "preparation at r=3, p=1.01, Table 5"),
    from_table("lap_caseA_entry_r1", "0.464564", "0.464564", "analytical", "tables/table_class_exhibit.tex",
               "Table 4 case A (prior 0.3), strong entry"),
    from_table("lap_caseB_entry_r1", "0.571808", "0.571808", "analytical", "tables/table_class_exhibit.tex",
               "Table 4 case B (prior 0.7), strong entry"),
    from_table("lap_caseC_entry_r1", "0.563404", "0.563404", "analytical", "tables/table_class_exhibit.tex",
               "Table 4 case C (wide classes), strong entry"),
    from_table("lap_gross_profit_unit", "0.140731", "0.140731", "numerical diagnostic", "main.tex",
               "informed investor's expected gross profit per unit at r=3, Section 6.1 (OA C.9); not recomputed in this project's audit"),
    from_table("lap_break_even_scale", "1.831923", "1.831923", "numerical diagnostic", "main.tex",
               "break-even trade scale, Section 6.1 (OA C.9); not recomputed in this project's audit"),
]

cols = ["key", "value", "display", "status", "source_script", "run_log", "note"]
with OUT.open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in cols})
        print(f"{r['key']:32s} {r['display']:28s} {r['status']}")
print(f"rows: {len(rows)} -> {OUT}")
