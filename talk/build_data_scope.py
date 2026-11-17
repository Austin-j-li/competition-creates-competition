#!/usr/bin/env python3
"""build_data_scope.py: writes src/data_scope.json, the printed numbers of the scope pages
(B4, B6, B13 and B17: show positions 32, 33, 34, 37, 38, 56 and 65). Number ids keep the names these
pages had before the 17 November deck (b27 b28 b29 b32 b33 b51 b59).

    python3 build_data_scope.py

Every number is a registry row (audit/slot_manuscript_2026_10_23/registry/registry.csv) rounded
half-up on its exact value (a Fraction parsed from the registry string, never a binary float) to
the digits the master prints. The registry key of each row is the one the earlier web deck
(presentation/content.js) uses for the same sentence. The master's own string is read from the
page dump (master_dump/slideNN.txt) and must occur there; a rounding that does not give it is
written with "mismatch": true and the master's string is printed. Standard library only.
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
OUT = HERE / "src" / "data_scope.json"


def read_registry() -> dict[str, dict]:
    with REGISTRY.open(newline="", encoding="utf-8") as fh:
        return {r["key"]: r for r in csv.DictReader(fh)}


REG = read_registry()


def half_up(x: Fraction, digits: int) -> str:
    sign = "-" if x < 0 else ""
    n = math.floor(abs(x) * 10 ** digits + Fraction(1, 2))
    s = str(n).rjust(digits + 1, "0")
    return sign + (s[:-digits] + "." + s[-digits:] if digits else s)


# (id, registry key, digits, master string, slide, kind)   kind: value | percent (value x 100)
ROWS: list[tuple[str, str, int, str, int, str]] = []


def add(ident: str, key: str, digits: int, master: str, slide: int, kind: str = "value") -> None:
    ROWS.append((ident, key, digits, master, slide, kind))


# b27: the lead page of B4
add("b27.R_hidden", "p2_base_hidden_proceeds", 2, "0.61", 32)
add("b27.R_seen", "p2_base_r1_proceeds", 2, "0.87", 32)
add("b27.W_hidden", "p2_base_hidden_surplus", 2, "2.55", 32)
add("b27.W_seen", "p2_base_r1_surplus", 2, "2.63", 32)
add("b27.transfer", "p2_access_gross_transfer", 3, "0.038", 32)
# b28: access values
add("b28.R_seen", "p2_base_r1_proceeds", 6, "0.872531", 33)
add("b28.W_seen", "p2_base_r1_surplus", 6, "2.634044", 33)
add("b28.R_hidden", "p2_base_hidden_proceeds", 6, "0.614583", 33)
add("b28.W_hidden", "p2_base_hidden_surplus", 6, "2.552083", 33)
# b29: gains at r1
add("b29.gain_R", "p2_access_proceeds_gain", 6, "0.257948", 34)
add("b29.gain_W", "p2_access_surplus_gain", 6, "0.081960", 34)
# b32: private signals
add("b32.alpha_I", "sig_comp_aT", 2, "0.94", 37)
add("b32.alpha_C", "sig_comp_d", 3, "0.505", 37)
add("b32.entry_r0", "p4_comp_b_r0_entry", 6, "0.250000", 37)
add("b32.entry_r1", "p4_comp_b_r1_entry", 6, "0.386933", 37)
add("b32.entry_no_y", "p4_comp_b_no_y_r1_entry", 6, "0.250000", 37)
# b33: scenario-specific Panel A inputs; fractions remain text
add("b33.moderate.low_lo", "p2_input_moderate_low_lo", 0, "1", 38)
add("b33.moderate.high_lo", "p2_input_moderate_high_lo", 0, "2", 38)
add("b33.bands.cost", "p2_input_bands_cost", 0, "6", 38)
add("b33.bands.r1", "p2_input_bands_r1", 0, "3", 38)
add("b33.ex_a.low_lo", "p2_input_ex_a_low_lo", 0, "1", 38)
add("b33.ex_a.high_lo", "p2_input_ex_a_high_lo", 0, "10", 38)
add("b33.ex_a.r1", "p2_input_ex_a_r1", 0, "3", 38)
add("b33.ex_b.low_lo", "p2_input_ex_b_low_lo", 0, "1", 38)
add("b33.ex_b.high_lo", "p2_input_ex_b_high_lo", 0, "10", 38)
add("b33.ex_b.r1", "p2_input_ex_b_r1", 0, "3", 38)
add("b33.ex_c.high_lo", "p2_input_ex_c_high_lo", 0, "1", 38)
add("b33.ex_c.high_hi", "p2_input_ex_c_high_hi", 0, "19", 38)
add("b33.ex_c.r0", "p2_input_ex_c_r0", 0, "1", 38)
add("b33.ex_d.low_lo", "p2_input_ex_d_low_lo", 0, "1", 38)
add("b33.ex_d.high_lo", "p2_input_ex_d_high_lo", 0, "10", 38)
add("b33.ex_d.r0", "p2_input_ex_d_r0", 0, "1", 38)
# b33: Panel B outcomes
for slug, key in [("moderate", "moderate"), ("bands", "bands"), ("low", "ex_a"), ("high", "ex_b"),
                  ("wide", "ex_c"), ("points", "ex_d")]:
    master = {"moderate": ("0.250000", "0.522757", "0.324401"), "bands": ("0.250000", "0.522757", "0.324401"),
              "low": ("0.250000", "0.472339", "0.194641"), "high": ("0.250000", "0.573175", "0.454162"),
              "wide": ("0.250000", "0.573175", "0.419819"), "points": ("0.250000", "0.250000", "0.175000")}[slug]
    add(f"b33.{slug}.E0", f"p2_{key}_r0_entry", 6, master[0], 38)
    add(f"b33.{slug}.E1", f"p2_{key}_r1_entry", 6, master[1], 38)
    add(f"b33.{slug}.OH1", f"p2_{key}_r1_ownership", 6, master[2], 38)
# b51: footnote
add("b51.entry_share", "ba_share_r1_B", 1, "90.2", 56, "percent")
# b59: best reserves (rho and k of the first two rows are inputs written as fractions: text)
add("b59.a.R", "rsvopt_a_R", 2, "1.25", 65)
add("b59.a.E", "rsvopt_a_E", 2, "0.25", 65)
add("b59.b.r0.R", "rsvopt_b_r0_R", 2, "1.00", 65)
add("b59.b.r0.E", "rsvopt_b_r0_E", 2, "0.20", 65)
add("b59.b.r1.p", "rsvopt_b_r1_p", 3, "1.325", 65)
add("b59.b.r1.R", "rsvopt_b_r1_R", 3, "1.069", 65)
add("b59.b.r1.E", "rsvopt_b_r1_E", 3, "0.491", 65)
add("b59.b.r2.p", "rsvopt_b_r2_p", 3, "1.906", 65)
add("b59.b.r2.R", "rsvopt_b_r2_R", 3, "1.038", 65)
add("b59.b.r2.E", "rsvopt_b_r2_E", 2, "0.20", 65)
add("b59.c.k", "rsvopt_k_c", 3, "0.017", 65)
add("b59.c.r0.p", "rsvopt_c_r0_p", 3, "1.793", 65)
add("b59.c.r0.R", "rsvopt_c_r0_R", 3, "0.519", 65)
add("b59.c.r0.E", "rsvopt_c_r0_E", 3, "0.427", 65)
add("b59.c.r1.p", "rsvopt_c_r1_p", 3, "1.325", 65)
add("b59.c.r1.R", "rsvopt_c_r1_R", 3, "1.044", 65)
add("b59.c.r1.E", "rsvopt_c_r1_E", 3, "0.427", 65)
add("b59.c.r2.p", "rsvopt_c_r2_p", 3, "1.849", 65)
add("b59.c.r2.R", "rsvopt_c_r2_R", 3, "0.968", 65)
add("b59.c.r2.E", "rsvopt_c_r2_E", 2, "0.10", 65)
add("b59.cut_lo", "rsvopt_cut_lo", 3, "0.104", 65)
add("b59.cut_hi", "rsvopt_cut_hi", 4, "0.2145", 65)
add("b59.rstar", "rsvopt_rstar", 3, "3.685", 65)


def main() -> None:
    dumps: dict[int, str] = {}
    numbers: dict[str, dict] = {}
    bad = 0
    for ident, key, digits, master, slide, kind in ROWS:
        if slide not in dumps:
            dumps[slide] = (DUMPS / f"slide{slide:02d}.txt").read_text(encoding="utf-8")
        row = REG[key]
        x = Fraction(row["value"].strip())
        if kind == "percent":
            x *= 100
        text = half_up(x, digits)
        in_dump = master in dumps[slide]
        mismatch = (text != master) or not in_dump
        bad += mismatch
        numbers[ident] = {"key": key, "kind": kind, "digits": digits, "text": master if mismatch else text,
                          "master": master, "mismatch": mismatch, "value": row["value"], "status": row["status"],
                          "where": f"slide{slide:02d}.txt"}
        flag = "" if not mismatch else f"   MISMATCH computed {text}, master in dump: {in_dump}"
        print(f"{ident:18s} {key:28s} {digits} {text:>9s}  master {master:>9s}{flag}")
    OUT.write_text(json.dumps({"meta": {"pages": "B4, B6, B7, B13, B17", "source": str(REGISTRY.relative_to(ROOT))},
                               "numbers": numbers}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(numbers)} numbers, {bad} mismatches")


if __name__ == "__main__":
    main()
