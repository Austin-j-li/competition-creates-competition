#!/usr/bin/env python3
"""Numbers and curves of the chart pages: backup B21 (research), backups B3 and B12, and the b25
variant of the entry chart. Writes src/data_charts.json.

Number ids and figure variants keep the names these pages had in an earlier deck (p18 is backup B21, show position 77;
b24 to b26 are B3, now show positions 25 to 27; b46 to b49 are B12, now 47 to 50, in the 20-page master). The dumps are
numbered by show position.

    python3 build_data_charts.py

Every printed number is a registry row (audit/slot_manuscript_2026_10_23/registry/registry.csv),
rounded half-up on the exact decimal or fraction to the digits the master prints, and checked
against the master's string in its dump (master_dump/). The registry key
behind each number is the one the earlier web deck uses for the same sentence
(presentation/content.js, frames b3b, b3c, b12b, b12c, b12d) or, for page 18, the research marks of
handout/figures.js; the source is recorded in each row. A mismatch is never forced: the row keeps
the master's string and says "mismatch": true.

Curves evaluate closed forms only (handout/figures.js: auction, lambdaR, entryResearch); every
boundary strength is read from its registry row. Nothing here searches for an equilibrium.
Standard library only; self-contained (it does not import build_data.py).
"""
from __future__ import annotations

import csv
import json
import math
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REGISTRY = ROOT / "audit/slot_manuscript_2026_10_23/registry/registry.csv"
DUMPS = HERE / "master_dump"
OUT = HERE / "src" / "data_charts.json"
COLUMNS = ["key", "value", "display", "status", "source_script", "run_log", "note"]


def read_registry() -> dict[str, dict]:
    with REGISTRY.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != COLUMNS:
            raise SystemExit(f"{REGISTRY}: columns {reader.fieldnames}, expected {COLUMNS}")
        rows = list(reader)
    out: dict[str, dict] = {}
    for row in rows:
        if row["key"] in out:
            raise SystemExit(f"{REGISTRY}: duplicate key {row['key']}")
        out[row["key"]] = row
    return out


REG = read_registry()


def exact(key: str) -> Fraction:
    return Fraction(REG[key]["value"].strip())


def half_up(x: Fraction, digits: int) -> str:
    sign = "-" if x < 0 else ""
    n = math.floor(abs(x) * 10 ** digits + Fraction(1, 2))
    s = str(n).rjust(digits + 1, "0")
    return sign + (s[:-digits] + "." + s[-digits:] if digits else s)


VULGAR = {Fraction(1, 2): "½", Fraction(1, 4): "¼", Fraction(3, 4): "¾"}


def coord(x) -> float:
    return float(half_up(Fraction(x), 6))


def shape_text(slide: str, shape: int) -> str:
    """The whole text of one shape of a dump, math included (numbers inside $...$ count)."""
    text, cur = [], None
    for line in (DUMPS / slide).read_text(encoding="utf-8").splitlines():
        if line.startswith(("SHAPE ", "TABLE ", "PICTURE ")):
            cur = int(line.split("id=")[1].split()[0])
            continue
        if line.startswith(("CLICK BUILDS", "LINK TARGETS")):
            cur = None
            continue
        if cur == shape:
            text.append(line)
    return "\n".join(text)


# (id, slide dump, shape id, master string, registry key, digits, source of the key)
P18 = "research marks of handout/figures.js (rR, entry_rR, rRbar, entry_cap, rQ, cap) and the r_C of frame b12c"
NUMBERS = [
    # page 18
    ("p18.cap", "slide77.txt", 20, "0.34", "res_cap", 2, P18),
    ("p18.shade.rR", "slide77.txt", 9, "1.50", "res_rR", 2, P18),
    ("p18.shade.rQ", "slide77.txt", 9, "2.17", "res_rQ", 2, P18),
    ("p18.sub.pi", "slide77.txt", 4, "½", "prim_pi", "fraction", "the declared prior of slot_data.py (the sub line)"),
    # B3, second page (content.js frame b3b)
    ("b25.entry_rA", "slide26.txt", 9, "0.454185", "entry_rA_B", 6, "content.js b3b {{entry_rA_B}}"),
    ("b25.rA", "slide26.txt", 9, "1.394", "rA", 3, "content.js b3b {{rA|3}}"),
    ("b25.entry_r0", "slide26.txt", 9, "0.250000", "entry_r0", 6, "content.js b3b {{entry_r0}}"),
    ("b25.plateau", "slide26.txt", 9, "0.522757", "entry_plateau_B", 6, "content.js b3b {{entry_plateau_B}}"),
    ("b25.rF", "slide26.txt", 9, "1.467", "rF_B", 3, "content.js b3b {{rF_B|3}}"),
    ("b25.rN", "slide26.txt", 9, "1.748", "rN", 3, "content.js b3b {{rN|3}}"),
    # B3, third page (content.js frame b3c)
    ("b26.rA", "slide27.txt", 28, "1.393958", "rA", 6, "content.js b3c {{rA}}"),
    ("b26.rF", "slide27.txt", 28, "1.467127", "rF_B", 6, "content.js b3c {{rF_B}}"),
    ("b26.rN", "slide27.txt", 28, "1.747878", "rN", 6, "content.js b3c {{rN}}"),
    ("b26.rJ", "slide27.txt", 28, "1.966097", "rJ", 6, "content.js b3c {{rJ}}"),
    ("b26.rS", "slide27.txt", 28, "2.124148", "rS_B", 6, "content.js b3c {{rS_B}}"),
    ("b26.rC", "slide27.txt", 28, "3.592659", "rC_B", 6, "content.js b3c {{rC_B}}"),
    # B12, second page (content.js frame b12b)
    ("b47.cap", "slide48.txt", 7, "0.336122", "res_cap", 6, "content.js b12b {{res_cap}}"),
    ("b47.rR", "slide48.txt", 8, "1.501", "res_rR", 3, "content.js b12b {{res_rR|3}}"),
    ("b47.entry_rR", "slide48.txt", 8, "0.500846", "res_entry_rR", 6, "content.js b12b {{res_entry_rR}}"),
    ("b47.rcap", "slide48.txt", 8, "1.678", "res_rcap", 3, "content.js b12b {{res_rcap|3}}"),
    ("b47.entry_cap", "slide48.txt", 8, "0.522757", "res_entry_cap", 6, "content.js b12b {{res_entry_cap}}"),
    # B12, third page (content.js frame b12c)
    ("b48.cap", "slide49.txt", 14, "0.336122", "res_cap", 6, "content.js b12c {{res_cap}}"),
    ("b48.rR", "slide49.txt", 14, "1.501023", "res_rR", 6, "content.js b12c {{res_rR}}"),
    ("b48.rcap", "slide49.txt", 14, "1.677633", "res_rcap", 6, "content.js b12c {{res_rcap}}"),
    ("b48.rN", "slide49.txt", 14, "1.747878", "res_rN", 6, "content.js b12c {{res_rN}}"),
    ("b48.rQ", "slide49.txt", 14, "2.166995", "res_rQ", 6, "content.js b12c {{res_rQ}}"),
    ("b48.rC", "slide49.txt", 14, "3.592659", "res_rC", 6, "content.js b12c {{res_rC}}"),
    ("b48.lambda_rR", "slide49.txt", 16, "0.193853", "res_lambda_rR", 6, "content.js b12c {{res_lambda_rR}}"),
    ("b48.entry_rR", "slide49.txt", 16, "0.500846", "res_entry_rR", 6, "content.js b12c {{res_entry_rR}}"),
    ("b48.entry_cap", "slide49.txt", 16, "0.522757", "res_entry_cap", 6, "content.js b12c {{res_entry_cap}}"),
    ("b48.rQ.3", "slide49.txt", 21, "2.167", "res_rQ", 3, "content.js b12c {{res_rQ|3}}"),
    # B12, fourth page (content.js frame b12d)
    ("b49.r155", "slide50.txt", 12, "1.55", "str_r155", 2, "content.js b12d {{str_r155}}"),
    ("b49.r160", "slide50.txt", 12, "1.60", "str_r160", 2, "content.js b12d {{str_r160}}"),
    ("b49.r165", "slide50.txt", 12, "1.65", "str_r165", 2, "content.js b12d {{str_r165}}"),
    ("b49.lambda_r155", "slide50.txt", 12, "0.237901", "res_lambda_r155", 6, "content.js b12d {{res_lambda_r155}}"),
    ("b49.lambda_r160", "slide50.txt", 12, "0.279037", "res_lambda_r160", 6, "content.js b12d {{res_lambda_r160}}"),
    ("b49.lambda_r165", "slide50.txt", 12, "0.316683", "res_lambda_r165", 6, "content.js b12d {{res_lambda_r165}}"),
    ("b49.entry_r155", "slide50.txt", 12, "0.507630", "res_entry_r155", 6, "content.js b12d {{res_entry_r155}}"),
    ("b49.entry_r160", "slide50.txt", 12, "0.513965", "res_entry_r160", 6, "content.js b12d {{res_entry_r160}}"),
    ("b49.entry_r165", "slide50.txt", 12, "0.519763", "res_entry_r165", 6, "content.js b12d {{res_entry_r165}}"),
]

# axis coordinates of page 18's chart (the master's tick labels; no registry row by nature)
AXIS = [("p18.chart.x.1", "slide77.txt", 22, "1"), ("p18.chart.x.125", "slide77.txt", 23, "1.25"),
        ("p18.chart.x.15", "slide77.txt", 24, "1.5"), ("p18.chart.x.175", "slide77.txt", 25, "1.75"),
        ("p18.chart.x.2", "slide77.txt", 26, "2"), ("p18.chart.y.zero", "slide77.txt", 21, "0")]


# tick labels of the three pictures redrawn on b24, b25 and b47 (axis coordinates, no registry row by
# nature; they stand in the master's pictures, not in its text, so there is no dump shape to check)
PIC_AXIS = [
    ("b24.ax.x.0", "0.0"), ("b24.ax.x.1", "0.1"), ("b24.ax.x.2", "0.2"),
    ("b24.ax.y.5", "0.5"), ("b24.ax.y.6", "0.6"), ("b24.ax.y.7", "0.7"),
    ("b25.ax.x.12", "1.2"), ("b25.ax.x.20", "2.0"), ("b25.ax.x.28", "2.8"), ("b25.ax.x.36", "3.6"),
    ("b25.ax.x.14", "1.4"), ("b25.ax.x.18", "1.8"), ("b25.ax.x.22", "2.2"),
    ("b25.ax.y.2", "0.2"), ("b25.ax.y.3", "0.3"), ("b25.ax.y.4", "0.4"), ("b25.ax.y.5", "0.5"),
    ("b25.ax.y.6", "0.6"),
]
PIC_WHERE = {"b24": "master picture 'Figure CoexRegion' (slide 26)",
             "b25": "master pictures 'Figure CoexPanelA', 'Figure CoexPanelC' (slide 27)"}


def build_numbers() -> tuple[dict, list]:
    numbers, log = {}, []
    for nid, slide, shape, master, key, digits, source in NUMBERS:
        # slide None: a retired row whose words left the master; kept until its page drops the span
        in_dump = master in shape_text(slide, shape) if slide else True
        row: dict = {"key": key, "kind": "value", "digits": digits}
        if digits == "fraction":
            row.update(digits=None, format="fraction")
        if key not in REG:
            row.update(text=master, mismatch=True, missing_key=True)
        else:
            text = VULGAR.get(exact(key), "") if digits == "fraction" else half_up(exact(key), digits)
            mismatch = text != master or not in_dump
            row.update(text=master if mismatch else text, mismatch=mismatch,
                       value=REG[key]["value"], status=REG[key]["status"])
        row.update(master=master, where=f"{slide} shape {shape}", source=source)
        if not in_dump:
            row["comment"] = "the master's string was not found in that shape of the dump"
        numbers[nid] = row
        log.append(f"{nid:20s} {key:18s} {row['text']:>10s}  master {master:>10s}"
                   + ("  MISMATCH" if row["mismatch"] else ""))
    for nid, slide, shape, label in AXIS:
        ok = label in shape_text(slide, shape)
        numbers[nid] = {"key": None, "kind": "axis", "digits": None, "text": label, "master": label,
                        "mismatch": not ok, "where": f"{slide} shape {shape}"}
        log.append(f"{nid:20s} {'(axis)':18s} {label:>10s}" + ("" if ok else "  NOT IN DUMP"))
    for nid, label in PIC_AXIS:
        numbers[nid] = {"key": None, "kind": "axis", "digits": None, "text": label, "master": label,
                        "mismatch": False, "where": PIC_WHERE[nid[:3]]}
    log.append(f"{len(PIC_AXIS)} picture axis rows (b24, b25)")
    return numbers, log


# ------------------------------------------------------------------ closed forms (handout/figures.js)
h, ell, p = exact("prim_h"), exact("prim_ell"), exact("prim_p")
rho, k = exact("prim_rho"), exact("prim_k")
beta, a = exact("beta_B"), exact("res_a")
CAP = exact("res_cap")
rR, rRbar, rN, rQ, rC = exact("res_rR"), exact("res_rcap"), exact("res_rN"), exact("res_rQ"), exact("res_rC")
r0, r1, r2 = exact("prim_r0"), exact("prim_r1"), exact("prim_r2")
ENTRY_CAP = exact("res_entry_cap")


def Delta(r: Fraction) -> Fraction:
    """figures.js auction(): Delta_T = (r - ell)^2/(2r)."""
    return (r - ell) ** 2 / (2 * r)


def lambda_R(r: Fraction) -> float:
    """figures.js lambdaR(): the positive root of A x^2 + B x + C (recruiting research below the cap)."""
    D = Delta(r)
    A2 = 2 * a * (1 - 2 * beta)
    B1 = 4 * a * beta + k * (1 - 2 * beta) + beta * D
    C0 = beta * (2 * k - D)
    disc = B1 * B1 - 4 * A2 * C0
    return float((-B1 + Fraction(math.sqrt(disc))) / (2 * A2))


def entry_research(lam) -> float:
    """figures.js entryResearch(): rho + (1 - rho)[beta + (1/2 - beta) lambda]."""
    return float(rho + (1 - rho) * (beta + (Fraction(1, 2) - beta) * Fraction(lam)))


def grid(lo: Fraction, hi: Fraction, n: int) -> list[Fraction]:
    return [lo + (hi - lo) * i / n for i in range(n + 1)]


def research_data() -> tuple[dict, list]:
    log = []
    rise = grid(rR, rRbar, 40)
    lam = [lambda_R(r) for r in rise]
    # the curve's ends are registry rows; the closed form must meet them
    log.append(f"lambda_R(r_R)    = {lam[0]:.9f}   res_lambda_rR = {float(exact('res_lambda_rR')):.9f}")
    log.append(f"lambda_R(r_cap)  = {lam[-1]:.9f}   res_cap       = {float(CAP):.9f}")
    log.append(f"entry(lambda_R(r_R)) = {entry_research(lam[0]):.9f}   res_entry_rR  = {float(exact('res_entry_rR')):.9f}")
    log.append(f"entry(cap)       = {entry_research(CAP):.9f}   res_entry_cap = {float(ENTRY_CAP):.9f}")
    for key in ("res_lambda_r155", "res_lambda_r160", "res_lambda_r165"):
        r = exact("str_r" + key[-3:])
        log.append(f"lambda_R({float(r):.2f})  = {lambda_R(r):.9f}   {key} = {float(exact(key)):.9f}")
    lam[0], lam[-1] = float(exact("res_lambda_rR")), float(CAP)      # ends exactly at the rows
    ent = [entry_research(x) for x in lam]
    ent[0], ent[-1] = float(exact("res_entry_rR")), float(ENTRY_CAP)
    strengths = {n: coord(v) for n, v in (("rR", rR), ("rcap", rRbar), ("rN", rN), ("rQ", rQ), ("rC", rC),
                                          ("r0", r0), ("r1", r1), ("r2", r2))}
    keys = {"rR": "res_rR", "rcap": "res_rcap", "rN": "res_rN", "rQ": "res_rQ", "rC": "res_rC",
            "r0": "prim_r0", "r1": "prim_r1", "r2": "prim_r2"}
    # page 18: the master's axis runs from 1 (x = 118 pt) to its arrow tip at 548 pt, 350 pt per unit;
    # research 0 sits 10 pt above the strength axis and the cap 154 pt above 0, the axis top 189 pt
    p18_x = [1.0, coord(1 + Fraction(430, 350))]
    p18_y = [coord(-CAP * Fraction(10, 154)), coord(CAP * Fraction(189, 154))]
    out = {
        "cap": coord(CAP), "rho": coord(rho), "entry_cap": coord(ENTRY_CAP),
        "lambda_rR": coord(exact("res_lambda_rR")), "entry_rR": coord(exact("res_entry_rR")),
        "strengths": strengths, "strength_keys": keys,
        "rise": {"lambda": [[coord(r), round(y, 6)] for r, y in zip(rise, lam)],
                 "entry": [[coord(r), round(y, 6)] for r, y in zip(rise, ent)],
                 "closed_form": "handout/figures.js lambdaR, entryResearch; ends set to res_lambda_rR/res_cap "
                                "and res_entry_rR/res_entry_cap"},
        "pages": {
            "p18": {"x_range": p18_x, "y_range": p18_y,
                    "x_ticks": [{"r": 1.0, "num": "p18.chart.x.1"}, {"r": 1.25, "num": "p18.chart.x.125"},
                                {"r": 1.5, "num": "p18.chart.x.15"}, {"r": 1.75, "num": "p18.chart.x.175"},
                                {"r": 2.0, "num": "p18.chart.x.2"}],
                    "y_ticks": [{"y": 0.0, "num": "p18.chart.y.zero"},
                                {"y": coord(CAP), "num": "p18.cap", "prefix_label": "charts.lambdabar",
                                 "prefix_join": " = "}],
                    "shade": {"from": "rR", "to": "rQ"}},
            "b47": {"x_range": [coord(r0 - Fraction(1, 10)), coord(r2 + Fraction(1, 10))],
                    "panels": {"lambda": {"y_range": [-0.03, 0.4]}, "entry": {"y_range": [0.2, 0.56]}}},
        },
    }
    return out, log


# ------------------------------------------------------------------ b24 and b25 (figures.js auction, entryR, entryT,
# plateau; lambdaQ for b47). Inputs are registry rows: M(1/2) = M_half_B, b = b_B, the prior pi = prim_pi.
cH, PI = exact("prim_cH"), exact("prim_pi")
M_HALF, B_SMALL = exact("M_half_B"), exact("b_B")
PLATEAU = exact("entry_plateau_B")
rA_, rF_, rN_, rJ_, rS_, rC_ = (exact(k_) for k_ in ("rA", "rF_B", "rN", "rJ", "rS_B", "rC_B"))


def gH(r: Fraction) -> Fraction:
    return h - r / 2 - p * p / (2 * r)


def gL(r: Fraction) -> Fraction:
    return (ell * ell - p * p) / (2 * r)


def tau(r: Fraction) -> Fraction:
    """figures.js auction(): tau = (c_H - g_L)/(g_H - g_L)."""
    return (cH - gL(r)) / (gH(r) - gL(r))


def J(r: Fraction) -> Fraction:
    return Delta(r) * (1 - tau(r))


def entry_R(r: Fraction) -> float:
    """figures.js entryR(): rho + (1 - rho) b Delta/(2k), the mixed purchase R."""
    return float(rho + (1 - rho) * B_SMALL * Delta(r) / (2 * k))


def entry_T(r: Fraction) -> float:
    """figures.js entryT(): rho + (b/2)(k - rho J)/(Delta (1 - tau)^2), the threshold pair T."""
    return float(rho + (B_SMALL / 2) * (k - rho * J(r)) / (Delta(r) * (1 - tau(r)) ** 2))


def frak(d: Fraction) -> Fraction:
    """The root above ell of Delta(r) = d (make_figures_src.py frak)."""
    return ell + d + Fraction(math.sqrt(d * d + 2 * ell * d))


def lambda_Q(r: Fraction) -> float:
    """figures.js lambdaQ(): floor-entry research, the root in [0, 1) of a lambda = rho Delta m_lambda - k."""
    D = Delta(r)
    A2 = a * (1 - 2 * beta)
    B1 = rho * D * beta + k * (1 - 2 * beta) + 2 * a * beta
    C0 = beta * (2 * k - rho * D)
    return float(-2 * C0 / (B1 + Fraction(math.sqrt(B1 * B1 - 4 * A2 * C0))))


def pt(x, y) -> list:
    return [coord(x), coord(y)]


def region_b24() -> tuple[dict, list]:
    """b24: the coexistence region in the plane (Delta_T, tau) at pi = 1/2 and the example's path through it."""
    log = []
    hi_pi = max(PI, 1 - PI)
    d_lo = lambda t: k / (1 - t)                       # the lower bound of the page's inequality
    d_hi = k / (rho * hi_pi)                           # its upper bound at pi = 1/2
    d_split = k / (1 - M_HALF)                         # where the informed trader starts to buy for sure
    taus = grid(PI, M_HALF, 60)
    left = [pt(d_lo(t), t) for t in taus]
    region = left + [pt(d_hi, M_HALF), pt(d_hi, PI)]
    x_end = Fraction(1, 5)                             # the path leaves the plot at its right edge
    r_end = frak(x_end + Fraction(3, 1000))            # the arrowhead's tip stands just past the edge
    path_ink = [pt(Delta(r), tau(r)) for r in grid(r0, rA_, 30)]
    path_up = [pt(Delta(r), tau(r)) for r in grid(rA_, r_end, 80)]
    marks = {n: pt(Delta(r), tau(r)) for n, r in (("r0", r0), ("rA", rA_), ("rF", rF_), ("rN", rN_))}
    # agreements with the registry
    log.append(f"b24 Delta(r_A) = {float(Delta(rA_)):.12f}   Delta_rA = {float(exact('Delta_rA')):.12f}")
    log.append(f"b24 tau(r_A)   = {float(tau(rA_)):.12f}   tau_rA   = {float(exact('tau_rA')):.12f}")
    log.append(f"b24 k/(1-tau(r_A)) = {float(d_lo(tau(rA_))):.12f} (r_A on the lower bound)")
    log.append(f"b24 Delta(r_F) = {float(Delta(rF_)):.12f}   k/(1-M) = {float(d_split):.12f}")
    log.append(f"b24 Delta(r_N) = {float(Delta(rN_)):.12f}   k/(rho max(pi,1-pi)) = {float(d_hi):.12f}")
    log.append(f"b24 tau(r0) = {float(tau(r0)):.9f}   tau_r0 = {float(exact('tau_r0')):.9f}")
    t_end = tau(frak(x_end))
    log.append(f"b24 tau where Delta = 0.2: {float(t_end):.6f} <= M(1/2) = {float(M_HALF):.6f}: {t_end <= M_HALF}"
               " (the path from r_A to the plot's edge stays where the informative market exists)")
    if not t_end <= M_HALF:
        raise SystemExit("b24: the path leaves tau <= M inside the plot; the green stretch would be false")
    gap = min(J(r) - k for r in grid(rA_, r_end, 400)[1:])
    log.append(f"b24 min of Delta(1 - tau) - k over (r_A, edge] = {float(gap):.6g} >= 0: {gap >= 0}"
               " (the path stays right of the lower bound k/(1 - tau))")
    if gap < 0:
        raise SystemExit("b24: the path crosses back over the lower bound; the green stretch would be false")
    return {
        "x_range": [0.0, 0.2], "y_range": [0.45, 0.765],
        "x_ticks": [{"v": 0.0, "num": "b24.ax.x.0"}, {"v": 0.1, "num": "b24.ax.x.1"}, {"v": 0.2, "num": "b24.ax.x.2"}],
        "y_ticks": [{"v": 0.5, "num": "b24.ax.y.5"}, {"v": 0.6, "num": "b24.ax.y.6"}, {"v": 0.7, "num": "b24.ax.y.7"}],
        "region": region,
        "lower": left,
        "upper": [pt(d_hi, PI), pt(d_hi, M_HALF)],
        "top": [left[-1], pt(d_hi, M_HALF)],
        "split": [pt(d_split, PI), pt(d_split, M_HALF)],
        "M": coord(M_HALF), "pi": coord(PI), "x_lo": 0.0, "x_hi": 0.2, "d_hi": coord(d_hi), "d_split": coord(d_split),
        "path_ink": path_ink, "path_up": path_up, "marks": marks,
        "keys": {"M": "M_half_B", "pi": "prim_pi", "k": "prim_k", "rho": "prim_rho", "r0": "prim_r0", "rA": "rA",
                 "rF": "rF_B", "rN": "rN"},
        "closed_form": "figures.js auction(): Delta = (r - ell)^2/(2r), tau = (c_H - g_L)/(g_H - g_L); "
                       "lower bound k/(1 - tau), upper bound k/(rho max{pi, 1 - pi}), split k/(1 - M(1/2))",
    }, log


def entry_b25() -> tuple[dict, list]:
    """b25: the master's panels (a) and (c), entry against strength with the branches N, R, F, Q, T."""
    log = []
    ent_A = exact("entry_rA_B")
    R = [pt(r, entry_R(r)) for r in grid(rA_, rF_, 40)]
    T = [pt(r, entry_T(r)) for r in grid(rA_, rJ_, 80)]
    R[0], R[-1] = pt(rA_, ent_A), pt(rF_, PLATEAU)          # ends exactly at the rows
    T[0], T[-1] = pt(rA_, ent_A), pt(rJ_, rho)
    log.append(f"b25 entryR(r_A) = {entry_R(rA_):.9f}   entryT(r_A) = {entry_T(rA_):.9f}   entry_rA_B = {float(ent_A):.9f}")
    log.append(f"b25 entryR(r_F) = {entry_R(rF_):.9f}   entry_plateau_B = {float(PLATEAU):.9f}")
    log.append(f"b25 entryT(r_J) = {entry_T(rJ_):.9f}   rho = {float(rho):.9f}")
    for n in ("155", "160", "165"):
        r = exact("str_r" + n)
        log.append(f"b25 entryT({float(r):.2f}) = {entry_T(r):.9f}   entry_th_r{n}_B = {float(exact('entry_th_r' + n + '_B')):.9f}")
    branches = {
        "N": [pt(r0, rho), pt(rN_, rho)],
        "Q": [pt(rN_, rho), pt(rJ_, rho)],
        "R": R,
        "F": [pt(rF_, PLATEAU), pt(rC_, PLATEAU)],
        "Ffloor": [pt(rC_, rho), pt(r2, rho)],
        "T": T,
    }
    S = {n: coord(v) for n, v in (("rA", rA_), ("rF", rF_), ("rN", rN_), ("rJ", rJ_), ("rS", rS_), ("rC", rC_))}
    c_range = [1.25, 2.35]
    return {
        "rho": coord(rho), "plateau": coord(PLATEAU), "entry_rA": coord(ent_A),
        "strengths": S,
        "strength_keys": {"rA": "rA", "rF": "rF_B", "rN": "rN", "rJ": "rJ", "rS": "rS_B", "rC": "rC_B",
                          "r0": "prim_r0", "r2": "prim_r2"},
        "branches": branches,
        "panels": {
            "a": {"x_range": [coord(r0), coord(r2)], "y_range": [0.15, 0.62],
                  "x_ticks": [{"v": 1.2, "num": "b25.ax.x.12"}, {"v": 2.0, "num": "b25.ax.x.20"},
                              {"v": 2.8, "num": "b25.ax.x.28"}, {"v": 3.6, "num": "b25.ax.x.36"}],
                  "y_ticks": [{"v": v / 10, "num": f"b25.ax.y.{v}"} for v in range(2, 7)],
                  "guides": ["rA", "rN", "rC"],
                  "zoom": c_range, "zoom_y": 0.585},
            "c": {"x_range": c_range, "y_range": [0.12, 0.62],
                  "x_ticks": [{"v": 1.4, "num": "b25.ax.x.14"}, {"v": 1.8, "num": "b25.ax.x.18"},
                              {"v": 2.2, "num": "b25.ax.x.22"}],
                  "y_ticks": [{"v": v / 10, "num": f"b25.ax.y.{v}"} for v in range(2, 7)],
                  "guides": ["rA", "rF", "rN", "rJ", "rS"]},
        },
        "shade": {"from": "rA", "to": "rN"},
        "closed_form": "figures.js entryR, entryT, plateau; ends set to entry_rA_B, entry_plateau_B, rho",
    }, log


def floor_entry_b47() -> tuple[dict, list]:
    """b47: floor-entry research on (r_N, r_Q): lambda_Q(Delta(r)) and entry rho."""
    log = []
    rr = grid(rN, rQ, 60)
    lam = [lambda_Q(r) for r in rr]
    lq = exact("res_lambda_floor_rQ")
    log.append(f"b47 lambda_Q(r_N) = {abs(lam[0]):.12f} (0: the branch starts on zero research)")
    log.append(f"b47 lambda_Q(r_Q) = {lam[-1]:.9f}   res_lambda_floor_rQ = {float(lq):.9f}")
    lam[0], lam[-1] = 0.0, float(lq)
    return {"lambda": [[coord(r), round(y, 6)] for r, y in zip(rr, lam)],
            "entry": [[coord(rN), coord(rho)], [coord(rQ), coord(rho)]],
            "lambda_rQ": coord(lq),
            "closed_form": "figures.js lambdaQ; ends set to 0 at r_N and res_lambda_floor_rQ at r_Q"}, log


def main() -> None:
    numbers, nlog = build_numbers()
    research, rlog = research_data()
    floor, flog = floor_entry_b47()
    research["floor_entry"] = floor
    region, glog = region_b24()
    panels, plog = entry_b25()
    rlog += flog + glog + plog
    data = {"meta": {"writer": "build_data_charts.py", "registry": str(REGISTRY.relative_to(ROOT))},
            "numbers": numbers, "research": research, "region": {"b24": region, "b25": panels}}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\n".join(nlog))
    print("\n".join(rlog))
    bad = [n for n, r in numbers.items() if r["mismatch"]]
    print(f"wrote {OUT.relative_to(ROOT)}: {len(numbers)} numbers, {len(bad)} mismatch {bad}")


if __name__ == "__main__":
    main()
