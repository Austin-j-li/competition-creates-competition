"""C3 three-point delay calculations. Print only. Exact fractions where possible."""
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt

mp.dps = 50

h = F(10)
ell = F(1)
p = F(1, 2)
rho = F(1, 4)
cH = F(6)
k = F(1, 50)


def objs(r):
    t0 = p * (1 - p / r)
    tH = r / 2 + p * p / (2 * r)
    tL = ell - (ell * ell - p * p) / (2 * r)
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    wL = tL - t0
    wH = tH - t0
    S = gH - gL
    return t0, tH, tL, gH, gL, DT, wL, wH, S


def Bfun(r, mu):
    _, _, _, gH, gL, _, _, _, _ = objs(r)
    return gL + mu * (gH - gL)


print("=== Three-point exact objects ===")
for r in [F(6, 5), F(3), F(18, 5), F(5), F(17, 2)]:
    t0, tH, tL, gH, gL, DT, wL, wH, S = objs(r)
    print(f"r={r} ({float(r)}): t0={t0} tH={tH} tL={tL} gH={gH} gL={gL} DT={DT} wL={wL} wH={wH} S={S}")
    print(f"  B(1/2)={Bfun(r, F(1,2))} tau={(cH-gL)/S} rho*DT/3={rho*DT/3} k={k}")
    gross_nodelay = rho * DT / 3
    gross1_delay = (DT * (1 + 2 * rho) + wL * (1 - rho)) / 9
    print(f"  Gross1 no-delay={gross_nodelay}={float(gross_nodelay)} Gross1 delay={gross1_delay}={float(gross1_delay)} diff={(1-rho)*(DT+wL)/9}")
    print(f"  Gross2 at mu1=1/2 wait branch={rho*DT/3}")

print()
print("=== Waiting value at mu1=1/2, b2=1: W=(delta*gH-cH)/6 if positive ===")
for r in [F(3), F(18, 5), F(5)]:
    _, _, _, gH, gL, DT, wL, _, S = objs(r)
    for delta in [F(4, 5), F(9, 10), F(19, 20)]:
        W = (delta * gH - cH) / 6
        N = Bfun(r, F(1, 2)) - cH
        print(f"r={r} delta={delta}: W={W}={float(W):.6f} N(1/2)={N}={float(N):.6f} delta*gH-cH={delta*gH-cH} thresh cH/gH={cH/gH}={float(cH/gH):.6f}")

print()
print("=== Entry and ownership, full trade ===")
E_one = rho + (1 - rho) * F(1, 6)
E_del = rho + (1 - rho) * F(5, 18)
OH_one = rho / 2 + (1 - rho) * F(1, 6)
OH_del = rho / 2 + (1 - rho) * F(5, 18)
print(f"E one-round={E_one}={float(E_one)} E delay={E_del}={float(E_del)}")
print(f"OH one-round={OH_one}={float(OH_one)} OH delay={OH_del}={float(OH_del)}")
print(f"P(mu1=1)=1/6 P(mu1=1/2,mu12=1)=1/9 sum=5/18={float(F(5,18))}")

print()
print("=== Thresholds in r (mpmath) ===")
rho_m = mpf("0.25")
k_m = mpf("0.02")
ell_m = mpf(1)


def r_of_d(d):
    return ell_m + d + sqrt(d * d + 2 * ell_m * d)


rT = r_of_d(3 * k_m / rho_m)
print(f"rT = r(3k/rho) = {rT}")
for cval in [mpf(6), mpf(6) / mpf("0.9"), mpf(6) / mpf("0.8"), mpf(6) / mpf("0.95")]:
    rc = (mpf(10) - cval) + sqrt((mpf(10) - cval) ** 2 - mpf("0.25"))
    print(f"ceiling for c={cval}: rC={rc}")

print()
print("=== General mu1 waiting cutoff, b2=1, r=3 ===")
rF = F(3)
_, _, _, gH, gL, DT, wL, _, S = objs(rF)
for delta in [F(4, 5), F(9, 10), F(19, 20), F(1)]:
    tau = (cH - gL) / S
    taud = (cH / delta - gL) / S
    mu_form = (cH - gL) / (S - (delta * gH - cH) / 3)
    W_taud = taud * (delta * gH - cH) / 3
    N_taud = cH * (1 - delta) / delta
    print(f"delta={delta}: tau={tau}={float(tau):.6f} tau_delta={taud}={float(taud):.6f} mu_form(below)={mu_form}={float(mu_form):.6f} W(taud)={float(W_taud):.6f} N(taud)={float(N_taud):.6f}")
    # full-region linear root for mu>=tau_delta, b2=1, bottom term zero:
    # (mu/3)(dgH-cH)+(2/3)(d*(gL+S mu)-cH) = gL+S mu-cH
    # mu*[(dgH-cH)/3 + 2 d S/3 - S] = (gL-cH) - (2/3)(d gL - cH)
    lhs_coef = (delta * gH - cH) / 3 + 2 * delta * S / 3 - S
    rhs = (gL - cH) - F(2, 3) * (delta * gL - cH)
    mu_full = rhs / lhs_coef
    print(f"  full-region root={mu_full}={float(mu_full):.6f} lhs_coef={lhs_coef} rhs={rhs}")

print()
print("=== Prices P1 P2 delay equilibrium r=3 delta=0.9 ===")
t0, tH, tL, gH, gL, DT, wL, wH, S = objs(F(3))
# P2(mu12)=t0+e2*(wL+DT*mu12); e2: mu=1 ->1, mu=1/2,0 ->rho (wait branch at mu1=1/2)
for mu, e2 in [(F(0), rho), (F(1, 2), rho), (F(1), F(1))]:
    P2 = t0 + e2 * (wL + DT * mu)
    print(f"mu12={mu} e2={e2} P2={P2}={float(P2):.6f}")
# P1(1/2)=E[P2|mu1=1/2]: probs mu12 0:1/6, 1/2:2/3, 1:1/6
P1_mid = F(1, 6) * (t0 + rho * wL) + F(2, 3) * (t0 + rho * (wL + DT / 2)) + F(1, 6) * (t0 + (wL + DT))
print(f"P1(mu1=1/2)={P1_mid}={float(P1_mid):.6f}")
print(f"P1(mu1=1)={t0 + (wL+DT)} P1(mu1=0) branch exit e=rho: P2 const belief 0 -> {t0+rho*wL}")
# Residual check at mu1=1/2
aH = (2 * rho + 1) / 3
aL = rho
ResH = F(1, 2) * (DT * aH + wL * (aH - aL))
print(f"aH={aH} aL={aL} ResH1(1/2)={ResH}={float(ResH):.6f} Gross1=(2/3)Res={float(F(2,3)*ResH):.6f}")

print()
print("=== Entry falls example: low cH so prior justifies entry ===")
cH_low = F(4)
for r in [F(3)]:
    _, _, _, gH, gL, DT, wL, _, S = objs(r)
    tau_low = (cH_low - gL) / S
    print(f"cH=4 r=3 tau={tau_low}={float(tau_low):.6f} B(1/2)={Bfun(r,F(1,2))} N(1/2)={Bfun(r,F(1,2))-cH_low}")
    for delta in [F(9, 10), F(19, 20)]:
        # W(1/2) b2=1: (1/6)(d gH-cH)_+ + (2/3)(d B(1/2)-cH)_+ + (1/6)(d gL-cH)_+
        def pos(x):
            return x if x > 0 else F(0)
        Wv = F(1, 6) * pos(delta * gH - cH_low) + F(2, 3) * pos(delta * Bfun(r, F(1, 2)) - cH_low) + F(1, 6) * pos(delta * gL - cH_low)
        print(f" delta={delta} W(1/2)={Wv}={float(Wv):.6f} N={float(Bfun(r,F(1,2))-cH_low):.6f}")
