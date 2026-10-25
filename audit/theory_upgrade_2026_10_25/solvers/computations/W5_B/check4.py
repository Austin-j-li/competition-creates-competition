from mpmath import mp, mpf, e as E, findroot
mp.dps = 30
exec(open('audit/theory_upgrade_2026_10_25/solvers/computations/W5_B/check1.py').read().split("for pi in")[0])
# Raw-test bias without recruitment, relative to I- and to the class component, and vs the recruitment term at r1
print("prior  r     (I+-I-)/I-   (I+-I-)/classcomp   noRec/(rec term at r1=3)")
for pi in [mpf('0.2'), mpf('0.3'), mpf('0.4'), mpf('0.4679'), mpf('0.49'), mpf('0.6'), mpf('0.8')]:
    for r in [mpf('3.9'), mpf(6)]:
        s = full(pi, r); a = s['a']; M, m = s['M'], s['m']
        noRec = rho*a['D']*((M-pi)-(pi-m))
        cc = rho*a['D']*(M-m)
        s1 = full(pi, mpf(3)); rec1 = (1-rho)*s1['A'](s1['M'])
        print(f"{float(pi):.4f} {float(r):.1f}  {float(noRec/s['Im']):+.4f}      {float(noRec/cc):+.4f}            {float(noRec/rec1):+.5f}")
# Where does full trade hold at prior pi in the benchmark auction (rho*kappa(pi)*Delta > k)?
def D(r): return (r-1)**2/(2*r)
print("\nfull-trade lower end r_S(pi) (rho*kappa*Delta=k) and ceiling r_C(pi) (tau=M):")
for pi in [mpf('0.3'), mpf('0.4'), mpf('0.4679'), mpf('0.5'), mpf('0.6')]:
    kap = min(mf(pi), 1-Mf(pi))
    rS = findroot(lambda r: rho*kap*D(r)-k, 2.5)
    try:
        rC = findroot(lambda r: auction(r)['tau']-Mf(pi), 3.5)
    except Exception as ex:
        rC = None
    print(f"pi={float(pi)}: kappa={float(kap):.4f} r_S={float(rS):.4f}  r_C={float(rC) if rC is not None else None}")
# tau on (1,h) and margin B_r(1/2) < c_H
for r in [mpf('1.0001'), mpf('1.2'), mpf(3), mpf('3.6'), mpf('9.99')]:
    a = auction(r); print(f"r={float(r)} tau={float(a['tau']):.4f} c_H - B_r(1/2) = {float(cH-(a['gH']+a['gL'])/2):.4f}")
