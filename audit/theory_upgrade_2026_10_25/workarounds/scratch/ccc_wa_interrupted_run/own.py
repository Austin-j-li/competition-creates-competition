import math

def brentq(f,a,b,xtol=1e-15):
    fa=f(a)
    for _ in range(200):
        c=(a+b)/2; fc=f(c)
        if (fc>0)==(fa>0): a,fa=c,fc
        else: b=c
    return (a+b)/2

def pm(h,l,p,r):
    # point masses h,l; R~U[0,r]; returns g_H,g_L,Delta,W_H
    def g(th):
        if r<=th: return th - r/2 - p*p/(2*r)
        return (th*th-p*p)/(2*r)
    def D():  # int_l^h (1-F)
        lo,hi=l,h
        if r<=lo: return 0.0
        top=min(hi,r)
        return (top-lo) - (top*top-lo*lo)/(2*r)
    return g(h),g(l),D(),min(1.0,h/r)

def m_of(lam,beta): return (1-lam)*beta/(2*beta+(1-2*beta)*lam)

def lamR(Delta,a,k,beta):
    f=lambda x: 2*a*x - (Delta*m_of(x,beta)-k)
    if Delta<=2*k: return None
    return brentq(f,0,1-1e-14,xtol=1e-15)

def lamE(tau,beta): return beta*(2*tau-1)/(beta+(1-2*beta)*(1-tau))

def Lp(lam,a,k,beta):  # closed-form dLambda/dDelta
    return beta*(1-lam)**2/(2*a*(2*beta+(1-2*beta)*lam*(2-lam))+k)

def state(r,P):
    h,l,p,cH,rho,k,beta,a,cap=[P[x] for x in 'h l p cH rho k beta a cap'.split()]
    gH,gL,Dl,WH=pm(h,l,p,r)
    tau=(cH-gL)/(gH-gL)
    out=dict(r=r,Delta=Dl,tau=tau,WH=WH)
    if not (0.5<tau<1) or rho*Dl>2*k:
        out['branch']=False; return out
    lE=lamE(tau,beta); phi=Dl*(1-tau)-k-2*a*lE
    lR=lamR(Dl,a,k,beta)
    br = lR is not None and phi>=0 and lR<cap
    out.update(branch=br,lamE=lE,phi=phi,lamR=lR)
    if lR is not None:
        EH=rho+(1-rho)*(beta+(1-beta)*lR)
        out['entry']=rho+(1-rho)*(beta+(0.5-beta)*lR)
        out['EH']=EH; out['own']=0.5*WH*EH; out['Lp']=Lp(lR,a,k,beta)
    return out
