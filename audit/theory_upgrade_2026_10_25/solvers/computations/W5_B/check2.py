import sys; sys.path.insert(0, 'audit/theory_upgrade_2026_10_25/solvers/computations/W5_B')
from mpmath import mp, mpf, sqrt
exec(open('audit/theory_upgrade_2026_10_25/solvers/computations/W5_B/check1.py').read().split("for pi in")[0])
# Identification from counts + sale impact, given rho*Delta
print("--- identification: lam = 2Q + sqrt(4Q^2 + EX^2), Q = Pr(-1) I- /(rho Delta) ---")
for pi in [mpf('0.3'), mpf('0.45'), mpf('0.5'), mpf('0.62')]:
    for r in [mpf('3'), mpf('3.6'), mpf('5')]:
        s = full(pi, r); a = s['a']
        EX = s['Pr'][1]-s['Pr'][-1]; v = s['Pr'][1]+s['Pr'][-1]
        Q = s['Pr'][-1]*s['Im']/(rho*a['D'])
        lam_hat = 2*Q + sqrt(4*Q**2 + EX**2)
        pi_hat = (1 + EX/lam_hat)/2
        b_hat = (v - lam_hat)/2
        beta_hat = b_hat/(1-lam_hat)
        # entry component recovered from prices and counts only
        EC = s['Ip'] - s['Pr'][-1]/s['Pr'][1]*s['Im']
        print(f"pi={float(pi)} r={float(r)}: lam_hat-lam={float(lam_hat-lam):.1e} pi_hat-pi={float(pi_hat-pi):.1e} "
              f"beta_hat-beta={float(beta_hat-beta):.1e}  Q-pi(1-pi)lam={float(Q-pi*(1-pi)*lam):.1e}  "
              f"EC={float(EC):.5f} (1-rho)chiA(M)={float((1-rho)*s['chi']*s['A'](s['M'])):.5f}  EX/v={float(EX/v):.5f} theta(2pi-1)={float(u/(2+u)*(2*pi-1)):.5f}")
# Known prior != 1/2: counts give slot, prices give rho*Delta
print("--- known prior: counts -> slot, sale impact -> rho*Delta ---")
for pi in [mpf('0.3'), mpf('0.45'), mpf('0.62')]:
    r = mpf('3.6'); s = full(pi, r); a = s['a']
    EX = s['Pr'][1]-s['Pr'][-1]; v = s['Pr'][1]+s['Pr'][-1]
    lam_c = EX/(2*pi-1); b_c = (v-lam_c)/2
    rhoD = s['Pr'][-1]*s['Im']/(pi*(1-pi)*lam_c)
    print(f"pi={float(pi)}: lam err {float(lam_c-lam):.1e}, b err {float(b_c-b):.1e}, rhoDelta err {float(rhoD-rho*a['D']):.1e}; "
          f"d lam / d EX = {float(1/(2*pi-1)):.2f}")
# Case pi >= tau: zero order recruits, sale deters
print("--- prior above threshold (sale deters) ---")
for pi, r in [(mpf('0.75'), mpf('3')), (mpf('0.8'), mpf('3.6'))]:
    s = full(pi, r); a = s['a']
    w = s['Pr'][1]*s['Ip'] - s['Pr'][-1]*s['Im']
    pred = -s['Pr'][-1]*(1-rho)*s['A'](s['m'])
    print(f"pi={float(pi)} r={float(r)} tau={float(a['tau']):.4f} m={float(s['m']):.4f} e=({s['ent'](s['m'])},{s['ent'](pi)},{s['ent'](s['M'])}) "
          f"wtest={float(w):+.5f} pred={float(pred):+.5f} Pbar-P0={float(s['Pbar']-s['P'][0]):+.5f} KH-k={float(s['KH']-k):+.4f} KL-k={float(s['KL']-k):+.4f}")
