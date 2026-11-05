"""Recompute the research branch (Lemma a5-middle, general form) for point-mass classes and a
uniform incumbent U[0, r], at the counterexample of W2.md and at the benchmark.
Prints only."""
from mpmath import mp, mpf, sqrt, e as E, log

mp.dps = 40


def payoffs(v, r, p):
    """Point value v >= p against R ~ U[0, r] (A6:245)."""
    if v <= r:
        t = v - (v * v - p * p) / (2 * r)
        g = (v * v - p * p) / (2 * r)
        W = v / r
    else:
        t = r / 2 + p * p / (2 * r)
        g = v - t
        W = mpf(1)
    return t, g, W


def m_of(lam, beta):
    return (1 - lam) * beta / (2 * beta + lam * (1 - 2 * beta))


def F_poly(lam, Delta, a, beta, k):
    return 2 * a * (1 - 2 * beta) * lam ** 2 + (4 * a * beta + k * (1 - 2 * beta) + beta * Delta) * lam + beta * (2 * k - Delta)


def lam_R(Delta, a, beta, k):
    A = 2 * a * (1 - 2 * beta)
    B = 4 * a * beta + k * (1 - 2 * beta) + beta * Delta
    C = beta * (2 * k - Delta)
    return (-B + sqrt(B * B - 4 * A * C)) / (2 * A)


def lam_E(tau, beta):
    return beta * (2 * tau - 1) / (beta + (1 - 2 * beta) * (1 - tau))


def Lambda_prime(Delta, lam, a, beta):
    den = 2 * beta + lam * (1 - 2 * beta)
    return m_of(lam, beta) / (2 * a + Delta * beta / den ** 2)


def state(r, P):
    h, ell, p, cH, rho, k, beta, a, cap = (P[x] for x in ("h", "ell", "p", "cH", "rho", "k", "beta", "a", "cap"))
    tH, gH, WH = payoffs(h, r, p)
    tL, gL, WL = payoffs(ell, r, p)
    Delta = tH - tL
    gam = gH - gL
    tau = (cH - gL) / gam
    lE = lam_E(tau, beta)
    lR = lam_R(Delta, a, beta, k)
    phi = Delta * (1 - tau) - k - 2 * a * lE
    Fcap = F_poly(cap, Delta, a, beta, k)
    eH = rho + (1 - rho) * (beta + (1 - beta) * lR)
    eL = rho + (1 - rho) * beta * (1 - lR)
    ent = rho + (1 - rho) * (beta + (mpf(1) / 2 - beta) * lR)
    OH = eH * WH / 2
    OL = eL * WL / 2
    return dict(r=r, Delta=Delta, gam=gam, tau=tau, gL=gL, gH=gH, WH=WH, WL=WL, lE=lE, lR=lR, phi=phi,
                Fcap=Fcap, eH=eH, eL=eL, ent=ent, OH=OH, OL=OL,
                cond=dict(tau_in=(tau > mpf(1) / 2 and tau < 1), rhoD_lt_2k=(rho * Delta < 2 * k),
                          rhoD_minus_2k=rho * Delta - 2 * k, phi_ge0=(phi >= 0), lamR_lt_cap=(lR < cap),
                          Fcap_pos=(Fcap > 0), lamE_ne_cap=(lE != cap), beta_le_third=(beta <= mpf(1) / 3),
                          Delta_gt_2k=(Delta > 2 * k)))


def fmt(x, n=6):
    return mp.nstr(x, n + 3) if not isinstance(x, bool) else str(x)


def show(s, rho):
    print(f"  r={fmt(s['r'])}: Delta={fmt(s['Delta'])} gamma={fmt(s['gam'])} tau={fmt(s['tau'])} "
          f"lamE={fmt(s['lE'])} lamR={fmt(s['lR'])} phi_a={fmt(s['phi'])} F(cap)={fmt(s['Fcap'])}")
    print(f"    W_H={fmt(s['WH'])} W_L={fmt(s['WL'])} e_H={fmt(s['eH'])} e_L={fmt(s['eL'])} entry={fmt(s['ent'])} "
          f"O_H={fmt(s['OH'])} O_L={fmt(s['OL'])}")
    SH = s['OH'] / (s['OH'] + s['OL'])
    entrant = s['eH'] / (s['eH'] + s['eL'])
    print(f"    multiplier e_H/rho={fmt(s['eH'] / rho)}  S_H=O_H/(O_H+O_L)={fmt(SH)}  "
          f"entrant share e_H/(e_H+e_L)={fmt(entrant)}  odds e_H/e_L={fmt(s['eH'] / s['eL'])}  W_H/W_L={fmt(s['WH'] / s['WL'])}")
    print("    conditions:", {k: (fmt(v) if not isinstance(v, bool) else v) for k, v in s['cond'].items()})


print("=== Counterexample of W2.md ===")
CX = dict(h=mpf(10), ell=mpf(1), p=mpf(1) / 2, cH=mpf(5) / 2, rho=mpf(1) / 20, k=mpf(1) / 5, beta=mpf(1) / 5,
          a=mpf(5), cap=mpf(9) / 10)
s11 = state(mpf(11), CX)
s12 = state(mpf(12), CX)
show(s11, CX['rho'])
show(s12, CX['rho'])
print("  hand formulas: Delta=9-49.5/r:", fmt(9 - mpf(49.5) / 11), fmt(9 - mpf(49.5) / 12),
      " tau=(2.5r-0.375)/49.5:", fmt((mpf(2.5) * 11 - mpf(0.375)) / mpf(49.5)), fmt((mpf(2.5) * 12 - mpf(0.375)) / mpf(49.5)))
dl_eH = log(s12['eH'] / s11['eH'])
dl_WH = log(s12['WH'] / s11['WH'])
dl_OH = log(s12['OH'] / s11['OH'])
print(f"  log change 11->12: e_H {fmt(dl_eH)}  W_H {fmt(dl_WH)}  O_H {fmt(dl_OH)} (sum check {fmt(dl_eH + dl_WH)})")
print(f"  pct change: entry {fmt(100 * (s12['ent'] / s11['ent'] - 1))}%  e_H {fmt(100 * (s12['eH'] / s11['eH'] - 1))}%  "
      f"W_H {fmt(100 * (s12['WH'] / s11['WH'] - 1))}%  O_H {fmt(100 * (s12['OH'] / s11['OH'] - 1))}%  "
      f"e_L {fmt(100 * (s12['eL'] / s11['eL'] - 1))}%")
# discrete channel decomposition: info channel at F_1 weights, direct channel at F_0 entry
info = (s12['eH'] - s11['eH']) * s12['WH'] / 2
direct = s11['eH'] * (s12['WH'] - s11['WH']) / 2
print(f"  O_H(12)-O_H(11)={fmt(s12['OH'] - s11['OH'])} = info {fmt(info)} + direct {fmt(direct)} (sum {fmt(info + direct)})")
# zero-research equilibrium at the same F
for s in (s11, s12):
    OZ = CX['rho'] * s['WH'] / 2
    print(f"  r={fmt(s['r'])}: zero-research O_H^Z={fmt(OZ)}  ratio O_H^R/O_H^Z={fmt(s['OH'] / OZ)}  diff={fmt(s['OH'] - OZ)}")
# local elasticities at r = 11, 12 (uniform, point masses, r > h)
for s in (s11, s12):
    Lp = Lambda_prime(s['Delta'], s['lR'], CX['a'], CX['beta'])
    eps_e = s['Delta'] * (1 - CX['rho']) * (1 - CX['beta']) * Lp / s['eH']
    print(f"  r={fmt(s['r'])}: Lambda'={fmt(Lp)}  eps_e = dlog e_H/dlog Delta={fmt(eps_e)}  Delta/gamma={fmt(s['Delta'] / s['gam'])}"
          f"  dlog e_H/dlog r={fmt(eps_e * s['gam'] / s['Delta'])} vs -dlog W_H/dlog r=1")

print("\n  scan of the counterexample family along r (branch membership, O_H)")
prev = None
for rr in [mpf(x) / 4 for x in range(40, 61)]:
    s = state(rr, CX)
    c = s['cond']
    on = c['tau_in'] and c['rhoD_lt_2k'] and c['phi_ge0'] and c['lamR_lt_cap'] and c['beta_le_third']
    print(f"   r={fmt(rr, 4)} branch={on} tau={fmt(s['tau'], 4)} rhoD-2k={fmt(c['rhoD_minus_2k'], 4)} phi={fmt(s['phi'], 4)} "
          f"lamR={fmt(s['lR'], 5)} entry={fmt(s['ent'], 6)} O_H={fmt(s['OH'], 6)}")

print("\n=== Benchmark (h=10, ell=1, p=1/2, c_H=6, rho=1/4, k=1/50, beta=0.294655, u=e-1, a=1/40) ===")
beta = mpf("0.294655")
u = E - 1
cap = u * beta / (1 + u * beta)
BM = dict(h=mpf(10), ell=mpf(1), p=mpf(1) / 2, cH=mpf(6), rho=mpf(1) / 4, k=mpf(1) / 50, beta=beta, a=mpf(1) / 40, cap=cap)
print("  cap lambda_bar =", fmt(cap), " b=(1-lam)beta =", fmt((1 - cap) * beta))
for rr in ("1.55", "1.60", "1.65"):
    s = state(mpf(rr), BM)
    show(s, BM['rho'])
    Lp = Lambda_prime(s['Delta'], s['lR'], BM['a'], beta)
    eps_e = s['Delta'] * (1 - BM['rho']) * (1 - beta) * Lp / s['eH']
    dDelta_dr = (1 - BM['ell'] ** 2 / mpf(rr) ** 2) / 2
    dlogD_dlogr = mpf(rr) * dDelta_dr / s['Delta']
    print(f"    Lambda'={fmt(Lp)} eps_e=dlog e_H/dlog Delta={fmt(eps_e)} dlog Delta/dlog r={fmt(dlogD_dlogr)} "
          f"dlog e_H/dlog r={fmt(eps_e * dlogD_dlogr)}  8*O_H={fmt(8 * s['OH'])}")

# branch ends: phi_a(r_R)=0 and F_r(cap)=0
from mpmath import findroot


def phi_r(rr):
    return state(rr, BM)['phi']


rR = findroot(phi_r, mpf("1.5"))
rcap = findroot(lambda rr: state(rr, BM)['Fcap'], mpf("1.68"))
rN = findroot(lambda rr: BM['rho'] * state(rr, BM)['Delta'] - 2 * BM['k'], mpf("1.75"))
sR = state(rR, BM)
scap = state(rcap, BM)
print(f"  r_R={fmt(rR)} lamE(r_R)={fmt(sR['lE'])} lamR(r_R)={fmt(sR['lR'])} entry(r_R)={fmt(sR['ent'])} e_H(r_R)={fmt(sR['eH'])} O_H(r_R)={fmt(sR['OH'])}")
print(f"  rbar_R={fmt(rcap)} lamR={fmt(scap['lR'])} entry={fmt(scap['ent'])} e_H={fmt(scap['eH'])} O_H={fmt(scap['OH'])}")
print(f"  r_N={fmt(rN)}  margin rN-rbar_R={fmt(rN - rcap)}")
ratio = scap['eH'] / sR['eH']
print(f"  e_H(cap)/e_H(r_R)={fmt(ratio)}  tolerable end-to-end W_H fall = 1 - 1/ratio = {fmt(1 - 1 / ratio)}")
print(f"  h - rbar_R = {fmt(BM['h'] - rcap)}, h - r_2 = {fmt(BM['h'] - mpf(18) / 5)}, h/r_2 = {fmt(BM['h'] / (mpf(18) / 5))}")

print("\n=== Proposition 2 at the benchmark ===")
lam = cap
b = (1 - lam) * beta
eH1 = BM['rho'] + (1 - BM['rho']) * (b + lam)
print(f"  b+lambda={fmt(b + lam)} e_H(F_1)={fmt(eH1)} own_r1=pi*e_H={fmt(eH1 / 2)} own_r0=pi*rho={fmt(BM['rho'] / 2)} "
      f"e_H-rho={fmt(eH1 - BM['rho'])} ratio own_r1/own_r0={fmt(eH1 / BM['rho'])} tolerable W_H fall 1-rho/e_H={fmt(1 - BM['rho'] / eH1)}")

print("\n=== Lambda'(Delta) against finite differences (benchmark slot, a=1/40) ===")
for D in (mpf("0.10"), mpf("0.12"), mpf("4.5")):
    for (aa, kk) in ((mpf(1) / 40, mpf(1) / 50), (mpf(5), mpf(1) / 5)):
        bb = beta if aa == mpf(1) / 40 else mpf(1) / 5
        if D <= 2 * kk:
            continue
        lr = lam_R(D, aa, bb, kk)
        hstep = mpf(10) ** -12
        fd = (lam_R(D + hstep, aa, bb, kk) - lam_R(D - hstep, aa, bb, kk)) / (2 * hstep)
        print(f"  Delta={fmt(D)} a={fmt(aa)} beta={fmt(bb)} k={fmt(kk)}: lamR={fmt(lr)} formula={fmt(Lambda_prime(D, lr, aa, bb), 10)} fd={fmt(fd, 10)}")
