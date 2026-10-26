from model import *
# Example with full-sale regime before the cap: benchmark auction with c_H=5, rho=1/2, a=1/10, benchmark slot
E = Prim(h=10, l=1, p=0.5, rho=0.5, cH=5, k=0.02, beta=0.294655, lbar=0.336122, a=0.1)
P = E
print("=== RF EXAMPLE (c_H=5, rho=1/2, a=1/10, benchmark slot) ===")
print("lamS =", lamS(P), " lbar =", P.lbar)
DN = 2*P.k/P.rho; DS = Dstar(P, lamS(P)); Dcap = Dstar(P, P.lbar)
print(f"Delta_N={DN:.6f} (r_N={fr(P,DN):.6f})  Delta_S={DS:.6f} (r_S^R={fr(P,DS):.6f})  Delta_cap={Dcap:.6f} (r_cap={fr(P,Dcap):.6f})")
print("check continuity at Delta_S: Lam =", Lam(P, DS), " LamF =", LamF(P, DS), " lamS =", lamS(P))
psi = lambda r: lam_star(P, Delta(P, r)) - lamE(P, tau(P, r))
rR = bisect(psi, 1.05, 1.6)
print(f"r_R = {rR:.6f}; psi on grid:")
for r in [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.8, 2.0, 2.04, 2.1, 2.5, 3.0]:
    D = Delta(P, r); ls = lam_star(P, D); tu = tau(P, r)
    print(f"  r={r:.3f} D={D:.4f} tau={tu:.5f} lamE={lamE(P,tu):.5f} lam*={ls:.5f} psi={ls-lamE(P,tu):+.5f}")
print("branch through three regimes: r, regime, lam*, slope dlam/dD (numeric), t, entry, eq check")
prev = None
for r in [1.35, 1.45, 1.49, 1.50, 1.52, 1.53, 1.55, 1.6, 1.7, 1.8, 1.9, 2.0, 2.04]:
    D = Delta(P, r); ls = lam_star(P, D); t = sale_rate(P, D, ls)
    regime = 'R' if P.rho*D/2 <= P.k else ('RF' if t >= ls - 1e-12 else 'RQ')
    h = 1e-6; slope = (lam_star(P, D+h) - lam_star(P, D-h))/(2*h)
    sig = {-1:t/ls, 0:1-t/ls}
    ok, ent = check_eq(P, r, ls, {1:1.0}, sig, verbose=False)
    print(f"  r={r:.3f} {regime:2s} D={D:.5f} lam*={ls:.6f} dlam/dD={slope:.4f} t={t:.5f} sigL(-1)={t/ls:.4f} entry={entry(P,ls):.6f} eq_ok={ok} recruit={tau(P,r)<=M_of(P,ls)} UL(-1)={P.rho*D*((1-ls)*P.beta/(2*(1-ls)*P.beta+t))-P.k:+.6f}")
print("analytic slopes at Delta_S from both sides:")
lam = lamS(P); m = m_of(P, lam); mp = mprime(P, lam)
print("  R side:", m/(2*P.a - DS*mp), "  RF side:", (1+P.rho)*m/(2*P.a - (1+P.rho)*DS*mp))
for r in [1.45, 1.52, 1.8]:
    D = Delta(P, r); ls = lam_star(P, D); t = sale_rate(P, D, ls)
    check_eq(P, r, ls, {1:1.0}, {-1:t/ls, 0:1-t/ls}, label=f'r={r}')
# capped branch beyond r_cap and ceiling
rC = bisect(lambda r: tau(P, r) - M_of(P, P.lbar), 2.0, 9.9)
print(f"ceiling r_C = {rC:.6f}, M_lbar = {M_of(P,P.lbar):.5f}")
