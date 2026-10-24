#!/usr/bin/env python3
"""Independent exact calculations for the research equilibrium.

Run from the project root. All output files stay beside this script.
The program reads real primitives and the checked registry. It prints results.
It imports no module from the checked package.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import platform
import re

HERE = Path(__file__).resolve().parent
TEAM = HERE.parent.parent


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    @staticmethod
    def of(x: object) -> Interval:
        if isinstance(x, Interval):
            return x
        v = Q(x)
        return Interval(v, v)

    def __add__(self, other: object) -> Interval:
        y = Interval.of(other)
        return Interval(self.lo + y.lo, self.hi + y.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: object) -> Interval:
        return self + (-Interval.of(other))

    def __rsub__(self, other: object) -> Interval:
        return Interval.of(other) - self

    def __mul__(self, other: object) -> Interval:
        y = Interval.of(other)
        endpoints = [x * z for x in (self.lo, self.hi) for z in (y.lo, y.hi)]
        return Interval(min(endpoints), max(endpoints))

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> Interval:
        y = Interval.of(other)
        if y.lo <= 0 <= y.hi:
            raise ArithmeticError("The interval divisor contains zero.")
        return self * Interval(1 / y.hi, 1 / y.lo)

    def __rtruediv__(self, other: object) -> Interval:
        return Interval.of(other) / self

    def __pow__(self, n: int) -> Interval:
        result = Interval.of(1)
        for _ in range(n):
            result = result * self
        return result

    def sqrt(self) -> Interval:
        scale = 10**65
        low = isqrt((self.lo.numerator * scale**2) // self.lo.denominator)
        high = isqrt((self.hi.numerator * scale**2) // self.hi.denominator)
        return Interval(Q(low, scale), Q(high + 1, scale))

    def text(self, digits: int = 24) -> str:
        return f"[{decimal(self.lo, digits, ROUND_FLOOR)}, {decimal(self.hi, digits, ROUND_CEILING)}]"


def decimal(x: Q, digits: int = 24, mode: str = ROUND_FLOOR) -> str:
    with localcontext() as ctx:
        ctx.prec = max(100, digits + 20)
        ctx.rounding = mode
        return str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal(1).scaleb(-digits)))


def box(x: object) -> Interval:
    return Interval.of(x)


def positive(x: object) -> bool:
    return box(x).lo > 0


def negative(x: object) -> bool:
    return box(x).hi < 0


def midpoint_integral(r: Q, function: object, knots: tuple[Q, ...]) -> Q:
    points = sorted({Q(0), r, *(v for v in knots if 0 < v < r)})
    return sum((right - left) * function((left + right) / 2)
               for left, right in zip(points, points[1:])) / r


def auction(r: Q) -> dict[str, Q]:
    """Integrate the actual auction payoffs on each affine segment."""
    p, low, high = Q(1, 2), Q(1), Q(10)
    t0 = midpoint_integral(r, lambda v: p if v >= p else Q(0), (p,))
    result = {"t0": t0, "S0": midpoint_integral(r, lambda v: v if v >= p else Q(0), (p,))}
    for label, value in (("H", high), ("L", low)):
        result["t" + label] = midpoint_integral(r, lambda v: max(p, min(v, value)), (p, value))
        result["g" + label] = midpoint_integral(r, lambda v: max(Q(0), value - max(p, v)), (p, value))
        result["S" + label] = midpoint_integral(r, lambda v: max(value, v), (value,))
    result["D"] = result["tH"] - result["tL"]
    result["tau"] = (Q(6) - result["gL"]) / (result["gH"] - result["gL"])
    return result


def spread(r: object) -> object:
    return (r - 1)**2 / (2 * r)


def threshold(r: object) -> object:
    return (48 * r - 3) / (4 * (20 * r - r * r - 1))


def low_posterior(lam: object, beta: Q) -> object:
    return beta * (1 - lam) / (2 * beta + (1 - 2 * beta) * lam)


def recruitment(r: object, beta: Q) -> object:
    tau = threshold(r)
    odds = (2 * tau - 1) / (1 - tau)
    return beta * odds / (1 + beta * odds)


def research_root(r: Q, beta: Q, cost: Q, entry: Q = Q(1), low_full: bool = False) -> Interval:
    """Use the quadratic formula for the KKT equation at each support."""
    d = auction(r)["D"]
    if low_full:
        quadratic = 2 * cost * (1 - 2 * beta)
        linear = 4 * cost * beta + 2 * K * (1 - 2 * beta) + (entry + RHO) * beta * d
        constant = beta * (4 * K - (entry + RHO) * d)
    else:
        quadratic = 2 * cost * (1 - 2 * beta)
        linear = 4 * cost * beta + K * (1 - 2 * beta) + entry * beta * d
        constant = beta * (2 * K - entry * d)
    discriminant = box(linear * linear - 4 * quadratic * constant).sqrt()
    return (-linear + discriminant) / (2 * quadratic)


def invert_spread(d: object) -> Interval:
    d = box(d)
    return 1 + d + (d * d + 2 * d).sqrt()


def rising_zero(function: object, left: Q, right: Q) -> Interval:
    for _ in range(160):
        middle = (left + right) / 2
        if function(middle) < 0:
            left = middle
        else:
            right = middle
    return Interval(left, right)


RHO, K, A, BETA = Q(1, 4), Q(1, 50), Q(1, 40), Q("0.294655")
E_PART = sum((Q(1, factorial(n)) for n in range(61)), Q(0))
# After n=60, the first omitted term is 1/61!. Each later ratio is at most 1/62.
E = Interval(E_PART, E_PART + Q(62, 61 * factorial(61)))
CAP = (E - 1) * BETA / (1 + (E - 1) * BETA)
M = E / (1 + E)
DATA: dict[str, object] = {"res_a": A, "res_cap": CAP}
MIDDLE = {"r155": Q(31, 20), "r160": Q(8, 5), "r165": Q(33, 20)}


def tuple_from_orders(r: Q, lam: object, low_full: bool, entry_plus: object,
                      idle: bool = False, hidden: bool = False) -> dict[str, object]:
    """Compute prices first. Compute all deviations from terminal values minus those prices."""
    auc = auction(r)
    noise = [BETA, 1 - 2 * BETA, BETA]
    orders = [-1, 0, 1]
    sh = [0, 1, 0] if idle else [0, 0, 1]
    sl = [0, 1, 0] if idle or not low_full else [1, 0, 0]
    fh = [(1 - lam) * eta + lam * s for eta, s in zip(noise, sh)]
    fl = [(1 - lam) * eta + lam * s for eta, s in zip(noise, sl)]
    mu = [h / (h + l) for h, l in zip(fh, fl)]
    entry = [RHO, RHO, entry_plus]
    prices = [auc["t0"] + en * (auc["tL"] - auc["t0"] + auc["D"] * post)
              for en, post in zip(entry, mu)]
    payoffs = {}
    for label in ("H", "L"):
        payoffs[label] = [q * (auc["t0"] + en * (auc["t" + label] - auc["t0"]) - price) - K * abs(q)
                          for q, en, price in zip(orders, entry, prices)]
    max_h = box(payoffs["H"][2]) if positive(payoffs["H"][2]) else box(0)
    max_l = box(payoffs["L"][0]) if positive(payoffs["L"][0]) else box(0)
    value = (max_h + max_l) / 2
    mass = [(h + l) / 2 for h, l in zip(fh, fl)]
    total_entry = sum((w * en for w, en in zip(mass, entry)), box(0))
    own = sum((h * en / 2 for h, en in zip(fh, entry)), box(0))
    proceeds, surplus = box(0), box(0)
    for label, class_mass in (("H", fh), ("L", fl)):
        for weight, en in zip(class_mass, entry):
            proceeds += weight / 2 * (auc["t0"] + en * (auc["t" + label] - auc["t0"]))
            surplus += weight / 2 * (auc["S0"] + en * (auc["S" + label] - auc["S0"]) - (en - RHO) * 6)
    return dict(lam=lam, mu=mu, entry=entry, prices=prices, payoffs=payoffs, value=value,
                total_entry=total_entry, own=own, proceeds=proceeds, surplus=surplus,
                hidden=hidden, mass=mass)


def show_tuple(r: Q, label: str, result: dict[str, object]) -> None:
    print(f"  {label}: lambda={box(result['lam']).text()}")
    for key in ("mu", "entry", "prices"):
        print(f"    {key} on (-1,0,1): " + " ".join(box(v).text(18) for v in result[key]))
    for kind in ("H", "L"):
        print(f"    U_{kind}(-1,0,1): " + " ".join(box(v).text(18) for v in result["payoffs"][kind]))
    print(f"    V={box(result['value']).text()}; V-a*lambda={box(result['value']-A*result['lam']).text()}")
    print(f"    entry={box(result['total_entry']).text()}; ownership={box(result['own']).text()}")


def enumerate_six() -> None:
    print("EXHAUSTIVE SUPPORT REDUCTION AT THE SIX STRENGTHS")
    for r in (Q(6, 5), *MIDDLE.values(), Q(3), Q(18, 5)):
        auc = auction(r)
        print(f"r={r}: Delta={auc['D']}, tau={auc['tau']}")
        print("  actual-auction minus closed forms:", [
            auc["t0"] - Q(1, 2) * (1 - Q(1, 2)/r),
            auc["tH"] - r/2 - Q(1, 8)/r,
            auc["tL"] - 1 + Q(3, 8)/r,
            auc["gH"] - 10 + r/2 + Q(1, 8)/r,
            auc["gL"] - Q(3, 8)/r, auc["D"] - spread(r)])
        if auc["D"] < K:
            print(f"  all nonzero supports excluded: k-Delta={K-auc['D']}")
            show_tuple(r, "Z", tuple_from_orders(r, Q(0), False, RHO, idle=True))
            print("  IM/C1=I0/C1=IM/CM=I0/CM: Z")
            continue
        if RHO * auc["D"] / 2 < K:
            print(f"  positive research forces H full; L full and L mixed excluded: k-rho*Delta/2={K-RHO*auc['D']/2}")
            low_full = False
        else:
            bound = RHO * auc["D"] * low_posterior(CAP, BETA) - K - A * CAP
            print("  every-profile lower bound minus a*cap:", box(bound).text())
            print("  H mixed, H idle, L mixed and L idle excluded by the positive uniform bound.")
            low_full = True
        zero_value = max(Q(0), RHO * auc["D"] / 2 - K)
        print(f"  zero research: V={zero_value}; feasible={zero_value == 0}")
        if zero_value == 0:
            show_tuple(r, "Z", tuple_from_orders(r, Q(0), False, RHO, idle=True))
        for en, label in ((RHO, "floor interior"), (Q(1), "recruit interior")):
            root = research_root(r, BETA, A, en, low_full)
            le = recruitment(r, BETA)
            direction = negative(root-le) if en == RHO else positive(root-le)
            admissible = positive(root) and positive(CAP-root) and direction
            print(f"  {label}: root={root.text()}, below cap={positive(CAP-root)}, correct entry side={direction}, feasible={admissible}")
            if admissible:
                show_tuple(r, label, tuple_from_orders(r, root, low_full, en))
        le = recruitment(r, BETA)
        es = ((2*A*le + (2*K if low_full else K)) / (auc["D"]*(1-auc["tau"]))
              - (RHO if low_full else 0))
        feasible_th = positive(CAP-le) and RHO < es < 1
        print(f"  threshold: lambda={le}, e*={es}, below cap={positive(CAP-le)}, rho<e*<1={RHO<es<1}, CM feasible={feasible_th}")
        if feasible_th:
            show_tuple(r, "T (CM)", tuple_from_orders(r, le, low_full, es))
        recruits = positive(M-auc["tau"])
        cap_entry = Q(1) if recruits else RHO
        candidate = tuple_from_orders(r, CAP, low_full, cap_entry)
        cap_ok = positive(candidate["value"]-A*CAP)
        print(f"  cap: recruits={recruits}, research KKT margin={box(candidate['value']-A*CAP).text()}, feasible={cap_ok}")
        if cap_ok:
            show_tuple(r, "cap", candidate)
        print("  IM/C1=I0/C1: " + ("Z,R; IM/CM=I0/CM: Z,R,T" if not low_full else "cap; IM/CM=I0/CM: cap"))


def calculate_registry() -> None:
    for tag, r in MIDDLE.items():
        auc = auction(r)
        root = research_root(r, BETA, A)
        le = recruitment(r, BETA)
        result = tuple_from_orders(r, root, False, Q(1))
        entries = {"lambda": root, "entry": result["total_entry"], "muplus": result["mu"][2],
                   "own": result["own"], "lamE": le, "Delta": auc["D"], "tau": auc["tau"],
                   "lamgap": root-le, "capgap": CAP-root, "UH": result["payoffs"]["H"][2],
                   "ULgap": K-RHO*auc["D"]/2}
        DATA.update({f"res_{name}_{tag}": value for name, value in entries.items()})
        es = (2*A*le+K)/(auc["D"]*(1-auc["tau"]))
        DATA[f"res_th_estar_{tag}"] = es
        DATA[f"res_th_entry_{tag}"] = RHO+(es-RHO)*(BETA+(Q(1, 2)-BETA)*le)
        old_root = research_root(r, Q(1, 3), A)
        DATA[f"res_calA_lambda_{tag}"] = old_root
        DATA[f"res_calA_entry_{tag}"] = Q(1, 2)+old_root/8

    phi = lambda r: spread(r)*(1-threshold(r))-K-2*A*recruitment(r, BETA)
    rr = rising_zero(phi, Q(6, 5), Q(7, 4))
    rcap = invert_spread((2*A*CAP+K)*(1+E))
    rn = invert_spread(2*K/RHO)
    ra = rising_zero(lambda r: spread(r)*(1-threshold(r))-K, Q(6, 5), Q(7, 4))
    # Clear the denominator in threshold(r)=M, then divide the equation by four.
    ceiling_linear = 12-20*M
    ceiling = (-ceiling_linear+(ceiling_linear**2-4*M*(M-Q(3, 4))).sqrt())/(2*M)
    dmin = Q(11, 72)
    c = 1-threshold(Q(7, 4))
    dmax = spread(Q(7, 4))
    tau_prime_bound = 3*(8*Q(7, 4)**2-Q(7, 4)+2)/(2*(20*Q(6, 5)-Q(6, 5)**2-1)**2)
    lead = dmin*c-dmax*tau_prime_bound
    lam_deriv = BETA*tau_prime_bound/(BETA+(1-2*BETA)*c)**2
    mono = lead/(2*lam_deriv)
    mono3 = lead/(2*Q(1, 3)*tau_prime_bound/(Q(1, 3)+Q(1, 3)*c)**2)
    vals = {"rR": rr, "rcap": rcap, "lambda_rR": recruitment(rr, BETA),
            "entry_rR": RHO+(1-RHO)*(BETA+(Q(1, 2)-BETA)*recruitment(rr, BETA)),
            "entry_cap": RHO+(1-RHO)*(BETA+(Q(1, 2)-BETA)*CAP),
            "amono": mono, "amono_third": mono3, "phi_r155": phi(Q(31, 20)),
            "phip_lb": lead-2*A*lam_deriv, "rA": ra, "dphi_lead": lead,
            "bound_dDelta": dmin, "bound_tau74": c, "bound_Delta74": dmax,
            "bound_taup": tau_prime_bound, "lamE_r175": recruitment(Q(7, 4), BETA),
            "rN": rn, "rC": ceiling, "rUR": invert_spread((K+A*CAP)*(1+E)/RHO)}
    DATA.update({"res_"+name: value for name, value in vals.items()})
    for tag, r in (("r1", Q(3)), ("r2", Q(18, 5))):
        auc = auction(r)
        DATA[f"margin_res_bound_{tag}_B"] = RHO*auc["D"]/(1+E)-K-A*CAP
        DATA[f"margin_res_tau_{tag}_B"] = M-auc["tau"] if tag == "r1" else auc["tau"]-M
        DATA[f"res_entry_{tag}"] = vals["entry_cap"] if tag == "r1" else RHO

    lo, hi = recruitment(Q(3), BETA), recruitment(Q(18, 5), BETA)
    upper = (spread(Q(31, 20))*(1-threshold(Q(31, 20)))-K)/(2*recruitment(Q(31, 20), BETA))
    lower = lambda cap: (spread(Q(33, 20))*low_posterior(cap, BETA)-K)/(2*cap)
    u3 = lambda cap: (RHO*spread(Q(3))*low_posterior(cap, BETA)-K)/cap
    u36 = lambda cap: (RHO*spread(Q(18, 5))*low_posterior(cap, BETA)-K)/cap
    for n, cap in enumerate((lo, Q(3, 10), Q(31, 100), Q(8, 25), Q(33, 100), CAP, hi)):
        for name, value in (("cap", cap), ("alo", lower(cap)), ("aU3", u3(cap)),
                            ("a36", u36(cap)), ("width", upper-lower(cap))):
            DATA[f"res_region_{name}_{n}"] = value
    region = {"cap_lo": lo, "cap_hi": hi, "a_up": upper, "a_lo": lower(CAP),
              "cap_lo_a": DATA["res_lambda_r165"],
              "a_floor3": (RHO*spread(Q(3))*(1-threshold(Q(3)))-K)/lo, "aU3_B": u3(CAP)}
    DATA.update({"res_"+name: value for name, value in region.items()})
    x = (spread(Q(33, 20))/(1+E)-K)/(2*A)
    DATA["res_beta_lo"] = x/((1-x)*(E-1))
    target = (spread(Q(31, 20))*(1-threshold(Q(31, 20)))-K)/(2*A)
    odds155 = (2*threshold(Q(31, 20))-1)/(1-threshold(Q(31, 20)))
    DATA["res_beta_hi"] = target/((1-target)*odds155)

    access = tuple_from_orders(Q(3), CAP, True, Q(1))
    hidden = tuple_from_orders(Q(3), CAP, True, RHO, hidden=True)
    for key, value in (("R_access_r1", access["proceeds"]), ("R_hidden_r1", hidden["proceeds"]),
                       ("dR_r1", access["proceeds"]-hidden["proceeds"]),
                       ("W_access_r1", access["surplus"]), ("W_hidden_r1", hidden["surplus"]),
                       ("dW_r1", access["surplus"]-hidden["surplus"]),
                       ("cost_r1", A*CAP*CAP/2), ("tcost_r1", K*CAP), ("Delta_r0", spread(Q(6, 5)))):
        DATA["res_"+key] = value
    margins = {"aup": upper-A, "alo": A-lower(CAP), "caplo": CAP-lo, "caphi": hi-CAP,
               "weak": K-spread(Q(6, 5)), "nosale": 2*K-RHO*spread(Q(33, 20)),
               "half": 6-(auction(Q(6, 5))["gH"]+auction(Q(6, 5))["gL"])/2,
               "beta": Q(1, 3)-BETA, "rR": Q(31, 20)-rr, "rcap": rcap-Q(33, 20),
               "rN": rn-rcap, "amono": mono-A, "lamcap": CAP-DATA["res_lambda_r165"]}
    DATA.update({f"margin_res_{key}_B": value for key, value in margins.items()})


def report_registry() -> None:
    path = TEAM/"registry/P3_research.csv"
    with path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    differences, unresolved, output, rational_rows = [], [], [], 0
    invalid_notes, rational_values, note_rows = [], [], []
    for row in rows:
        key = row["key"]
        if key not in DATA:
            unresolved.append(key)
            continue
        result = box(DATA[key])
        display = row["display"]
        target = Q(display)
        if "/" in display:
            compatible = result.lo == target == result.hi
            rational_rows += 1
        else:
            decimals = len(display.partition(".")[2])
            half_unit = Q(1, 2*10**decimals)
            compatible = target-half_unit <= result.lo and result.hi <= target+half_unit
        delta = result-Q(row["value"])
        if not compatible:
            differences.append(key)
        rational_identity = "not a rational value field"
        if "/" in row["value"]:
            rational_identity = str(result.lo == Q(row["value"]) == result.hi)
            rational_values.append((key, rational_identity))
        match = re.search(r"enclosure \[([^,]+), ([^\]]+)\]", row["note"])
        if match:
            written_low, written_high = map(Q, match.groups())
            if result.hi < written_low or written_high < result.lo:
                invalid_notes.append(key)
                note_rows.append(dict(key=key, written_lo=match.group(1), written_hi=match.group(2),
                                      corrected_lo=decimal(result.lo, 45),
                                      corrected_hi=decimal(result.hi, 45, ROUND_CEILING)))
        output.append(dict(key=key, checked_value=row["value"], display=display,
                           independent_lo=decimal(result.lo, 45), independent_hi=decimal(result.hi, 45, ROUND_CEILING),
                           delta_lo=decimal(delta.lo, 45), delta_hi=decimal(delta.hi, 45, ROUND_CEILING),
                           display_agrees=compatible, exact_rational_identity=rational_identity))
        print(f"  {key}: {result.text(30)} display={display}, agrees={compatible}, exact={rational_identity}")
    with (HERE/"registry_comparison.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    with (HERE/"invalid_enclosures.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["key", "written_lo", "written_hi", "corrected_lo", "corrected_hi"])
        writer.writeheader()
        writer.writerows(note_rows)
    exact = {key: dict(lo=str(box(value).lo), hi=str(box(value).hi)) for key, value in DATA.items()}
    (HERE/"exact_enclosures.json").write_text(json.dumps(exact, indent=2)+"\n")
    print(f"REGISTRY: input={len(rows)}, recomputed={len(output)}, unresolved={unresolved}, display differences={differences}, rational displays={rational_rows}")
    print(f"RATIONAL VALUE FIELDS: count={len(rational_values)}, different={[key for key, identity in rational_values if identity != 'True']}")
    print(f"WRITTEN ENCLOSURES THAT EXCLUDE THE EXACT VALUE: count={len(invalid_notes)}, keys={invalid_notes}")


def main() -> None:
    print("XP3 independent research calculation; exact rational endpoints; Python", platform.python_version())
    print("e enclosure:", E.text(78))
    print("cap enclosure:", CAP.text(45))
    enumerate_six()
    calculate_registry()
    print("REGISTRY RECOMPUTATION")
    report_registry()
    print("REGION ENDPOINTS AND BOUNDS")
    for key in ("res_cap_lo", "res_cap_hi", "res_a_lo", "res_a_up", "res_beta_lo", "res_beta_hi",
                "res_region_aU3_6", "res_region_a36_6", "res_rR", "res_rcap", "res_rUR"):
        print(key, box(DATA[key]).text(40))
    print("GENERAL BETA: uniform research margin at beta=1/3:",
          box(RHO*spread(Q(3))/(1+E)-K-A*(E-1)/(E+2)).text())
    print("PRICE ACCESS")
    for key in ("res_R_hidden_r1", "res_R_access_r1", "res_dR_r1", "res_W_hidden_r1", "res_W_access_r1",
                "res_dW_r1", "res_cost_r1", "res_tcost_r1"):
        print(key, box(DATA[key]).text(40))
    print("SCOPE AND CERTIFICATE CORRECTIONS")
    lo160 = (spread(Q(8, 5))*low_posterior(CAP, BETA)-K)/(2*CAP)
    print("lower cost for strict rise across the triple, with a cap at 1.65 allowed:", box(lo160).text(40))
    print("cap gap at the upper boundary:", box(DATA["margin_res_caphi_B"]).text(40))
    print("posterior gap at the upper boundary:", box(DATA["margin_res_tau_r2_B"]).text(40))
    print("at r_C, CM allows every e_plus in [rho,1], so aggregate entry spans:",
          box(RHO).text(), box(DATA["res_entry_cap"]).text())
    print("research at cap stays strict at r_C: lower bound inherited from r=3:",
          box(DATA["margin_res_bound_r1_B"]).text())
    weak = auction(Q(6, 5))
    print("weak-incumbent general-statement counterexample, c_H=1:",
          "prior gross profit minus c_H =", (weak["gH"]+weak["gL"])/2-1,
          "; Delta<k, zero research, high-cost entry=1, total entry=1")
    sources = [TEAM/"proofs/P3_research.tex", TEAM/"memos/P3_research.md", TEAM/"registry/P3_research.csv",
               TEAM/"proofs/P1_core.tex", HERE/"recompute.py"]
    receipt = {"date": "2026-10-23", "method": "independent exact rational interval arithmetic; no imported package code",
               "e_partial_sum_last_term": 60, "sqrt_scale": "10^65", "rational_bisection_steps": 160,
               "python": platform.python_version(),
               "sha256": {str(path.relative_to(TEAM)): sha256(path.read_bytes()).hexdigest() for path in sources}}
    (HERE/"receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")


if __name__ == "__main__":
    main()
