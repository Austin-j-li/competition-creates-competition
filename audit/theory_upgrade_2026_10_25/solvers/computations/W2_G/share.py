"""Composition (class-H share) checks, the Solver F hazard-order conjecture, the reverse-hazard order of the
uniform family, and a research-branch path at benchmark primitives with a non-uniform incumbent family.
Prints only."""
from mpmath import mp, mpf, sqrt, e as E

mp.dps = 40


# ---------- incumbent laws as finite mixtures of uniforms: list of (weight, lo, hi) ----------
def Fmix(y, mix):
    s = mpf(0)
    for w, lo, hi in mix:
        if y <= lo:
            c = 0
        elif y >= hi:
            c = 1
        else:
            c = (y - lo) / (hi - lo)
        s += w * c
    return s


def intF(v, mix):
    """int_{-inf}^v F(y) dy, exact for uniform mixtures."""
    s = mpf(0)
    for w, lo, hi in mix:
        if v <= lo:
            c = 0
        elif v >= hi:
            c = (hi - lo) / 2 + (v - hi)
        else:
            c = (v - lo) ** 2 / (2 * (hi - lo))
        s += w * c
    return s


def point_payoffs(v, p, mix):
    """Point value v >= p: g_v = int_p^v F, t_v - t_0 = pF(p) + int_p^v (1-F), W_v = F(v)."""
    g = intF(v, mix) - intF(p, mix)
    wv = p * Fmix(p, mix) + (v - p) - g
    return g, wv, Fmix(v, mix)


print("=== (1) Solver F conjecture: hazard-rate order of the classes makes W_L/W_H fall under every FOSD shift? ===")
# point masses ell=1 < h=3 satisfy every class order (lr, hr, rh)
F0 = [(mpf(1), mpf(0), mpf(2))]
F1 = [(mpf(1) / 2, mpf(0), mpf(1)), (mpf(1) / 2, mpf(3), mpf(4))]
grid = [mpf(i) / 100 for i in range(0, 501)]
print("  F1 <= F0 everywhere on [0,5]:", all(Fmix(y, F1) <= Fmix(y, F0) + mpf(10) ** -30 for y in grid))
for name, F in (("F0=U[0,2]", F0), ("F1=0.5U[0,1]+0.5U[3,4]", F1)):
    WL, WH = Fmix(mpf(1), F), Fmix(mpf(3), F)
    print(f"  {name}: W_L=F(1)={mp.nstr(WL, 6)} W_H=F(3)={mp.nstr(WH, 6)} W_L/W_H={mp.nstr(WL / WH, 6)}")
# Solver F's own two-point classes, same FOSD pair idea
GL = [(mpf(1) / 2, mpf(2)), (mpf(1) / 2, mpf(10))]
GH = [(mpf(49) / 100, mpf(5) / 2), (mpf(51) / 100, mpf(10))]
Fa = [(mpf(1), mpf("2.1"), mpf("2.4"))]
Fb = [(mpf(1), mpf("2.6"), mpf(9))]
for name, F in (("U[2.1,2.4]", Fa), ("U[2.6,9]", Fb)):
    WL = sum(w * Fmix(v, F) for w, v in GL)
    WH = sum(w * Fmix(v, F) for w, v in GH)
    print(f"  Solver F classes, F={name}: W_L={mp.nstr(WL, 6)} W_H={mp.nstr(WH, 6)} W_L/W_H={mp.nstr(WL / WH, 6)}")

print("\n=== (2) reverse-hazard-rate order of the uniform scale family: F_{r'}/F_r nondecreasing in y ===")
for r, rp in ((mpf(1.5), mpf(1.7)), (mpf(11), mpf(12)), (mpf(3), mpf(18) / 5)):
    ys = [mpf(i) / 50 * rp for i in range(1, 60)]
    ratios = [Fmix(y, [(1, 0, rp)]) / Fmix(y, [(1, 0, r)]) for y in ys]
    mono = all(ratios[i + 1] >= ratios[i] - mpf(10) ** -30 for i in range(len(ratios) - 1))
    print(f"  r={mp.nstr(r, 4)} -> r'={mp.nstr(rp, 4)}: ratio nondecreasing on (0, 1.2 r']: {mono}; first {mp.nstr(ratios[0], 5)} last {mp.nstr(ratios[-1], 5)}")


# ---------- research branch (Lemma a5-middle) for point-mass classes and a mixture incumbent ----------
def m_of(lam, beta):
    return (1 - lam) * beta / (2 * beta + lam * (1 - 2 * beta))


def lam_R(Delta, a, beta, k):
    A = 2 * a * (1 - 2 * beta)
    B = 4 * a * beta + k * (1 - 2 * beta) + beta * Delta
    C = beta * (2 * k - Delta)
    return (-B + sqrt(B * B - 4 * A * C)) / (2 * A)


def branch(mix, P):
    h, ell, p, cH, rho, k, beta, a, cap = (P[x] for x in ("h", "ell", "p", "cH", "rho", "k", "beta", "a", "cap"))
    gH, wH, WH = point_payoffs(h, p, mix)
    gL, wL, WL = point_payoffs(ell, p, mix)
    Delta = wH - wL
    gam = gH - gL
    tau = (cH - gL) / gam
    lE = beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))
    lR = lam_R(Delta, a, beta, k)
    phi = Delta * (1 - tau) - k - 2 * a * lE
    eH = rho + (1 - rho) * (beta + (1 - beta) * lR)
    eL = rho + (1 - rho) * beta * (1 - lR)
    ent = rho + (1 - rho) * (beta + (mpf(1) / 2 - beta) * lR)
    OH, OL = eH * WH / 2, eL * WL / 2
    ok = (mpf(1) / 2 < tau < 1) and (rho * Delta < 2 * k) and (phi >= 0) and (lR < cap) and (lE != cap)
    return dict(Delta=Delta, tau=tau, lE=lE, lR=lR, phi=phi, WH=WH, WL=WL, eH=eH, eL=eL, ent=ent, OH=OH, OL=OL,
                SH=OH / (OH + OL), entrant=eH / (eH + eL), ok=ok, rhoD2k=rho * Delta - 2 * k, gH=gH, gL=gL)


beta = mpf("0.294655")
u = E - 1
BM = dict(h=mpf(10), ell=mpf(1), p=mpf(1) / 2, cH=mpf(6), rho=mpf(1) / 4, k=mpf(1) / 50, beta=beta, a=mpf(1) / 40,
          cap=u * beta / (1 + u * beta))

print("\n=== (3) benchmark classes, costs, slot, a and cap; incumbent (1-q)U[0,r0] + q U[c-d,c+d], c moving across h ===")
r0, q, d = mpf("1.5"), mpf("0.004"), mpf("0.01")
prev = None
for c in [mpf("9.97"), mpf("9.98"), mpf("9.99"), mpf("10.00"), mpf("10.01"), mpf("10.02"), mpf("10.03")]:
    mix = [(1 - q, mpf(0), r0), (q, c - d, c + d)]
    s = branch(mix, BM)
    print(f"  c={mp.nstr(c, 5)} branch={s['ok']} Delta={mp.nstr(s['Delta'], 9)} tau={mp.nstr(s['tau'], 7)} "
          f"lamE={mp.nstr(s['lE'], 7)} lamR={mp.nstr(s['lR'], 9)} rhoD-2k={mp.nstr(s['rhoD2k'], 5)} phi={mp.nstr(s['phi'], 5)}")
    print(f"      W_H={mp.nstr(s['WH'], 7)} W_L={mp.nstr(s['WL'], 7)} entry={mp.nstr(s['ent'], 9)} e_H={mp.nstr(s['eH'], 9)} "
          f"O_H={mp.nstr(s['OH'], 9)} S_H={mp.nstr(s['SH'], 9)} entrant share={mp.nstr(s['entrant'], 9)}")
# FOSD check of the path: F_c' <= F_c for c' > c
ys = [mpf(i) / 1000 * 12 for i in range(0, 1001)]
mA = [(1 - q, mpf(0), r0), (q, mpf("9.97") - d, mpf("9.97") + d)]
mB = [(1 - q, mpf(0), r0), (q, mpf("10.03") - d, mpf("10.03") + d)]
print("  FOSD: F_{10.03} <= F_{9.97} on grid:", all(Fmix(y, mB) <= Fmix(y, mA) + mpf(10) ** -30 for y in ys))
print("  point-mass bound check: 1 - W_H <= Delta/(h-ell) at c=10.03:",
      mp.nstr(1 - branch(mB, BM)['WH'], 6), "<=", mp.nstr(branch(mB, BM)['Delta'] / 9, 6))

print("\n=== (4) the same path with the counterexample's costs (rho=0.05, k=0.2, beta=0.2, a=5, cap=0.9, c_H=2.5) ===")
CX = dict(h=mpf(10), ell=mpf(1), p=mpf(1) / 2, cH=mpf(5) / 2, rho=mpf(1) / 20, k=mpf(1) / 5, beta=mpf(1) / 5, a=mpf(5),
          cap=mpf(9) / 10)
for r in (mpf(11), mpf(12)):
    s = branch([(mpf(1), mpf(0), r)], CX)
    print(f"  uniform r={mp.nstr(r, 3)}: branch={s['ok']} entry={mp.nstr(s['ent'], 7)} O_H={mp.nstr(s['OH'], 7)} O_L={mp.nstr(s['OL'], 7)} "
          f"S_H={mp.nstr(s['SH'], 7)} entrant share={mp.nstr(s['entrant'], 7)} W_L/W_H={mp.nstr(s['WL'] / s['WH'], 5)}")
