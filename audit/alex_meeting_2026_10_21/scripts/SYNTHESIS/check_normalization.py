"""Red-team check 7: c_L is slack inside its window; the window edges.

Print-only. Run from the repository root with .venv/bin/python.
"""
from mpmath import mp, mpf, exp, log

mp.dps = 25
h, ell, p, rho, cH, b, k = mpf(10), mpf(1), mpf('0.5'), mpf('0.25'), mpf(6), mpf(2), mpf('0.02')
m = 1 / (1 + exp(2 / b)); M = 1 - m


def auction(r):
    t0 = p * (1 - p / r); tH = r / 2 + p**2 / (2 * r); tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - r / 2 - p**2 / (2 * r); gL = (ell**2 - p**2) / (2 * r)
    return t0, tH, tL, gH, gL


def closed_forms(r, cL):
    t0, tH, tL, gH, gL = auction(r)
    tau = (cH - gL) / (gH - gL); xs = (b / 2) * log(tau / (1 - tau))
    aH = 1 - exp((xs - 1) / b) / 2; aL = exp(-(xs + 1) / b) / 2
    E = rho + (1 - rho) * (aH + aL) / 2; OH = (rho + (1 - rho) * aH) / 2
    floor_ok = cL < gL + m * (gH - gL)
    return E, OH, floor_ok


print("=== 7. c_L enters no closed form of eq. (12); entry is constant on the floor window ===")
for r, label in ((mpf(3), 'r1'), (mpf('3.6'), 'r2')):
    t0, tH, tL, gH, gL = auction(r)
    print(f"   {label}={float(r)}: B_r(m) = {float(gL + m*(gH-gL)):.6f}, g_L = {float(gL):.6f}")
for cL in [mpf(0), mpf('0.125'), mpf(1), mpf('2.26'), mpf('2.3'), mpf('2.36'), mpf('2.366'), mpf('2.4')]:
    E, OH, ok = closed_forms(mpf(3), cL)
    print(f"   c_L={float(cL):5.3f}: floor c_L < B_r1(m) {'holds' if ok else 'FAILS'};  eq.(12) entry={float(E):.6f} ownership={float(OH):.6f} (identical by construction: c_L is absent from (12))")
print("   Window for parts (i)-(ii): [0, B_r1(m)) = [0, 2.366); for the three-economy result [0, B_r2(m)) = [0, 2.272). The memo's 2.26 is a grid endpoint, not the edge.")
