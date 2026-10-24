"""Print the numbers shown on the order-slot explainer page (print only)."""
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt, e, findroot
mp.dps = 30
h, ell, p, rho, cH, k = 10, 1, F(1, 2), F(1, 4), 6, F(1, 50)

def objs(r):
    r = F(r)
    t0 = p * (1 - p / r); tH = r / 2 + p**2 / (2 * r); tL = ell - (ell**2 - p**2) / (2 * r)
    gH = h - tH; gL = ell - tL; D = tH - tL
    return t0, tH, tL, gH, gL, D

def tau(r):
    t0, tH, tL, gH, gL, D = objs(r)
    return (cH - gL) / (gH - gL)

print("tau(3) =", tau(3), float(tau(3)), " tau(18/5) =", tau(F(18, 5)), float(tau(F(18, 5))))
print("Delta(6/5) =", objs(F(6, 5))[5], " Delta(3) =", objs(3)[5], " Delta(18/5) =", objs(F(18, 5))[5])

def calib(lam, beta, exact=True):
    b = (1 - lam) * beta; u = lam / b; M = (1 + u) / (2 + u); w = 2 * b + lam
    E = rho + (1 - rho) * w / 2; O = F(1, 8) + 3 * (b + lam) / 8 if exact else mpf(1)/8 + 3*(b+lam)/8
    return b, u, M, E, O

lam, beta = F(6, 17), F(1, 3)
b, u, M, E, O = calib(lam, beta)
print("A: b =", b, " u =", u, float(u), " M =", M, " E(3) =", E, float(E), " O_H =", O, float(O))
print("   strip in u: (82/59, 2686/1559) =", float(F(82, 59)), float(F(2686, 1559)))
rC = (50 + sqrt(2529)) / 29
print("   r_C =", rC)
# r_N, r_A, r_F
def rr(D): D = mpf(D); return 1 + D + sqrt(D * D + 2 * D)
rN = rr(2 * k / rho); rF = rr(k / (1 - M))
print("   r_N =", rN, " r_F =", rF)
def Dm(r): return (r - 1)**2 / (2 * r)
def taum(r): return (48 * r - 3) / (4 * (20 * r - r * r - 1))
rA = findroot(lambda r: Dm(r) * (1 - taum(r)) - mpf(k), 1.4)
print("   r_A =", rA)
for r in [mpf('1.40'), mpf('1.43'), rF]:
    print("   interior-branch entry at", r, "=", rho + (1 - rho) * mpf(b) * Dm(r) / (2 * mpf(k)))
# sale threshold for class L: rho*Delta*(1-M) = k
rS = rr(k / (rho * (1 - M)))
print("   class L starts to sell at r =", rS)
# Calibration B
uB = e - 1
def entry_of(beta):
    beta = mpf(beta); lamB = uB * beta / (1 + uB * beta); bB = beta / (1 + uB * beta)
    return mpf(1) / 4 + mpf(3) / 4 * (bB + lamB / 2), lamB, bB
betaB = findroot(lambda x: entry_of(x)[0] - mpf('0.522757'), 0.3)
EB, lamB, bB = entry_of(betaB)
MB = (1 + uB) / (2 + uB)
print("B: beta =", betaB, " lambda =", lamB, " M =", MB, " E =", EB, " O_H =", mpf(1)/8 + 3*(bB+lamB)/8)
# ceiling at M_B
rCB = (10 * MB - 6 + sqrt((10 * MB - 6)**2 + MB * (mpf(3) / 4 - MB))) / MB
print("   r_C(M_B) =", rCB, " paper M = e/(1+e) =", e / (1 + e))
print("   margin at 18/5:", float(F(4245, 5804)), "-", MB, "=", mpf(4245) / 5804 - MB)
