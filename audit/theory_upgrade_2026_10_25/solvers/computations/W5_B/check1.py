from mpmath import mp, mpf, e as E, sqrt
mp.dps = 30
h, ell, p, rho, cH, k = mpf(10), mpf(1), mpf(1)/2, mpf(1)/4, mpf(6), mpf(1)/50
beta = mpf(294655)/10**6
u = E - 1
lam = u*beta/(1+u*beta)
b = (1-lam)*beta
b0 = (1-lam)*(1-2*beta)
print("lam", lam, "b", b, "u", u, "b0", b0)

def auction(r):
    t0 = p*(1-p/r); tH = r/2 + p**2/(2*r); tL = ell - (ell**2-p**2)/(2*r)
    gH = h - r/2 - p**2/(2*r); gL = (ell**2-p**2)/(2*r)
    D = tH - tL
    tau = (cH-gL)/(gH-gL)
    return dict(t0=t0,tH=tH,tL=tL,gH=gH,gL=gL,D=D,tau=tau,wL=tL-t0)

def Mf(pi): return pi*(1+u)/(pi*(1+u)+1-pi)
def mf(pi): return pi/(pi+(1-pi)*(1+u))

def full(pi, r):
    a = auction(r)
    M, m = Mf(pi), mf(pi)
    tau = a['tau']
    ent = lambda mu: 1 if mu >= tau else rho   # rule C1
    A = lambda mu: a['wL'] + a['D']*mu
    P = {x: a['t0'] + ent(mu)*A(mu) for x, mu in [(-1,m),(0,pi),(1,M)]}
    Pr = {1: b+pi*lam, -1: b+(1-pi)*lam, 0: b0}
    Ip = P[1]-P[0]; Im = P[0]-P[-1]
    Pbar = sum(Pr[x]*P[x] for x in Pr)
    chi = 1 if M >= tau else 0
    # trading incentives under full orders
    KH = ent(M)*a['D']*(1-M); KL = ent(m)*a['D']*m
    return dict(a=a,M=M,m=m,P=P,Pr=Pr,Ip=Ip,Im=Im,Pbar=Pbar,chi=chi,KH=KH,KL=KL,A=A,ent=ent)

for pi in [mpf('0.3'), mpf('0.4'), mpf('0.4679'), mpf('0.49'), mpf('0.5'), mpf('0.6'), mpf('0.7')]:
    for r in [mpf(3), mpf('3.4'), mpf('3.6'), mpf('3.9'), mpf(6)]:
        s = full(pi, r); a = s['a']; M, m = s['M'], s['m']
        noRec = rho*a['D']*((M-pi)-(pi-m))
        formula = pi*(1-pi)*u**2*(1-2*pi)/((1+pi*u)*(1+(1-pi)*u))
        rec = (1-rho)*s['chi']*s['A'](M)
        lhs = s['Ip']-s['Im']
        w = s['Pr'][1]*s['Ip'] - s['Pr'][-1]*s['Im']
        print(f"pi={float(pi):.4f} r={float(r):.2f} tau={float(a['tau']):.4f} M={float(M):.4f} chi={s['chi']} "
              f"I+={float(s['Ip']):.5f} I-={float(s['Im']):.5f} I+-I-={float(lhs):+.5f} "
              f"[noRec {float(noRec):+.5f} chk {float(rho*a['D']*formula - noRec):.1e}] rec={float(rec):.4f} "
              f"wtest={float(w):+.5f} Pbar-P0={float(s['Pbar']-s['P'][0]):+.5f} pred={float(s['Pr'][1]*rec):+.5f} "
              f"KH-k={float(s['KH']-k):+.4f} KL-k={float(s['KL']-k):+.4f} pi<tau={pi<a['tau']}")
