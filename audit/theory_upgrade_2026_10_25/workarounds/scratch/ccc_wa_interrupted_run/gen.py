# general discrete classes, R~U[0,r]
import sys; sys.path.insert(0,'/tmp/ccc_wa')
from own import m_of,lamR,lamE,Lp
def F(y,r): return 0.0 if y<=0 else min(y/r,1.0)
def g(th,r,p):  # int_p^th F
    if th<=p: return 0.0
    if r<=p: return th-p
    if th<=r: return (th*th-p*p)/(2*r)
    return (r*r-p*p)/(2*r)+(th-r)
def t_minus(th,r,p): pass
def objs(GH,GL,r,p):
    gH=sum(w*g(x,r,p) for x,w in GH); gL=sum(w*g(x,r,p) for x,w in GL)
    WH=sum(w*F(x,r) for x,w in GH)
    meanH=sum(w*x for x,w in GH); meanL=sum(w*x for x,w in GL)
    # Delta + gamma = mean gap  => Delta = gap - gamma
    Dl=(meanH-meanL)-(gH-gL)
    return gH,gL,Dl,WH
def state(r,P,GH,GL):
    p,cH,rho,k,beta,a,cap=[P[x] for x in 'p cH rho k beta a cap'.split()]
    gH,gL,Dl,WH=objs(GH,GL,r,p)
    tau=(cH-gL)/(gH-gL)
    out=dict(r=r,Delta=Dl,tau=tau,WH=WH)
    if not (0.5<tau<1) or rho*Dl>2*k or Dl<=2*k: out['branch']=False; return out
    lE=lamE(tau,beta); phi=Dl*(1-tau)-k-2*a*lE; lR=lamR(Dl,a,k,beta)
    out.update(branch=(phi>=0 and lR<cap),lamR=lR)
    EH=rho+(1-rho)*(beta+(1-beta)*lR)
    out.update(EH=EH,own=0.5*WH*EH,entry=rho+(1-rho)*(beta+(0.5-beta)*lR),Lp=Lp(lR,a,k,beta))
    return out
