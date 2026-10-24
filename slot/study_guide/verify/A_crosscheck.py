#!/usr/bin/env python3
"""Recompute headline values from primitives; print differences and decimal sources.

No chapter program is imported or called. Registry values enter only the final
comparison. Exact fractions define the auction, costs, decimal input beta, and
research equations. Rational bisection encloses rational roots. Other expressions
use 220 decimal digits. This program reports results; it never asserts.
"""

from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import argparse
import re
import sys
from typing import Callable

import mpmath as mp


HERE = Path(__file__).resolve().parent
SNAPSHOT = Path(__file__).resolve().parents[2] / "manuscript" / "numbers.tex"
mp.mp.dps = 220
H, L, P, RHO, COST, K, PI = map(Q, ("10", "1", "1/2", "1/4", "6", "1/50", "1/2"))
BETA, A = Q("0.294655"), Q("1/40")
STRENGTHS = (Q("6/5"), Q("3"), Q("18/5"))


def real(value: Q | mp.mpf | int) -> mp.mpf:
    if isinstance(value, Q):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def show(value: Q | mp.mpf | int, digits: int = 20) -> str:
    return mp.nstr(real(value), digits)


def bracket(function: Callable[[Q], Q], low: Q, high: Q) -> tuple[Q, Q]:
    """Print a setup problem, if present, then perform exact-sign bisection."""
    left_sign, right_sign = function(low), function(high)
    if left_sign == 0:
        return low, low
    if right_sign == 0:
        return high, high
    if left_sign * right_sign > 0:
        print(f"ROOT BRACKET DISAGREEMENT: same endpoint signs at {low}, {high}")
        return low, high
    for _ in range(370):
        middle = (low + high) / 2
        middle_sign = function(middle)
        if middle_sign == 0:
            return middle, middle
        if middle_sign * left_sign > 0:
            low, left_sign = middle, middle_sign
        else:
            high = middle
    return low, high


def auction(r: Q | mp.mpf) -> dict[str, Q | mp.mpf]:
    # Integrate the two pieces of max(p,R), then the constant value after R=v.
    values = {"t0": P * (r - P) / r}
    for name, v in (("H", H), ("L", L)):
        upper = min(r, v)
        target = (P * P + (upper * upper - P * P) / 2 + v * (r - upper)) / r
        rent = (P * (v - P) + v * (upper - P) - (upper * upper - P * P) / 2) / r
        values[f"t{name}"] = target
        values[f"g{name}"] = rent
        values[f"w{name}"] = target - values["t0"]
    values["D"] = values["tH"] - values["tL"]
    values["B"] = (values["gH"] + values["gL"]) / 2
    values["tau"] = (COST - values["gL"]) / (values["gH"] - values["gL"])
    return values


def gross(r: Q | mp.mpf, belief: Q | mp.mpf) -> Q | mp.mpf:
    pay = auction(r)
    return belief * pay["gH"] + (1 - belief) * pay["gL"]


def jump_return(r: Q | mp.mpf) -> Q | mp.mpf:
    pay = auction(r)
    return pay["D"] * (1 - pay["tau"])


def root_spread(d: Q | mp.mpf) -> mp.mpf:
    d = real(d)
    return real(L) + d + mp.sqrt(d * d + 2 * real(L) * d)


def equilibrium(r: Q, presence: mp.mpf, full: bool, hidden: bool = False) -> dict:
    pay = auction(r)
    eta = (BETA, 1 - 2 * BETA, BETA)
    high_orders = (0, 0, 1) if full else (0, 1, 0)
    low_orders = (1, 0, 0) if full else (0, 1, 0)
    f_high = tuple((1 - presence) * real(e) + presence * s for e, s in zip(eta, high_orders))
    f_low = tuple((1 - presence) * real(e) + presence * s for e, s in zip(eta, low_orders))
    beliefs = tuple(fh / (fh + fl) for fh, fl in zip(f_high, f_low))
    entry = tuple(real(RHO) if hidden or gross(r, mu) < COST else mp.mpf(1) for mu in beliefs)
    prices = tuple(real(pay["t0"]) + e * (real(pay["wL"]) + real(pay["D"]) * mu)
                   for e, mu in zip(entry, beliefs))
    e_high = sum(f * e for f, e in zip(f_high, entry))
    e_low = sum(f * e for f, e in zip(f_low, entry))
    average_entry = (e_high + e_low) / 2
    proceeds = real(pay["t0"]) + (e_high * real(pay["wH"]) + e_low * real(pay["wL"])) / 2
    allocation = real((r * r - P * P) / (2 * r))
    allocation += (e_high * real(pay["gH"] + P * P / r) + e_low * real(pay["gL"] + P * P / r)) / 2
    surplus = allocation - real(COST) * (average_entry - real(RHO))
    return dict(entry=average_entry, own=e_high / 2, proceeds=proceeds, surplus=surplus,
                eH=e_high, eL=e_low, mu=beliefs, price=prices)


def registry(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"\\expandafter\\def\\csname reg@([^\\]+)\\endcsname\{(.*)\}", line)
        if match:
            result[match[1]] = match[2]
    return result


def number(raw: str) -> tuple[Q, Q] | None:
    """Return a display value and half a unit of its last displayed place."""
    text = raw.strip()
    percent = text.endswith(r"\%")
    if percent:
        text = text[:-2]
    scale = Q(1, 100) if percent else Q(1)
    try:
        value = Q(text) * scale
    except ValueError:
        return None
    precision = Q(0) if "." not in text else Q(1, 2 * 10 ** len(text.split(".")[1])) * scale
    return value, precision


def compute() -> tuple[list[tuple[str, str, Q | mp.mpf]], list[str]]:
    rows, notes = [], []

    def add(description: str, keys: str, value: Q | mp.mpf) -> None:
        for key in keys.split():
            rows.append((description, key, value))

    e_low = sum((Q(1, factorial(n)) for n in range(111)), Q(0))
    e_high = e_low + Q(112, 111 * factorial(111))
    e = real((e_low + e_high) / 2)
    print("EULER ENCLOSURE: S=sum(1/n!, n=0,...,110); S < e < S+112/(111*111!).")
    print(f"Exact rational width={e_high - e_low}")
    print(f"Width in decimals={show(e_high - e_low, 10)}; arithmetic=220 digits.")
    print(f"mpmath e minus lower endpoint={show(mp.e - real(e_low), 10)}")
    print("The rational enclosure is exact. General expressions below use high precision, not interval certificates.")
    u = e - 1
    presence = u * real(BETA) / (1 + u * real(BETA))
    b = (1 - presence) * real(BETA)
    top = (b + presence) / (2 * b + presence)
    bottom = b / (2 * b + presence)
    for name, keys, value in (
        ("lambda", "lambda_B lambda_p5_B res_cap", presence),
        ("beta", "beta_B beta_p5_B", BETA),
        ("u", "u_B u_p5_B", u),
        ("b", "b_B b_p5_B", b),
        ("neutral liquidity mass", "b0_B", (1 - presence) * real(1 - 2 * BETA)),
        ("M", "M_half_B M_p5_B", top),
        ("m and kappa", "m_half_B m_p5_B", bottom),
        ("b+lambda", "b_plus_lambda_B", b + presence),
        ("purchase probability", "d_slot_B", b + presence / 2),
    ):
        add(name, keys, value)
    print(f"DERIVED kappa={show(min(bottom, 1 - top))} (the registry has no separate kappa key).")

    for index, r in enumerate(STRENGTHS):
        pay = auction(r)
        for obj in ("t0", "tH", "tL", "gH", "gL", "wH", "wL", "D"):
            suffix = {"tH": "th", "tL": "tl", "gH": "gh", "gL": "gl", "wH": "wh", "wL": "wl"}.get(obj, obj)
            add(f"{obj}(r{index})", f"p4_r{index}_{suffix}", pay[obj])
        add(f"Delta(r{index})", f"Delta_r{index}", pay["D"])
        add(f"tau(r{index})", f"tau_r{index} tau_r{index}_frac", pay["tau"])
        add(f"B prior(r{index})", ("Bprior_r0 B_r0_half", "Bprior_r1_B B_r1_half", "Bprior_r2")[index], pay["B"])
        print(f"EXACT AUCTION r{index}: " + "; ".join(f"{key}={value}" for key, value in pay.items()))

    r0, r1, r2 = STRENGTHS
    add("H1 lower margin", "margin_weakcost_B", COST - auction(r0)["B"])
    add("H1 upper margin", "margin_recruit_B", gross(r1, top) - COST)
    add("H2 lower margin", "margin_kweak_B", K - auction(r0)["D"])
    add("H2 upper margin", "margin_kstrong_B", real(RHO * auction(r1)["D"]) * bottom - real(K))
    add("H3 margin", "margin_return_B", real(COST) - gross(r2, top))
    add("H1 posterior margin", "margin_recruit_post_B", top - real(auction(r1)["tau"]))
    add("H3 posterior margin", "margin_return_post_B", real(auction(r2)["tau"]) - top)

    outcomes = [equilibrium(r, presence, i > 0) for i, r in enumerate(STRENGTHS)]
    for i, out in enumerate(outcomes):
        for obj in ("entry", "own", "proceeds"):
            add(f"{obj}(r{i})", f"p4_base_r{i}_{obj}", out[obj])
        add(f"entry(r{i})", ("entry_r0", "entry_r1_B U_entry_B entry_r1_B_7 res_entry_r1", "entry_r2 res_entry_r2")[i], out["entry"])
        add(f"ownership(r{i})", ("own_r0", "own_r1_B", "own_r2_B")[i], out["own"])
        if i == 0:
            add("weak price", "price_r0", out["price"][0])
        else:
            for j, tag in enumerate(("m1", "0", "p1")):
                add(f"price(r{i},{j-1})", f"price_r{i}_{tag}_B", out["price"][j])
    add("class H entry(r1)", "eH_r1_B", outcomes[1]["eH"])
    add("class L entry(r1)", "eL_r1_B", outcomes[1]["eL"])

    lo, hi = Q(82, 59), Q(2686, 1559)
    # Derive the u bounds from M=(1+u)/(2+u), rather than use the displayed fractions.
    tau1, tau2 = auction(r1)["tau"], auction(r2)["tau"]
    for label, tau, keys in (("lower", tau1, "u_lo u_lo_frac"), ("upper", tau2, "u_hi u_hi_frac")):
        bound = (2 * tau - 1) / (1 - tau)
        add(f"u band {label}", keys, bound)
        prior = real(tau) / (real(tau) + real(1 - tau) * e)
        add(f"prior window {label}", f"prior_{'lo' if label == 'lower' else 'hi'}_B", prior)
        add(f"presence band {label}", f"lambda_{'lo' if label == 'lower' else 'hi'}_B res_cap_{'lo' if label == 'lower' else 'hi'}",
            real(bound * BETA) / real(1 + bound * BETA))
    notes.append(f"The independently derived exact u band is {lo} < u < {hi}.")

    root_a = bracket(lambda r: jump_return(r) - K, r0, r2)
    root_j = bracket(lambda r: RHO * jump_return(r) - K, r0, r2)
    ra, rj = (real((bounds[0] + bounds[1]) / 2) for bounds in (root_a, root_j))
    rf, rn, rs = (root_spread(d) for d in (real(K) / bottom, 2 * K / RHO, real(K / RHO) / bottom))
    rc = (top * real(H) - real(COST) + mp.sqrt((top * real(H) - real(COST)) ** 2 + top * ((1 - top) * real(L * L) - real(P * P)))) / top
    for description, keys, value in (("r_A", "rA", ra), ("r_F", "rF_B rF_check_B", rf),
                                      ("r_N", "rN rN_check_B", rn), ("r_J", "rJ", rj),
                                      ("r_S", "rS_B rS_p5_B", rs), ("r_C", "rC_B rC_check_B res_rC", rc)):
        add(description, keys, value)
    print(f"ROOT ENCLOSURES: r_A width={show(root_a[1]-root_a[0], 8)}, r_J width={show(root_j[1]-root_j[0], 8)}")
    add("tau(r_A)", "tau_rA", auction(ra)["tau"])
    add("Delta(r_A)", "Delta_rA", auction(ra)["D"])
    add("entry at r_A", "entry_rA_B", real(RHO) + real(1 - RHO) * b * auction(ra)["D"] / real(2 * K))
    add("entry at r_F", "entry_plateau_B", real(RHO) + real(1 - RHO) * b * auction(rf)["D"] / real(2 * K))
    add("J(r0)", "J_r0", jump_return(r0))
    add("rho J(r1)", "rhoJ_r1", RHO * jump_return(r1))
    add("rho J(r2)", "rhoJ_r2", RHO * jump_return(r2))

    for text in ("1.55", "1.60", "1.65"):
        r, tag = Q(text), text.replace(".", "")
        pay = auction(r)
        def polynomial(lam: Q) -> Q:
            # Clear the denominators in a*lambda=(Delta*m_lambda-k)/2.
            liquidity = (1 - lam) * BETA
            return (2 * A * lam + K) * (2 * liquidity + lam) - pay["D"] * liquidity
        interval = bracket(polynomial, Q(0), Q(1))
        research = real((interval[0] + interval[1]) / 2)
        local_b = (1 - research) * real(BETA)
        local_m = local_b / (2 * local_b + research)
        recruit = BETA * (2 * pay["tau"] - 1) / (BETA + (1 - 2 * BETA) * (1 - pay["tau"]))
        entry = real(RHO) + real(1 - RHO) * (local_b + research / 2)
        own = (real(RHO) + real(1 - RHO) * (local_b + research)) / 2
        e_star = (2 * A * recruit + K) / jump_return(r)
        threshold_entry = RHO + (e_star - RHO) * (BETA + (Q(1, 2) - BETA) * recruit)
        exogenous_e_star = K / jump_return(r)
        threshold_rate = b * real((2 * pay["tau"] - 1) / (1 - pay["tau"]))
        exogenous_entry = real(RHO) + (real(exogenous_e_star) - real(RHO)) * (b + threshold_rate / 2)
        for description, keys, value in (
            ("research intensity", f"res_lambda_r{tag}", research),
            ("research recruitment intensity", f"res_lamE_r{tag}", recruit),
            ("research entry", f"res_entry_r{tag}", entry),
            ("research ownership", f"res_own_r{tag}", own),
            ("research purchase posterior", f"res_muplus_r{tag}", 1 - local_m),
            ("CM research threshold entry", f"res_th_entry_r{tag}", threshold_entry),
            ("CM research purchase entry", f"res_th_estar_r{tag}", e_star),
            ("exogenous CM purchase entry", f"estar_r{tag}", exogenous_e_star),
            ("exogenous CM total entry", f"entry_th_r{tag}_B", exogenous_entry),
        ):
            add(f"{description} at {text}", keys, value)
        print(f"RESEARCH ROOT r={text}: exact bracket width={show(interval[1]-interval[0],8)}, residual={show(polynomial((interval[0]+interval[1])/2),8)}")

    for i, r in enumerate(STRENGTHS):
        for regime in ("frozen", "hidden"):
            out = equilibrium(r, presence, regime == "frozen" or i > 0, regime == "hidden")
            for obj in ("entry", "own", "proceeds"):
                # The manuscript reports these controls at the first two strengths.
                if i < 2:
                    add(f"{regime} {obj}(r{i})", f"p4_{regime}_r{i}_{obj}", out[obj])
                else:
                    print(f"DERIVED {regime} {obj}(r2)={show(out[obj])}; no separate headline registry row.")
            if regime == "hidden" and i == 1:
                for label, value in zip(("sell", "zero", "buy"), out["price"]):
                    add(f"hidden {label} price", f"p4_hidden_r1_{label}_price", value)
    pay = auction(r1)
    hidden = equilibrium(r1, presence, True, True)
    dr = outcomes[1]["proceeds"] - hidden["proceeds"]
    dw = outcomes[1]["surplus"] - hidden["surplus"]
    transfer = presence * real(pay["D"]) * (1 - top + real(RHO) * bottom) / 2
    for description, keys, value in (
        ("access proceeds", "p2_base_r1_proceeds", outcomes[1]["proceeds"]),
        ("hidden proceeds", "p2_base_hidden_proceeds", hidden["proceeds"]),
        ("access surplus", "p2_base_r1_surplus", outcomes[1]["surplus"]),
        ("hidden surplus", "p2_base_hidden_surplus", hidden["surplus"]),
        ("access proceeds gain", "p2_access_proceeds_gain res_dR_r1", dr),
        ("access surplus gain", "p2_access_surplus_gain res_dW_r1", dw),
        ("gross transfer", "p2_access_gross_transfer", transfer),
        ("conditional gross profit", "p2_access_gross_conditional", transfer / presence),
        ("break-even trade scale", "p2_access_break_even", dr / transfer),
    ):
        add(description, keys, value)
    entry_component = real(1 - RHO) * (real(pay["wL"]) + real(pay["D"]) * top)
    class_component = real(RHO * pay["D"]) * (top - bottom)
    spread = outcomes[1]["price"][2] - outcomes[1]["price"][0]
    for description, keys, value in (
        ("spread class component", "ba_class_r1_B", class_component),
        ("spread entry component", "ba_entry_r1_B", entry_component),
        ("execution spread", "ba_r1_B", spread),
        ("spread entry share", "ba_share_r1_B", entry_component / spread),
        ("access/hidden spread ratio", "ba_ratio_r1_B", spread / class_component),
        ("sale impact", "impact_sell_r1_B", class_component / 2),
        ("purchase impact", "impact_buy_r1_B", class_component / 2 + entry_component),
        ("spread at r2", "ba_r2_B", outcomes[2]["price"][2] - outcomes[2]["price"][0]),
    ):
        add(description, keys, value)
    return rows, notes


def compare(rows: list, values: dict[str, str]) -> Counter:
    counts = Counter()
    print("\nREGISTRY COMPARISON: difference = independent value minus displayed registry value.")
    for label, key, value in rows:
        raw = values.get(key)
        parsed = number(raw) if raw is not None else None
        if parsed is None:
            status = "MISSING_KEY" if raw is None else "UNPARSED_DISPLAY"
            print(f"{status} | {label} | {key} | registry={raw} | independent={show(value)}")
        else:
            displayed, half_unit = parsed
            difference = real(value) - real(displayed)
            # Rational registry entries must agree exactly where the result is rational.
            if isinstance(value, Q) and half_unit == 0:
                same = value == displayed
            else:
                same = abs(difference) <= real(half_unit) + mp.mpf("1e-105")
            status = "AGREE" if same else "DISAGREE"
            print(f"{status} | {label} | {key} | registry={raw} | independent={show(value)} | difference={show(difference, 10)}")
        counts[status] += 1
    print("REGISTRY SUMMARY: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    return counts


DECIMAL = re.compile(r"(?<![\d.])[-+]?\d+\.\d+(?![\d.])")
OUTPUT_NUMBER = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w.])")
SOURCE = re.compile(r"verify/([A-Za-z0-9_]+)\.py")


def split_comment(line: str) -> tuple[str, str]:
    match = re.search(r"(?<!\\)%", line)
    return (line[:match.start()], line[match.start()+1:]) if match else (line, "")


def decimal_scan(chapters: Path, outputs: Path) -> Counter:
    counts, source_outputs = Counter(), {}
    files = sorted(chapters.glob("*.tex"))
    print("\nTYPED DECIMAL SCAN: every chapter; reg arguments and comments excluded.")
    print("Each occurrence reports an adjacent source comment, literal presence, and rounding agreement.")
    print("LAYOUT_OR_REFERENCE is an inventory item, not an economic discrepancy.")
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        in_tikz = False
        for index, line in enumerate(lines):
            code, _ = split_comment(line)
            code = re.sub(r"\\reg\{[^}]*\}", lambda m: " " * len(m[0]), code)
            if r"\begin{tikzpicture}" in code:
                in_tikz = True
            for match in DECIMAL.finditer(code):
                token = match[0]
                # Inventory figure coordinates, dimensions, reference labels and paths explicitly.
                prefix, suffix = code[:match.start()], code[match.end():]
                spans = list(re.finditer(r"\\(?:paper|Cref|cref|ref|label|includegraphics|input)\{[^}]*\}", code))
                spans += list(re.finditer(r"\\(?:renewcommand|setlength)\{[^}]*\}\{[^}]*\}", code))
                in_reference = any(item.start() <= match.start() < item.end() for item in spans)
                in_reference = in_reference or bool(re.search(r"(?:Section|Sec\.|Appendix|App\.)[~\s]*$", prefix))
                layout = in_tikz or in_reference or bool(re.match(r"(?:cm|mm|em|ex|pt|\\(?:line|text)width)", suffix))
                if layout:
                    status, source, literal, rounded = "LAYOUT_OR_REFERENCE", "-", "-", "-"
                else:
                    lower, upper = index, index
                    while lower > 0 and lines[lower-1].strip():
                        lower -= 1
                    while upper + 1 < len(lines) and lines[upper+1].strip():
                        upper += 1
                    refs = []
                    for j in range(lower, upper+1):
                        _, comment = split_comment(lines[j])
                        refs.extend((abs(j-index), j, stem) for stem in SOURCE.findall(comment))
                    # The next comment can stand immediately after a paragraph's final number.
                    refs.sort()
                    nearest = [item for item in refs if item[0] == refs[0][0]] if refs else []
                    stems = sorted({item[2] for item in nearest})
                    source = ",".join(stems) if stems else "-"
                    literal, rounded = "no", "no"
                    if not stems:
                        status = "NO_SOURCE_COMMENT"
                    elif len(stems) > 1:
                        status = "AMBIGUOUS_SOURCE_COMMENT"
                    else:
                        stem = stems[0]
                        if stem not in source_outputs:
                            output = outputs / f"{stem}.txt"
                            source_outputs[stem] = output.read_text(encoding="utf-8") if output.exists() else None
                        content = source_outputs[stem]
                        if content is None:
                            status = "OUTPUT_MISSING"
                        else:
                            literal = "yes" if re.search(r"(?<![\w.])" + re.escape(token) + r"(?![\w.])", content) else "no"
                            target = Q(token)
                            decimals = len(token.split(".")[1])
                            half_unit = Q(1, 2 * 10 ** decimals)
                            printed = [Q(item[0]) for item in OUTPUT_NUMBER.finditer(content)]
                            same_value = any(value == target for value in printed)
                            same_round = any(abs(value-target) < half_unit for value in printed)
                            rounded = "yes" if same_round else "no"
                            status = "LITERAL_MATCH" if literal == "yes" else "FORMAT_ONLY" if same_value else "ROUNDING_ONLY" if same_round else "ABSENT_FROM_OUTPUT"
                counts[status] += 1
                print(f"{path.name}:{index+1}:{match.start()+1} | {token} | {status} | source={source} | literal={literal} | rounds={rounded}")
            if r"\end{tikzpicture}" in code:
                in_tikz = False
        print(f"CHAPTER SCANNED: {path.name} ({len(lines)} lines)")
    print(f"DECIMAL SUMMARY: chapters={len(files)}, occurrences={sum(counts.values())}; "
          + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())))
    print("A matching token proves presence only. It does not identify the formula or validate the chapter's argument.")
    return counts


class PrintLog:
    """Send the same printed evidence to the terminal and the saved output."""

    def __init__(self, terminal, saved) -> None:
        self.terminal, self.saved = terminal, saved

    def write(self, text: str) -> int:
        self.terminal.write(text)
        return self.saved.write(text)

    def flush(self) -> None:
        self.terminal.flush()
        self.saved.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=SNAPSHOT)
    parser.add_argument("--chapters", type=Path, default=HERE.parent / "chapters")
    parser.add_argument("--output", type=Path, default=HERE / "output")
    arguments = parser.parse_args()
    arguments.output.mkdir(parents=True, exist_ok=True)
    with (arguments.output / "A_crosscheck.txt").open("w", encoding="utf-8") as saved:
        with redirect_stdout(PrintLog(sys.stdout, saved)):
            print(f"Registry source: {arguments.registry}")
            rows, notes = compute()
            for note in notes:
                print(note)
            compare(rows, registry(arguments.registry))
            saved.flush()
            decimal_scan(arguments.chapters, arguments.output)
            print("\nNo test suite ran. Numerical comparisons and source gaps are reports, not assertions.")


if __name__ == "__main__":
    main()
