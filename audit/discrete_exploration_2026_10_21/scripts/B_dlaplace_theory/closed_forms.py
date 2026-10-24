"""Print-only check of the closed forms in memos/B_dlaplace_theory.md (50-digit arithmetic).

Each block computes one object two ways: from the closed form in the memo, and from primitives
(quadrature over the incumbent value, or direct sums over integer flows). It prints both values
and their difference. Nothing is asserted.

Run from the repository root:
    .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/B_dlaplace_theory/closed_forms.py
"""
from mpmath import mp, mpf, exp, quad, nstr

mp.dps = 50

H, ELL, P = mpf(10), mpf(1), mpf(1) / 2
RHO, K_COST, B_SCALE = mpf(1) / 4, mpf(1) / 50, mpf(2)
NFLOW = 320  # flows |x| <= NFLOW; a^NFLOW = exp(-160) at b = 2


def show(x, d=15):
    return nstr(x, d)


def auction(r):
    return dict(
        t0=P * (1 - P / r),
        tH=r / 2 + P**2 / (2 * r),
        tL=ELL - (ELL**2 - P**2) / (2 * r),
        gH=H - r / 2 - P**2 / (2 * r),
        gL=(ELL**2 - P**2) / (2 * r),
        D=(r - ELL) ** 2 / (2 * r),
    )


def auction_quad(r):
    """Integrate the second-price payoffs over R ~ U[0, r] (paper eq. A.1)."""
    w = 1 / r

    def proceeds(theta):
        pts = sorted({mpf(0), P, min(theta, r), r})
        return quad(lambda R: max(P, min(R, theta)), pts) * w

    def profit(theta):
        pts = sorted({mpf(0), P, min(theta, r), r})
        return quad(lambda R: max(theta - max(P, R), 0), pts) * w

    t0 = quad(lambda R: P if R >= P else mpf(0), [0, P, r]) * w
    return dict(t0=t0, tH=proceeds(H), tL=proceeds(ELL), gH=profit(H), gL=profit(ELL),
                D=proceeds(H) - proceeds(ELL))


def noise_closed(z, a):
    return (1 - a) / (1 + a) * a ** abs(z)


def noise_convolution(z, a, nmax=400):
    """P(G1 - G2 = z) for independent geometric counts P(G = n) = (1 - a) a^n."""
    lo = max(0, -z)
    return sum((1 - a) * a ** (z + n) * (1 - a) * a**n for n in range(lo, lo + nmax))


def flow_laws(a, pi, lam, bH, bL):
    """Direct conditional flow laws and posteriors on x = -NFLOW..NFLOW+1."""
    sH, sL = lam * bH, lam * bL
    xs = list(range(-NFLOW, NFLOW + 2))
    f = {x: noise_closed(x, a) for x in range(-NFLOW - 1, NFLOW + 2)}
    pH = {x: (1 - sH) * f[x] + sH * f[x - 1] for x in xs}
    pL = {x: (1 - sL) * f[x] + sL * f[x - 1] for x in xs}
    mu = {x: pi * pH[x] / (pi * pH[x] + (1 - pi) * pL[x]) for x in xs}
    return xs, f, pH, pL, mu


def closed_posteriors(a, pi, lam, bH, bL):
    g = 1 / (1 + a)
    d = 2 * g - 1
    sH, sL = lam * bH, lam * bL
    up = pi * (1 - g + d * sH) / (pi * (1 - g + d * sH) + (1 - pi) * (1 - g + d * sL))
    dn = pi * (g - d * sH) / (pi * (g - d * sH) + (1 - pi) * (g - d * sL))
    return up, dn


def k_closed(D, a, pi, s, e_up, e_dn):
    g = 1 / (1 + a)
    d = 2 * g - 1
    Np, Nm = 1 - g + pi * d * s, g - pi * d * s
    return D * (1 - pi) * g * (1 - g) * (e_up / Np + e_dn / Nm)


def k_direct(D, a, pi, s, schedule):
    """H's gross purchase payoff by a direct sum over flows: sum_x f(x-1) e(x) D (1 - mu_x)."""
    xs, f, pH, pL, mu = flow_laws(a, pi, mpf(1), s, mpf(0))
    return sum(f[x - 1] * schedule(x) * D * (1 - mu[x]) for x in xs)


def main():
    a = exp(-1 / B_SCALE)
    g = 1 / (1 + a)
    d = 2 * g - 1
    print("=== Noise constants (b = 2) ===")
    print("a = exp(-1/b) =", show(a, 20))
    print("gamma = 1/(1+a) = P(Z>=0) =", show(g, 20))
    print("1-gamma = a/(1+a) = P(Z>=1) =", show(1 - g, 20))
    print("delta = 2 gamma - 1 = (1-a)/(1+a) =", show(d, 20))
    print("m1 = 1/(1+e^{1/b}) =", show(1 / (1 + exp(1 / B_SCALE)), 20), " M1 =", show(1 - 1 / (1 + exp(1 / B_SCALE)), 20))
    print("gamma(1-gamma) = a/(1+a)^2 =", show(g * (1 - g), 20))

    print("\n=== A. Auction objects: closed form (eq. 4) minus quadrature ===")
    for r in [mpf("1.2"), mpf("1.6"), mpf(3), mpf("3.6"), mpf("4.2")]:
        c, q = auction(r), auction_quad(r)
        diffs = {kk: c[kk] - q[kk] for kk in c}
        print(f"r = {show(r, 3)}:", ", ".join(f"{kk}={show(c[kk], 12)} (diff {show(diffs[kk], 3)})" for kk in c))
        print("   split identity D + (gH - gL) =", show(c["D"] + c["gH"] - c["gL"], 20), "(h - l = 9)")

    print("\n=== B. Noise law: closed form minus convolution of two geometric counts ===")
    worst = max(abs(noise_closed(z, a) - noise_convolution(z, a)) for z in range(-12, 13))
    print("max |difference| over |z| <= 12:", show(worst, 5))
    tot = sum(noise_closed(z, a) for z in range(-NFLOW, NFLOW + 1))
    print("total mass on |z| <= NFLOW:", show(tot, 30))
    print("P(Z>=0) direct:", show(sum(noise_closed(z, a) for z in range(0, NFLOW + 1)), 25), " gamma:", show(g, 25))
    print("P(Z>=1) direct:", show(sum(noise_closed(z, a) for z in range(1, NFLOW + 1)), 25), " 1-gamma:", show(1 - g, 25))

    print("\n=== C. Posteriors: direct Bayes on each flow vs. the two closed forms ===")
    profiles = [
        (mpf(1) / 2, mpf(1), mpf(1), mpf(0)),
        (mpf(1) / 2, mpf(1), mpf("0.3"), mpf(0)),
        (mpf(1) / 2, mpf("0.6"), mpf(1), mpf(0)),
        (mpf("0.3"), mpf(1), mpf(1), mpf(0)),
        (mpf("0.7"), mpf(1), mpf("0.8"), mpf("0.25")),
        (mpf(1) / 2, mpf(1), mpf("0.2"), mpf("0.9")),
    ]
    for pi, lam, bH, bL in profiles:
        xs, f, pH, pL, mu = flow_laws(a, pi, lam, bH, bL)
        up, dn = closed_posteriors(a, pi, lam, bH, bL)
        dev_up = max(abs(mu[x] - up) for x in xs if x >= 1)
        dev_dn = max(abs(mu[x] - dn) for x in xs if x <= 0)
        pmin = min(pi * pH[x] + (1 - pi) * pL[x] for x in range(-5, 6))
        print(f"pi={show(pi,3)} lam={show(lam,3)} bH={show(bH,3)} bL={show(bL,3)}: mu+={show(up,15)} mu-={show(dn,15)}"
              f"  max dev on x>=1: {show(dev_up,3)}, on x<=0: {show(dev_dn,3)}; min P(x) on |x|<=5: {show(pmin,6)}")
    for pi in [mpf(1) / 2, mpf("0.3"), mpf("0.7")]:
        M1 = pi / (pi + (1 - pi) * a)
        m1 = pi * a / (pi * a + 1 - pi)
        print(f"global bounds at pi={show(pi,3)}: m1(pi)={show(m1,15)}, M1(pi)={show(M1,15)}; 1-M1(pi) - m1(1-pi) =",
              show(1 - M1 - (1 - pi) * a / ((1 - pi) * a + pi), 3))

    print("\n=== D. Purchase payoff K(s): direct flow sum vs closed form ===")
    D3 = auction(mpf(3))["D"]
    pi = mpf(1) / 2
    for s in [mpf(0), mpf("0.3"), mpf("0.7"), mpf(1)]:
        for name, eu, ed in [("(rho,rho)", RHO, RHO), ("(1,rho)", mpf(1), RHO), ("(1,1)", mpf(1), mpf(1))]:
            sched = (lambda x, eu=eu, ed=ed: eu if x >= 1 else ed)
            kd, kc = k_direct(D3, a, pi, s, sched), k_closed(D3, a, pi, s, eu, ed)
            print(f"s={show(s,2)} e={name}: direct={show(kd,18)} closed={show(kc,18)} diff={show(kd-kc,3)}")
    # a schedule that varies inside the good-news half-line: only the f-weighted average matters
    sched = (lambda x: (RHO + (1 - RHO) * (x % 2)) if x >= 1 else RHO)
    num = sum(noise_closed(x, a) * sched(x) for x in range(1, NFLOW + 1))
    ebar = num / (1 - g)
    s = mpf("0.4")
    print(f"varying schedule on x>=1, s=0.4: direct={show(k_direct(D3, a, pi, s, sched),18)}",
          f"closed with average e+={show(ebar,12)}: {show(k_closed(D3, a, pi, s, ebar, RHO),18)}")
    print("bounds at r=3, pi=1/2: (1-pi)D =", show(D3 / 2, 15), "; rho*Lambda*D = 2 rho gamma(1-gamma) D =",
          show(2 * RHO * g * (1 - g) * D3, 15), "; rho*m1*D (brief) =", show(RHO * (1 - g) * D3, 15))
    print("feedback at r=3: K(1;1,rho)-k =", show(k_closed(D3, a, pi, mpf(1), mpf(1), RHO) - K_COST, 15),
          "; K(1;rho,rho)-k =", show(k_closed(D3, a, pi, mpf(1), RHO, RHO) - K_COST, 15))


if __name__ == "__main__":
    main()
