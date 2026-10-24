"""Shared objects for the P1_core scripts: benchmark primitives, auction objects,
exact polynomial arithmetic, interval helpers, and the registry writer.

Exact inputs are Fractions. Every quantity that depends on Euler's number uses
mpmath.iv (outward-rounded intervals). A sign counts only if its interval excludes zero.
Printed enclosures come from the exact endpoints: the lower end rounds down, the upper end up.
"""
import csv
import pathlib
from fractions import Fraction as Fr

from mpmath import iv, mp, mpf, nstr

iv.dps = 50
mp.dps = 50

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
REGISTRY = TEAM / "registry" / "P1_core.csv"
COLS = ["key", "value", "display", "status", "source_script", "run_log", "note"]

# Benchmark primitives (Laplace manuscript, Appendix A.8; brief section 3).
h, ell, p = Fr(10), Fr(1), Fr(1, 2)
rho, cH, k, pi_half = Fr(1, 4), Fr(6), Fr(1, 50), Fr(1, 2)
r0, r1, r2 = Fr(6, 5), Fr(3), Fr(18, 5)
# Slot primitives at calibration B: 1 + u = e, beta an exact decimal.
beta_B = Fr(294655, 1000000)
# Calibration A (rational), used as an exact cross-check.
lam_A, beta_A = Fr(6, 17), Fr(1, 3)


# ---------------------------------------------------------------- auction objects
def auction(r):
    """Closed forms (4) of the Laplace manuscript for point masses and R ~ U[0, r]."""
    r = Fr(r)
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    D = tH - tL
    return dict(t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D)


def _integrate_piecewise_linear(f, knots):
    """Exact integral of a function that is linear between consecutive knots (midpoint rule)."""
    total = Fr(0)
    for a, b in zip(knots[:-1], knots[1:]):
        if b > a:
            total += (b - a) * f((a + b) / 2)
    return total


def auction_by_integration(r):
    """Direct integration over R ~ U[0, r] of the sale payoffs (no closed form used)."""
    r = Fr(r)

    def proceeds(theta, R):  # target receives max{p, min(R, theta)} for theta >= p
        return max(p, min(R, theta))

    def profit(theta, R):  # challenger keeps (theta - max{p, R})_+
        return max(Fr(0), theta - max(p, R))

    def no_entry(R):
        return p if R >= p else Fr(0)

    out = {}
    for name, theta in (("H", h), ("L", ell)):
        knots = sorted({Fr(0), r, *(x for x in (p, theta) if 0 < x < r)})
        out["t" + name] = _integrate_piecewise_linear(lambda R: proceeds(theta, R), knots) / r
        out["g" + name] = _integrate_piecewise_linear(lambda R: profit(theta, R), knots) / r
    knots = sorted({Fr(0), r, *(x for x in (p,) if 0 < x < r)})
    out["t0"] = _integrate_piecewise_linear(no_entry, knots) / r
    out["D"] = out["tH"] - out["tL"]
    return out


def tau(r):
    a = auction(r)
    return (cH - a["gL"]) / (a["gH"] - a["gL"])


def B(r, mu):
    a = auction(r)
    return a["gL"] + mu * (a["gH"] - a["gL"])


def Delta(r):
    return auction(r)["D"]


def J(r):
    """Return of a purchase that reaches the threshold posterior with full entry."""
    return Delta(r) * (1 - tau(r))


# ---------------------------------------------------------------- polynomials (exact)
def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pneg(a):
    return [-c for c in a]


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    out = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return ptrim(out)


def ptrim(a):
    a = [Fr(c) for c in a]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def pder(a):
    return ptrim([i * a[i] for i in range(1, len(a))]) if len(a) > 1 else [Fr(0)]


def peval(a, x):
    x = Fr(x)
    v = Fr(0)
    for c in reversed(a):
        v = v * x + c
    return v


def pdivmod(a, b):
    a = ptrim(a)
    b = ptrim(b)
    q = [Fr(0)] * max(1, len(a) - len(b) + 1)
    r = a[:]
    while len(r) >= len(b) and not (len(r) == 1 and r[0] == 0):
        coef = r[-1] / b[-1]
        shift = len(r) - len(b)
        q[shift] = coef
        r = psub(r, [Fr(0)] * shift + [coef * c for c in b])
        if len(r) < len(b):
            break
    return ptrim(q), ptrim(r)


def sturm_chain(a):
    chain = [ptrim(a), pder(a)]
    while not (len(chain[-1]) == 1 and chain[-1][0] == 0):
        _, rem = pdivmod(chain[-2], chain[-1])
        if len(rem) == 1 and rem[0] == 0:
            break
        chain.append(pneg(rem))
    return chain


def sign_changes(chain, x):
    signs = [peval(c, x) for c in chain]
    signs = [s for s in signs if s != 0]
    return sum(1 for u, v in zip(signs[:-1], signs[1:]) if (u > 0) != (v > 0))


def roots_in(a, lo, hi):
    """Number of distinct real roots of a in (lo, hi] by Sturm's theorem."""
    chain = sturm_chain(a)
    return sign_changes(chain, lo) - sign_changes(chain, hi)


def pstr(a):
    return " + ".join(f"({c})*r^{i}" for i, c in enumerate(a) if c != 0)


# Polynomial forms in r of the benchmark objects (built from the primitives).
R1 = [Fr(0), Fr(1)]  # the polynomial r
TAU_NUM = psub(pmul([Fr(0), 2 * cH], [Fr(1)]), [ell * ell - p * p])        # 2 r c_H - (l^2 - p^2)
TAU_DEN = ptrim([-ell * ell, 2 * h, Fr(-1)])                                 # 2 r h - r^2 - l^2
ONE_MINUS_TAU_NUM = ptrim([-p * p, 2 * (h - cH), Fr(-1)])                    # 2 r (h - c_H) - r^2 - p^2
DELTA_NUM = ptrim([ell * ell, -2 * ell, Fr(1)])                               # (r - l)^2
DELTA_DEN = [Fr(0), Fr(2)]                                                    # 2 r


# ---------------------------------------------------------------- intervals
# Arithmetic: mpmath.iv at 50 digits (outward rounding in every operation).
# Serialization: the endpoints of an interval convert exactly to Fractions. A printed
# enclosure rounds its lower end down and its upper end up, so it contains the interval.
# A display (round to nearest) counts as certified only if both exact ends give it.
ENC_PLACES = 24


def ivq(x):
    """Outward interval for an exact rational."""
    x = Fr(x)
    return iv.mpf(x.numerator) / iv.mpf(x.denominator)


def ivbr(lo, hi):
    """Outward interval that contains the rational bracket [lo, hi]."""
    return iv.mpf([ivq(lo).a, ivq(hi).b])


def ivends(x):
    """The two endpoints of an interval as exact Fractions."""
    out = []
    for raw in x._mpi_:
        sign, man, exp, _ = raw
        v = Fr(man) * (Fr(2) ** exp)
        out.append(-v if sign else v)
    return out[0], out[1]


def _fixed(n, places):
    """Integer n scaled by 10^-places, as a fixed-point decimal string."""
    neg = n < 0
    n = abs(n)
    if places == 0:
        body = str(n)
    else:
        body = str(n).rjust(places + 1, "0")
        body = body[:-places] + "." + body[-places:]
    return ("-" if neg and n != 0 else "") + body


def floor_dec(q, places=ENC_PLACES):
    """Largest decimal with `places` places that is <= q (exact)."""
    q = Fr(q)
    return _fixed((q.numerator * 10**places) // q.denominator, places)


def ceil_dec(q, places=ENC_PLACES):
    """Smallest decimal with `places` places that is >= q (exact)."""
    q = Fr(q)
    return _fixed(-((-q.numerator * 10**places) // q.denominator), places)


def round_dec(q, places=6):
    """Nearest decimal with `places` places (exact; a half rounds away from zero)."""
    q = Fr(q)
    n = (abs(q) * 10**places + Fr(1, 2)).__floor__()
    return _fixed(-n if q < 0 else n, places)


def sig_str(q, digits=16):
    """Value column: q to `digits` significant digits (nearest)."""
    q = Fr(q)
    if q == 0:
        return "0"
    from decimal import Decimal, localcontext
    with localcontext() as ctx:
        ctx.prec = digits + 40
        d = Decimal(q.numerator) / Decimal(q.denominator)
    return format(d, f".{digits}g")


def qbrstr(lo, hi, places=ENC_PLACES):
    """Outward decimal enclosure of the rational bracket [lo, hi]."""
    return f"[{floor_dec(lo, places)}, {ceil_dec(hi, places)}]"


def ivstr(x, places=ENC_PLACES):
    """Outward decimal enclosure of an interval."""
    lo, hi = ivends(x)
    return qbrstr(lo, hi, places)


def ivsign(x):
    if x.a > 0:
        return "+"
    if x.b < 0:
        return "-"
    return "0?"


def value_str(x, digits=16):
    """Value column: the midpoint of the exact enclosure, 16 significant digits."""
    lo, hi = ivends(x)
    return sig_str((lo + hi) / 2, digits)


def ivdisp(x, decimals=6):
    """Display of an interval and a flag: certified when both exact ends round to it."""
    lo, hi = ivends(x)
    dlo, dhi = round_dec(lo, decimals), round_dec(hi, decimals)
    return dlo, dlo == dhi, dhi


# ---------------------------------------------------------------- registry and log
class Log:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.fh = self.path.open("w")

    def __call__(self, *args):
        line = " ".join(str(a) for a in args)
        print(line)
        self.fh.write(line + "\n")

    def close(self):
        self.fh.close()


class Registry:
    def __init__(self, source_script, run_log):
        self.rows = []
        self.source = source_script
        self.log = run_log
        self.uncertified = []

    def add(self, key, value, display, status, note=""):
        self.rows.append(dict(key=key, value=str(value), display=str(display), status=status,
                              source_script=self.source, run_log=self.log, note=note))

    def add_frac(self, key, x, status, note="", decimals=6):
        x = Fr(x)
        disp = f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)
        self.add(key, f"{x.numerator}/{x.denominator}", disp, status, note)

    def add_dec_exact(self, key, x, status, note="", decimals=6):
        x = Fr(x)
        self.add(key, f"{x.numerator}/{x.denominator}", round_dec(x, decimals), status, note)

    def _flag(self, key, note, dlo, dhi):
        if dlo != dhi:
            self.uncertified.append(key)
            return (note + f" ROUNDING NOT CERTIFIED: ends round to {dlo} and {dhi}").strip()
        return note

    def add_iv(self, key, x, status, note="", decimals=6):
        dlo, _, dhi = ivdisp(x, decimals)
        note = self._flag(key, note, dlo, dhi)
        self.add(key, value_str(x), dlo, status, (note + f"; outward enclosure {ivstr(x)}").strip("; "))

    def add_bracket(self, key, lo, hi, status, note="", decimals=6):
        """Quantity known to lie in the exact rational bracket [lo, hi]."""
        lo, hi = Fr(lo), Fr(hi)
        dlo, dhi = round_dec(lo, decimals), round_dec(hi, decimals)
        note = self._flag(key, note, dlo, dhi)
        self.add(key, sig_str((lo + hi) / 2), dlo, status,
                 (note + f"; outward enclosure of the rational bracket {qbrstr(lo, hi)}").strip("; "))

    def write(self, path=REGISTRY, mode="w"):
        exists = path.exists() and mode == "a"
        with path.open(mode, newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS)
            if not exists:
                w.writeheader()
            for row in self.rows:
                w.writerow(row)


# ---------------------------------------------------------------- exact bisection
def bisect_root(f, lo, hi, width=Fr(1, 10**40)):
    """Exact rational bisection for an increasing f with f(lo) < 0 < f(hi).
    Returns (lo, hi, f(lo), f(hi)) with hi - lo <= width."""
    lo, hi = Fr(lo), Fr(hi)
    flo, fhi = f(lo), f(hi)
    while hi - lo > width:
        mid = (lo + hi) / 2
        fm = f(mid)
        if fm < 0:
            lo, flo = mid, fm
        elif fm > 0:
            hi, fhi = mid, fm
        else:
            return mid, mid, fm, fm
    return lo, hi, flo, fhi


def frak_r(d):
    """Root above ell of Delta(r) = (r - ell)^2 / (2r) = d, as an interval (d an interval)."""
    L = ivq(ell)
    return L + d + iv.sqrt(d * d + 2 * L * d)


def e_series_bracket(n=110):
    """Rational bracket S_n < e < S_n + (n + 2)/((n + 1)(n + 1)!) from the exponential series."""
    from math import factorial
    S = sum((Fr(1, factorial(i)) for i in range(n + 1)), Fr(0))
    return S, S + Fr(n + 2, (n + 1) * factorial(n + 1))
