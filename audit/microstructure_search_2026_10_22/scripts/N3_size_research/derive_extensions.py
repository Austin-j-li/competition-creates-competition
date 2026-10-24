"""Exact order-slot calculations. Run from the repository root; output is print-only."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __add__(self, other):
        other = iv(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -iv(other)

    def __rsub__(self, other):
        return iv(other) + -self

    def __mul__(self, other):
        other = iv(other)
        values = [self.lo * other.lo, self.lo * other.hi,
                  self.hi * other.lo, self.hi * other.hi]
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = iv(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("The denominator interval contains zero.")
        return self * Interval(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other):
        return iv(other) / self


def iv(value):
    return value if isinstance(value, Interval) else Interval(F(value), F(value))


def show(value):
    value = iv(value)
    if value.lo == value.hi:
        return f"{value.lo} ({float(value.lo):.12f})"
    def decimal_bound(endpoint, upper):
        scaled = endpoint * 10 ** 12
        integer = (-(-scaled.numerator // scaled.denominator) if upper
                   else scaled.numerator // scaled.denominator)
        sign = "-" if integer < 0 else ""
        magnitude = abs(integer)
        return f"{sign}{magnitude // 10 ** 12}.{magnitude % 10 ** 12:012d}"
    return (f"[{decimal_bound(value.lo, False)}, {decimal_bound(value.hi, True)}] "
            f"rational_width={value.hi - value.lo}")


def root(function, lo=F(0), hi=F(1), steps=100):
    flo, fhi = function(lo), function(hi)
    print(f"  root endpoint signs: {flo} ; {fhi}")
    if flo * fhi >= 0:
        print("  no strict sign bracket; no root interval returned")
        return None
    for _ in range(steps):
        mid = (lo + hi) / 2
        fmid = function(mid)
        if fmid == 0:
            return iv(mid)
        if flo * fmid < 0:
            hi = mid
        else:
            lo, flo = mid, fmid
    result = Interval(lo, hi)
    print(f"  root rational endpoints: {lo} ; {hi}")
    print(f"  root final endpoint signs: {function(lo)} ; {function(hi)}")
    return result


def auction(r):
    p = F(1, 2)
    return {
        "t0": p * (1 - p / r), "tH": r / 2 + p * p / (2 * r),
        "tL": 1 - (1 - p * p) / (2 * r),
        "gH": 10 - r / 2 - p * p / (2 * r), "gL": F(3, 8) / r,
        "D": (r - 1) ** 2 / (2 * r),
        "tau": (48 * r - 3) / (4 * (20 * r - r * r - 1)),
        "S0": r / 2 - p * p / (2 * r), "SH": F(10),
        "SL": (r * r + 1) / (2 * r),
    }


K, RHO = F(1, 50), F(1, 4)
SIZES = (-2, -1, 0, 1, 2)
LAM_SIZE = F(1, 5)
ETA_SIZE = {-2: F(5, 28), -1: F(1, 20), 0: F(19, 35),
            1: F(1, 20), 2: F(5, 28)}
ETA_UNIT = {-1: F(1, 3), 0: F(1, 3), 1: F(1, 3)}


def order_game(r, lam, eta, high, low, hidden=False):
    a = auction(r)
    masses, mu, entry, price = {}, {}, {}, {}
    utilities = {"H": {}, "L": {}}
    for q in eta:
        masses[q] = (iv((1 - lam) * eta[q]) + lam * high.get(q, F(0)),
                     iv((1 - lam) * eta[q]) + lam * low.get(q, F(0)))
        hq, lq = masses[q]
        mu[q] = hq / (hq + lq)
        if hidden or mu[q].hi < a["tau"]:
            entry[q] = iv(RHO)
        elif mu[q].lo >= a["tau"]:
            entry[q] = iv(1)
        else:
            entry[q] = Interval(RHO, F(1))
        price[q] = a["t0"] + entry[q] * (a["tL"] - a["t0"] + a["D"] * mu[q])
        for cls in utilities:
            value = a["t0"] + entry[q] * (a["t" + cls] - a["t0"])
            utilities[cls][q] = q * (value - price[q]) - K * abs(q)
    total_entry, revenue, welfare, volume = iv(0), iv(0), iv(0), iv(0)
    for q, (hq, lq) in masses.items():
        total_entry += (hq + lq) / 2 * entry[q]
        for cls, mq in (("H", hq), ("L", lq)):
            revenue += mq / 2 * (a["t0"] + entry[q] * (a["t" + cls] - a["t0"]))
            welfare += mq / 2 * (a["S0"] + entry[q] * (a["S" + cls] - a["S0"])
                                       - (entry[q] - RHO) * 6)
        volume += lam * (high.get(q, F(0)) + low.get(q, F(0))) * abs(q) / 2
    return {"mu": mu, "e": entry, "P": price, "U": utilities,
            "E": total_entry, "R": revenue, "W": welfare,
            "informed_volume": volume, "W_net_trade": welfare - K * volume}


def report_game(label, r, lam, eta, high, low, hidden=False):
    print(f"\n{label}: r={r} lambda={show(lam)} hidden={hidden}")
    print("  high probabilities:", {q: show(v) for q, v in high.items()})
    print("  low probabilities:", {q: show(v) for q, v in low.items()})
    game = order_game(r, lam, eta, high, low, hidden)
    for q in eta:
        print(f"  q={q}: mu={show(game['mu'][q])} e={show(game['e'][q])} "
              f"price={show(game['P'][q])}")
        print(f"        U_H={show(game['U']['H'][q])} U_L={show(game['U']['L'][q])}")
    for key in ("E", "R", "W", "informed_volume", "W_net_trade"):
        print(f"  {key}={show(game[key])}")
    return game


def size_results():
    print("SECTION A: SIZE CHOICE; EXACT PARAMETERS")
    print("lambda=1/5; eta(+/-1)=1/20; eta(+/-2)=5/28; eta(0)=19/35")
    print("eta sum:", sum(ETA_SIZE.values()))
    print("b1=1/25 b2=1/7 M1_full=6/7 M2_full=12/17")
    for r in (F(6, 5), F(31, 20), F(8, 5), F(33, 20), F(3), F(18, 5)):
        a = auction(r)
        print(f"auction r={r}: D={a['D']} tau={a['tau']}")
    report_game("weak", F(6, 5), LAM_SIZE, ETA_SIZE, {0: F(1)}, {0: F(1)})
    old_entry = None
    for r in (F(31, 20), F(8, 5), F(33, 20)):
        a1 = F(1, 25) * (auction(r)["D"] / K - 2)
        high = {1: a1 / LAM_SIZE, 0: 1 - a1 / LAM_SIZE}
        game = report_game("small-order branch", r, LAM_SIZE, ETA_SIZE, high, {0: F(1)})
        print("  chosen purchase identity residual U_H(1)=", show(game["U"]["H"][1]))
        if old_entry is not None:
            print("  entry increase=", show(game["E"] - old_entry))
        old_entry = game["E"]
        report_game("no informed trade", r, LAM_SIZE, ETA_SIZE, {0: F(1)}, {0: F(1)})
    # The low class uses both sizes at r=3. The utility difference falls strictly in a1.
    r = F(3)
    d = auction(r)["D"]
    def low_difference(a1):
        return (RHO * d * F(1, 25) / (F(2, 25) + a1) - K
                - 2 * (RHO * d * F(1, 7) / (F(2, 7) + LAM_SIZE - a1) - K))
    a1 = root(low_difference, F(0), LAM_SIZE)
    low = {-1: a1 / LAM_SIZE, -2: 1 - a1 / LAM_SIZE}
    strong = report_game("large purchase, partial expected sale", r, LAM_SIZE, ETA_SIZE, {2: F(1)}, low)
    hidden = report_game("hidden price equilibrium", r, LAM_SIZE, ETA_SIZE,
                         {1: a1 / LAM_SIZE, 2: 1 - a1 / LAM_SIZE}, low, True)
    for key in ("R", "W", "W_net_trade"):
        print(f"price access difference {key}={show(strong[key] - hidden[key])}")
    report_game("floor equilibrium", F(18, 5), LAM_SIZE, ETA_SIZE, {2: F(1)}, {-2: F(1)})
    # Both strong economies also support a high-class mixture across sizes.
    for r in (F(3), F(18, 5)):
        d = auction(r)["D"]
        def high_difference(a1):
            return (d * F(1, 25) / (F(2, 25) + a1) - K
                    - 2 * (RHO * d * F(1, 7) / (F(2, 7) + LAM_SIZE - a1) - K))
        a1h = root(high_difference, F(0), LAM_SIZE)
        if r == F(3):
            low = {-1: a1 / LAM_SIZE, -2: 1 - a1 / LAM_SIZE}
        else:
            low = {-2: F(1)}
        report_game("alternative with entry after size one", r, LAM_SIZE, ETA_SIZE,
                    {1: a1h / LAM_SIZE, 2: 1 - a1h / LAM_SIZE}, low)
    # A nonzero smaller sale cannot be pure when the unused large sale earns twice its upper bound.
    print("pure small sale exclusion, r=3: baseline per unit=", RHO * auction(F(3))["D"] / 2 - K)


def research_results():
    print("\nSECTION B: PRIVATE RESEARCH WITH A SUCCESS CEILING")
    cap, coefficient = F(6, 17), F(1, 40)
    print("C(lambda)=a*lambda^2/2; a=1/40; cap=6/17; eta each=1/3")
    previous_lam = previous_entry = None
    for r in (F(31, 20), F(8, 5), F(33, 20)):
        a = auction(r)
        d, tau = a["D"], a["tau"]
        # V=(D*(1-lambda)/(2+lambda)-k)/2; C'=a*lambda.
        def equation(lam):
            return (2 * coefficient * lam + K) * (2 + lam) - d * (1 - lam)
        lam = root(equation, F(0), cap)
        game = report_game("research branch", r, lam, ETA_UNIT, {1: F(1)}, {0: F(1)})
        value = game["U"]["H"][1] / 2
        print("  research value=", show(value), "marginal cost=", show(coefficient * lam))
        print("  private deviation derivative residual=", show(value - coefficient * lam))
        print("  net research payoff=", show(lam * value - coefficient * lam * lam / 2))
        print("  surplus after research and informed trade costs=",
              show(game["W_net_trade"] - coefficient * lam * lam / 2))
        if previous_lam is not None:
            print("  research increase=", show(lam - previous_lam))
            print("  entry increase=", show(game["E"] - previous_entry))
        previous_lam, previous_entry = lam, game["E"]
        threshold = (2 * tau - 1) / (2 - tau)
        print("  cost upper bound for recruitment=", show((d * (1 - tau) - K) / (2 * threshold)))
        print("  cost lower bound for slack capacity=", show((d * (1 - cap) / (2 + cap) - K) / (2 * cap)))
        tied_e = (2 * coefficient * threshold + K) / (d * (1 - tau))
        print("  threshold success probability=", show(threshold))
        print("  CM entry at threshold=", show(tied_e))
        threshold_entry = RHO + (tied_e - RHO) * ((1 - threshold) / 3 + threshold / 2)
        print("  CM aggregate entry=", show(threshold_entry))
    # An open cost interval keeps the whole requested triple strictly interior.
    dl = auction(F(33, 20))["D"]
    lower_cost = (dl * (1 - cap) / (2 + cap) - K) / (2 * cap)
    a0 = auction(F(31, 20))
    threshold = (2 * a0["tau"] - 1) / (2 - a0["tau"])
    upper_cost = (a0["D"] * (1 - a0["tau"]) - K) / (2 * threshold)
    print("open cost coefficient interval:", show(lower_cost), ";", show(upper_cost))
    for r in (F(3), F(18, 5)):
        a = auction(r)
        lower_value = RHO * a["D"] * F(11, 40) - K
        print(f"uniform research margin r={r}: {lower_value - coefficient * cap}")
        game = report_game("capacity research", r, cap, ETA_UNIT, {1: F(1)}, {-1: F(1)})
        print("  surplus after research and informed trade costs=",
              show(game["W_net_trade"] - coefficient * cap * cap / 2))
    seen = order_game(F(3), cap, ETA_UNIT, {1: F(1)}, {-1: F(1)})
    unseen = order_game(F(3), cap, ETA_UNIT, {1: F(1)}, {-1: F(1)}, True)
    print("research cost at cap:", coefficient * cap * cap / 2)
    for key in ("R", "W_net_trade"):
        print(f"research price access difference {key}={show(seen[key] - unseen[key])}")


def no_ceiling_results():
    print("\nSECTION C: PRIVATE RESEARCH WITHOUT THE SUCCESS CEILING")
    a = auction(F(18, 5))
    threshold = (2 * a["tau"] - 1) / (2 - a["tau"])
    lower_value = RHO * a["D"] * (1 - a["tau"]) - K
    print("same cost as Section B, a=1/40: no floor equilibrium at r=18/5")
    print("  necessary lambda upper bound:", show(threshold))
    print("  research value lower bound:", show(lower_value))
    print("  marginal research cost upper bound:", show(threshold / 40))
    print("  strict excess research incentive:", show(lower_value - threshold / 40))
    coefficient = F(1, 4)
    print("C(lambda)=lambda^2/8; lambda in [0,1]; eta each=1/3")
    for r in (F(3), F(18, 5)):
        a = auction(r)
        d, tau = a["D"], a["tau"]
        for eplus in (RHO, F(1)):
            multiplier = (eplus + RHO) / 2
            def equation(lam):
                return (coefficient * lam + K) * (2 + lam) - multiplier * d * (1 - lam)
            lam = root(equation, F(0), F(9, 10))
            game = report_game(f"unbounded research eplus={eplus}", r, lam, ETA_UNIT,
                               {1: F(1)}, {-1: F(1)})
            value = (game["U"]["H"][1] + game["U"]["L"][-1]) / 2
            print("  private deviation derivative residual=", show(value - coefficient * lam))
        threshold = (2 * tau - 1) / (2 - tau)
        tied_e = 2 * (coefficient * threshold + K) / (d * (1 - tau)) - RHO
        print("  CM lambda threshold=", show(threshold), "entry=", show(tied_e))
        print("  CM aggregate entry=", show(RHO + (tied_e - RHO) * ((1 - threshold) / 3 + threshold / 2)))


def receipt():
    base = Path("audit/microstructure_search_2026_10_22/scripts/N3_size_research")
    pinned = {}
    for name in ("main.tex", "online_appendix.tex"):
        data = subprocess.check_output(["git", "-C", "overleaf/paper", "show", "01bd5d6:" + name])
        pinned[name] = hashlib.sha256(data).hexdigest()
    print("\nRECEIPT", json.dumps({
        "python": sys.version, "platform": platform.platform(), "arithmetic": "exact fractions and rational intervals",
        "root_steps": 100, "pinned_commit": "01bd5d6", "pinned_sha256": pinned,
        "script_sha256": hashlib.sha256((base / "derive_extensions.py").read_bytes()).hexdigest(),
        "benchmark": {"h": "10", "ell": "1", "p": "1/2", "rho": "1/4", "c_L": "0", "c_H": "6", "k": "1/50", "pi": "1/2"},
        "scope": "Selected equilibria; complete capped research correspondence at the stated middle strengths.",
    }, sort_keys=True))


if __name__ == "__main__":
    size_results()
    research_results()
    no_ceiling_results()
    receipt()
