from mpmath import mp, mpf, e as E, findroot, diff
mp.dps = 30
u = E-1; beta = mpf(294655)/10**6; lam = u*beta/(1+u*beta); b=(1-lam)*beta
pi = mpf(1)/2; M = pi*(1+u)/(pi*(1+u)+1-pi); m = 1-M
h, ell, p, cH, rho, k = mpf(10), mpf(1), mpf('0.95'), mpf(6), mpf(1)/4, mpf(1)/250
def objs(r):
    t0 = p*(1-p/r); tL = ell-(ell**2-p**2)/(2*r); D=(r-ell)**2/(2*r)
    gH = h - r/2 - p**2/(2*r); gL=(ell**2-p**2)/(2*r); tau=(cH-gL)/(gH-gL)
    A = tL-t0+D*M; S = rho*D*(M-m)+(1-rho)*A; Ip = rho*D*(M-pi)+(1-rho)*A
    return dict(A=A,S=S,Ip=Ip,tau=tau,D=D)
for key in ['S','Ip','A']:
    rt = findroot(lambda r: diff(lambda x: objs(x)[key], r), mpf('1.75'))
    print(f"{key} turns up at r = {float(rt):.4f}")
rlo = findroot(lambda r: rho*m*objs(r)['D']-k, mpf('1.4'))
print("full trade unique for r >", float(rlo), " tau at 1.5..1.8:", [round(float(objs(mpf(x))['tau']),4) for x in ('1.5','1.8')])
for r in ['1.5','1.72','1.78','1.826']:
    o = objs(mpf(r)); print(r, "A(M)=%.5f S=%.5f I+=%.5f margin=%.5f" % (o['A'], o['S'], o['Ip'], rho*m*o['D']-k))
# family members at r=3 and r=3.6: full-trade margins for the low-class sale and high-class purchase
print("\nfamily full-trade margins (data at pi0=0.6, benchmark slot)")
hB, pB, kB = mpf(10), mpf(1)/2, mpf(1)/50
def aB(r):
    gH = hB - r/2 - pB**2/(2*r); gL=(1-pB**2)/(2*r); return (r-1)**2/(2*r), (cH-gL)/(gH-gL)
pi0 = mpf('0.6'); f1 = b+pi0*lam; fm = b+(1-pi0)*lam; EX=f1-fm; v=f1+fm
for pip in [mpf('0.56'), mpf('0.6'), mpf('0.65')]:
    lp = EX/(2*pip-1); bp=(v-lp)/2; up=lp/bp
    Mp = pip*(1+up)/(pip*(1+up)+1-pip); mp_ = pip/(pip+(1-pip)*(1+up))
    out=[]
    for r in [mpf(3), mpf('3.6')]:
        D, tau = aB(r); out.append((float(rho*D*mp_-kB), float(D*(1-Mp)-kB), bool(Mp>=tau), bool(pip<tau)))
    print(f" pi'={float(pip)}: (KL-k, KH-k, recruits, pi'<tau) at r=3: {out[0]}, r=3.6: {out[1]}")
