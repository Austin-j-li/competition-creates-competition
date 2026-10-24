"""Exact rational evaluation of buy-only bounded-noise candidates.

Print-only. Every equilibrium inequality below uses fractions.Fraction.
Benchmark: h=10, l=1, p=1/2, rho=1/4, cL=0, cH=6, k=1/50, pi=1/2.
Alpha is the effective class-H purchase probability, alpha = lambda * beta_H.
Class L never buys (per-unit payoff at most -k at every belief).
"""
from fractions import Fraction as F
from math import comb

H, ELL, P, RHO, K = F(10), F(1), F(1, 2), F(1, 4), F(1, 50)
PI = F(1, 2)
CH = F(6)


def auction(r, cH=CH):
    t0 = P * (1 - P / r)
    tH = r / 2 + P * P / (2 * r)
    tL = ELL - (ELL * ELL - P * P) / (2 * r)
    gH = H - r / 2 - P * P / (2 * r)
    gL = (ELL * ELL - P * P) / (2 * r)
    D = (r - ELL) ** 2 / (2 * r)
    tau = (cH - gL) / (gH - gL)
    return dict(r=r, t0=t0, tH=tH, tL=tL, gH=gH, gL=gL, D=D, tau=tau, cH=cH)


def Bval(a, mu):
    return a["gL"] + mu * (a["gH"] - a["gL"])


def erule(a, mu):
    """Challenger rule E: prepare at indifference. cL = 0 floor included."""
    return F(1) if Bval(a, mu) >= a["cH"] else RHO


def conv(f, g):
    out = {}
    for x, px in f.items():
        for y, py in g.items():
            out[x + y] = out.get(x + y, F(0)) + px * py
    return out


def b1(theta):
    return {-1: theta, 0: 1 - 2 * theta, 1: theta}


def trinomial(N, theta):
    f = {0: F(1)}
    one = b1(theta)
    for _ in range(N):
        f = conv(f, one)
    return f


def binomial_buy(N, beta):
    return {j: F(comb(N, j)) * beta ** j * (1 - beta) ** (N - j) for j in range(N + 1)}


def uniform(M):
    return {z: F(1, 2 * M + 1) for z in range(-M, M + 1)}


def geom5():
    w = {-2: F(1), -1: F(2), 0: F(4), 1: F(2), 2: F(1)}
    return {z: v / 10 for z, v in w.items()}


def evaluate(f, alpha, qsize, a, e_forced=None, ic=True):
    """Posteriors, entry, outcomes, and deviation payoffs at conjectured alpha.

    qsize is the conjectured class-H order size. Returns dict with per-flow
    tables and the per-unit gross payoff of deviation orders 1 and 2.
    e_forced: if a Fraction, force entry to that value at every flow.
    Off-path flows (zero mass in both classes) get belief 1 if ic else 1/2.
    """
    zs = sorted(f)
    flows = sorted(set(zs) | {z + qsize for z in zs} | {z + 1 for z in zs} | {z + 2 for z in zs})
    fL = {x: f.get(x, F(0)) for x in flows}
    fH = {x: (1 - alpha) * f.get(x, F(0)) + alpha * f.get(x - qsize, F(0)) for x in flows}
    mu, ent = {}, {}
    for x in flows:
        den = PI * fH[x] + (1 - PI) * fL[x]
        if den == 0:
            mu[x] = F(1) if ic else PI
        else:
            mu[x] = PI * fH[x] / den
        ent[x] = e_forced if e_forced is not None else erule(a, mu[x])
    w = {x: PI * fH[x] + (1 - PI) * fL[x] for x in flows}
    entry = sum(w[x] * ent[x] for x in flows)
    eH = sum(fH[x] * ent[x] for x in flows)
    eL = sum(fL[x] * ent[x] for x in flows)
    OH = PI * eH  # prepared class H always wins (h > r)
    RT = a["t0"] + PI * eH * (a["tH"] - a["t0"]) + (1 - PI) * eL * (a["tL"] - a["t0"])
    hc_prep = sum(w[x] * (ent[x] - RHO) for x in flows)  # high-cost prep prob
    W = ((a["r"] ** 2 - P * P) / (2 * a["r"])
         + PI * eH * (a["gH"] + P * P / a["r"])
         + (1 - PI) * eL * (a["gL"] + P * P / a["r"])
         - a["cH"] * hc_prep)
    gross = {}
    for qd in (1, 2):
        gross[qd] = sum(f[z] * ent[z + qd] * a["D"] * (1 - mu[z + qd]) for z in zs)
    return dict(mu=mu, ent=ent, w=w, fH=fH, fL=fL, entry=entry, eH=eH, eL=eL,
                OH=OH, RT=RT, W=W, gross=gross,
                U={qd: gross[qd] - K for qd in gross},
                S={qd: gross[qd] / a["D"] for qd in gross})


def show(x, nd=6):
    return f"{x} ({float(x):.{nd}f})" if isinstance(x, F) else str(x)


def candidate(name, f, lam, qsize=1, rs=(F(6, 5), F(3), F(18, 5)), cH=CH):
    b = max(f)
    print(f"\n=== {name} | lambda={lam} q={qsize} f(b)={f[b]} ===")
    print("noise:", {z: str(v) for z, v in sorted(f.items())})
    for r in rs:
        a = auction(r, cH)
        ev0 = evaluate(f, F(0), qsize, a)          # NT conjecture, IC belief
        evF = evaluate(f, lam, qsize, a)           # full purchase conjecture
        evR = evaluate(f, lam, qsize, a, e_forced=RHO)  # entry forced to rho
        rec = [x for x in sorted(evF["mu"]) if evF["w"][x] > 0 and evF["ent"][x] == 1]
        print(f" r={r} tau={show(a['tau'])} Delta={a['D']}")
        print(f"   mu(alpha=lambda): " + " ".join(
            f"x{x}:{evF['mu'][x]}" for x in sorted(evF['mu']) if evF['w'][x] > 0))
        print(f"   recruiting flows: {rec}")
        print(f"   U_NTdev(IC)={show(ev0['U'][qsize])}  U_full={show(evF['U'][qsize])}")
        print(f"   C_N={show(ev0['S'][qsize])} C_rho(lam)={show(evR['S'][qsize])} "
              f"C_T={show(evF['S'][qsize])} gap={show(evF['S'][qsize]-ev0['S'][qsize])} "
              f"info={show(evR['S'][qsize]-ev0['S'][qsize])} entryeff={show(evF['S'][qsize]-evR['S'][qsize])}")
        print(f"   E_full={show(evF['entry'])} OH={show(evF['OH'])} RT={show(evF['RT'])} W={show(evF['W'])}")
        if r == 3:
            hid = evaluate(f, lam, qsize, a, e_forced=RHO)
            print(f"   A.9 at r=3: U_hidden_full={show(hid['U'][qsize])} "
                  f"dRT={show(evF['RT']-hid['RT'])} dW={show(evF['W']-hid['W'])}")


def main():
    print("Benchmark auction objects")
    for r in (F(6, 5), F(3), F(18, 5), F(17, 2)):
        a = auction(r)
        print(f" r={r}: Delta={a['D']} gL={a['gL']} gH={a['gH']} tau={a['tau']} "
              f"B(1/2)={Bval(a, F(1,2))} tL-t0={a['tL']-a['t0']}")

    print("\n########## B1 symmetric three-point ##########")
    for th in (F(1, 10), F(3, 20), F(1, 5), F(11, 50), F(1, 4), F(1, 3), F(2, 5), F(9, 20)):
        candidate(f"B1 theta={th}", b1(th), F(1))
    for th in (F(3, 20), F(1, 5)):
        for lam in (F(3, 4), F(1, 2)):
            candidate(f"B1 theta={th}", b1(th), lam)

    print("\n########## B2a trinomial N traders ##########")
    for (N, th) in [(2, F(1, 3)), (3, F(1, 3)), (4, F(1, 3)), (5, F(1, 3)), (8, F(1, 3)),
                    (2, F(1, 5)), (3, F(1, 5)), (3, F(1, 4))]:
        candidate(f"B2a N={N} theta={th}", trinomial(N, th), F(1))
    candidate("B2a N=3 theta=1/3", trinomial(3, F(1, 3)), F(1, 2))

    print("\n########## B2b binomial buy/abstain ##########")
    for (N, be) in [(1, F(1, 2)), (2, F(1, 2)), (3, F(1, 2)), (4, F(1, 2)),
                    (3, F(1, 4)), (4, F(1, 4)), (5, F(1, 4))]:
        candidate(f"B2b N={N} beta={be}", binomial_buy(N, be), F(1))

    print("\n########## B2 parity: no abstention ##########")
    for N in (2, 3):
        f = trinomial(N, F(1, 2))
        f = {z: v for z, v in f.items() if v > 0}
        candidate(f"B2parity N={N} theta=1/2", f, F(1), rs=(F(3),))

    print("\n########## B3a fixed two-unit order ##########")
    for th in (F(1, 5), F(1, 4), F(1, 3), F(2, 5), F(9, 20)):
        candidate(f"B3a theta={th}", b1(th), F(1), qsize=2)

    print("\n########## B3 x B2 two units, wider noise ##########")
    for (N, th) in [(2, F(1, 3)), (3, F(1, 3)), (3, F(1, 5))]:
        candidate(f"B3xB2 N={N} theta={th}", trinomial(N, th), F(1), qsize=2)

    print("\n########## B3b size choice deviations at r=3 ##########")
    r = F(3)
    a = auction(r)
    for th in (F(3, 20), F(1, 5), F(1, 4), F(1, 3), F(2, 5), F(9, 20)):
        for lam in (F(1), F(3, 4), F(1, 2)):
            f = b1(th)
            c1 = evaluate(f, lam, 1, a)                    # conjecture buy 1
            c1p = evaluate(f, lam, 1, a, ic=False)         # passive belief at x=3
            c2 = evaluate(f, lam, 2, a)                    # conjecture buy 2
            tot1 = c1["U"][1]
            dev2 = 2 * c1["U"][2]
            dev2p = 2 * c1p["U"][2]
            tot2 = 2 * c2["U"][2]
            dev1 = c2["U"][1]
            print(f" theta={th} lam={lam}: buy1={show(tot1)} dev2(IC)={show(dev2)} "
                  f"dev2(passive)={show(dev2p)} | buy2={show(tot2)} dev1={show(dev1)} "
                  f"| buy1stable(IC)={tot1 >= dev2} buy2stable={tot2 >= dev1}")

    print("\n########## B4 other bounded laws ##########")
    candidate("B4 uniform M=2", uniform(2), F(1))
    candidate("B4 uniform M=3", uniform(3), F(1))
    candidate("B4 geom5 (1,2,4,2,1)/10", geom5(), F(1))
    candidate("B4 two-point {-1,1}", {-1: F(1, 2), 1: F(1, 2)}, F(1), rs=(F(3),))

    print("\n########## Weaker (iii'): r=17/2 rows ##########")
    candidate("B1 theta=3/20", b1(F(3, 20)), F(1), rs=(F(17, 2),))
    candidate("B1 theta=1/5", b1(F(1, 5)), F(1), rs=(F(17, 2),))
    candidate("B2a N=3 theta=1/5", trinomial(3, F(1, 5)), F(1), rs=(F(17, 2),))
    candidate("B2b N=3 beta=1/4", binomial_buy(3, F(1, 4)), F(1), rs=(F(17, 2),))
    candidate("B3a theta=1/3", b1(F(1, 3)), F(1), qsize=2, rs=(F(17, 2),))

    print("\n########## Rescue by cH: cH=41/5, B1 theta=1/5 ##########")
    candidate("B1 theta=1/5 cH=41/5", b1(F(1, 5)), F(1), cH=F(41, 5))
    candidate("B1 theta=1/20 cH=41/5", b1(F(1, 20)), F(1), cH=F(41, 5))


if __name__ == "__main__":
    main()
