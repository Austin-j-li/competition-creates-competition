from model import *
A = Prim(h=10, l=1, p=0.5, rho=0.5, cH=4.5, k=0.5, beta=0.2, lbar=0.4, a=0.01)
P = A
print("=== the referee COUNTEREXAMPLE ===")
print("lamS =", lamS(P), " lbar =", P.lbar)
Dcap = Dstar(P, P.lbar); DN = 2*P.k/P.rho
print(f"Delta_cap={Dcap:.6f} Delta_N={DN:.6f}  r_cap={fr(P,Dcap):.6f} r_N={fr(P,DN):.6f}")
psi = lambda r: lam_star(P, Delta(P, r)) - lamE(P, tau(P, r))
print("psi(r) = lam*(Delta) - lamE(tau) on a grid:")
for r in [3.5, 4.0, 4.5, 5.0, 5.5, 5.83, 6.0, 6.5, 7.0, 7.28, 7.5, 8.0, 9.0]:
    D = Delta(P, r); ls = lam_star(P, D); tu = tau(P, r)
    print(f"  r={r:.3f} D={D:.4f} tau={tu:.5f} lamE={lamE(P,tu):.5f} lam*={ls:.5f} psi={ls-lamE(P,tu):+.5f} phi_a={J(P,r)-P.k-2*P.a*lamE(P,tu):+.5f}")
rR = bisect(psi, 3.5, 5.0)
print(f"r_R = {rR:.6f}")
print("branch across r_N: r, regime, lam*, t, sigma_L(-1), entry, equilibrium check")
for r in [5.0, 5.5, 5.8284, 5.9, 6.2, 6.5, 6.8, 7.0, 7.2, 7.28]:
    D = Delta(P, r); ls = lam_star(P, D); t = sale_rate(P, D, ls)
    regime = 'R' if P.rho*D/2 <= P.k else ('RF' if t >= ls else 'RQ')
    ok, ent = check_eq(P, r, ls, {1:1.0}, {-1:t/ls, 0:1-t/ls} if ls>0 else {0:1.0}, verbose=False)
    print(f"  r={r:.4f} {regime:2s} lam*={ls:.6f} t={t:.6f} sigL(-1)={t/ls:.4f} entry={entry(P,ls):.6f} (recomputed {ent:.6f}) eq_ok={ok} recruit={tau(P,r)<=M_of(P,ls)}")
print("detailed checks at r=6.5 (RQ) and r=5.5 (R):")
for r in [5.5, 6.5, 7.2]:
    D = Delta(P, r); ls = lam_star(P, D); t = sale_rate(P, D, ls)
    check_eq(P, r, ls, {1:1.0}, {-1:t/ls, 0:1-t/ls}, label=f'branch r={r}')
# beyond the cap: capped branch, recruit until tau = M_lbar
rC = bisect(lambda r: tau(P, r) - M_of(P, P.lbar), 7.3, 9.9)
print(f"ceiling at the cap r_C = {rC:.6f} (M_lbar={M_of(P,P.lbar):.5f}); h = {P.h}")
print("non-recruiting branch beyond r_N:")
for r in [5.9, 6.5, 7.0, 7.28, 8.0, 9.0]:
    D = Delta(P, r); lq = lamQ(P, D); lqc = min(lq, P.lbar)
    print(f"  r={r:.3f} lamQ={lq:.5f} M={M_of(P,lqc):.5f} tau={tau(P,r):.5f} exists={tau(P,r)>M_of(P,lqc)}")
