#!/usr/bin/env python3
"""build_data.py: writes src/data.json, the numbers, marked strengths and curves of the demo.

    python3 build_data.py            # writes src/data.json beside this file and prints a check table

Sources (all read, none written):
  - the number registry, audit/slot_manuscript_2026_10_23/registry/registry.csv (key, value, display, ...);
  - the master's page dumps, numbered by show position: master_dump/slide19.txt (main page 18, the numerical
    example), slide20.txt (page 19, the entry chart), slide21.txt (page 20), slide23.txt (page 22), from which
    every master string is read by shape id, never typed here. The data names p14, p16 and p17 (number ids,
    curves.pages, the entry chart's variants) are the names the chart pages 19, 20 and 22 had in an earlier
    deck; "example" is page 18. They are names, not page numbers.

Every printed number is a registry row rounded half-up on its exact value (a Fraction parsed from the
registry's decimal or fraction string; never a binary float). The curves evaluate the closed forms of the
example (ported below, each with the function it comes from) at registry declarations; a boundary strength
is always a registry row and is compared with other rows only, never recomputed and never decided by the
sign of a margin. Nothing here searches for an equilibrium. Curve coordinates are written with 6 decimals;
they are drawing coordinates and are never printed. Standard library only.
"""
from __future__ import annotations

import csv
import decimal
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[0]
REGISTRY = ROOT / "audit/slot_manuscript_2026_10_23/registry/registry.csv"
DUMPS = HERE / "master_dump"
OUT = HERE / "src" / "data.json"
COLUMNS = ["key", "value", "display", "status", "source_script", "run_log", "note"]


# ------------------------------------------------------------------ registry
def read_registry() -> dict[str, dict]:
    """Same reading as handout/slot_data.py: read_registry."""
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
    """A registry value as an exact rational (decimal, fraction or exponent string)."""
    return Fraction(REG[key]["value"].strip())


# ------------------------------------------------------------------ exact rounding
def half_up(x: Fraction, digits: int) -> str:
    """x rounded half-up (away from zero on a tie) to `digits` decimals, exactly."""
    sign = "-" if x < 0 else ""
    n = math.floor(abs(x) * 10 ** digits + Fraction(1, 2))
    s = str(n).rjust(digits + 1, "0")
    return sign + (s[:-digits] + "." + s[-digits:] if digits else s)


VULGAR = {Fraction(1, 2): "½", Fraction(1, 4): "¼", Fraction(3, 4): "¾"}


def coord(x: Fraction) -> float:
    """A drawing coordinate: 6 decimals, written through the decimal string (shortest float repr)."""
    return float(half_up(x, 6))


def sci(x: Fraction) -> str:
    """A small difference for the build log, in decimal (exponent) notation; never printed on a page."""
    if x == 0:
        return "0"
    with decimal.localcontext() as ctx:
        ctx.prec = 3
        return str(decimal.Decimal(x.numerator) / decimal.Decimal(x.denominator))


# ------------------------------------------------------------------ master dumps
SHAPE_RE = re.compile(r"^SHAPE id=(\d+) '([^']*)' box=x=([\d.]+) y=([\d.]+) w=([\d.]+) h=([\d.]+)")
RUN_RE = re.compile(r"\[[^\]]*\]\{([^}]*)\}")       # a text run [attrs]{text}; math ($...$) is left out
NUM_RE = re.compile(r"\d+(?:\.\d+)?|[½¼¾]")
MATH_RE = re.compile(r"\$([^$]*)\$")
SCRIPT_RE = re.compile(r"[_^](?:\{[^{}]*\}|\w)")   # sub- and superscripts (r_{0}, c_{H}) are not numbers


def read_dump(name: str) -> dict[int, dict]:
    shapes: dict[int, dict] = {}
    cur = None
    for line in (DUMPS / name).read_text(encoding="utf-8").splitlines():
        m = SHAPE_RE.match(line)
        if m:
            cur = int(m.group(1))
            shapes[cur] = {"name": m.group(2), "box": tuple(float(v) for v in m.group(3, 4, 5, 6)), "lines": []}
            continue
        if line.startswith(("CLICK BUILDS", "LINK TARGETS")):
            cur = None
            continue
        if cur is not None and line.strip().startswith(("|", "<br>")):
            shapes[cur]["lines"].append("".join(RUN_RE.findall(line)))
            shapes[cur].setdefault("math", []).extend(SCRIPT_RE.sub("", m) for m in MATH_RE.findall(line))
    for s in shapes.values():
        s["text"] = " ".join(s["lines"])
        s["math"] = s.get("math", [])
    return shapes


DUMP = {"p14": ("slide20.txt", read_dump("slide20.txt")), "p16": ("slide21.txt", read_dump("slide21.txt")),
        "p17": ("slide23.txt", read_dump("slide23.txt")), "example": ("slide19.txt", read_dump("slide19.txt"))}


def master_string(page: str, shape: int, occ: int | str) -> str | None:
    """The occ-th numeral of a shape's words, or with occ = "mN" the N-th numeral of its mathematics."""
    shapes = DUMP[page][1]
    if shape not in shapes:
        return None
    if isinstance(occ, str):
        found = NUM_RE.findall(" ".join(shapes[shape]["math"]))
        occ = int(occ[1:])
    else:
        found = NUM_RE.findall(shapes[shape]["text"])
    return found[occ] if occ < len(found) else None


# ------------------------------------------------------------------ the printed numbers
# (id, page, dump shape, occurrence of a numeral in that shape's words, registry key, digits or "fraction",
#  kind, alternative rows with the same printed string, comment)
# kind: "value" is a registry row; "axis" is an axis coordinate label (no registry row by nature).
NUMBERS = [
    # page 14, chart
    ("p14.chart.y.plateau", "p14", 22, 0, "entry_r1_B", 2, "value", ["entry_plateau_B", "p2_base_r1_entry"], ""),
    ("p14.chart.y.rho", "p14", 23, 0, "prim_rho", 2, "value", ["entry_r0"],
     "label 'rho = 0.25'; build_results.js used entry_r0 (same 1/4); prim_rho is the declared rho of slot_data.py"),
    ("p14.chart.y.zero", "p14", 24, 0, None, 0, "axis", [], ""),
    ("p14.chart.x.1", "p14", 25, 0, None, 0, "axis", [], ""),
    ("p14.chart.x.rA", "p14", 44, 0, "rA", 2, "value", ["res_rA"], ""),
    ("p14.chart.x.rJ", "p14", 45, 0, "rJ", 2, "value", [],
     "build_results.js (13 Nov) printed rN here; the master now prints 1.97 = rJ"),
    ("p14.chart.x.3", "p14", 26, 0, None, 0, "axis", [], ""),
    ("p14.chart.x.4", "p14", 27, 0, None, 0, "axis", [], ""),
    # main page 16 (data name p14), the two run-ins beside the chart
    ("p14.rhs.plateau.1", "p14", 109, 0, "entry_r1_B", 2, "value", ["entry_plateau_B"], ""),
    ("p14.rhs.rF", "p14", 109, "m0", "rF_B", 2, "value", [], "the ramp reaches the plateau at rF; the old text said rA"),
    ("p14.rhs.plateau.2", "p14", 109, 1, "entry_r1_B", 2, "value", [], ""),
    ("p14.rhs.rC.1", "p14", 109, "m1", "rC_B", 2, "value", [], ""),
    ("p14.rhs.rC.2", "p14", 110, 0, "rC_B", 2, "value", [], ""),
    ("p14.rhs.rho", "p14", 111, "m0", "prim_rho", 2, "value", ["entry_r0"], ""),
    # page 14, the note
    ("p14.note.h", "p14", 101, 0, "prim_h", 0, "value", [], ""),
    ("p14.note.ell", "p14", 101, 1, "prim_ell", 0, "value", [], ""),
    ("p14.note.p", "p14", 101, 2, "prim_p", "fraction", "value", [], ""),
    ("p14.note.pi", "p14", 101, 3, "prim_pi", "fraction", "value", [], ""),
    ("p14.note.rho", "p14", 101, 4, "prim_rho", "fraction", "value", [], ""),
    # page 16, chart
    ("p16.chart.y.plateau", "p16", 22, 0, "entry_r1_B", 2, "value", ["p4_frozen_entry_below_ceiling"], ""),
    ("p16.chart.y.rho", "p16", 23, 0, "prim_rho", 2, "value", ["entry_r0"], ""),
    ("p16.chart.y.zero", "p16", 24, 0, None, 0, "axis", [], ""),
    ("p16.chart.x.1", "p16", 25, 0, None, 0, "axis", [], ""),
    ("p16.chart.x.2", "p16", 26, 0, None, 0, "axis", [], ""),
    ("p16.chart.x.3", "p16", 27, 0, None, 0, "axis", [], ""),
    ("p16.chart.x.rC", "p16", 37, 0, "rC_B", 2, "value", [], ""),
    ("p16.chart.x.4", "p16", 28, 0, None, 0, "axis", [], ""),
    # page 17, chart
    ("p17.chart.y.plateau", "p17", 22, 0, "entry_r1_B", 2, "value", [], ""),
    ("p17.chart.y.rho", "p17", 23, 0, "prim_rho", 2, "value", ["entry_r0"], ""),
    ("p17.chart.y.zero", "p17", 24, 0, None, 0, "axis", [], ""),
    ("p17.chart.x.1", "p17", 25, 0, None, 0, "axis", [], ""),
    ("p17.chart.x.rA", "p17", 49, 0, "rA", 2, "value", [], ""),
    ("p17.chart.x.rJ", "p17", 50, 0, "rJ", 2, "value", [], ""),
    ("p17.chart.x.3", "p17", 26, 0, None, 0, "axis", [], ""),
    ("p17.chart.x.4", "p17", 27, 0, None, 0, "axis", [], ""),
    # main page 17 (data name p16), "In the example"
    ("p16.text.frozen", "p16", 64, "m0", "p4_frozen_entry_below_ceiling", 2, "value", ["entry_r1_B"],
     "orders held fixed: flat at 0.52 from r0 to r1"),
    ("p16.text.rho", "p16", 65, "m0", "prim_rho", 2, "value", ["p2_base_hidden_entry"], "price hidden: flat at rho"),
    # main page 18, the numerical example (data name example): kicker, table, band, note
    ("example.r0", "example", 106, "m0", "prim_r0", 1, "value", [], "also printed in the head of the weak column"),
    ("example.r1", "example", 106, "m1", "prim_r1", 0, "value", [], "also printed in the head of the strong column"),
    ("example.r2", "example", 106, "m2", "prim_r2", 1, "value", [], "also printed in the head of the very strong column"),
    ("example.spread.r0", "example", 114, 0, "Delta_r0", 3, "value", ["p2_base_r0_delta"], ""),
    ("example.spread.r1", "example", 115, 0, "Delta_r1", 3, "value", ["p2_base_r1_delta"], ""),
    ("example.spread.r2", "example", 116, 0, "Delta_r2", 3, "value", ["p2_base_r2_delta"], ""),
    ("example.k", "example", 117, "m0", "prim_k", 2, "value", [], "order cost k = 0.02"),
    ("example.bprior.r0", "example", 120, 0, "Bprior_r0", 2, "value", ["B_r0_half"], ""),
    ("example.bprior.r1", "example", 121, 0, "Bprior_r1_B", 2, "value", ["B_r1_half"], ""),
    ("example.bprior.r2", "example", 122, 0, "Bprior_r2", 2, "value", ["p2_base_r2_low_profit_zero"], ""),
    ("example.cH.1", "example", 123, "m0", "prim_cH", 0, "value", [], "diligence cost c_H = 6"),
    ("example.bpurchase.r0", "example", 126, 0, "p2_base_r0_low_profit_plus", 2, "value", ["Bprior_r0"],
     "no informed order at r0, so the belief after a purchase is the prior"),
    ("example.bpurchase.r1", "example", 127, 0, "p2_base_r1_low_profit_plus", 2, "value", [], "B_{r1}(M(1/2))"),
    ("example.bpurchase.r2", "example", 128, 0, "p2_base_r2_low_profit_plus", 3, "value", [],
     "B_{r2}(M(1/2)); 3 digits, so that it does not print as 6.00 beside c_H = 6"),
    ("example.cH.2", "example", 129, "m0", "prim_cH", 0, "value", [], ""),
    ("example.entry.r0", "example", 132, 0, "entry_r0", 2, "value", ["p2_base_r0_entry"], ""),
    ("example.entry.r1", "example", 133, 0, "entry_r1_B", 2, "value", ["p2_base_r1_entry"], ""),
    ("example.entry.r2", "example", 134, 0, "entry_r2", 2, "value", ["p2_base_r2_entry"], ""),
    ("example.rho", "example", 135, "m0", "prim_rho", 2, "value", ["entry_r0"], "entry floor rho = 0.25"),
    ("example.band.bpurchase.r1", "example", 138, "m0", "p2_base_r1_low_profit_plus", 2, "value", [], "6.22 > c_H"),
    ("example.band.bpurchase.r2", "example", 138, "m1", "p2_base_r2_low_profit_plus", 3, "value", [], "5.997 < c_H"),
    ("example.note.h", "example", 101, 0, "prim_h", 0, "value", [], ""),
    ("example.note.ell", "example", 101, 1, "prim_ell", 0, "value", [], ""),
    ("example.note.p", "example", 101, 2, "prim_p", "fraction", "value", [], ""),
    ("example.note.pi", "example", 101, 3, "prim_pi", "fraction", "value", [], ""),
    ("example.note.rho", "example", 101, 4, "prim_rho", "fraction", "value", [], ""),
    # page 17, the note
    ("p17.note.rA", "p17", 59, 0, "rA", 2, "value", [], ""),
    ("p17.note.rJ", "p17", 59, 1, "rJ", 2, "value", [], ""),
    # the strength control (not in the master; master is null)
    ("ctl.r.r0", None, None, None, "prim_r0", 1, "value", [], ""),
    ("ctl.r.rA", None, None, None, "rA", 2, "value", [], ""),
    ("ctl.r.rJ", None, None, None, "rJ", 2, "value", [], ""),
    ("ctl.r.r1", None, None, None, "prim_r1", 0, "value", [], ""),
    ("ctl.r.rC", None, None, None, "rC_B", 2, "value", [], ""),
    ("ctl.r.r2", None, None, None, "prim_r2", 1, "value", [], ""),
    ("ctl.entry.r0", None, None, None, "entry_r0", 2, "value", [], ""),
    ("ctl.entry.rho", None, None, None, "prim_rho", 2, "value", [], "entry rho of the branch with no informed order at 1.39"),
    ("ctl.entry.rA", None, None, None, "entry_rA_B", 2, "value", [],
     "printed nowhere in the master; it is the start of the ramp at 1.39"),
    ("ctl.entry.plateau", None, None, None, "entry_r1_B", 2, "value", [], ""),
    ("ctl.entry.r2", None, None, None, "entry_r2", 2, "value", [], ""),
]

# The axis labels are coordinates; their value is the label itself.
AXIS_VALUE = {"0": Fraction(0), "1": Fraction(1), "2": Fraction(2), "3": Fraction(3), "4": Fraction(4)}
AXIS_FROM_ID = {"zero": "0", "1": "1", "2": "2", "3": "3", "4": "4"}


def build_numbers() -> tuple[dict, list]:
    numbers, table = {}, []
    for nid, page, shape, occ, key, digits, kind, alts, comment in NUMBERS:
        master = master_string(page, shape, occ) if page else None
        entry: dict = {"key": key, "kind": kind}
        if kind == "axis":
            label = AXIS_FROM_ID[nid.rsplit(".", 1)[1]]
            text, value = label, AXIS_VALUE[label]
            entry.update(digits=0, text=text)
        elif key not in REG:
            text, value = master, None
            entry.update(digits=digits, text=text, missing_key=True)
        else:
            value = exact(key)
            if digits == "fraction":
                text = VULGAR.get(value)
                entry.update(digits=None, format="fraction", text=text)
            else:
                text = half_up(value, digits)
                entry.update(digits=digits, text=text)
        mismatch = master is not None and text != master or (page is not None and master is None) \
            or entry.get("missing_key", False) or text is None
        if mismatch and master is not None:
            entry["text"] = master  # never force a key; print the master's string and flag it
        entry.update(master=master, mismatch=bool(mismatch))
        if key in REG:
            entry["value"] = REG[key]["value"]
            entry["status"] = REG[key]["status"]
        if page:
            entry["where"] = f"{DUMP[page][0]} shape {shape}"
        if alts:
            entry["alt_keys"] = [a for a in alts if a in REG]
        if comment:
            entry["comment"] = comment
        numbers[nid] = entry
        table.append((nid, key or "-", entry["text"], master, mismatch, entry.get("value", "")))
    return numbers, table


# ------------------------------------------------------------------ the example's closed forms
rho, k, cH = exact("prim_rho"), exact("prim_k"), exact("prim_cH")
h, ell, p = exact("prim_h"), exact("prim_ell"), exact("prim_p")
b, lam, M = exact("b_B"), exact("lambda_B"), exact("M_half_B")
rA, rF, rN, rJ, rC = exact("rA"), exact("rF_B"), exact("rN"), exact("rJ"), exact("rC_B")
r0, r1, r2 = exact("prim_r0"), exact("prim_r1"), exact("prim_r2")
PLATEAU = exact("entry_r1_B")
FROZEN_LO, FROZEN_HI = exact("p4_frozen_entry_below_ceiling"), exact("p4_frozen_entry_above_ceiling")
LO, HI = Fraction(1), Fraction(9, 2)        # the master's strength axis runs from 1 to 4.5 (last tick)
YTOP = Fraction(3, 5)                        # its entry axis from 0 to 0.6


def Delta(r: Fraction) -> Fraction:
    """handout/figures.js auction(): Delta = (r - ell)^2/(2r)."""
    return (r - ell) ** 2 / (2 * r)


def gL(r: Fraction) -> Fraction:
    """handout/figures.js auction(): g_L = (ell^2 - p^2)/(2r)."""
    return (ell * ell - p * p) / (2 * r)


def gH(r: Fraction) -> Fraction:
    """handout/figures.js auction(): g_H = h - r/2 - p^2/(2r)."""
    return h - r / 2 - p * p / (2 * r)


def B(r: Fraction, mu: Fraction) -> Fraction:
    """handout/figures.js auction(): B(mu) = g_L + mu (g_H - g_L)."""
    return gL(r) + mu * (gH(r) - gL(r))


def entry_R(r: Fraction) -> Fraction:
    """handout/figures.js entryR() = make_figures_src.py ent_branch_R(): rho + (1 - rho) b Delta/(2k)."""
    return rho + (1 - rho) * b * Delta(r) / (2 * k)


def plateau_cf() -> Fraction:
    """handout/figures.js plateau() = make_figures_src.py ent_plateau(): rho + (1 - rho)(b + lambda/2)."""
    return rho + (1 - rho) * (b + lam / 2)


def equilibria(r: Fraction) -> list[str]:
    """handout/figures.js equilibria(): the forms Appendix A4 lists at strength r of the example's path
    (an indifferent informed trader may mix; an indifferent costly rival prepares). Boundaries are registry rows."""
    ids = []
    if r <= rN:
        ids.append("N")
    if rA <= r < rF:
        ids.append("R")
    if r >= rF:
        ids.append("F")
    if rN < r < rJ:
        ids.append("Q")
    return ids


def entry_of(form: str, r: Fraction) -> Fraction:
    """handout/figures.js form(): entry E of form N, R, F or Q at r (N and Q never recruit; F recruits up to r_C)."""
    if form == "R":
        return entry_R(r)
    if form == "F":
        return PLATEAU if r <= rC else rho
    return rho


# ------------------------------------------------------------------ curves
def pts(*xy: tuple[Fraction, Fraction]) -> list[list[float]]:
    return [[coord(x), coord(y)] for x, y in xy]


RAMP_N = 24
ramp_r = [rA + (rF - rA) * Fraction(i, RAMP_N) for i in range(RAMP_N + 1)]

BREAKS = {
    "lo": {"key": None, "r": LO, "printed": "p14.chart.x.1"},
    "rA": {"key": "rA", "r": rA, "printed": "p14.chart.x.rA"},
    "rF": {"key": "rF_B", "r": rF, "printed": None},
    "rN": {"key": "rN", "r": rN, "printed": None},
    "rJ": {"key": "rJ", "r": rJ, "printed": "p14.chart.x.rJ"},
    "rC": {"key": "rC_B", "r": rC, "printed": "p14.rhs.rC.1"},
    "hi": {"key": None, "r": HI, "printed": None},
}

# style is one of solid, dashed, dotted. The dump records colour and width but no dash pattern, so dash patterns
# are read from the renders of an older save (style_confirmed false where the dump contradicts that render).
# dump_shapes: the master's shapes that draw the segment, by page ("p16" lists the pale trace for the full model).
SEGMENTS = {
    "none.a": dict(branch="none", form="N", style="solid", style_confirmed=True, y_key="prim_rho", ends=("lo", "rA"),
                   points=pts((LO, rho), (rA, rho)),
                   start={"included": True}, end={"included": True, "interior": True},
                   dump_shapes={"p14": [30], "p16": [5], "p17": [29]},
                   master="p14 shape 30 (click 1); p17 shape 29 (first part); p16 pale trace shape 5"),
    "none.b": dict(branch="none", form="N", style="solid", style_confirmed=True, y_key="prim_rho", ends=("rA", "rN"),
                   points=pts((rA, rho), (rN, rho)),
                   start={"included": True, "interior": True}, end={"included": True, "marker": None},
                   dump_shapes={"p14": [106], "p16": [5], "p17": [29]},
                   master="p14 shape 106 (click 4); p17 shape 29 (second part); p16 pale trace shape 5"),
    "none.dashed": dict(branch="none", form="Q", style="dashed", style_confirmed=True, y_key="prim_rho",
                        ends=("rN", "rJ"), points=pts((rN, rho), (rJ, rho)),
                        start={"included": False, "marker": None}, end={"included": False, "marker": "open"},
                        dump_shapes={"p14": [34, 35], "p17": [30, 31]},
                        master="p14 shape 34 + open circle 35 (click 4); p17 shape 30 + open circle 31"),
    "informed.ramp": dict(branch="informed", form="R", style="solid", style_confirmed=True, y_key=None,
                          ends=("rA", "rF"), points=pts(*[(r, entry_R(r)) for r in ramp_r]),
                          start={"included": True, "marker": "filled", "y_key": "entry_rA_B"},
                          end={"included": True, "interior": True, "y_key": "entry_r1_B"},
                          dump_shapes={"p14": [37, 38], "p16": [6], "p17": [32, 33]},
                          master="p14 polyline 37 first leg + filled circle 38 (click 2); p17 polyline 32 + circle 33"),
    "informed.flat": dict(branch="informed", form="F", style="solid", style_confirmed=True, y_key="entry_r1_B",
                          ends=("rF", "rC"), points=pts((rF, PLATEAU), (rC, PLATEAU)),
                          start={"included": True, "interior": True}, end={"included": True, "marker": "filled"},
                          dump_shapes={"p14": [37, 39], "p16": [6], "p17": [32, 34]},
                          master="p14 polyline 37 second leg + filled circle 39 (click 2); p17 polyline 32 + circle 34"),
    "informed.drop": dict(branch="informed", form=None, style="dotted", style_confirmed=True, connector=True,
                          y_key=None, ends=("rC", "rC"), points=pts((rC, PLATEAU), (rC, rho)),
                          dump_shapes={"p14": [47], "p17": [35]},
                          master="p14 shape 47, 1.25 pt (click 3); p17 shape 35; dotted in the renders"),
    "informed.floor": dict(branch="informed", form="F", style="solid", style_confirmed=True, y_key="prim_rho",
                           ends=("rC", "hi"), points=pts((rC, rho), (HI, rho)),
                           start={"included": False, "marker": None}, end={"included": True, "axis_end": True},
                           dump_shapes={"p14": [48], "p16": [7], "p17": [36]},
                           master="p14 shape 48 (click 3); p17 shape 36; p16 pale trace shape 7"),
    "fixed.flat": dict(branch="orders held fixed", form="F at every r", style="solid", style_confirmed=True,
                       y_key="p4_frozen_entry_below_ceiling", ends=("lo", "rC"),
                       points=pts((LO, FROZEN_LO), (rC, FROZEN_LO)),
                       start={"included": False, "axis_end": True}, end={"included": True},
                       dump_shapes={"p16": [33]}, master="p16 shape 33, #1B3A6B 3.5 pt (click 3)"),
    "fixed.drop": dict(branch="orders held fixed", form=None, style="dotted", style_confirmed=True, connector=True,
                       y_key=None, ends=("rC", "rC"), points=pts((rC, FROZEN_LO), (rC, FROZEN_HI)),
                       dump_shapes={"p16": [34]}, master="p16 shape 34, 1.25 pt (click 3); dotted in the older render"),
    "fixed.floor": dict(branch="orders held fixed", form="F at every r", style="dashed", style_confirmed=False,
                        style_note="dashed only in the older render, whose colour (orange) the dump contradicts (#1B3A6B)",
                        y_key="p4_frozen_entry_above_ceiling", ends=("rC", "hi"),
                        points=pts((rC, FROZEN_HI), (HI, FROZEN_HI)),
                        start={"included": False}, end={"included": True, "axis_end": True},
                        dump_shapes={"p16": [35]}, master="p16 shape 35, #1B3A6B 3.5 pt (click 3)"),
    "hidden": dict(branch="price hidden from the rival", form="rho at every r", style="solid", style_confirmed=True,
                   y_key="prim_rho", ends=("lo", "hi"), points=pts((LO, rho), (HI, rho)),
                   dump_shapes={"p16": [30]}, master="p16 shape 30, #8C8C8C 3.5 pt (click 3)"),
}

INCUMBENTS = [
    {"inc": 0, "r_key": "prim_r0", "r": coord(r0), "r_num": "ctl.r.r0", "entry_key": "entry_r0", "y": coord(exact("entry_r0")),
     "branch": "none", "segment": "none.a", "label_tex": "r_{0}"},
    {"inc": 1, "r_key": "prim_r1", "r": coord(r1), "r_num": "ctl.r.r1", "entry_key": "entry_r1_B", "y": coord(PLATEAU),
     "branch": "informed", "segment": "informed.flat", "label_tex": "r_{1}"},
    {"inc": 2, "r_key": "prim_r2", "r": coord(r2), "r_num": "ctl.r.r2", "entry_key": "entry_r2", "y": coord(exact("entry_r2")),
     "branch": "informed", "segment": "informed.floor", "label_tex": "r_{2}"},
]

# The master's rho tick reads "$\rho$ = 0.25": math, then the words " = ", then the number.
Y_TICKS = [{"y": 0.0, "num": "{p}.chart.y.zero"},
           {"y": coord(rho), "num": "{p}.chart.y.rho", "prefix_tex": "\\rho", "prefix_join": " = "},
           {"y": coord(PLATEAU), "num": "{p}.chart.y.plateau"}]
PATHS = {"none": ["none.a", "none.b", "none.dashed"],
         "informed": ["informed.ramp", "informed.flat", "informed.drop", "informed.floor"],
         "orders held fixed": ["fixed.flat", "fixed.drop", "fixed.floor"],
         "price hidden from the rival": ["hidden"]}


def ticks(page: str, spec: list) -> list[dict]:
    out = []
    for r, num in spec:
        t = {"r": coord(r)}
        t["num"] = num.format(p=page) if num else None
        out.append(t)
    return out


X14 = [(LO, "{p}.chart.x.1"), (rA, "{p}.chart.x.rA"), (rJ, "{p}.chart.x.rJ"), (Fraction(5, 2), None),
       (Fraction(3), "{p}.chart.x.3"), (Fraction(7, 2), None), (Fraction(4), "{p}.chart.x.4"), (HI, None)]
X16 = [(LO, "{p}.chart.x.1"), (Fraction(3, 2), None), (Fraction(2), "{p}.chart.x.2"), (Fraction(5, 2), None),
       (Fraction(3), "{p}.chart.x.3"), (Fraction(7, 2), None), (rC, "{p}.chart.x.rC"), (Fraction(4), "{p}.chart.x.4"),
       (HI, None)]

MARKERS = [{"at": "rA", "segment": "informed.ramp", "r": coord(rA), "y": coord(entry_R(rA)), "fill": "filled"},
           {"at": "rJ", "segment": "none.dashed", "r": coord(rJ), "y": coord(rho), "fill": "open"},
           {"at": "rC", "segment": "informed.flat", "r": coord(rC), "y": coord(PLATEAU), "fill": "filled"}]


def page_chart(page: str) -> dict:
    y_ticks = [{**t, "num": t["num"].format(p=page)} for t in Y_TICKS]
    base = {"x_range": [coord(LO), coord(HI)], "y_range": [0.0, coord(YTOP)], "y_ticks": y_ticks,
            "incumbents": [i["inc"] for i in INCUMBENTS]}
    if page == "p14":
        base.update(
            x_ticks=ticks(page, X14),
            segments=["none.a", "none.b", "none.dashed", "informed.ramp", "informed.flat", "informed.drop", "informed.floor"],
            markers=MARKERS, shade={"from": "rA", "to": "rJ", "r": [coord(rA), coord(rJ)]},
            brackets=[{"from": "lo", "to": "rA", "words_shape": 32}, {"from": "rF", "to": "rC", "words_shape": 41},
                      {"from": "rC", "to": "hi", "words_shape": 50}],
            dump_clicks={"none.a": 1, "incumbent 0": 1, "informed.ramp": 2, "informed.flat": 2, "incumbent 1": 2,
                         "informed.drop": 3, "informed.floor": 3, "incumbent 2": 3, "none.b": 4, "none.dashed": 4,
                         "shade": 4, "p14.chart.x.rJ": 4, "p14.chart.x.rA": 2, "the two run-ins beside the chart": 5})
    elif page == "p17":
        base.update(
            x_ticks=ticks(page, X14),
            segments=["none.a", "none.b", "none.dashed", "informed.ramp", "informed.flat", "informed.drop", "informed.floor"],
            markers=MARKERS, shade={"from": "rA", "to": "rJ", "r": [coord(rA), coord(rJ)]},
            brackets=[{"from": "lo", "to": "rA", "words_shape": 46}, {"from": "rA", "to": "rJ", "words_shape": 64},
                      {"from": "rJ", "to": "hi", "words_shape": 48}],
            dump_clicks={"all curves, markers and incumbents": 0, "shade": 1, "brackets": 1, "p17.chart.x.rA": 1,
                         "p17.chart.x.rJ": 1, "branch words": 2})
    else:
        base.update(
            x_ticks=ticks(page, X16),
            trace=["none.a", "none.b", "informed.ramp", "informed.flat", "informed.floor"],
            segments=["fixed.flat", "fixed.drop", "fixed.floor", "hidden"],
            markers=[],
            dump_clicks={"trace, incumbents, 'full model'": 0, "fixed.flat": 2, "fixed.drop": 2, "fixed.floor": 2,
                         "hidden": 2, "p16.chart.x.rC (and its tick)": 2})
    return base


# ------------------------------------------------------------------ marks (the stops of the strength control)
WORDS = {  # exact phrases of each page's dump; None where the page has no word for the branch
    "none": {"p14": "no informed order", "p16": None, "p17": "no informed order"},
    "informed": {"p14": "Informed-order equilibrium", "p16": None,
                 "p17": "purchases in class H expected"},
    "model": {"p16": "full model"},
}

STOPS = [("r0", "prim_r0", "ctl.r.r0", 0), ("rA", "rA", "ctl.r.rA", None), ("rJ", "rJ", "ctl.r.rJ", None),
         ("r1", "prim_r1", "ctl.r.r1", 1), ("rC", "rC_B", "ctl.r.rC", None), ("r2", "prim_r2", "ctl.r.r2", 2)]
FORM_BRANCH = {"N": "none", "Q": "none", "R": "informed", "F": "informed"}


def entry_row(stop: str, form: str) -> tuple[str, str]:
    """The registry row (and its number id) that stands behind the entry of `form` at `stop`."""
    if form in ("N", "Q"):
        return ("entry_r0", "ctl.entry.r0") if stop == "r0" else ("prim_rho", "ctl.entry.rho")
    if form == "R":
        return ("entry_rA_B", "ctl.entry.rA")
    if stop == "r2":
        return ("entry_r2", "ctl.entry.r2")
    return ("entry_r1_B", "ctl.entry.plateau")


def segment_at(form: str, r: Fraction) -> str:
    if form == "N":
        return "none.a" if r < rA else "none.b"   # at rA itself the dot sits where none.a meets none.b
    if form == "Q":
        return "none.dashed"
    if form == "R":
        return "informed.ramp"
    return "informed.flat" if r <= rC else "informed.floor"


ENDPOINT = {
    "rA": [{"segment": "informed.ramp", "included": True, "master": "filled circle: the branch with informed orders starts here"},
           {"segment": "none.b", "included": True,
            "master": "no marker; the branch with no informed order runs through (none.a ends and none.b starts here)"}],
    "rJ": [{"segment": "none.dashed", "included": False,
            "master": "open circle: the dashed stretch at rho ends before 1.97; 1.97 is not on it"}],
    "rC": [{"segment": "informed.flat", "included": True, "master": "filled circle: the flat stretch at 0.52 includes 3.59"},
           {"segment": "informed.floor", "included": False,
            "master": "no marker; the closed form puts 3.59 on the flat stretch, so the stretch at rho starts just after it"}],
}


def build_marks(numbers: dict) -> list[dict]:
    marks = []
    for sid, key, num, inc in STOPS:
        r = exact(key)
        forms = equilibria(r)
        eqs = []
        for f in forms:
            ekey, enum = entry_row(sid, f)
            cf = entry_of(f, r)
            eqs.append({"form": f, "branch": FORM_BRANCH[f], "segment": segment_at(f, r),
                        "words": {pg: w for pg, w in WORDS[FORM_BRANCH[f]].items()},
                        "entry_key": ekey, "entry_num": enum, "entry_text": numbers[enum]["text"],
                        "y": coord(cf), "closed_form": half_up(cf, 9)})
        mark = {"id": sid, "key": key, "r": coord(r), "num": num, "text": numbers[num]["text"],
                "inc": inc, "equilibria": eqs, "count": len(eqs)}
        if sid in ENDPOINT:
            mark["endpoints"] = ENDPOINT[sid]
        marks.append(mark)
    return marks


# ------------------------------------------------------------------ notes
def build_notes(numbers: dict) -> tuple[list[str], list[str]]:
    log = []
    # the ramp is a curve; the master draws its chord
    chord = [entry_R(rA) + (entry_R(rF) - entry_R(rA)) * (r - rA) / (rF - rA) for r in ramp_r]
    gap = max(c - entry_R(r) for c, r in zip(chord, ramp_r))
    pt_per_entry = Fraction(98) / rho          # the master: rho at 300 pt, 0 at 398 pt
    pt_per_r = Fraction(425) / Fraction(7, 2)  # the master: 1 at 118 pt, 4.5 at 543 pt
    stage = Fraction(1600, 960)
    gap_px = gap * pt_per_entry * stage
    close_px = (r2 - rC) * pt_per_r * stage
    # consistency of the closed forms with their registry rows
    checks = [
        ("entry on the ramp at rA vs entry_rA_B", entry_R(rA), exact("entry_rA_B")),
        ("entry on the ramp at rF vs entry_r1_B", entry_R(rF), PLATEAU),
        ("rho + (1 - rho)(b + lambda/2) vs entry_r1_B", plateau_cf(), PLATEAU),
        ("Delta(r0) vs Delta_r0", Delta(r0), exact("Delta_r0")),
        ("Delta(r1) vs Delta_r1", Delta(r1), exact("Delta_r1")),
        ("Delta(r2) vs Delta_r2", Delta(r2), exact("Delta_r2")),
        ("B_r0(1/2) vs Bprior_r0", B(r0, Fraction(1, 2)), exact("Bprior_r0")),
        ("B_r1(1/2) vs Bprior_r1_B", B(r1, Fraction(1, 2)), exact("Bprior_r1_B")),
        ("B_r2(1/2) vs Bprior_r2", B(r2, Fraction(1, 2)), exact("Bprior_r2")),
        ("B_r1(M) vs p2_base_r1_low_profit_plus", B(r1, M), exact("p2_base_r1_low_profit_plus")),
        ("B_r2(M) vs p2_base_r2_low_profit_plus", B(r2, M), exact("p2_base_r2_low_profit_plus")),
        ("B_rC(M) - c_H at the registry rC_B", B(rC, M) - cH, Fraction(0)),
    ]
    for name, a, c in checks:
        log.append(f"{name}: closed form {half_up(a, 12)}, registry {half_up(c, 12)}, difference {sci(a - c)}")
    worst = max(abs(a - c) for name, a, c in checks)
    b1 = B(LO, Fraction(1, 2))
    # where the master puts the breakpoints, read from its boxes on page 14 (axis: 1 at 118 pt, 4.5 at 543 pt;
    # entry 0 at 398 pt, rho at 300 pt)
    box = {i: s["box"] for i, s in DUMP["p14"][1].items()}
    to_r = lambda x: half_up(1 + (Fraction(str(x)) - 118) * Fraction(7, 2) / 425, 3)          # noqa: E731
    to_e = lambda y: half_up((398 - Fraction(str(y))) * rho / 98, 4)                          # noqa: E731
    x_rF = Fraction(str(box[37][0])) + Fraction(120609, 12700)  # the polyline corner, in EMU (12700 per pt)
    placed = (f"the flat stretch at {to_e(box[37][1])} against {half_up(PLATEAU, 4)}, the ramp start at "
              f"{to_e(box[38][1] + box[38][3] / 2)} against {half_up(entry_R(rA), 4)}, rA at {to_r(box[38][0] + box[38][2] / 2)}, "
              f"rF at {to_r(x_rF)}, rN at {to_r(box[34][0])}, rJ at {to_r(box[35][0] + box[35][2] / 2)}, "
              f"rC at {to_r(box[47][0])}, r2 at {to_r(box[49][0] + box[49][2] / 2)}")
    notes = [
        "No printed number is a mismatch: every string the master prints on pages 14, 16 and 17 is the half-up rounding "
        "of the registry row given as its key. Axis labels 0, 1, 2, 3, 4 are coordinates and carry key null; ordinals "
        "(step numbers, Result 1 and 2, page counters) and the citation years on page 16 are words, "
        "not numbers, and are not listed.",
        "The chart label 'rho = 0.25' is prim_rho (build_results.js used entry_r0, same 1/4). The tick and text "
        "1.97 is rJ: build_results.js (13 Nov) printed and shaded to rN = 1.75, and the master was changed to 1.97 since; "
        "that script is stale on this point. All other keys are confirmed.",
        "The dashed grey stretch on pages 14 and 17 runs from rN = 1.75 (registry rN, printed nowhere) to rJ = 1.97. It is "
        "not the equilibrium with no informed order: it is the mixed-order equilibrium at the entry floor (form Q of "
        "handout/figures.js): class H buys and class L sells, each at rate s = t = b(rho Delta_T/k - 2) > 0, no order "
        "attracts the costly rival, entry is rho. The solid grey part from 1 to 1.75 is form N (no informed order), "
        "closed at 1.75. The master marks neither end at 1.75 and puts an open circle at 1.97 (Q excludes it). "
        "Page 14's bracket 'no informed order' covers only 1 to 1.39, so the master's words are not wrong, but page 17's "
        "'No order expected: entry stays at rho ...' sits beside a branch that, from 1.75 to 1.97, has "
        "informed orders (page 17's note 'may mix over its best orders' covers it). No stop of the control falls in "
        "1.75 to 1.97, so the control never lands on the dashed stretch.",
        "The ramp from 1.39 to rF = 1.47 (registry rF_B, printed nowhere) is form R, entry rho + (1 - rho) b Delta_T(r)/(2k): "
        f"{numbers['ctl.entry.rA']['text']} at 1.39 (registry entry_rA_B) rising to 0.52 at 1.47. The master draws it as a "
        "straight solid segment (the manuscript and the handout draw R dashed). The curve lies below its chord by at most "
        f"{half_up(gap, 5)} in entry, {half_up(gap_px, 2)} px on the 1600 x 900 stage at the master's scale: the sampled "
        "curve and the master's chord are the same picture.",
        "Page 14's text says 'Entry reaches 0.52 at r = 1.47' (rF_B), as the closed form has it: entry is 0.45 at 1.39 and "
        "reaches 0.52 only at 1.47. The control's stop at 1.39 prints 0.45 there (entry_rA_B, printed nowhere in the master).",
        "Control numbers with no registry row at that strength: entry 0.25 at 1.39 (prim_rho; the branch with no "
        "informed order has entry rho at every strength, but no row states it at rA), and entry 0.52 at 1.97 and at 3.59 "
        "(entry_r1_B, a row stated at r1; the closed form rho + (1 - rho)(b + lambda/2) is the same on the whole flat "
        "stretch from rF to rC, and p4_frozen_entry_below_ceiling states it for 1 < r <= rC, but with orders held fixed). "
        "They are right by the closed form; they are not certain registry rows. The other control numbers are rows at "
        "their own strength (entry_r0, entry_rA_B, entry_r2, prim_r0, rA, rJ, prim_r1, rC_B, prim_r2).",
        "Page 14's middle bracket ('a purchase raises the belief and attracts the costly rival', shape 41 over path 36) "
        "starts at rF = 1.47, not at 1.39: the ramp from 1.39 to 1.47 sits under no bracket, although a purchase attracts "
        "the costly rival there too (form R recruits after a purchase). curves.pages.p14.brackets keeps the master's span.",
        "Endpoints from the closed forms (handout/figures.js equilibria, tie rule of page 17's note): no informed order "
        "for r <= rN (1.75); the ramp for rA <= r < rF (closed at 1.39, filled circle in the master); the flat stretch for "
        "rF <= r <= rC (closed at 3.59, filled circle); the stretch at rho for r > rC (open at 3.59; the manuscript draws "
        "an open circle there, the master draws none); the dashed stretch for rN < r < rJ (open at both ends). Two "
        "equilibria at every r in [1.39, 1.97): no informed order with the ramp on [1.39, 1.47), with the flat stretch on "
        "[1.47, 1.75], the dashed stretch with the flat stretch on (1.75, 1.97). At 1.97 itself only the flat stretch: "
        "the shading's right edge is excluded, as the master's open circle shows.",
        "The vertical drop at 3.59 (pages 14, 16, 17) is a connector, not an equilibrium: no strength has an entry between "
        "rho and 0.52 there. The master draws it 1.25 pt and dotted; it carries no data, so the 3 px floor for data "
        "lines does not bind it. data.json marks it connector: true.",
        "Page 16, 'orders held fixed': full orders at every strength (form F with s = lambda); entry is "
        "p4_frozen_entry_below_ceiling (= entry_r1_B, 0.52) for 1 < r <= rC and p4_frozen_entry_above_ceiling (rho) "
        "after. Its stretch after 3.59 is dashed only in the older render (whose colour, orange, the dump contradicts: "
        "#1B3A6B); the dump records no dash pattern, so that style is unconfirmed. Three lines lie on rho from 3.59 to "
        "4.5: it, 'price hidden from the rival' and the pale full-model trace; a dash lets all three show there.",
        "Page 16, 'price hidden from the rival': entry rho at every strength, because the rival prepares on the prior and "
        f"B_r(1/2) <= B_1(1/2) = {half_up(b1, 3)} < c_H = 6 on the whole axis (B falls in r). Registry rows exist only at "
        "the incumbents (p4_hidden_r0_entry, p4_hidden_r1_entry, p2_base_hidden_entry: 0.25); beyond r1 the line is the "
        "closed form alone.",
        "Page 16's pale 'full model' trace in the dump is: no informed order from 1 to rN (shape 5), the ramp and the flat "
        "stretch (shape 6), and the stretch at rho after 3.59 (shape 7). It leaves out the dashed stretch, the drop and the "
        "endpoint circles; curves.pages.p16.trace lists those segments.",
        "Under the other tie rule (an indifferent costly rival may prepare with any probability), the threshold pair T adds "
        "an equilibrium on [1.39, 1.97] (handout/explorer.js draws it thin and dashed). The master and this data leave it out.",
        f"The control stops 3.59 (rC) and 3.6 (r2) are {half_up(close_px, 2)} px apart on the stage at the master's scale; "
        "the marker, the dots and the two labels at these stops must not rely on their x position alone to be told apart.",
        f"Placement noise in the master, all under 1.5 pt on its 960 x 540 page (read from its boxes on page 14): "
        f"{placed}. data.json gives the closed-form positions; the '0.52' tick sits at the closed-form 0.5228.",
        f"Closed forms against their registry rows (build log): the largest difference over {len(checks)} checks is "
        f"{sci(worst)} (B_rC(M) - c_H at the rounded registry rC_B is rounding noise; which side of 3.59 a "
        "branch takes is decided by comparing registry rows, never by that sign).",
    ]
    return notes, log


# ------------------------------------------------------------------ master coordinates, for the build log
def master_xy(r: Fraction, e: Fraction) -> str:
    x = 118 + (r - 1) * Fraction(425) / Fraction(7, 2)
    y = 398 - e * Fraction(98) / rho
    return f"({half_up(x, 1)}, {half_up(y, 1)})"


def main() -> None:
    numbers, table = build_numbers()
    marks = build_marks(numbers)
    notes, checklog = build_notes(numbers)
    words_found = {}
    for branch, per in WORDS.items():
        for pg, w in per.items():
            if w:
                words_found[f"{branch}/{pg}"] = any(w in s["text"] for s in DUMP[pg][1].values())
    segs = {}
    for sid, s in SEGMENTS.items():
        d = dict(s)
        a, z = d.pop("ends")
        d["from"], d["to"] = a, z
        segs[sid] = d
    data = {
        "meta": {
            "built_by": "build_data.py",
            "registry": {"path": str(REGISTRY.relative_to(ROOT)),
                         "sha256": hashlib.sha256(REGISTRY.read_bytes()).hexdigest()},
            "master_dump": {"md5_of_master": (DUMPS / "MASTER_MD5.txt").read_text(encoding="utf-8").split()[0],
                            "files": {pg: f for pg, (f, _) in DUMP.items()}},
            "rounding": "half-up on the exact registry value (Fraction), never through a binary float",
            "coordinates": "curves: x = incumbent strength r, y = entry; 6-decimal drawing coordinates, never printed",
            "styles": "segment style is solid, dashed or dotted; the dump records colour and width but no dash pattern, "
                      "so dash patterns come from the renders of an older save (style_confirmed false where the dump "
                      "contradicts that render); connector true marks a vertical drop that carries no data",
            "forms": "N no informed order; Q mixed orders at the entry floor; R mixed purchase (the ramp); F full "
                     "purchase (flat at 0.52 up to rC, rho after). Internal names from handout/figures.js; not page words.",
        },
        "numbers": numbers,
        "marks": marks,
        "curves": {
            "x_label_words": "incumbent strength", "y_label_words": "entry",
            "breaks": {k_: {"key": v["key"], "r": coord(v["r"]), "printed": v["printed"],
                            **({"value": REG[v["key"]]["value"]} if v["key"] else {})} for k_, v in BREAKS.items()},
            "segments": segs,
            "paths": PATHS,
            "incumbents": INCUMBENTS,
            "pages": {pg: page_chart(pg) for pg in ("p14", "p16", "p17")},
        },
        "words": WORDS,
        "notes": notes,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)\n")
    print(f"{'id':26} {'key':30} {'text':>7} {'master':>7}  mismatch  value")
    for nid, key, text, master, mism, value in table:
        print(f"{nid:26} {key:30} {str(text):>7} {str(master):>7}  {str(bool(mism)):8}  {value}")
    print("\nsegments: closed-form endpoints in the master's points (x = 118 + (r-1) 425/3.5, y = 398 - entry 392),"
          "\nthen each dump shape's box (x, y, w, h) read from the dump")
    for sid, s in SEGMENTS.items():
        first, last = s["points"][0], s["points"][-1]
        a = master_xy(Fraction(str(first[0])), Fraction(str(first[1])))
        z = master_xy(Fraction(str(last[0])), Fraction(str(last[1])))
        print(f"  {sid:15} {s['style']:7} {a} -> {z}")
        for pg, ids in s["dump_shapes"].items():
            for i in ids:
                sh = DUMP[pg][1][i]
                x, y, w, hh = sh["box"]
                print(f"  {'':15} {pg} shape {i:<4} '{sh['name']}': x {x} to {x + w}, y {y} to {y + hh}")
    print("\nmarks:")
    for m in marks:
        eqs = "; ".join(f"{e['form']}/{e['branch']} entry {e['entry_text']} ({e['entry_key']}, closed form {e['closed_form']})"
                        for e in m["equilibria"])
        print(f"  {m['text']:>5} ({m['key']}): {m['count']} -> {eqs}")
    print("\nwords found in the dumps:", words_found)
    print("\nclosed forms against registry rows:")
    for line in checklog:
        print("  " + line)


if __name__ == "__main__":
    main()
