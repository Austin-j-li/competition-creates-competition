from model import *
# Benchmark
B = Prim(h=10, l=1, p=0.5, rho=0.25, cH=6, k=0.02, beta=0.294655, lbar=0.336122, a=1/40)
P = B
print("=== BENCHMARK ===")
print("lamS =", lamS(P), " lbar =", P.lbar, " -> full-sale regime reached before cap?", lamS(P) < P.lbar)
Dcap = Dstar(P, P.lbar); DN = 2*P.k/P.rho
print(f"Delta_cap={Dcap:.6f} Delta_N={DN:.6f}  r_cap={fr(P,Dcap):.6f} r_N={fr(P,DN):.6f}")
mlb = m_of(P, P.lbar)
print(f"m_lbar={mlb:.6f}  condition rho(2a lbar+k) <= 2k m_lbar: {P.rho*(2*P.a*P.lbar+P.k):.6f} <= {2*P.k*mlb:.6f}  margin={2*P.k*mlb-P.rho*(2*P.a*P.lbar+P.k):.6f}")
aN = P.k*(2*mlb - P.rho)/(2*P.rho*P.lbar)
print(f"a_N (max a with cap before selling) = {aN:.6f}; a = {P.a}; ratio a/a_N = {P.a/aN:.4f}")
# start r_R: psi(r) = lam*(Delta(r)) - lamE(tau(r)) crosses 0
psi = lambda r: lam_star(P, Delta(P, r)) - lamE(P, tau(P, r))
rR = bisect(psi, 1.2, 1.75)
print(f"r_R = {rR:.6f}  (paper 1.501023); lam at r_R = {lam_star(P, Delta(P, rR)):.6f} (paper 0.193853)")
# sale regime at the cap beyond r_N
rS_cap = fr(P, P.k/(P.rho*mlb))
print(f"r where L sells fully at the cap: r_S^cap = {rS_cap:.6f}; r_U(paper)=2.434046, r_C(paper)=3.592659")
print("capped recruiting branch beyond r_N: r, t (informed sale prob), sigma_L(-1), V vs a*lbar, tau vs M_lbar")
for r in [1.70, 1.7479, 1.8, 1.9, 2.0, 2.124, 2.3, 2.434, 3.0, 3.59, 3.6]:
    D = Delta(P, r); t = sale_rate(P, D, P.lbar)
    bh = (1-P.lbar)*P.beta
    mu_minus = bh/(2*bh+t)
    UL = P.rho*D*mu_minus - P.k
    V = 0.5*(D*mlb - P.k) + 0.5*max(UL, 0)
    print(f"  r={r:.4f} D={D:.5f} t={t:.5f} sigL(-1)={t/P.lbar:.4f} V={V:.6f} a*lbar={P.a*P.lbar:.6f} tau={tau(P,r):.5f} M_lbar={M_of(P,P.lbar):.5f} recruit={tau(P,r)<=M_of(P,P.lbar)}")
# non-recruiting research branch beyond r_N: lamQ, M_{lamQ} vs tau
print("non-recruiting research branch (H buys, L sells, e=rho): r, lamQ, capped?, M_{lamQ^c}, tau, exists?")
for r in [1.75, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.434, 2.5]:
    D = Delta(P, r); lq = lamQ(P, D); lqc = min(lq, P.lbar)
    U = P.rho*D*m_of(P, P.lbar) - P.k - P.a*P.lbar
    print(f"  r={r:.4f} lamQ={lq:.5f} capped={lq>=P.lbar} U={U:+.5f} M={M_of(P,lqc):.5f} tau={tau(P,r):.5f} exists={tau(P,r)>M_of(P,lqc)}")
rX = bisect(lambda r: tau(P, r) - M_of(P, min(lamQ(P, Delta(P, r)), P.lbar)), 1.76, 2.6)
print(f"r_X (non-recruiting branch dies, tau = M_lamQ) = {rX:.6f}")
rU = bisect(lambda r: P.rho*Delta(P,r)*m_of(P,P.lbar) - P.k - P.a*P.lbar, 1.8, 3.5)
print(f"r_U recomputed = {rU:.6f}")
# full equilibrium checks at r = 2 (both), r = 1.9, 2.3
for r in [1.9, 2.0, 2.3]:
    D = Delta(P, r); t = sale_rate(P, D, P.lbar)
    check_eq(P, r, P.lbar, {1:1.0}, {-1:t/P.lbar, 0:1-t/P.lbar}, label='capped recruiting, L mixes')
    lq = lamQ(P, D)
    check_eq(P, r, min(lq,P.lbar), {1:1.0}, {-1:1.0}, label='non-recruiting interior research')
