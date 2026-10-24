"""Buy-only discrete-Laplace model at noise scales b = 2 and b = 1, with c_H = 6 and c_H = 5.

Question: with one-sided (buy-only) investor orders, does a smaller noise scale restore the paper's
benchmark (c_H = 6; strengths 1.2, 3, 3.6)? Direct flow sums, 40 digits, pure investor strategies,
challenger prepares at indifference, investor picks zero at indifference. Print only.
"""
from mpmath import mp, mpf, exp, sqrt

mp.dps = 40
h, ell, p, rho, k, pi = mpf(10), mpf(1), mpf("0.5"), mpf("0.25"), mpf("0.02"), mpf("0.5")
XMAX = 400


def objs(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p**2 / (2 * r)
    tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r)
    gL = (ell**2 - p**2) / (2 * r)
    return t0, tH, tL, gH, gL, tH - tL


def B(r, mu):
    _, _, _, gH, gL, _ = objs(r)
    return gL + mu * (gH - gL)


def entry(r, mu, cH):
    return rho + (1 - rho) * (1 if B(r, mu) >= cH else 0)


def noise(a):
    c = (1 - a) / (1 + a)
    return lambda z: c * a ** abs(z)


def root_DT(d):
    # root above ell of (r - ell)^2 / (2 r) = d
    s = ell + d
    return s + sqrt(s * s - ell**2)


def solve_rC(mu, cH):
    lo, hi = mpf("1.0001"), mpf(9.99)
    for _ in range(200):
        mid = (lo + hi) / 2
        if B(mid, mu) >= cH:
            lo = mid
        else:
            hi = mid
    return lo


def equilibria(r, a, cH):
    """Return the pure profiles (qH, qL) that are equilibria, with entry and H ownership."""
    n = noise(a)
    t0, tH, tL, gH, gL, DT = objs(r)
    out = []
    for qH in (0, 1):
        for qL in (0, 1):
            def mu(x):
                if qH == qL:
                    return pi
                fH, fL = n(x - qH), n(x - qL)
                return pi * fH / (pi * fH + (1 - pi) * fL)

            def price(x):
                m = mu(x)
                return t0 + entry(r, m, cH) * (tL - t0 + DT * m)

            def buy_payoff(tj):
                s = mpf(0)
                for x in range(-XMAX, XMAX + 2):
                    m = mu(x)
                    e = entry(r, m, cH)
                    s += n(x - 1) * (t0 + e * (tj - t0) - price(x))
                return s - k

            KH, KL = buy_payoff(tH), buy_payoff(tL)
            okH = KH >= 0 if qH == 1 else KH <= 0
            okL = KL >= 0 if qL == 1 else KL <= 0
            if okH and okL:
                E = sum(pi * n(x - qH) * entry(r, mu(x), cH) + (1 - pi) * n(x - qL) * entry(r, mu(x), cH)
                        for x in range(-XMAX, XMAX + 2))
                OH = sum(pi * n(x - qH) * entry(r, mu(x), cH) for x in range(-XMAX, XMAX + 2))
                out.append(((qH, qL), float(KH), float(KL), float(E), float(OH)))
    return out


for b, cH in [(2, 5), (2, 6), (1, 6)]:
    b = mpf(b)
    cH = mpf(cH)
    a = exp(-1 / b)
    M1 = 1 / (1 + a)
    m1 = a / (1 + a)
    Lam = 2 * a / (1 + a) ** 2
    KF_hat = (1 + rho) * a / (1 + a) ** 2
    rF, rN = root_DT(k / KF_hat), root_DT(k / (rho * (1 - pi)))
    print("=" * 78)
    print(f"b = {float(b)}, c_H = {float(cH)}: a = {float(a):.6f}, m1 = {float(m1):.6f}, M1 = {float(M1):.6f}")
    print(f"  c_H window (B_1.2(1/2), B_3(M1)] = ({float(B(mpf('1.2'), pi)):.6f}, {float(B(mpf(3), M1)):.6f}]")
    print(f"  k window ((1-pi)DT(1.2), rho*Lambda*DT(3)) = ({float((1-pi)*objs(mpf('1.2'))[5]):.6f}, "
          f"{float(rho*Lam*objs(mpf(3))[5]):.6f}); Lambda = {float(Lam):.6f}")
    print(f"  ceiling r_C (B_r(M1) = c_H) = {float(solve_rC(M1, cH)):.9f};  B_3.6(M1) = {float(B(mpf('3.6'), M1)):.6f}")
    print(f"  no-trade unique below r(2k) = {float(root_DT(2*k)):.6f}; full purchases unique above "
          f"r(k/rho Lambda) = {float(root_DT(k/(rho*Lam))):.6f}")
    print(f"  coexistence [r_F, r_N] = [{float(rF):.6f}, {float(rN):.6f}]; feedback coefficient "
          f"{float(KF_hat):.6f} vs rho/2 = {float(rho/2)}")
    for r in ["1.2", "1.44", "1.5", "1.55", "1.6", "1.65", "1.75", "2", "3", "3.6", "4.2"]:
        eqs = equilibria(mpf(r), a, cH)
        desc = "; ".join(f"{q}: entry {E:.6f}, H-own {OH:.6f}" for q, KH, KL, E, OH in eqs) or "NO PURE EQUILIBRIUM"
        print(f"  r = {r:>4}: {desc}")
