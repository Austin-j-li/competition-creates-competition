# Benchmark closed forms, calibration B slot. Prior set P(F) at fixed strength.
h,l,p,rho,cH,k=10,1,0.5,0.25,6,0.02
u=1.718282; beta=0.294655; lam=u*beta/(1+u*beta); b=(1-lam)*beta
def Dl(r): return (r-l)**2/(2*r)
def tau(r): return (48*r-3)/(4*(20*r-r*r-1))
def M(pi): return pi*(1+u)/(1+pi*u)
def Minv(t): return t/(t+(1-t)*(1+u))
def Pset(r):
    D,t=Dl(r),tau(r); J=D*(1-t)
    lo=max(Minv(t),1-k/(rho*D)); hi=min(t,k/(rho*D))
    return D,t,J,lo,hi
for r in [1.393958,1.42,1.467127,1.6,1.747878,1.9]:
    D,t,J,lo,hi=Pset(r)
    pk=(b*D/k-b)/(b*D/k+lam)  # prior where full purchase starts
    print(f"r={r:.6f} Delta={D:.5f} tau={t:.5f} J={J:.5f} J>=k:{J>=k-1e-9}  prior set=[{lo:.6f},{hi:.6f}{')' if hi==t else ']'}  entry-peak prior={pk:.4f}")
