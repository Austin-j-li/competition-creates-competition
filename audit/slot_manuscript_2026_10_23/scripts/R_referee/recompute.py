"""Independent referee calculations. Print exact or outward interval results."""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
import csv
import re
from mpmath import iv

iv.dps = 65
ROOT = Path(__file__).resolve().parents[4]
TEAM = ROOT / "audit/slot_manuscript_2026_10_23"


def I(x):
    x = Q(x)
    return iv.mpf(x.numerator) / x.denominator


def show(name, value):
    if isinstance(value, (Q, int)):
        print(name, "exact", value)
        value = I(value)
    ends = []
    for part, direction in zip(value._mpi_, (ROUND_FLOOR, ROUND_CEILING)):
        sign, mantissa, exponent, _ = part
        with localcontext() as ctx:
            ctx.prec = 1500
            x = Decimal(mantissa) * Decimal(2) ** exponent
            if sign:
                x = -x
            ends.append(str(x.quantize(Decimal("1e-25"), rounding=direction)))
    print(name, "outward", "[" + ", ".join(ends) + "]")


N = 100
es = sum((Q(1, factorial(j)) for j in range(N + 1)), Q(0))
tail = Q(N + 2, (N + 1) * factorial(N + 1))
E = I(es) + iv.mpf([0, 1]) * I(tail)
beta, rho, k, a = I("0.294655"), I("1/4"), I("1/50"), I("1/40")
u = E - 1
lam = beta * u / (1 + beta * u)
b = (1 - lam) * beta
b0 = (1 - lam) * (1 - 2 * beta)
M, m = E / (1 + E), 1 / (1 + E)
v = 2 * b + lam


def auction(r):
    p, ell, h = I("1/2"), I(1), I(10)
    t0 = p * (1 - p / r)
    th = (p * p + (r * r - p * p) / 2) / r
    tl = (p * p + (ell * ell - p * p) / 2 + ell * (r - ell)) / r
    gh, gl = h - th, ell - tl
    return t0, th, tl, gh, gl


def delta(r):
    return (r - 1) ** 2 / (2 * r)


def tau(r):
    _, _, _, gh, gl = auction(r)
    return (6 - gl) / (gh - gl)


def root_delta(d):
    return 1 + d + iv.sqrt(d * d + 2 * d)


def exact_delta(r):
    return (r - 1) ** 2 / (2 * r)


def exact_tau(r):
    return (48 * r - 3) / (4 * (20 * r - r * r - 1))


def bracket(function, left, right, steps=200):
    for _ in range(steps):
        middle = (left + right) / 2
        if function(middle) > 0:
            right = middle
        else:
            left = middle
    return I(left) + iv.mpf([0, 1]) * I(right - left)


print("Exact rational exponential tail; outward intervals at 65 digits")
for name, value in [("lambda_B", lam), ("b_B", b), ("M_B", M), ("volume_B", v)]:
    show(name, value)
for name, rr in [("r0", "6/5"), ("r1", "3"), ("r2", "18/5")]:
    r = I(rr)
    t0, th, tl, gh, gl = auction(r)
    for label, value in [("Delta", delta(r)), ("tau", tau(r)), ("Bprior", (gh + gl) / 2),
                         ("top_profit_minus_cost", gl + M * (gh - gl) - 6),
                         ("floor_order_minus_k", rho * delta(r) * m - k)]:
        show(name + "_" + label, value)
show("entry_r1", rho + (1 - rho) * (b + lam / 2))
show("ownership_r1", (rho + (1 - rho) * (b + lam)) / 2)
show("prior_lower", I("141/200") / (I("141/200") + I("59/200") * E))
show("prior_upper", I("4245/5804") / (I("4245/5804") + I("1559/5804") * E))
print("\nWelfare, spread and announcement values from the fixed full-order tuple")
for name, rr in [("r1", "3"), ("r2", "18/5")]:
    r = I(rr)
    t0, th, tl, gh, gl = auction(r)
    d = b + lam / 2
    buy_entry = I(1) if name == "r1" else rho
    price_minus = t0 + rho * (tl - t0 + delta(r) * m)
    price_zero = t0 + rho * (tl - t0 + delta(r) / 2)
    price_plus = t0 + buy_entry * (tl - t0 + delta(r) * M)
    entry = rho + (buy_entry - rho) * d
    proceeds = d * price_minus + (1 - 2 * d) * price_zero + d * price_plus
    prep_change = (d * rho * (1 - rho) * (tl - t0 + delta(r) * m)
                   + (1 - 2 * d) * rho * (1 - rho) * (tl - t0 + delta(r) / 2)
                   + d * buy_entry * (1 - buy_entry) * (tl - t0 + delta(r) * M)) / entry
    for label, value in [("price_sale", price_minus), ("price_zero", price_zero),
                         ("price_purchase", price_plus), ("proceeds", proceeds),
                         ("spread", price_plus - price_minus), ("prepared_announcement_mean", prep_change)]:
        show(name + "_" + label, value)
    if name == "r1":
        show("access_proceeds_gain", (1 - rho) * d * (tl - t0 + delta(r) * M))
        show("access_surplus_gain", (1 - rho) * d * (gl + M * (gh - gl) - 6 + I("1/4") / r))
rA = bracket(lambda r: exact_delta(r) * (1 - exact_tau(r)) - Q(1, 50), Q(6, 5), Q(3, 2))
rJ = bracket(lambda r: Q(1, 4) * exact_delta(r) * (1 - exact_tau(r)) - Q(1, 50), Q(9, 5), Q(2))
rstar = bracket(lambda r: Q(1, 4) * exact_delta(r) * exact_tau(r) - Q(1, 50), Q(3, 2), Q(7, 4))
aa = 10 * M - 6
rC = (aa + iv.sqrt(aa * aa + M * (I("3/4") - M))) / M
for name, value in [("rA", rA), ("rF", root_delta(k / m)), ("rN", root_delta(2 * k / rho)),
                    ("rJ", rJ), ("rS", root_delta(k / (rho * m))), ("rC", rC),
                    ("pi_A_lo", tau(rA) / (tau(rA) + E * (1 - tau(rA)))),
                    ("pi_A_hi", tau(rA)), ("pi_max", tau(rstar))]:
    show(name, value)
for rr in ["31/20", "8/5", "33/20"]:
    r = I(rr)
    d, tt = delta(r), tau(r)
    coeff2 = 2 * a * (1 - 2 * beta)
    coeff1 = 4 * a * beta + k * (1 - 2 * beta) + beta * d
    coeff0 = beta * (2 * k - d)
    lr = -2 * coeff0 / (coeff1 + iv.sqrt(coeff1 * coeff1 - 4 * coeff2 * coeff0))
    le = beta * (2 * tt - 1) / (beta + (1 - 2 * beta) * (1 - tt))
    show(rr + "_research", lr)
    show(rr + "_research_recruitment_gap", lr - le)
    show(rr + "_entry", rho + (1 - rho) * (beta + (I("1/2") - beta) * lr))

print("\nProposition A.12(a): an algebraic pair outside the slot domain")
up = I("1/10")
betap = v / (2 + up * (1 - v))
show("u_prime", up)
show("beta_prime", betap)
show("beta_prime_minus_one_third", betap - I("1/3"))

print("\nProposition A.12(e): a mixed purchase from Proposition 3")
r = I("7/5")
s = b * (delta(r) / k - 2)
mean = s / 2
show("r_1p4_sigma_H_purchase", s / lam)
show("r_1p4_actual_lambda", lam)
show("r_1p4_claimed_lambda_2mean", 2 * mean)
show("r_1p4_purchase_posterior_minus_threshold", (b + s) / (2 * b + s) - tau(r))
show("r_1p4_low_sale_net", rho * delta(r) / 2 - k)

print("\nSection 8: the IM upper endpoint belongs to the count range")
theta = I("19/25")
lp = v * theta
bp = v * (1 - theta) / 2
betap = bp / (1 - lp)
show("endpoint_beta", betap)
show("endpoint_H_purchase_net", I("2/3") * (1 - theta) / 2 - k)
show("endpoint_L_sale_net_exact", Q(1, 4) * Q(2, 3) * Q(3, 25) - Q(1, 50))
show("endpoint_purchase_posterior_minus_threshold", (1 + theta) / 2 - tau(I(3)))

print("\nPrivate signals at B with a_T=7/10,d=3/4")
signal_buy_net = I("2/5") * m * I("137/192") - k
show("r1_favorable_signal_purchase_net", signal_buy_net)
show("r0_favorable_signal_purchase_probability", (I("119/96") * b) / lam)
show("r1_unfavorable_signal_sale_probability", (I("4/3") * b) / lam)

print("\nPayment rule at omega=1/2")
show("increase_E_R_minus_ell", Q(2, 3) - Q(1, 60))
show("spread_change_at_half", (1 - 2 * Q(1, 2)) * (Q(2, 3) - Q(1, 60)))

print("\nEntry at an exclusion reserve and a deterrence reserve")
for pp in ["101/100", "31/20"]:
    p = I(pp)
    for rr in ["6/5", "3"]:
        r = I(rr)
        if Q(pp) >= Q(rr):
            th, gh = p, 10 - p
        else:
            th = r / 2 + p * p / (2 * r)
            gh = 10 - th
        show("p=" + pp + ",r=" + rr + "_top_margin", M * gh - 6)

print("\nExact derivative polynomials and Sturm counts")


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
                 for i in range(max(len(p), len(q)))])


def neg(p):
    return [-x for x in p]


def mul(p, q):
    result = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            result[i + j] += x * y
    return trim(result)


def diff(p):
    return trim([i * p[i] for i in range(1, len(p))] or [Q(0)])


def remainder(p, q):
    result = p[:]
    while len(result) >= len(q) and result != [0]:
        offset = len(result) - len(q)
        scalar = result[-1] / q[-1]
        result = add(result, [Q(0)] * offset + [-scalar * x for x in q])
    return result


def at(p, x):
    result = Q(0)
    for coeff in reversed(p):
        result = result * x + coeff
    return result


def sturm(p, left, right):
    seq = [p, diff(p)]
    while seq[-1] != [0]:
        rem = neg(remainder(seq[-2], seq[-1]))
        if rem == [0]:
            break
        rem = [x / abs(rem[-1]) for x in rem]
        seq.append(rem)
    counts = []
    for xx in [left, right]:
        signs = [(at(poly, xx) > 0) - (at(poly, xx) < 0) for poly in seq]
        signs = [x for x in signs if x]
        counts.append(sum(x != y for x, y in zip(signs, signs[1:])))
    print("Sturm variations", counts, "root count", counts[0] - counts[1])


q1 = [Q(1), Q(-2), Q(1)]
q2 = [Q(-1, 4), Q(8), Q(-1)]
q3 = [Q(-1), Q(20), Q(-1)]
for label, numerator, denominator, right in [
    ("J_derivative", mul(q1, q2), mul([Q(0), Q(2)], q3), Q(18, 5)),
    ("Delta_times_1_minus_tau_squared_derivative", mul(q1, mul(q2, q2)),
     mul([Q(0), Q(2)], mul(q3, q3)), Q(2)),
]:
    polynomial = add(mul(diff(numerator), denominator), neg(mul(numerator, diff(denominator))))
    # A positive common factor fixes the constant coefficient at -1.
    polynomial = [x / abs(polynomial[0]) for x in polynomial]
    print(label, "coefficients in ascending order", [str(x) for x in polynomial])
    print("left sign", (at(polynomial, Q(6, 5)) > 0) - (at(polynomial, Q(6, 5)) < 0))
    sturm(polynomial, Q(6, 5), right)

print("\nRegistry enclosure example")
records = {row["key"]: row for row in csv.DictReader((TEAM / "registry/registry.csv").open())}
print("vol_full_B registry note:", records["vol_full_B"]["note"])
show("vol_full_B independent", v)

print("\nNamed script and log paths in Appendix A")
missing = []
for file in sorted((ROOT / "overleaf/competition_slot/appendix").glob("*.tex")):
    for match in re.finditer(r"\\nolinkurl\{(audit/slot_manuscript_2026_10_23/scripts/[^}]+)\}", file.read_text()):
        if not (ROOT / match[1]).exists():
            missing.append((str(file.relative_to(ROOT)), match[1]))
print("Missing fully qualified paths:", missing)
