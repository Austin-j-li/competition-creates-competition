
def brentq(f,lo,hi):
    for _ in range(200):
        mid=(lo+hi)/2
        if f(lo)*f(mid)<=0: hi=mid
        else: lo=mid
    return (lo+hi)/2

def Delta(r,h=10,l=1):
    if r<=l: return 0.0
    if r<=h: return (r-l)**2/(2*r)
    return (h-l)-(h*h-l*l)/(2*r)
def WH(r,h=10): return min(1,h/r)
def WL(r,l=1): return min(1,l/r)
def lamR(D,a,k,b):
    m=lambda x: b*(1-x)/(2*b+(1-2*b)*x)
    return brentq(lambda x: 2*a*x-(D*m(x)-k),0,1)
def report(r,a,k,b,rho,h=10,l=1):
    D=Delta(r,h,l); lam=lamR(D,a,k,b)
    m=b*(1-lam)/(2*b+(1-2*b)*lam); M=1-m
    eH=rho+(1-rho)*(b+(1-b)*lam); eL=rho+(1-rho)*b*(1-lam)
    E=(eH+eL)/2; OH=0.5*eH*WH(r,h); Ohid=0.5*rho*WH(r,h)
    PHe=eH/(eH+eL); Etheta=PHe*h+(1-PHe)*l
    PHwin=eH*WH(r,h)/(eH*WH(r,h)+eL*WL(r,l))
    print(f"r={r:6.3f} D={D:.6f} lam={lam:.6f} entry={E:.6f} WH={WH(r,h):.4f} OH={OH:.6f} Ohid={Ohid:.6f} Phi=OH/Ohid={OH/Ohid:.6f} eH/eL={eH/eL:.6f} P(H|entry)={PHe:.6f} M(=P(H|highcost entry))={M:.6f} E[theta|entry]={Etheta:.4f} P(H|challenger wins)={PHwin:.6f}")
print("counterexample: c_H=2.5 rho=.05 k=.2 beta=.2 a=5")
for r in [11,11.5,12]: report(r,5,.2,.2,.05)
print("benchmark: rho=1/4 k=1/50 beta=0.294655 a=1/40")
for r in [1.55,1.60,1.65]: report(r,1/40,1/50,0.294655,.25)
