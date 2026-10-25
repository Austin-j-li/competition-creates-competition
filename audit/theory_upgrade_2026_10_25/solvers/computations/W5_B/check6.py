from mpmath import mp, mpf, e as E
mp.dps = 30
exec(open('audit/theory_upgrade_2026_10_25/solvers/computations/W5_B/check1.py').read().split("for pi in")[0])
# Covariances under full trade at general prior (point-mass benchmark: W_H=1, W_L=ell/r)
for pi, r in [(mpf('0.5'), mpf(3)), (mpf('0.6'), mpf('3.6')), (mpf('0.4'), mpf('3.9')), (mpf('0.5'), mpf('3.9'))]:
    s = full(pi, r); a = s['a']; Pr = s['Pr']; mu = {-1: s['m'], 0: pi, 1: s['M']}
    e = {x: s['ent'](mu[x]) for x in mu}
    WH, WL = mpf(1), 1/r
    EX = Pr[1]-Pr[-1]
    covA = sum(Pr[x]*x*e[x] for x in Pr) - EX*sum(Pr[x]*e[x] for x in Pr)
    wx = {x: e[x]*(mu[x]*WH+(1-mu[x])*WL) for x in mu}
    covW = sum(Pr[x]*x*wx[x] for x in Pr) - EX*sum(Pr[x]*wx[x] for x in Pr)
    chi = s['chi']
    print(f"pi={float(pi)} r={float(r)} chi={chi}: covA={float(covA):.6f} formula={(float((1-rho)*chi*Pr[1]*(1-EX))):.6f} | "
          f"covW={float(covW):.6f}" + (f" formula(no rec)={float(2*rho*pi*(1-pi)*lam*(WH-WL)):.6f}" if chi==0 else ""))
# same-counts family at pi0=0.6, r=3: the weighted sale impact differs across members
pi0 = mpf('0.6'); r = mpf(3); s = full(pi0, r); EX = s['Pr'][1]-s['Pr'][-1]; v = s['Pr'][1]+s['Pr'][-1]; a = auction(r)
print("\nfamily: f_- I_- = rho*Delta*pi'(1-pi')lam'  (data generated at pi0=0.6)")
for pip in [mpf('0.56'), mpf('0.58'), mpf('0.6'), mpf('0.62'), mpf('0.65')]:
    lp = EX/(2*pip-1); print(f" pi'={float(pip)} lam'={float(lp):.4f} f-I- = {float(rho*a['D']*pip*(1-pip)*lp):.5f}  (I- itself = {float(rho*a['D']*pip*(1-pip)*lp/s['Pr'][-1]):.5f})")
print("share of benchmark prior band below 1/2:", (0.5-0.467850)/(0.500424-0.467850))
# raw test sufficient condition check: rho<=1/2 => recruitment implies I+>I-; try rho=0.9 with tiny wL to break it
