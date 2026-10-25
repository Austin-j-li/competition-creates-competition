from mpmath import mp, mpf, e as E
mp.dps = 30
exec(open('audit/theory_upgrade_2026_10_25/solvers/computations/W5_B/check1.py').read().split("for pi in")[0])
# (1) purchases-only pattern (sigma_H = delta_1, sigma_L = delta_0) WITHOUT recruitment: weighted test / no-order return
print("purchases-only, no recruitment (form Q-like): P0 - Pbar should be nonzero")
for pi, r in [(mpf('0.5'), mpf('6')), (mpf('0.4'), mpf('3.6'))]:
    a = auction(r)
    fH = {-1: b, 0: b0, 1: b+lam}; fL = {-1: b, 0: b0+lam, 1: b}
    Pr = {x: pi*fH[x]+(1-pi)*fL[x] for x in fH}
    mu = {x: pi*fH[x]/Pr[x] for x in fH}
    ent = {x: (1 if mu[x] >= a['tau'] else rho) for x in mu}
    P = {x: a['t0'] + ent[x]*(a['wL']+a['D']*mu[x]) for x in mu}
    Pbar = sum(Pr[x]*P[x] for x in Pr)
    print(f" pi={float(pi)} r={float(r)} mu={[round(float(mu[x]),4) for x in (-1,0,1)]} tau={float(a['tau']):.4f} entry={[ent[x] for x in (-1,0,1)]} "
          f"Pbar-P0={float(Pbar-P[0]):+.5f}  rho*Delta*(pi-mu0)={float(rho*a['D']*(pi-mu[0])):+.5f}")
# (4) unknown-prior family with the same counts: data generated at (pi0, lam, beta); members (pi', lam') with lam'(2pi'-1)=EX, 2b'+lam'=v
print("\nfamily with same counts as data at pi0=0.6, r=3 (tau(3)=0.7050):")
pi0 = mpf('0.6'); s = full(pi0, mpf(3)); EX = s['Pr'][1]-s['Pr'][-1]; v = s['Pr'][1]+s['Pr'][-1]
tau3 = auction(mpf(3))['tau']; tau36 = auction(mpf('3.6'))['tau']
for pip in [mpf('0.56'), mpf('0.58'), mpf('0.6'), mpf('0.65'), mpf('0.7'), mpf('0.8'), mpf('0.95')]:
    lp = EX/(2*pip-1)
    if not (0 < lp < v): print(f" pi'={float(pip)}: lam'={float(lp):.4f} infeasible (needs 0<lam'<v={float(v):.4f})"); continue
    bp = (v-lp)/2; betap = bp/(1-lp); up = lp/bp
    Mp = pip*(1+up)/(pip*(1+up)+1-pip); mp_ = pip/(pip+(1-pip)*(1+up))
    print(f" pi'={float(pip)}: lam'={float(lp):.4f} beta'={float(betap):.4f} (<=1/3: {betap<=mpf(1)/3}) M'={float(Mp):.4f} recruits@3: {Mp>=tau3}  recruits@3.6: {Mp>=tau36}  m'={float(mp_):.4f}")
