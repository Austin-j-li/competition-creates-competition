"""Seller's reserve in the paper's point-value example, using the kernel in
appendix/A7_welfare.tex. Prints proceeds and entry at each reserve. New calculation,
not in the paper. A row is 'open' when neither trade bound decides the order plan."""
import math
h,l,pi,cH=10.,1.,.5,6.
lam,beta=0.336122,0.294655
b=(1-lam)*beta; u=lam/b
M=pi*(1+u)/(pi*(1+u)+1-pi); m=pi/(pi+(1-pi)*(1+u)); kap=min(m,1-M)
def kern(th,p,r):
    t0=p*max(1-p/r,0)
    if th<p: return t0,0.
    if r<=p: return p,th-p
    if th<=r: return th-(th*th-p*p)/(2*r),(th*th-p*p)/(2*r)
    return r/2+p*p/(2*r),th-r/2-p*p/(2*r)
def out(r,p,rho,k):
    t0=p*max(1-p/r,0); tH,gH=kern(h,p,r); tL,gL=kern(l,p,r); D=tH-tL
    B=lambda mu:gL+mu*(gH-gL)
    if D<k: plan='none'; beliefs=[(1.,pi)]; 
    elif rho*kap*D>k: plan='full'
    else: return dict(plan='open',D=D)
    if plan=='none':
        e=rho+(1-rho)*(B(pi)>=cH); eH=eL=e
    else:
        b0=1-lam-2*b
        eup=rho+(1-rho)*(B(M)>=cH); e0=rho+(1-rho)*(B(pi)>=cH); edn=rho+(1-rho)*(B(m)>=cH)
        eH=(b+lam)*eup+b0*e0+b*edn; eL=b*eup+b0*e0+(b+lam)*edn
    E=pi*eH+(1-pi)*eL
    R=t0+pi*eH*(tH-t0)+(1-pi)*eL*(tL-t0)
    return dict(plan=plan,D=D,E=E,R=R,top=B(M))
print('M',round(M,6),'kappa',round(kap,6),'u',round(u,6))
print('check, baseline p=.5 rho=.25 k=.02:',{r:round(out(r,.5,.25,.02)['R'],6) for r in(1.2,3,3.6)})
def best(r,rho,k):
    bestrow=None; opens=0
    for i in range(1,9996):
        p=i/1000
        o=out(r,p,rho,k)
        if o['plan']=='open': opens+=1; continue
        if bestrow is None or o['R']>bestrow[1]['R']: bestrow=(p,o)
    return bestrow,opens
for rho,k in [(.25,.02),(.2,.02),(.15,.02),(.1,.017)]:
    print(f'\nrho={rho} k={k}  H2: Delta0={(1.2-1)**2/2.4:.5f} < k < rho*kappa*Delta1={rho*kap*(4/6):.5f}')
    for r in (1.2,3,3.6):
        (p,o),op=best(r,rho,k); low=out(r,.5,rho,k)
        print(f' r={r}: best p={p:.3f} R={o["R"]:.4f} E={o["E"]:.4f} plan={o["plan"]} | p=.5 R={low["R"]:.4f} E={low["E"]:.4f} | posted p=9.9 R={out(r,9.9,rho,k)["R"]:.4f} | open rows {op}')
# cutoff rho where the posted price stops beating the best recruiting reserve
print('\nbest recruiting reserve vs posted price, by rho (k chosen so full orders hold)')
for rho in (.25,.2,.15,.12,.1,.05):
  row=[]
  for r in (1.2,3,3.6):
    k=min(.02,rho*kap*.5)
    bb=None
    for i in range(1,9996):
        p=i/1000;o=out(r,p,rho,1e-6)
        if o['plan']=='full' and o['top']>=cH and (bb is None or o['R']>bb[1]['R']): bb=(p,o)
    row.append((r, None if bb is None else (bb[0],round(bb[1]['R'],4))))
  print(rho,'posted',round(9.9*rho*pi,4),row)
# reserve below the low value: recruitment and the spread
print('\nspread and top profit at low reserves, r=3 and r=3.6')
for p in (.01,.25,.48,.5,1.):
  for r in (1.2,3,3.6,3.7):
    tH,gH=kern(h,p,r);tL,gL=kern(l,p,r);print(f' p={p} r={r} D={tH-tL:.5f} B(M)={gL+M*(gH-gL):.5f}',end=';')
  print()
