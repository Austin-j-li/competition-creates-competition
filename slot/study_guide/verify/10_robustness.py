"""Recompute chapter 10 from primitives. Run with python3; print values only."""
from fractions import Fraction as F
from itertools import product
import mpmath as mp

mp.mp.dps = 60
N = mp.mpf
P = N(1) / 2
RHO = N(1) / 4
BETA = N("0.294655")
U = mp.e - 1
LAM = U * BETA / (1 + U * BETA)
B = (1 - LAM) * BETA
B0 = (1 - LAM) * (1 - 2 * BETA)
M = mp.e / (1 + mp.e)
MLOW = 1 - M


def show(label: str, *values: object) -> None:
    print(label + ":", "  ".join(mp.nstr(v, 14) if isinstance(v, N) else str(v) for v in values))


def kernel(r: N, v: N, p: N = P) -> tuple[N, N, N]:
    if v < p:
        return p * max(1 - p / r, N(0)), N(0), N(0)
    if r <= p:
        return p, v - p, N(1)
    if v <= r:
        g = (v * v - p * p) / (2 * r)
        return v - g, g, v / r
    t = r / 2 + p * p / (2 * r)
    return t, v - t, N(1)


def class_objects(r: N, band: tuple[str, str]) -> tuple[N, N, N]:
    lo, hi = map(N, band)
    if lo == hi:
        return kernel(r, lo)
    cuts = sorted(set([lo, hi] + [x for x in (P, r) if lo < x < hi]))
    return tuple(mp.quad(lambda v: kernel(r, v)[j], cuts) / (hi - lo) for j in range(3))


def point_objects(r: N) -> tuple[N, N, N, N, N, N]:
    th, gh, _ = kernel(r, N(10))
    tl, gl, _ = kernel(r, N(1))
    t0 = P * (1 - P / r)
    return th, tl, gh, gl, th - tl, th - t0


def profit(r: N, mu: N) -> N:
    _, _, gh, gl, _, _ = point_objects(r)
    return gl + mu * (gh - gl)


def phi(mu: N, accuracy: N) -> N:
    return accuracy * mu / (accuracy * mu + (1 - accuracy) * (1 - mu))


def signal_case(rho: N, cost: N, fee: N, r0: N, r1: N, a: N, d: N) -> None:
    z = 2 * a - 1
    mu_top = 1 - a + z * M
    delta0, wh0 = point_objects(r0)[4:]
    delta1 = point_objects(r1)[4]
    margins = (cost - profit(r0, d), profit(r1, phi(mu_top, d)) - cost,
               fee - z * (delta0 + (1 - rho) * (2 * d - 1) * wh0),
               z * rho * MLOW * delta1 - fee,
               cost - profit(r1, phi(mu_top, 1 - d)))
    show("five signal margins (private, joint, weak, strong, other)", *margins)
    eh = rho + (1 - rho) * d * (B + a * LAM)
    el = rho + (1 - rho) * (1 - d) * (B + (1 - a) * LAM)
    show("weak entry/ownership; strong entry/ownership", rho, rho / 2, (eh + el) / 2, eh / 2)
    show("no-Y top-profit gaps (cost minus profit)", cost - profit(r0, mu_top), cost - profit(r1, mu_top))


def main() -> None:
    show("slot lambda, b, b0, m, M", LAM, B, B0, MLOW, M)
    print("\nCOST BANDS: low support [0,1/5], high uniform [6-epsilon,6+epsilon]")
    for eps in (N(1) / 10, N(1) / 1000):
        for r in (N(3), N(18) / 5):
            top = profit(r, M)
            high_cdf = min(N(1), max(N(0), (top - 6 + eps) / (2 * eps)))
            entry = RHO + (1 - RHO) * (B + LAM / 2) * high_cdf
            own = (RHO + (1 - RHO) * (B + LAM) * high_cdf) / 2
            show(f"epsilon={eps}, r={r}: top profit, high CDF, entry, ownership", top, high_cdf, entry, own)
    show("maximum width for strict return to floor at r2", 6 - profit(N(18) / 5, M))
    show("cost support margins at width 1/10", profit(N(3), MLOW) - N(1) / 5,
         N("5.9") - profit(N(6) / 5, N(1) / 2), profit(N(3), M) - N("6.1"))

    print("\nSIX CLASS ECONOMIES: entry0, entry1, ownership1, four H1/H2 margins, H3 margin")
    cases = (
        ("Moderate", ("1", "1"), ("2", "2"), "0.5", "0.89", "0.002", "1.05", "1.5", None),
        ("Narrow", ("0.95", "1.05"), ("9.95", "10.05"), "0.5", "6", "0.02", "1.2", "3", "3.6"),
        ("Low prior", ("1", "1"), ("10", "10"), "0.3", "4.5", "0.01", "1.1", "3", "3.6"),
        ("High prior", ("1", "1"), ("10", "10"), "0.7", "7.2", "0.01", "1.1", "3", "3.6"),
        ("Wide", ("0.6", "1.4"), ("1", "19"), "0.7", "6.7", "0.02", "1", "4.5", "5.5"),
        ("Same means", ("1", "1"), ("10", "10"), "0.7", "6.7", "0.02", "1", "4.5", "5.5"),
    )
    for name, low, high, prior, cost, fee, weak, strong, third in cases:
        pi, c, k, r0, r1 = map(N, (prior, cost, fee, weak, strong))
        m = pi / (pi + (1 - pi) * mp.e)
        top = pi * mp.e / (pi * mp.e + 1 - pi)
        l0, h0 = class_objects(r0, low), class_objects(r0, high)
        l1, h1 = class_objects(r1, low), class_objects(r1, high)
        bp0 = (1 - pi) * l0[1] + pi * h0[1]
        bp1 = (1 - top) * l1[1] + top * h1[1]
        recruit = N(int(bp1 > c))
        e0 = RHO + (1 - RHO) * N(int(bp0 > c))
        e1 = RHO + (1 - RHO) * (B + pi * LAM) * recruit
        own = pi * (RHO + (1 - RHO) * (B + LAM) * recruit) * h1[2]
        margins = (c - bp0, bp1 - c, k - h0[0] + l0[0],
                   RHO * min(m, 1 - top) * (h1[0] - l1[0]) - k)
        show(name, e0, e1, own, *margins)
        if third:
            l2, h2 = class_objects(N(third), low), class_objects(N(third), high)
            show("  H3 cost minus top profit", c - ((1 - top) * l2[1] + top * h2[1]))
        if name == "Wide":
            show("  high-class win probability at r1", h1[2])
            w_exact = F(1, 18) * (((F(9, 2) ** 2 - 1) / (2 * F(9, 2))) + (19 - F(9, 2)))
            print("  exact W_H(r1) =", w_exact, "; W_H(r0) =", h0[2])

    print("\nFOUR CLASSES: all 16 weight vertices")
    ts = tuple(kernel(N(3), N(v))[0] for v in ("1", "1.001", "9.999", "10"))
    means = tuple(sum(w * t for w, t in zip(ws, ts)) / sum(ws)
                  for ws in product((N(1), mp.e), repeat=4))
    gamma = min(min(ts[2:]) - max(means), min(means) - max(ts[:2]))
    show("posterior mean min/max; separation; trade margin", min(means), max(means), gamma, RHO * gamma - N("0.02"))

    print("\nTHREE-CLASS COLLISION: posterior, mean, price, each class payoff [sell,zero,buy]")
    w = (1 + 2 * B0 + LAM) / 2
    show("weight w; 1-w; (1-lambda)(4beta-1)/2; 2b+b0+lambda", w, 1 - w, (1 - LAM) * (4 * BETA - 1) / 2,
         2 * B + B0 + LAM)
    show("auction at R~U[0,8], p=1: t0, t(1), t(10), g(10)", 1 - N(1) / 8,
         kernel(N(8), N(1), N(1))[0], kernel(N(8), N(10), N(1))[0], kernel(N(8), N(10), N(1))[1])
    ts = (N(1), 1 + N(49) * w / 16, N(65) / 16)
    priors = (N(1) / 4, N(1) / 2, N(1) / 4)
    means = []
    for idx, base in enumerate((B, B0, B)):
        mass = base + LAM * priors[idx]
        post = tuple(priors[j] * (base + LAM * N(int(j == idx))) / mass for j in range(3))
        mean = sum(post[j] * ts[j] for j in range(3))
        means.append(mean)
        show(f"order {idx-1}", *post, mean, N(7) / 8 + RHO * (mean - N(7) / 8))
    for tj in ts:
        show("class payoffs", RHO * (means[0] - tj) - N(1) / 8, N(0), RHO * (tj - means[2]) - N(1) / 8)
    show("common-mean difference", means[1] - means[2])

    print("\nSIGNALS S(B)")
    signal_case(N("0.85"), N("7.14"), N("0.015"), N("1.1"), N("2.3"), N("0.7"), N("0.75"))
    print("\nEXACT SIGNAL WITNESS: lambda=1/3, beta=3/10")
    # Every primitive in this witness is rational. The five margins are exact.
    rho, cost, fee, a, d = F(17, 20), F(357, 50), F(3, 200), F(7, 10), F(3, 4)
    def exact(r: F, mu: F) -> F:
        return (1 - mu) * F(3, 8) / r + mu * (10 - r / 2 - F(1, 8) / r)
    r0, r1, m, mt = F(11, 10), F(23, 10), F(3, 11), F(8, 11)
    z = 2 * a - 1
    mu = 1 - a + z * mt
    def update(d0: F) -> F:
        return d0 * mu / (d0 * mu + (1 - d0) * (1 - mu))
    delta0, delta1 = (r0 - 1) ** 2 / (2 * r0), (r1 - 1) ** 2 / (2 * r1)
    wh0 = r0 / 2 + F(1, 8) / r0 - F(1, 2) + F(1, 4) / r0
    for value in (cost - exact(r0, d), exact(r1, update(d)) - cost,
                  fee - z * (delta0 + (1 - rho) * (2 * d - 1) * wh0),
                  z * rho * m * delta1 - fee, cost - exact(r1, update(1 - d))):
        print(value)
    print("witness b, u, m, M:", F(2, 3) * F(3, 10), F(1, 3) / (F(2, 3) * F(3, 10)),
          1 / (2 + F(5, 3)), (1 + F(5, 3)) / (2 + F(5, 3)))
    print("\nBENCHMARK WITH S(B) ACCURACIES (IM)")
    # Exact constants at the benchmark auction (rho=1/4, c_H=6, k=1/50) with a_T=7/10, d=3/4.
    a, d, rho, k = F(7, 10), F(3, 4), F(1, 4), F(1, 50)
    eh, el = rho + (1 - rho) * d, rho + (1 - rho) * (1 - d)
    dp0 = el * F(1, 60) + (eh - el) * F(33, 80)
    coef0 = (2 * a - 1) * dp0
    print("r0: (e_H, e_L), Delta_P, (2a-1)Delta_P:", (eh, el), dp0, coef0)
    print("r0: zero-profit rate s/b = 50*coef - 2:", 50 * coef0 - 2)
    print("r0: return minus k at s=0 (exact):", coef0 / 2 - k)
    show("r0: return minus k at s=lambda", N(coef0.numerator) / coef0.denominator / (2 + U) - N(1) / 50)
    show("r0: B(phi+(mu-)) - c_H, c_H - B(phi-(mu+))",
         profit(N(6) / 5, phi(N("0.3") + N("0.4") * MLOW, N("0.75"))) - 6,
         6 - profit(N(6) / 5, phi(N("0.3") + N("0.4") * M, N("0.25"))))
    dp1 = el * F(2, 3) + (eh - el) * F(9, 8)
    print("r1: Delta_P when Y=+ recruits:", dp1)
    show("r1: purchase lower bound (2/5) m Delta_P - k", N(2) / 5 * MLOW * N(137) / 192 - N(1) / 50)
    tau1 = F(141, 200)
    mu_thr = tau1 * (1 - d) / (d * (1 - tau1) + tau1 * (1 - d))   # phi_+(mu) = tau1
    nu_thr = (mu_thr - (1 - a)) / (2 * a - 1)
    print("r1: sale threshold mu(-1), nu(-1), t/b:", mu_thr, nu_thr, 1 / nu_thr - 2)
    floor = (2 * a - 1) * nu_thr * rho * F(2, 3)
    print("r1: floor sale return on that range, minus k:", floor, floor - k)
    print("r1: sale coefficient (2a-1) rho Delta_1 (payoff = coef*b/(2b+t) - k):", (2 * a - 1) * rho * F(2, 3),
          "; zero at t/b =", 50 * (2 * a - 1) * rho * F(2, 3) - 2)
    print("r1: zero-profit sale rate t/b; mu(-1) there:", F(4, 3), (1 - a) + (2 * a - 1) / (2 + F(4, 3)))
    t = N(4) / 3 * B
    entry1 = RHO + (1 - RHO) / 2 * (N("0.75") * (1 - B - N("0.3") * t) + N("0.25") * (1 - B - N("0.7") * t))
    show("r1: entry from event probabilities; 5/8-23b/40", entry1, N(5) / 8 - N(23) * B / 40)
    show("weak buy/sale probability; entry; ownership", N(119) / (96 * U), N(5) / 8, N(13) / 32)
    show("strong buy/sale probability; entry; ownership", N(1), N(4) / (3 * U),
         N(5) / 8 - N(23) * B / 40, N(13) / 32 - N(63) * B / 160)
    show("no-Y: strong buy and sale probability; entry at both strengths", N(4) / (3 * U), RHO)
    print("\nBENCHMARK WITH a=0.94, d=0.505")
    signal_case(RHO, N(6), N("0.02"), N("1.2"), N(3), N("0.94"), N("0.505"))
    show("Laplace scale with same likelihood bound", 2 / mp.log(1 + U))


if __name__ == "__main__":
    main()
