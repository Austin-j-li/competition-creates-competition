"""Small float scans: B1 (theta, lambda) feasibility and branch birth r_I.

Print-only. Numerical diagnostic: complements the analytical lambda=1 bounds
in the memo and the exact certificates in t3_branches.py.
"""
from math import sqrt

KF, RHOF = 0.02, 0.25
THRESH = 124 / 605  # k / Delta(31/20)


def Delta(r):
    return (r - 1.0) ** 2 / (2 * r)


def tau(r):
    gL = 3.0 / (8 * r)
    gH = 10 - r / 2 - 1.0 / (8 * r)
    return (6 - gL) / (gH - gL)


def r_of_Delta(d):
    return 1 + d + sqrt(d * d + 2 * d)


def rC(mu):
    disc = (mu * 10 - 6) ** 2 + mu * ((1 - mu) - 0.25)
    return (mu * 10 - 6 + sqrt(max(disc, 0.0))) / mu


def mu01(alpha, th):
    d = 1 - 3 * th
    return ((1 - 2 * th) - alpha * d) / (2 * (1 - 2 * th) - alpha * d), \
           (th + alpha * d) / (2 * th + alpha * d)


def S(alpha, th, e0, e1):
    d = 1 - 3 * th
    return th * (1 - 2 * th) * (e0 / (2 * (1 - 2 * th) - alpha * d) + e1 / (2 * th + alpha * d))


def alpha_star(r, th):
    t = tau(r)
    if th < 1 / 3:
        return th * (2 * t - 1) / ((1 - 3 * th) * (1 - t))
    return (1 - 2 * th) * (2 * t - 1) / ((3 * th - 1) * (1 - t))


def main():
    print(f"threshold C_T for r_F <= 1.55: {THRESH:.6f}")
    best = {"low": (0.0, None), "high": (0.0, None)}
    both = []
    th = 0.02
    while th <= 0.4901:
        lam = 0.05
        while lam <= 1.001:
            if abs(th - 1 / 3) > 0.004:
                low = th < 1 / 3
                mu0, mu1 = mu01(lam, th)
                murec = mu1 if low else mu0
                e0, e1 = (RHOF, 1.0) if low else (1.0, RHOF)
                if murec >= tau(3.0):
                    CT = S(lam, th, e0, e1)
                    key = "low" if low else "high"
                    if CT > best[key][0]:
                        best[key] = (CT, (round(th, 3), round(lam, 3)))
                    CN = RHOF * (1 - th) / 2
                    rF = r_of_Delta(KF / CT)
                    top = min(r_of_Delta(KF / CN), rC(murec))
                    if CT > CN and rF <= 1.55 and top >= 1.65:
                        both.append((round(th, 3), round(lam, 3), round(CT, 4)))
            lam += 0.025
        th += 0.005
    print("max C_T subject to interior recruitment at r=3:")
    print(" low side (theta<1/3):", best["low"])
    print(" high side (theta>1/3):", best["high"])
    print("grid points with recruit_r1 AND NT+full window covering [1.55,1.65]:", both[:20],
          "count:", len(both))

    print("\nBranch birth r_I: first r (grid 0.001) with U(alpha*+) >= 0, alpha* in [0,1]")
    for th in (0.10, 0.14, 0.15, 0.20, 0.45):
        low = th < 1 / 3
        e0, e1 = (RHOF, 1.0) if low else (1.0, RHOF)
        CN = RHOF * (1 - th) / 2
        rN = r_of_Delta(KF / CN)
        rI = None
        r = 1.001
        while r < 2.5:
            astar = alpha_star(r, th)
            if 0 <= astar <= 1 and Delta(r) * S(astar, th, e0, e1) - KF >= 0:
                rI = r
                break
            r += 0.001
        print(f" theta={th}: r_I~{rI} r_N={rN:.4f}")


if __name__ == "__main__":
    main()
