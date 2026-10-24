"""C3 discrete-Laplace delay calculations. Print only. High precision."""
from mpmath import mp, mpf, e, sqrt

mp.dps = 50

h = mpf(10)
ell = mpf(1)
p = mpf("0.5")
rho = mpf("0.25")
kk = mpf("0.02")
bpar = mpf(2)
a = e ** (-1 / bpar)
m1 = a / (1 + a)
M1 = 1 / (1 + a)
m2 = (a * a) / (1 + a * a)
M2 = 1 / (1 + a * a)
print(f"a={a}")
print(f"m1={m1} M1={M1} m2={m2} M2={M2}")
print(f"P good given H buy={M1} given L no-buy={m1} uncond good full={(M1+M1*0+m1)/2} check pg={(1/(1+a)+a/(1+a))/2}")


def objs(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    wL = tL - t0
    S = gH - gL
    return t0, tH, tL, gH, gL, DT, wL, S


def Bf(r, mu):
    _, _, _, gH, gL, _, _, _ = objs(r)
    return gL + mu * (gH - gL)


def entry_now(r, mu, cH):
    return rho + (1 - rho) * (1 if Bf(r, mu) >= cH else 0)


def entry_late(r, mu, cH, delta):
    return rho + (1 - rho) * (1 if delta * Bf(r, mu) >= cH else 0)


print()
print("=== B values and one-round objects, cH=5 ===")
cH5 = mpf(5)
for r in [mpf("1.2"), mpf(3), mpf("3.6"), mpf(4), mpf("4.2"), mpf(5)]:
    t0, tH, tL, gH, gL, DT, wL, S = objs(r)
    print(f"r={r}: DT={DT} gH={gH} gL={gL} wL={wL}")
    print(f"  B(m1)={Bf(r,m1)} B(1/2)={Bf(r,mpf('0.5'))} B(M1)={Bf(r,M1)} B(m2)={Bf(r,m2)} B(M2)={Bf(r,M2)} tau={(cH5-gL)/S}")
    print(f"  rho*m1*DT={rho*m1*DT} rho*DT/2={rho*DT/2} DT={DT}")

print()
print("=== One-round Gross(beta), r=3, cH=5 and cH=5.5 ===")


def mu_pm(beta):
    Lp = 1 - beta + beta / a
    Lm = 1 - beta + beta * a
    return Lp / (1 + Lp), Lm / (1 + Lm), Lp, Lm


def gross_one(r, beta, cH):
    _, _, _, gH, gL, DT, wL, S = objs(r)
    mup, mum, Lp, Lm = mu_pm(beta)
    ep = entry_now(r, mup, cH)
    em = entry_now(r, mum, cH)
    return DT * (M1 * ep / (1 + Lp) + m1 * em / (1 + Lm)), mup, mum, ep, em


for cH in [mpf(5), mpf("5.5"), mpf(6)]:
    print(f"-- cH={cH} r=3 --")
    for beta in [mpf(0), mpf("0.1"), mpf("0.25"), mpf("0.5"), mpf("0.75"), mpf(1)]:
        g, mup, mum, ep, em = gross_one(mpf(3), beta, cH)
        print(f" beta={beta}: Gross={g} mu+={mup} mu-={mum} e+={ep} e-={em} net={g-kk}")
    # fine grid minimum and maximum
    vals = []
    for i in range(0, 2001):
        beta = mpf(i) / 2000
        g, _, _, _, _ = gross_one(mpf(3), beta, cH)
        vals.append((g, beta))
    print(f" grid min Gross={min(vals)} grid max Gross={max(vals)}")

print()
print("=== Two-round full-buy posteriors and probs ===")
print(f"P(GG|H)={M1*M1} P(GG|L)={m1*m1} P(GG)={(M1*M1+m1*m1)/2}")
print(f"P(good2|M1)={M1*M1+m1*m1} P(good2|m1)={2*m1*M1}")
print(f"P(M2)={(M1*M1+m1*m1)/2} P(1/2 final)={2*m1*M1} P(m2)={(M1*M1+m1*m1)/2} sum={(M1*M1+m1*m1)+2*m1*M1}")

print()
print("=== Delay values at r=3, cH=5, full buy ===")
r = mpf(3)
Pg2_M1 = M1 * M1 + m1 * m1
for delta in [mpf("0.8"), mpf("0.85"), mpf("0.9"), mpf("0.95"), mpf(1)]:
    NM1 = Bf(r, M1) - cH5
    Nm1 = Bf(r, m1) - cH5
    WM1 = Pg2_M1 * max(delta * Bf(r, M2) - cH5, mpf(0)) + (1 - Pg2_M1) * max(delta * Bf(r, mpf("0.5")) - cH5, mpf(0))
    Pg2_m1 = 2 * m1 * M1
    Wm1 = Pg2_m1 * max(delta * Bf(r, mpf("0.5")) - cH5, mpf(0)) + (1 - Pg2_m1) * max(delta * Bf(r, m2) - cH5, mpf(0))
    dstar = (cH5 + NM1 / Pg2_M1) / Bf(r, M2)
    print(f"delta={delta}: N(M1)={NM1} W(M1)={WM1} N(m1)={Nm1} W(m1)={Wm1} delta_star(M1)={dstar} tau_delta={(cH5/delta - objs(r)[4])/objs(r)[7]}")

print()
print("=== Entry ownership r=3 cH=5 ===")
Eone = rho + (1 - rho) * mpf("0.5")
OHone = rho / 2 + (1 - rho) * (M1 / 2)
PGG = (M1 * M1 + m1 * m1) / 2
PHGG = M1 * M1 / 2
Edel = rho + (1 - rho) * PGG
OHdel = rho / 2 + (1 - rho) * PHGG
print(f"E one={Eone} OH one={OHone} P(H|good)={M1}")
print(f"PGG={PGG} PHGG={PHGG} E delay(wait after G)={Edel} OH delay={OHdel} P(H|GG)={PHGG/PGG}")

print()
print("=== Round2 and Round1 gross, r=3 cH=5 delta=0.95 wait branch ===")
delta = mpf("0.95")
t0, tH, tL, gH, gL, DT, wL, S = objs(r)
eGG = entry_late(r, M2, cH5, delta)
eMid = entry_late(r, mpf("0.5"), cH5, delta)
eBB = entry_late(r, m2, cH5, delta)
print(f"eGG={eGG} eMid={eMid} eBB={eBB}")
Gross2_M1_wait = DT * (M1 * eGG * (1 - M2) + m1 * eMid * mpf("0.5"))
Gross2_M1_now = DT * (M1 * 1 * (1 - M2) + m1 * 1 * mpf("0.5"))
Gross2_m1_exit = DT * (M1 * rho * mpf("0.5") + m1 * rho * (1 - m2))
print(f"Gross2(M1,wait)={Gross2_M1_wait} Gross2(M1,now e=1)={Gross2_M1_now} Gross2(m1,exit)={Gross2_m1_exit}")
aH_M1 = M1 * eGG + m1 * eMid
aL_M1 = m1 * eGG + M1 * eMid
Res_M1 = (1 - M1) * (DT * aH_M1 + wL * (aH_M1 - aL_M1))
Res_m1 = (1 - m1) * DT * rho
Gross1_del = M1 * Res_M1 + m1 * Res_m1
Res_M1_one = 1 * DT * (1 - M1)
Gross1_one = M1 * Res_M1_one + m1 * Res_m1
print(f"aH(M1)={aH_M1} aL(M1)={aL_M1} Res(M1) delay={Res_M1} one={Res_M1_one}")
print(f"Gross1 delay={Gross1_del} Gross1 one-round full={Gross1_one}")

print()
print("=== Prices delay equilibrium r=3 cH=5 delta=0.95 ===")


def P2fun(r, mu12, e2):
    t0, _, _, _, _, DT, wL, _ = objs(r)
    return t0 + e2 * (wL + DT * mu12)


for name, mu12, e2 in [("GG M2", M2, eGG), ("mid 1/2", mpf("0.5"), eMid), ("BB m2", m2, eBB)]:
    print(f"{name}: P2={P2fun(r, mu12, e2)}")
P1_M1 = Pg2_M1 * P2fun(r, M2, eGG) + (1 - Pg2_M1) * P2fun(r, mpf("0.5"), eMid)
Pg2_m1v = 2 * m1 * M1
P1_m1 = Pg2_m1v * P2fun(r, mpf("0.5"), rho) + (1 - Pg2_m1v) * P2fun(r, m2, rho)
print(f"P1(M1)={P1_M1} P1(m1)={P1_m1} one-round P(M1)={P2fun(r, M1, mpf(1))} P(m1)={P2fun(r, m1, rho)} P(1/2)={P2fun(r, mpf('0.5'), rho)}")

print()
print("=== Ceilings by bisection, cH=5 ===")


def bisect_root(fun, lo, hi, n=200):
    flo = fun(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = fun(mid)
        if flo * fm <= 0:
            hi = mid
        else:
            lo = mid
            flo = fm
    return (lo + hi) / 2


rC1 = bisect_root(lambda rr: Bf(rr, M1) - cH5, mpf(3), mpf(5))
print(f"rC1 B(M1)=5: {rC1} B check={Bf(rC1, M1)}")
for delta in [mpf("0.8"), mpf("0.9"), mpf("0.95"), mpf(1)]:
    rCd = bisect_root(lambda rr, d=delta: d * Bf(rr, M2) - cH5, mpf(3), mpf(8))
    print(f"delta={delta}: rC delay delta*B(M2)=5: {rCd} B(M2)={Bf(rCd, M2)} B(M1)={Bf(rCd, M1)}")

print()
print("=== Entry path scan, cH=5, delta=0.9 and 0.95, full buy where Gross min bound holds ===")
for delta in [mpf("0.9"), mpf("0.95")]:
    print(f"-- delta={delta} --")
    for r in [mpf("1.2"), mpf(2), mpf("2.5"), mpf(3), mpf("3.6"), mpf(4), mpf("4.2"), mpf("4.8"), mpf(5), mpf(6)]:
        t0, tH, tL, gH, gL, DT, wL, S = objs(r)
        NM1 = Bf(r, M1) - cH5
        WM1 = Pg2_M1 * max(delta * Bf(r, M2) - cH5, mpf(0)) + (1 - Pg2_M1) * max(delta * Bf(r, mpf("0.5")) - cH5, mpf(0))
        branch = "wait" if (WM1 > max(NM1, mpf(0))) else ("now" if NM1 >= 0 else "exit")
        # high-cost entry prob under full buy and branch at M1; at m1 W=0 in this range (printed)
        Wm1 = Pg2_m1v * max(delta * Bf(r, mpf("0.5")) - cH5, mpf(0)) + (1 - Pg2_m1v) * max(delta * Bf(r, m2) - cH5, mpf(0))
        if branch == "wait":
            phigh = PGG
        elif branch == "now":
            phigh = mpf("0.5")
        else:
            phigh = mpf(0)
        Efull = rho + (1 - rho) * phigh
        bound = 2 * rho * DT * m1 * M1
        print(f" r={r}: DT={DT} bound2rhoDTm1M1={bound} N(M1)={NM1} W(M1)={WM1} W(m1)={Wm1} branchG={branch} E_if_full={Efull}")

print()
print("=== Coexistence example: r=3, cH=5.5, delta=0.95, k=0.09 ===")
cHx = mpf("5.5")
kx = mpf("0.09")
deltax = mpf("0.95")
r = mpf(3)
g0_one, _, _, _, _ = gross_one(r, mpf(0), cHx)
g1_one, _, _, _, _ = gross_one(r, mpf(1), cHx)
print(f"one-round Gross(0)={g0_one} Gross(1)={g1_one} k={kx}")
NM1x = Bf(r, M1) - cHx
WM1x = Pg2_M1 * max(deltax * Bf(r, M2) - cHx, mpf(0))
Wm1x = Pg2_m1v * max(deltax * Bf(r, mpf("0.5")) - cHx, mpf(0))
print(f"N(M1)={NM1x} W(M1)={WM1x} W(m1)={Wm1x} B(M1)={Bf(r,M1)} B(M2)={Bf(r,M2)} delta*B(M2)={deltax*Bf(r,M2)}")
t0, tH, tL, gH, gL, DT, wL, S = objs(r)
eGGx = entry_late(r, M2, cHx, deltax)
eMidx = entry_late(r, mpf("0.5"), cHx, deltax)
G2M1x = DT * (M1 * eGGx * (1 - M2) + m1 * eMidx * mpf("0.5"))
G2m1x = DT * (M1 * rho * mpf("0.5") + m1 * rho * (1 - m2))
aHx = M1 * eGGx + m1 * eMidx
aLx = m1 * eGGx + M1 * eMidx
ResM1x = (1 - M1) * (DT * aHx + wL * (aHx - aLx))
Resm1x = (1 - m1) * DT * rho
G1x = M1 * ResM1x + m1 * Resm1x
print(f"eGG={eGGx} eMid={eMidx} Gross2(M1)={G2M1x} Gross2(m1)={G2m1x} Gross1 delay={G1x}")
print(f"P1(M1)={Pg2_M1*P2fun(r,M2,eGGx)+(1-Pg2_M1)*P2fun(r,mpf('0.5'),eMidx)} P1(m1)={Pg2_m1v*P2fun(r,mpf('0.5'),rho)+(1-Pg2_m1v)*P2fun(r,m2,rho)}")
print(f"E delay full={rho+(1-rho)*PGG} E no-trade={rho} (B(1/2)={Bf(r,mpf('0.5'))} < cH)")

print()
print("=== Round2 Gross(beta2) grids at r=3 (lower-bound check) ===")


def gross2_grid(mu1, branch_e_plus, branch_e_minus_fixed=None):
    # branch_e_plus/minus are entry rates at the two round-2 posteriors under beta2=1.
    # For general beta2, posteriors move; entry uses late/now/exit rule by posterior value.
    # This helper is used only for the printed beta2=1 values and the rho lower bound E[1-mu].
    o1 = mu1 / (1 - mu1)
    vals = []
    for i in range(0, 1001):
        beta = mpf(i) / 1000
        Lp = 1 - beta + beta / a
        Lm = 1 - beta + beta * a
        Eone = M1 / (1 + o1 * Lp) + m1 / (1 + o1 * Lm)
        vals.append((Eone, beta))
    return min(vals), max(vals)


for name, mu1 in [("m1", m1), ("1/2", mpf("0.5")), ("M1", M1)]:
    mn, mx = gross2_grid(mu1, None)
    print(f"mu1={name}: min E_buy[1-mu12]={mn} max={mx} rho*DT*minE at r=3={rho*mpf(2)/3*mn[0]}")

print()
print("=== Entry creation window at r=3 ===")
print(f"B(M1)={Bf(mpf(3),M1)} B(M2)={Bf(mpf(3),M2)} ratio B(M1)/B(M2)={Bf(mpf(3),M1)/Bf(mpf(3),M2)}")
for delta in [mpf("0.9"), mpf("0.95")]:
    print(f"delta={delta}: delta*B(M2)={delta*Bf(mpf(3),M2)} window (B(M1), delta*B(M2)] width={delta*Bf(mpf(3),M2)-Bf(mpf(3),M1)}")
