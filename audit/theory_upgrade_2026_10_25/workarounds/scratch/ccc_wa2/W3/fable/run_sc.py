from model import *
B = Prim(h=10, l=1, p=0.5, rho=0.25, cH=6, k=0.02, beta=0.294655, lbar=0.336122, a=1/40)
P = B
# single crossing: a_mono(path) = inf J'(r) [beta+(1-2beta)(1-tau)]^2 /(2 beta tau'(r))
def Jp(r, h=1e-6): return (J(P, r+h) - J(P, r-h))/(2*h)
def taup(r, h=1e-6): return (tau(P, r+h) - tau(P, r-h))/(2*h)
def lamEp(t): return P.beta/(P.beta + (1-2*P.beta)*(1-t))**2
print("=== SINGLE CROSSING, BENCHMARK ===")
grid = [1.2 + i*0.005 for i in range(0, 481)]  # r in [1.2, 3.6]
vals = [(r, Jp(r)/(2*lamEp(tau(P,r))*taup(r))) for r in grid]
for lo, hi in [(1.2, 1.75), (1.2, 1.7479), (1.2, 2.0), (1.2, 3.6)]:
    sub = [v for r, v in vals if lo <= r <= hi]
    print(f"  inf over [{lo},{hi}] of J'/(2 lamE' tau') = {min(sub):.6f}  (paper a_mono on [r0,7/4] = 0.161713; a = 0.025)")
print("  crude bound (beta/2) inf dJ/dtau on [1.2,1.75]:", min(P.beta/2*Jp(r)/taup(r) for r in grid if r <= 1.75))
print("  J'(r) at r0, r_R, 7/4:", Jp(1.2), Jp(1.501023), Jp(1.75), " tau'(r):", taup(1.2), taup(1.501023), taup(1.75))
print("  dJ/dtau at r0, 7/4:", Jp(1.2)/taup(1.2), Jp(1.75)/taup(1.75))
# phi_a sign changes for various a on [1.2, 3.6]
for a in [0.025, 0.1, 0.16, 0.2, 0.3, 0.5, 1.0]:
    Q = Prim(**{**B.__dict__, 'a': a})
    phi = [J(Q, r) - Q.k - 2*a*lamE(Q, tau(Q, r)) for r in grid]
    changes = sum(1 for i in range(1, len(phi)) if (phi[i] > 0) != (phi[i-1] > 0))
    print(f"  a={a}: sign changes of phi_a on [1.2,3.6] = {changes}; phi_a(1.2)={phi[0]:+.4f} phi_a(3.6)={phi[-1]:+.4f}; min phi_a' approx {min((phi[i]-phi[i-1])/0.005 for i in range(1,len(phi))):+.4f}")
# elasticity version: eps_Delta,tau vs eps_DeltaE,tau along the path
def DE(t): return (P.k + 2*P.a*lamE(P,t))/(1-t)
print("elasticity check at a few r: eps(Delta) vs eps(Delta_E), both w.r.t. tau along the path")
for r in [1.25, 1.4, 1.5, 1.6, 1.7]:
    t = tau(P,r); h=1e-6
    epsD = (math.log(Delta(P,r+h))-math.log(Delta(P,r-h)))/(math.log(tau(P,r+h))-math.log(tau(P,r-h)))
    epsE = (math.log(DE(t+1e-7))-math.log(DE(t-1e-7)))/(math.log(t+1e-7)-math.log(t-1e-7))
    print(f"  r={r}: eps_Delta={epsD:.3f} eps_DeltaE={epsE:.3f}  (a=0 part tau/(1-tau)={t/(1-t):.3f})")
