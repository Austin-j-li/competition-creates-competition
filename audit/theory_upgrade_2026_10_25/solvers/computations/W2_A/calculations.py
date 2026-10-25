from decimal import Decimal, getcontext

getcontext().prec = 60
D = Decimal


def root(function, lo, hi):
    lo, hi = D(lo), D(hi)
    for _ in range(220):
        mid = (lo + hi) / 2
        if function(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def pointmass(r, c_H, rho, k, beta, a, cap, h='10', ell='1', p='.5'):
    r, c_H, rho, k, beta, a, cap, h, ell, p = map(D, (r, c_H, rho, k, beta, a, cap, h, ell, p))

    def gross(v):
        if v <= r:
            return (v*v - p*p) / (2*r)
        return v - r/2 - p*p/(2*r)

    g_H, g_L = gross(h), gross(ell)
    gamma = g_H - g_L
    delta = h - ell - gamma
    tau = (c_H-g_L)/gamma
    m = lambda x: beta*(1-x)/(2*beta+(1-2*beta)*x)
    lam = root(lambda x: 2*a*x+k-delta*m(x), '0', '1')
    lam_E = beta*(2*tau-1)/(beta+(1-2*beta)*(1-tau))
    e_H = rho + (1-rho)*(beta+(1-beta)*lam)
    e_L = rho + (1-rho)*beta*(1-lam)
    entry = (e_H+e_L)/2
    W_H, W_L = min(D(1),h/r), min(D(1),ell/r)
    O_H, O_L = W_H*e_H/2, W_L*e_L/2
    O_Z = rho*W_H/2
    delta_slope = (1-ell*ell/(r*r))/2 if r<h else (h*h-ell*ell)/(2*r*r)
    posterior_denom = 2*beta+(1-2*beta)*lam
    lam_slope = m(lam)*delta_slope/(2*a+delta*beta/(posterior_denom*posterior_denom))
    entry_log_slope = (1-rho)*(1-beta)*lam_slope/e_H
    win_log_loss = D(0) if r<h else 1/r
    values = dict(r=r, delta=delta, gamma=gamma, tau=tau, lam=lam, lam_E=lam_E,
                  recruitment_margin=1-m(lam)-tau, no_sale_margin=k-rho*delta/2,
                  cap_margin=cap-lam, e_H=e_H, e_L=e_L, entry=entry,
                  W_H=W_H, O_H=O_H, O_L=O_L, O_Z=O_Z, ownership_ratio=O_H/O_Z,
                  ownership_gain=O_H-O_Z, H_share_entrants=e_H/(e_H+e_L),
                  H_share_challenger_winners=O_H/(O_H+O_L),
                  research_cost=a*lam*lam/2, lam_slope=lam_slope,
                  H_entry_log_slope=entry_log_slope, H_win_log_loss=win_log_loss,
                  ownership_log_slope=entry_log_slope-win_log_loss)
    return values


def show(label, rows):
    print(label)
    for row in rows:
        print(' '.join(f'{key}={value:.12f}' for key, value in row.items()))


beta_B = D('.294655')
cap_B = ((D(1).exp()-1)*beta_B)/(1+(D(1).exp()-1)*beta_B)
benchmark = [pointmass(r,'6','.25','.02',beta_B,'.025',cap_B) for r in ('1.55','1.6','1.65')]
show('BENCHMARK', benchmark)
print('benchmark cap', cap_B)
print('benchmark h-r_max', D(10)-D('3.6'))
print('benchmark branch r_cap', root(lambda r: pointmass(r,'6','.25','.02',beta_B,'.025',cap_B)['lam']-cap_B,'1.65','1.75'))
counter = [pointmass(r,'2.5','.05','.2','.2','5','.9') for r in ('11','11.5','12')]
show('KNOWN COUNTEREXAMPLE', counter)
print('counterexample r=11 to r=12 proportional changes')
for key in ('lam','entry','e_H','W_H','O_H','ownership_ratio','ownership_gain'):
    print(key, counter[-1][key]/counter[0][key]-1)
show('HIGH CLASS CAN LOSE WHILE OWNERSHIP RISES', [pointmass(r,'2.4','.05','2','.2','.025','.9') for r in ('11','11.1')])


def from_auction(delta, gamma, g_L, W_H, W_L, c_H, rho, k, beta, a):
    delta, gamma, g_L, W_H, W_L, c_H, rho, k, beta, a = map(D,(delta,gamma,g_L,W_H,W_L,c_H,rho,k,beta,a))
    tau = (c_H-g_L)/gamma
    m = lambda lam: beta*(1-lam)/(2*beta+(1-2*beta)*lam)
    lam = root(lambda lam: 2*a*lam+k-delta*m(lam),'0','1')
    e_H = rho+(1-rho)*(beta+(1-beta)*lam)
    e_L = rho+(1-rho)*beta*(1-lam)
    O_H, O_L = W_H*e_H/2,W_L*e_L/2
    return dict(delta=delta,tau=tau,lam=lam,recruitment_margin=1-m(lam)-tau,
                no_sale_margin=k-rho*delta/2,W_H=W_H,W_L=W_L,O_H=O_H,
                H_share_challenger_winners=O_H/(O_H+O_L),
                H_share_entrants=e_H/(e_H+e_L))


show('WINNER SHARE DOES NOT GENERALIZE', [
    from_auction('4.4','4.6','.1875','1','.5','2.7','.05','.2','.2','5'),
    from_auction('4.5','4.5','.1875','.5','.5','2.7','.05','.2','.2','5')
])
show('CONSTANT W_H BELOW ONE', [
    from_auction('.95','3.55','0','.5','0','2','.25','.2','.2','1'),
    from_auction('1','3.5','0','.5','0','2','.25','.2','.2','1')
])

print('COUNTEREXAMPLE WHOLE-INTERVAL BOUNDS')
print('purchase posterior minus threshold lower bound', 1-D('.2')*(1-counter[0]['lam'])/(D('.4')+D('.6')*counter[0]['lam'])-counter[-1]['tau'])
print('H entry log slope upper bound', D('.76')*D('.5')*(D('49.5')/D(11)**2)/(D(10)*D('.24')))
print('H win log loss lower bound', 1/D(12))
print('BENCHMARK MEAN VALUE AMONG PREPARED CHALLENGERS')
for row in benchmark:
    print(row['r'],1+9*row['H_share_entrants'])
