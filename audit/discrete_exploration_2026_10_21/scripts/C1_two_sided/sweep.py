"""C1 sweep over incumbent strength: corner intervals and branch windows.

Print only. Double precision. Baseline tie rules for corners (strict nets
reported; equalities occur only at isolated thresholds). Edge roots use the
conventional investor mixture at indifference.

Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/C1_two_sided/sweep.py
"""
import math

h, ell, p, rho, k, b = 10.0, 1.0, 0.5, 0.25, 0.02, 2.0
a = math.exp(-1.0 / b)
d = 1.0 - a
alpha = a / (1 + a)
beta = 1.0 / (1 + a)
gamma = (1 - a) / (1 + a)
delta = a * a / (1 + a)
phi = a * (1 - a) / (1 + a)
m1, M1 = alpha, beta


def auction(r):
    gH = h - r / 2 - p * p / (2 * r)
    gL = (ell * ell - p * p) / (2 * r)
    DT = (r - ell) ** 2 / (2 * r)
    return gH, gL, DT


def mus(u, v):
    Ap = 1 + u * d / a
    Bp = 1 - v * d
    Am = 1 - u * d
    Bm = 1 + v * d / a
    return Ap / (Ap + Bp), Am / (Am + Bp), Am / (Am + Bm)


def nets(u, v, tau, DT, ep=None, e0=None, em=None):
    mup, mu0, mum = mus(u, v)
    if ep is None:
        ep = 1.0 if mup >= tau else rho
        e0 = 1.0 if mu0 >= tau else rho
        em = 1.0 if mum >= tau else rho
    gH = DT * (beta * ep * (1 - mup) + phi * e0 * (1 - mu0) + delta * em * (1 - mum))
    gL = DT * (delta * ep * mup + phi * e0 * mu0 + beta * em * mum)
    return gH - k, gL - k, (ep, e0, em)


def outcome(u, v, ep, e0, em):
    pHp = (1 - u) * alpha + u * beta
    pH0 = (1 - u) * gamma + u * phi
    pHm = (1 - u) * alpha + u * delta
    pLp = (1 - v) * alpha + v * delta
    pL0 = (1 - v) * gamma + v * phi
    pLm = (1 - v) * alpha + v * beta
    E = 0.5 * (pHp * ep + pH0 * e0 + pHm * em + pLp * ep + pL0 * e0 + pLm * em)
    OH = 0.5 * (pHp * ep + pH0 * e0 + pHm * em)
    return E, OH


def corners(r, cH):
    gH, gL, DT = auction(r)
    tau = (cH - gL) / (gH - gL)
    res = {}
    for (u, v, nm) in [(0, 0, "NT"), (1, 1, "T"), (1, 0, "BNS"), (0, 1, "SNB")]:
        nH, nL, es = nets(u, v, tau, DT)
        okH = nH <= 1e-12 if u == 0 else nH >= -1e-12
        okL = nL <= 1e-12 if v == 0 else nL >= -1e-12
        E, OH = outcome(u, v, *es)
        res[nm] = (okH and okL, nH, nL, E, OH, es)
    return res, tau, DT


print("Corner gain coefficients (gross/DT), pattern-dependent:")
cBNS_H_rec = alpha * beta * (1 + rho)
cBNS_L_rec = delta * M1 + rho * m1 * (phi + beta)
cSNB_L_rec = alpha * beta * (1 + rho)
cSNB_H_rec = (beta + phi) * m1 + delta * rho * beta
print(f" BNS with recruitment (M1>=tau): coeffH={cBNS_H_rec:.10f} coeffL={cBNS_L_rec:.10f}")
print(f" SNB with recruitment at + and 0: coeffH={cSNB_H_rec:.10f} coeffL={cSNB_L_rec:.10f}")
cBNS_H_rho = 2 * rho * alpha * beta
cBNS_L_rho = rho * (delta * M1 + (phi + beta) * m1)
print(f" BNS/SNB at constant rho: trader coeff={cBNS_H_rho:.10f} abstainer-deviation coeff={cBNS_L_rho:.10f}")
print(f" NT deviation coeff rho/2={rho/2:.10f}; T coeff with recruitment=0.2278252063 (posteriors.py)")


def r_of_DT(dd):
    return ell + dd + math.sqrt(dd * dd + 2 * ell * dd)


print(f" BNS(rec) DT window [{k/cBNS_H_rec:.8f},{k/cBNS_L_rec:.8f}] -> r [{r_of_DT(k/cBNS_H_rec):.8f},{r_of_DT(k/cBNS_L_rec):.8f}]")
print(f" BNS/SNB(rho) DT window [{k/cBNS_H_rho:.8f},{k/cBNS_L_rho:.8f}] -> r [{r_of_DT(k/cBNS_H_rho):.8f},{r_of_DT(k/cBNS_L_rho):.8f}]")
print(" (Windows apply only where the stated entry pattern holds at that r.)")

for cH in [5.0, 6.0]:
    print(f"\n===== Sweep cH={cH}, r step 0.01: corner equilibrium sets (changes only) =====")
    prev = None
    r = 1.05
    while r <= 8.001:
        res, tau, DT = corners(round(r, 2), cH)
        s = "".join([nm[0] if res[nm][0] else "." for nm in ["NT", "T", "BNS", "SNB"]])
        # encode: N=NT, T=T, B=BNS, S=SNB positions
        key = (res["NT"][0], res["T"][0], res["BNS"][0], res["SNB"][0])
        if key != prev:
            names = [nm for nm in ["NT", "T", "BNS", "SNB"] if res[nm][0]]
            print(f" r={r:.2f} tau={tau:.4f}: corners {names} "
                  f"E(T)={res['T'][3]:.4f} nets NT={res['NT'][1]:+.2e} T={res['T'][1]:+.2e}")
            prev = key
        r += 0.01

print("\n===== Selected strengths: full corner table =====")
for cH in [5.0, 6.0]:
    for r in [1.2, 1.55, 1.6, 1.65, 1.9, 3.0, 3.6, 4.5, 7.0]:
        res, tau, DT = corners(r, cH)
        line = " | ".join([f"{nm}:{'EQ' if res[nm][0] else '--'} E={res[nm][3]:.4f} OH={res[nm][4]:.4f}"
                           for nm in ["NT", "T", "BNS", "SNB"]])
        print(f"cH={cH} r={r} tau={tau:.4f}: {line}")

print("\n===== cH=6 baseline root (1,v) inside recruitment segment =====")
for r in [1.515, 1.52, 1.525, 1.53, 1.535, 1.54, 1.545, 1.55]:
    gH, gL, DT = auction(r)
    tau = (6.0 - gL) / (gH - gL)
    omt = 1 - tau
    vs = (1 - (1 + d / a) * omt / tau) / d
    nH_r, nL_r, _ = nets(1.0, vs + 1e-9, tau, DT)
    nH_1, nL_1, _ = nets(1.0, 1.0, tau, DT)
    print(f" r={r}: v*={vs:.6f} netL(v*+)={nL_r:+.3e} netL(1)={nL_1:+.3e} netH(v*+)={nH_r:+.3e}")
    if nL_r * nL_1 < 0:
        lo, hi, flo = vs, 1.0, nL_r
        for _ in range(80):
            mid = (lo + hi) / 2
            _, fm, _ = nets(1.0, mid, tau, DT, 1.0, rho, rho)
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        vv = (lo + hi) / 2
        nH, nL, _ = nets(1.0, vv, tau, DT, 1.0, rho, rho)
        E, OH = outcome(1.0, vv, 1.0, rho, rho)
        print(f"   BASELINE ROOT v={vv:.10f} netH={nH:+.3e} netL={nL:+.3e} E={E:.8f} OH={OH:.8f}")

print("\n===== cH=5 and cH=6 baseline root (1,v) window endpoints by bisection in r =====")
# Lower endpoint: net at (1,1)=0 (analytic r=1.515898...). Upper: netL at other end =0.
for cH in [5.0, 6.0]:
    def upper_net(r):
        gH, gL, DT = auction(r)
        tau = (cH - gL) / (gH - gL)
        if cH == 5.0:
            _, nL, _ = nets(1.0, 0.0, tau, DT)
            return nL
        omt = 1 - tau
        vs = (1 - (1 + d / a) * omt / tau) / d
        _, nL, _ = nets(1.0, vs + 1e-9, tau, DT)
        return nL
    lo, hi = 1.516, 1.60
    flo, fhi = upper_net(lo), upper_net(hi)
    print(f" cH={cH}: upper-end net at r=1.516: {flo:+.3e}; at 1.60: {fhi:+.3e}")
    if flo * fhi < 0:
        for _ in range(70):
            mid = (lo + hi) / 2
            fm = upper_net(mid)
            if (fm > 0) == (flo > 0):
                lo, flo = mid, fm
            else:
                hi = mid
        print(f"   upper endpoint r in [{lo:.10f},{hi:.10f}]")
