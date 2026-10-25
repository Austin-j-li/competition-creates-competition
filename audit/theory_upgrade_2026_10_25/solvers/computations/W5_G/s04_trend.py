"""Entry-component trend: A_F(M) = t_L - t_0 + Delta*M along FOSD paths.

Point-mass classes (h=10, ell=1, p=1/2 unless stated); F a finite mixture of uniforms.
Exact piecewise integration. Prints regime checks at the benchmark slot, prior 1/2.
"""
import sys
sys.path.insert(0, "audit/theory_upgrade_2026_10_25/solvers/computations/W5_G")
from mpmath import mp, mpf, nstr
from model import slot, Mtop, mbot, rho, cH, k

s = slot()
u = s["u"]


def Phi(y, a, c):
    """antiderivative of the U[a,c] cdf, zero at a"""
    if y <= a:
        return mpf(0)
    if y <= c:
        return (y - a) ** 2 / (2 * (c - a))
    return (c - a) / 2 + (y - c)


def cdf(mix, y):
    tot = mpf(0)
    for w, a, c in mix:
        if y <= a:
            continue
        tot += w * (min(y, c) - a) / (c - a)
    return tot


def intF(mix, x0, x1):
    return sum(w * (Phi(x1, a, c) - Phi(x0, a, c)) for w, a, c in mix)


def auc(mix, h=mpf(10), ell=mpf(1), p=mpf(1) / 2):
    Fp = cdf(mix, p)
    t0 = p * (1 - Fp)
    wL = p * Fp + (ell - p) - intF(mix, p, ell)
    wH = p * Fp + (h - p) - intF(mix, p, h)
    gL = intF(mix, p, ell)
    gH = intF(mix, p, h)
    D = wH - wL
    gam = gH - gL
    tau = (cH - gL) / gam
    return dict(Fp=Fp, t0=t0, wL=wL, wH=wH, gL=gL, gH=gH, D=D, gam=gam, tau=tau)


def report(label, mix, pi=mpf(1) / 2, **kw):
    a = auc(mix, **kw)
    M, m = Mtop(pi, u), mbot(pi, u)
    Am = a["wL"] + a["D"] * M
    kap = min(m, 1 - M)
    rec = a["tau"] <= M
    print(f"{label:34} F(p)={nstr(a['Fp'],4):7} D={nstr(a['D'],6):9} wL={nstr(a['wL'],6):9} "
          f"tau={nstr(a['tau'],5):8} recruit={str(rec):5} rhoDkap-k={nstr(rho*a['D']*kap-k,4):9} "
          f"A(M)={nstr(Am,6):9} entry comp={nstr((1-rho)*Am if rec else 0,6):9} class comp={nstr(rho*a['D']*(M-m),6)}")
    return a, Am


half = mpf(1) / 2
print("M(1/2) =", nstr(Mtop(half, u), 8))
print("\n== (1) Solver F's 90/10 mixture: low component moved across the reserve ==")
report("F : .9U[0,.5]+.1U[9,10]", [(mpf("0.9"), mpf(0), mpf("0.5")), (mpf("0.1"), mpf(9), mpf(10))])
report("F~: .9U[.5,1]+.1U[9,10]", [(mpf("0.9"), mpf("0.5"), mpf(1)), (mpf("0.1"), mpf(9), mpf(10))])
report("F~': .9U[.5,1]+.1U[9.02,10.02]", [(mpf("0.9"), mpf("0.5"), mpf(1)), (mpf("0.1"), mpf("9.02"), mpf("10.02"))])

print("\n== (2) financial / strategic incumbent: financial value U[x-.3,x+.3] w.p. 1/2, strategic U[1.5+e s,2.5+e s] w.p. 1/2 ==")
print("    path s in [0,1]: x = 0.4 + 0.2 s, strategic shift e = 0.02 (FOSD in s)")
prev = None
for i in range(0, 11):
    sv = mpf(i) / 10
    x = mpf("0.4") + mpf("0.2") * sv
    e = mpf("0.02") * sv
    mix = [(half, x - mpf("0.3"), x + mpf("0.3")), (half, mpf("1.5") + e, mpf("2.5") + e)]
    a, Am = report(f"s={nstr(sv,2)}", mix)
    if prev is not None:
        print(f"      dD={nstr(a['D']-prev[0]['D'],4)}  dA(M)={nstr(Am-prev[1],4)}")
    prev = (a, Am)

print("\n== kernel check: A(M) = E_F[alpha_M(R)], alpha_M = p (R<p), int_p^R (1-G_M) (R>=p) ==")
from mpmath import quad
M = Mtop(half, u)
p = half


def alpha(R):
    if R < p:
        return p
    if R < 1:
        return R - p
    if R < 10:
        return (1 - p) + M * (R - 1)
    return (1 - p) + M * 9


for mix in ([(half, mpf("0.1"), mpf("0.7")), (half, mpf("1.5"), mpf("2.5"))],
            [(half, mpf("0.3"), mpf("0.9")), (half, mpf("1.52"), mpf("2.52"))]):
    EA = sum(w * quad(lambda y: alpha(y) / (c - a0), [a0, min(max(a0, p), c), c]) for w, a0, c in mix)
    a = auc(mix)
    print("  E[alpha] =", nstr(EA, 10), "  wL + D M =", nstr(a["wL"] + a["D"] * M, 10))

print("\n== (3) benchmark U[0,r]: dA_r(M)/dr = M/2 + (1-4M)/(8 r^2) ==")
from model import fr
rS = fr(k / (rho * mbot(half, u)))
rC = mpf("3.592658520")
for r in (mpf(1), rS, mpf(3), rC):
    print("  r =", nstr(r, 6), " dA/dr =", nstr(M / 2 + (1 - 4 * M) / (8 * r**2), 6))
print("  min over [r_S, r_C] is at r_S (the derivative rises in r since 1-4M<0)")
for pi in (mpf("0.3"), mpf("0.5"), mpf("0.7"), mpf("0.9")):
    Mp = Mtop(pi, u)
    print(f"  pi={nstr(pi,2)} M={nstr(Mp,5)}: dA/dr at r=1.2: {nstr(Mp/2+(1-4*Mp)/(8*mpf('1.44')),5)},"
          f" condition r^2 > 1-1/(4M) = {nstr(1-1/(4*Mp),4)}")
