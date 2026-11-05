exec(open('check.py').read().split("for r in [6.0")[0])
import math
beta=0.294655; u=math.e-1; cap=u*beta/(1+u*beta); k=1/50; a=1/40
rho=0.6
print('rho=0.6 IM cond k-rho(2a cap+k)=',k-rho*(2*a*cap+k))
prev=None
for r in [1.50,1.55,1.60,1.62,1.64,1.65,1.66,1.67,1.68,1.70]:
    show(' B rho=.6',r,10,1,.5,6,k,rho,beta,a,cap)
# condition (i) primitive margin: g_H - c_H  vs (tau+omega)(Delta + 2a lamE'(tau)), benchmark
print('--- condition (i) in benchmark: LHS=g_H-c_H, RHS=(tau+omega)(Delta+2a lamE_prime)')
def lamEp(tau,beta): return beta/(beta+(1-2*beta)*(1-tau))**2
for (lab,h,l,p,cH,kk,aa,bb) in [('bench',10,1,.5,6,1/50,1/40,beta),('CE',10,1,.5,4.5,.5,.01,.2)]:
    for r in ([1.3,1.4,1.5,1.6,1.7,2,3,3.5] if lab=='bench' else [4,4.5,5,6,7,7.3]):
        D,gam,gL=auction(r,h,l,p); tau=(cH-gL)/gam
        omega=(l*l-p*p)/(2*r*r)/((r*r-l*l)/(2*r*r))
        lhs=gam*(1-tau); rhs=(tau+omega)*(D+2*aa*lamEp(tau,bb))
        print(' ',lab,'r=%.2f LHS=%.4f RHS=%.4f ratio=%.2f omega=%.3f Delta/gamma=%.4f'%(r,lhs,rhs,lhs/rhs,omega,D/gam))
