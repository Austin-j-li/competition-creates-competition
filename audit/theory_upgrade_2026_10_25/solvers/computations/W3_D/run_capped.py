from model import *
E = Prim(h=10, l=1, p=0.5, rho=0.5, cH=5, k=0.02, beta=0.294655, lbar=0.336122, a=0.1)
B = Prim(h=10, l=1, p=0.5, rho=0.25, cH=6, k=0.02, beta=0.294655, lbar=0.336122, a=1/40)
A = Prim(h=10, l=1, p=0.5, rho=0.5, cH=4.5, k=0.5, beta=0.2, lbar=0.4, a=0.01)
print("=== capped recruiting branch, RF economy (cap reached inside full-sale regime) ===")
for r in [2.05, 2.1, 3.0, 4.0, 6.3, 6.4]:
    P = E; D = Delta(P, r); t = sale_rate(P, D, P.lbar)
    print(f"  regime at cap: t={t:.5f} lbar={P.lbar}  rho*D*m_lbar-k={P.rho*D*m_of(P,P.lbar)-P.k:+.5f}")
    check_eq(P, r, P.lbar, {1:1.0}, {-1:t/P.lbar, 0:1-t/P.lbar}, label=f'RF econ capped r={r}')
print("=== benchmark capped branch just past r_N (L barely mixes) and at r_N- ===")
for r in [1.745, 1.76, 2.12, 2.13]:
    P = B; D = Delta(P, r); t = sale_rate(P, D, P.lbar)
    check_eq(P, r, P.lbar, {1:1.0}, {-1:t/P.lbar, 0:1-t/P.lbar}, label=f'bench capped r={r}')
print("=== rule I0 in the referee economy beyond r_N: non-recruiting branch only? ===")
for r in [5.9, 6.5, 7.28, 8.0]:
    P = A; D = Delta(P, r); lq = lamQ(P, D)
    check_eq(P, r, min(lq, P.lbar), {1:1.0}, {-1:1.0}, label=f'the referee non-recruiting r={r}')
print("the referee: at the cap, L sells fully only when rho*D*m_lbar >= k, i.e. D >=", A.k/(A.rho*m_of(A,A.lbar)), " r >=", fr(A, A.k/(A.rho*m_of(A,A.lbar))), " (> h=10)")
print("=== rho margin in the benchmark slot for the cap-before-selling condition ===")
P = B; mlb = m_of(P, P.lbar)
print("  rho_max = 2k m_lbar/(2a lbar + k) =", 2*P.k*mlb/(2*P.a*P.lbar + P.k), " rho =", P.rho)
print("  2a lbar / k: benchmark", 2*B.a*B.lbar/B.k, " the referee", 2*A.a*A.lbar/A.k, "; 2 m_lbar: benchmark", 2*mlb, " the referee", 2*m_of(A, A.lbar))
# first-order two-parameter example for J' > 0 but phi_a' < 0 at r = 1.6 benchmark
P = B; r = 1.6; h = 1e-6
Jp = (J(P, r+h)-J(P, r-h))/(2*h); taup = (tau(P, r+h)-tau(P, r-h))/(2*h)
lEp = P.beta/(P.beta + (1-2*P.beta)*(1-tau(P,r)))**2
D = Delta(P, r); g = gamma(P, r); y0 = 0.75
dtau_eps = (y0 - P.p)/g   # d tau per unit mass moved from below p to y0
print("=== first-order two-parameter check at r=1.6 ===")
print(f"  J'={Jp:.5f} tau'={taup:.5f} lamE'={lEp:.4f} Delta={D:.5f} gamma={g:.4f} dtau/deps={dtau_eps:.5f}")
for eps, dr in [(0.1, 0.004), (0.1, 0.0035), (0.1, 0.005)]:
    dJ = Jp*dr - D*dtau_eps*eps
    dphi = dJ - 2*P.a*lEp*(taup*dr + dtau_eps*eps)
    print(f"  eps={eps} dr={dr}: dJ={dJ:+.6f} dphi_a={dphi:+.6f}")
