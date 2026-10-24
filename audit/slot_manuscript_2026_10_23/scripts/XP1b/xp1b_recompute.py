"""Print independent exact certificates for the four round-2 rows and the CM endpoint.

Run from the repository root. All output stays beside this file.
No checked module is imported. Rational intervals bound every computed value.
"""

import csv
import hashlib
import math
from pathlib import Path
import re
from fractions import Fraction as Q


HERE = Path(__file__).resolve().parent
TEAM = HERE.parents[1]
RHO, FEE, BETA = Q(1, 4), Q(1, 50), Q("0.294655")


class Interval:
    """Closed intervals with rational endpoints and exact arithmetic."""

    def __init__(self, low, high=None):
        if isinstance(low, Interval):
            self.low, self.high = low.low, low.high
        else:
            self.low = Q(low)
            self.high = self.low if high is None else Q(high)

    def __add__(self, other):
        other = Interval(other)
        return Interval(self.low + other.low, self.high + other.high)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.high, -self.low)

    def __sub__(self, other):
        return self + -Interval(other)

    def __rsub__(self, other):
        return Interval(other) + -self

    def __mul__(self, other):
        other = Interval(other)
        ends = [a * b for a in (self.low, self.high)
                for b in (other.low, other.high)]
        return Interval(min(ends), max(ends))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Interval(other)
        if other.low <= 0 <= other.high:
            raise ValueError("The divisor contains zero.")
        return self * Interval(1 / other.high, 1 / other.low)

    def __rtruediv__(self, other):
        return Interval(other) / self


def decimal(q, digits=24, upper=False):
    """Round a rational endpoint outwards as a decimal."""
    q = Q(q)
    scale = 10 ** digits
    value = (-((-q.numerator * scale) // q.denominator) if upper
             else (q.numerator * scale) // q.denominator)
    sign = "-" if value < 0 else ""
    value = abs(value)
    return f"{sign}{value // scale}.{value % scale:0{digits}d}"


def enclosure(x):
    x = Interval(x)
    return f"[{decimal(x.low)}, {decimal(x.high, upper=True)}]"


def nearest(q, digits=6):
    q = Q(q)
    scale = 10 ** digits
    value = (abs(q) * scale + Q(1, 2)).__floor__()
    sign = "-" if q < 0 else ""
    return f"{sign}{value // scale}.{value % scale:0{digits}d}"


def sign(x):
    x = Interval(x)
    if x.low > 0:
        return "positive"
    if x.high < 0:
        return "negative"
    if x.low == x.high == 0:
        return "exact zero"
    return "contains zero"


def auction(r):
    """Integrate auction proceeds and rents, split at p and ell."""
    reserve, low, high = Q(1, 2), Q(1), Q(10)
    t0 = reserve * (r - reserve) / r
    th = (reserve * reserve + (r * r - reserve * reserve) / 2) / r
    tl = (reserve * reserve + (low * low - reserve * reserve) / 2
          + low * (r - low)) / r
    gh = ((high - reserve) * reserve + high * (r - reserve)
          - (r * r - reserve * reserve) / 2) / r
    gl = ((low - reserve) * reserve + (low - reserve) * (low - reserve) / 2) / r
    return t0, th, tl, gh, gl


def spread(r):
    a = auction(r)
    return a[1] - a[2]


def threshold(r):
    a = auction(r)
    return (6 - a[4]) / (a[3] - a[4])


def bisect_root(fn):
    """Bracket a root by exact rational signs on the stated path."""
    low, high = Q(6, 5), Q(18, 5)
    initial = (fn(low), fn(high))
    while high - low > Q(1, 10 ** 80):
        middle = (low + high) / 2
        value = fn(middle)
        if value == 0:
            low = high = middle
            break
        if value < 0:
            low = middle
        else:
            high = middle
    return Interval(low, high), initial, (fn(low), fn(high))


def main():
    files = [TEAM / "proofs/P1_core.tex", TEAM / "proofs/build/P1_core.pdf",
             TEAM / "memos/P1_core.md", TEAM / "registry/P1_core.csv",
             TEAM / "memos/XP1_check.md"]
    files += sorted((TEAM / "scripts/P1_core").glob("*.py"))
    hashes = {str(p.relative_to(TEAM)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in files}
    (HERE / "checked_sources.sha256").write_text("".join(
        f"{value}  {path}\n" for path, value in hashes.items()))
    lines = []

    def say(*parts):
        line = " ".join(map(str, parts))
        print(line)
        lines.append(line)

    say("XP1b: exact rational interval certificates; calibration B.")
    say("Inputs: h=10, ell=1, p=1/2, rho=1/4, c_H=6, k=1/50, beta=0.294655.")
    say("Auction objects come from the piecewise integrals in this script.")
    # The exponential tail is bounded by a geometric series after term 100.
    total = sum((Q(1, math.factorial(n)) for n in range(101)), Q(0))
    exponential = Interval(total, total + Q(102, 101 * math.factorial(101)))
    say("e bracket: S_100 < e < S_100 + 102/(101*101!).", enclosure(exponential))
    roots = {}
    functions = {
        "r_A": lambda r: spread(r) * (1 - threshold(r)) - FEE,
        "r_star": lambda r: RHO * spread(r) * threshold(r) - FEE,
        "r_N": lambda r: RHO * spread(r) / 2 - FEE,
    }
    for name, function in functions.items():
        root, initial, ends = bisect_root(function)
        roots[name] = root
        say(name, enclosure(root), "initial signs", sign(initial[0]), sign(initial[1]),
            "final signs", sign(ends[0]), sign(ends[1]),
            "width below 1e-80:", root.high - root.low < Q(1, 10 ** 80))

    # Image intervals use natural interval arithmetic. No monotone image assumption enters them.
    r = roots["r_star"]
    prior = threshold(r)
    d = spread(r)
    relative = exponential - 1
    liquidity = BETA / (1 + BETA * relative)
    presence = relative * BETA / (1 + BETA * relative)
    zero_mass = (1 - 2 * BETA) / (1 + BETA * relative)
    top = prior * (liquidity + presence) / (liquidity + prior * presence)
    zero_posterior = prior * zero_mass / (zero_mass + (1 - prior) * presence)
    numbers = {
        "entry_cmend_B": RHO + (1 - RHO) * (liquidity + prior * presence),
        "margin_tau_rN_half_B": threshold(roots["r_N"]) - Q(1, 2),
        "margin_pimax_tauA_B": prior - threshold(roots["r_A"]),
        "margin_u_kstrong_B": Q(19, 3) - relative,
        "rstar": r,
        "pimax": prior,
        "M_pimax_B": top,
        "mu0_pimax_B": zero_posterior,
        "margin_cmend_B": d * (1 - top) - FEE,
        "margin_tauA_3q_B": Q(3, 4) - threshold(roots["r_A"]),
    }
    rows = {row["key"]: row for row in csv.DictReader(
        (TEAM / "registry/P1_core.csv").open())}
    pattern = re.compile(r"outward enclosure(?: of the rational bracket)? \[([-0-9.]+), ([-0-9.]+)\]")
    records = []
    say("Registry comparison: printed bounds must contain the complete independent interval.")
    for key, value in numbers.items():
        row = rows[key]
        match = pattern.search(row["note"])
        contains = (Q(match[1]) <= value.low and value.high <= Q(match[2])) if match else None
        same_display = nearest(value.low) == nearest(value.high) == row["display"]
        say(key, enclosure(value), "display", nearest(value.low),
            "registry enclosure contains interval:", contains,
            "display agrees at both ends:", same_display)
        records.append({"key": key, "low": str(value.low), "high": str(value.high),
                        "outward_low": decimal(value.low),
                        "outward_high": decimal(value.high, upper=True),
                        "display": nearest(value.low), "registry_contains": contains,
                        "display_agrees": same_display})
    with (HERE / "xp1b_intervals.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    say("Endpoint identities: pi=tau(r_star), rho*Delta(r_star)*pi=k exactly by definition.")
    say("No-trade tuple: sigma_H=sigma_L=delta_0; mu=(pi,pi,pi); e=(rho,rho,rho).")
    say("Informative tuple: sigma_H=delta_1, sigma_L=delta_0; mu=(pi,mu0,M); e=(rho,rho,1).")
    t0, th, tl, gh, gl = auction(r)
    for name, mus, entries in (
        ("N", (prior, prior, prior), (RHO, RHO, RHO)),
        ("F", (prior, zero_posterior, top), (RHO, RHO, Q(1))),
    ):
        prices = tuple(t0 + e * (tl - t0 + d * mu) for mu, e in zip(mus, entries))
        for q, price, mu in zip((-1, 0, 1), prices, mus):
            say(name, "order", q, "price", enclosure(price),
                "B(mu)-6", enclosure(gl + mu * (gh - gl) - 6))
        for cls, proceeds in (("H", th), ("L", tl)):
            for q, e, price in zip((-1, 0, 1), entries, prices):
                payoff = q * (t0 + e * (proceeds - t0) - price) - FEE * abs(q)
                say(name, cls, "q", q, "net payoff", enclosure(payoff), sign(payoff))
        say(name, "L sale payoff is exactly zero after the endpoint identity.")
    say("N H purchase sign:", sign(RHO * d * (1 - prior) - FEE))
    say("F H purchase sign:", sign(numbers["margin_cmend_B"]))
    say("F mu0<pi<M: signs", sign(prior - zero_posterior), sign(top - prior))
    say("CM permits high-cost abstention at posterior pi=tau; C1 requires preparation there.")
    say("IM and I0 permit low-class abstention at its exact zero payoff.")

    # A real rational input separates the display cutoff from the exact cutoff.
    rounded_prior, near_strength = Q("0.650059"), Q("1.634217")
    cutoff_top = rounded_prior * exponential / (1 + rounded_prior * (exponential - 1))
    say("Literal decimal cutoff: pi=0.650059, r=1.634217, IM/C1.")
    for name, value in (
        ("tau(r)-pi", threshold(near_strength) - rounded_prior),
        ("k-rho*Delta(r)*pi", FEE - RHO * spread(near_strength) * rounded_prior),
        ("J(r)-k", spread(near_strength) * (1 - threshold(near_strength)) - FEE),
        ("M(pi)-tau(r)", cutoff_top - threshold(near_strength)),
        ("full-purchase net return", spread(near_strength) * (1 - cutoff_top) - FEE),
    ):
        say(name, enclosure(value), sign(value))

    # Read the prior independent output; do not run a script that edits checked files.
    previous = {row["key"]: row for row in csv.DictReader(
        (TEAM / "scripts/XP1/xp1_registry_recompute.csv").open())}
    common, contained = 0, 0
    for key, row in rows.items():
        match = pattern.search(row["note"])
        if match and key in previous:
            common += 1
            prior_row = previous[key]
            complete = Q(match[1]) <= Q(prior_row["low"]) <= Q(prior_row["high"]) <= Q(match[2])
            contained += complete
            if not complete:
                say("Prior independent interval lies outside registry enclosure:", key)
    say("Shared registry enclosures:", common, "; complete independent intervals contained:", contained)
    changed = [path for path, digest in hashes.items()
               if hashlib.sha256((TEAM / path).read_bytes()).hexdigest() != digest]
    say("Checked source files with a changed hash:", changed)
    (HERE / "xp1b_recompute.log").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
