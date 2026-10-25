import math, sys
sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W3_B')
from model import *

u = math.e - 1
beta = 0.294655
lbar = u*beta/(1+u*beta)
B = Par(h=10, ell=1, p=0.5, cH=6, k=0.02, rho=0.25, beta=beta, a=1/40, lbar=lbar)
print("benchmark lbar", lbar, "m_lbar", m_of(lbar,B), "1/(1+e)", 1/(1+math.e))
for r in (1.55, 1.60, 1.65):
    A = auction(B, r)
    print(r, "Delta %.6f tau %.6f lamE %.6f lamR %.6f entry %.6f" % (A['Delta'], A['tau'], lamE_of(A['tau'],B), Lam_R(A['Delta'],B), entry_branch(Lam_R(A['Delta'],B),B)))
# r_R: phi_a = 0 on [1.2, 1.75]
rR = bisect(lambda r: phi_a(auction(B,r)['Delta'], auction(B,r)['tau'], B), 1.2, 1.75)
Dcap = (2*B.a*B.lbar + B.k)/m_of(B.lbar,B)
rcap = fr(Dcap, B)
rN = fr(2*B.k/B.rho, B)
print("r_R %.6f  rbar_R %.6f  r_N %.6f" % (rR, rcap, rN))
print("lamE(r_R) %.6f entry(r_R) %.6f entry_cap %.6f" % (lamE_of(auction(B,rR)['tau'],B), entry_branch(lamE_of(auction(B,rR)['tau'],B),B), entry_branch(lbar,B)))
# condition (ii): rho(2 a lbar + k) <= 2 k m_lbar
lhs = B.rho*(2*B.a*B.lbar + B.k); rhs = 2*B.k*m_of(B.lbar,B)
print("cond (ii): lhs %.6g rhs %.6g  margin %.6g ratio %.4f" % (lhs, rhs, rhs-lhs, lhs/rhs))
print("normalized: rho(1+2a lbar/k)(1+u_lbar/2) =", B.rho*(1+2*B.a*B.lbar/B.k)*(1+ (B.lbar/((1-B.lbar)*B.beta))/2))
# critical a for (ii) at benchmark, critical rho
acrit = (2*B.k*m_of(B.lbar,B)/B.rho - B.k)/(2*B.lbar)
rhocrit = 2*B.k*m_of(B.lbar,B)/(2*B.a*B.lbar + B.k)
print("critical a %.6f (bench a=0.025, A.2 window (0.021469, 0.036763)); critical rho %.6f" % (acrit, rhocrit))
# r_C ceiling: tau = M_lbar
rC = bisect(lambda r: auction(B,r)['tau'] - M_of(B.lbar,B), 2.0, 3.6)
print("r_C %.6f" % rC)

print("\n--- the referee counterexample ---")
X = Par(h=10, ell=1, p=0.5, cH=4.5, k=0.5, rho=0.5, beta=0.2, a=0.01, lbar=0.4)
print("m_lbar", m_of(X.lbar,X), "Delta_N", 2*X.k/X.rho, "Delta_cap", (2*X.a*X.lbar+X.k)/m_of(X.lbar,X))
print("r_N %.6f r_cap %.6f" % (fr(2*X.k/X.rho,X), fr((2*X.a*X.lbar+X.k)/m_of(X.lbar,X),X)))
for r in (4.0, 4.5, 5.0, 5.5, 5.828427, 6.0, 6.5, 7.0, 7.28, 7.3):
    A = auction(X, r)
    print("r %.4f Delta %.4f tau %.4f J %.4f phi_a %.5f phi* %.5f lamE %.4f" % (r, A['Delta'], A['tau'], A['J'], phi_a(A['Delta'],A['tau'],X), phi_star(A['Delta'],A['tau'],X), lamE_of(A['tau'],X)))
