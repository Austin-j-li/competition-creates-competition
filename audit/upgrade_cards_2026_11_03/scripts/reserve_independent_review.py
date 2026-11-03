"""Independent reserve calculations. Prints results; no assertions."""
import mpmath as m
m.mp.dps=60
D=m.mpf
beta=D('0.294655'); lam=(m.e-1)*beta/(1+(m.e-1)*beta)
b=(1-lam)*beta; M=m.e/(1+m.e); kap=1-M; A=b+lam; Q=b+lam/2
rs=list(map(D,['1.2','3','3.6']))
rhos=list(map(D,['.25','.2','.15','.125','.1']))
def fmt(x): return m.nstr(x,17)
def kernel(r,p,v):
 t0=p*max(0,1-p/r)
 if v<p:return t0,D(0)
 if r<=p:return p,v-p
 if v<=r:return v-(v*v-p*p)/(2*r),(v*v-p*p)/(2*r)
 return r/2+p*p/(2*r),v-r/2-p*p/(2*r)
def objects(r,p,h=D(10),ell=D(1)):
 t0=p*max(0,1-p/r); th,gh=kernel(r,p,h); tl,gl=kernel(r,p,ell)
 return t0,th,tl,gh,gl
def outcome(r,p,rho,k,h=D(10)):
 t0,th,tl,gh,gl=objects(r,p,h); delta=th-tl
 if delta<k: plan='N'; eh=el=rho; entry=rho
 elif rho*kap*delta>k:
  plan='F'; ep=[rho+(1-rho)*int(gl+u*(gh-gl)>=6-D('1e-50')) for u in [kap,D('.5'),M]]
  eh=b*ep[0]+(1-lam-2*b)*ep[1]+(b+lam)*ep[2]
  el=(b+lam)*ep[0]+(1-lam-2*b)*ep[1]+b*ep[2]
  entry=(eh+el)/2
 else:return None
 return t0+(eh*(th-t0)+el*(tl-t0))/2,entry,plan
print('slot',*[fmt(x) for x in [beta,lam,b,M,kap,A,Q]])
print('PRINTED ROWS reserve,r,proceeds,entry,sale,two')
for p in map(D,['.5','1.01','1.55']):
 for r in rs[:2]:
  rho=D('.25'); k=D('.02'); out=outcome(r,p,rho,k)
  eh=rho if out[2]=='N' or out[1]==rho else rho+(1-rho)*A
  el=rho if out[2]=='N' or out[1]==rho else rho+(1-rho)*b
  f=min(p/r,1); admissL=int(p<=1)
  sale=1-f+f*(eh+el*admissL)/2; two=(1-f)*(eh+el*admissL)/2
  print(*map(fmt,[p,r,out[0],out[1],sale,two]))
print('BASE')
for r in rs:print(fmt(r),outcome(r,D('.5'),D('.25'),D('.02')))
a=10-6/M
print('a',fmt(a))
def recruit_cap(r,h=D(10)):
 aa=h-6/M
 if aa>=r:return aa
 if 2*r*aa-r*r>0:
  ph=m.sqrt(2*r*aa-r*r)
  if ph>1:return ph
 # below low value: B(M)=M*(h-r/2)+kap/(2*r)-p²/(2*r)
 z=2*r*(M*(h-r/2)+kap/(2*r)-6)
 return m.sqrt(z) if z>0 else None
for rho in rhos:
 k=D('.017') if rho==D('.1') else D('.02')
 print('RHO',fmt(rho),'k',fmt(k),'H margins',*[fmt(x) for x in [k-D(1)/60,rho*kap*D(2)/3-k]])
 for r in rs:
  cap=recruit_cap(r); C=(rho+(1-rho)*A)/2
  pd=r*(1-rho/2)/(2-3*rho/2)
  cand=[D('.00000000001'),D('.5'),D(1),D('1.000000000001'),pd,r,10-D('1e-30')]
  if cap: cand += [cap,cap+D('1e-25')]
  vals=[(outcome(r,p,rho,k),p) for p in cand if 0<p<10]
  vals=[v for v in vals if v[0] is not None]
  best=max(vals,key=lambda x:x[0][0])
  print('BEST',fmt(r),fmt(best[1]),*[fmt(x) if not isinstance(x,str) else x for x in best[0]],'cap',fmt(cap),'floor interior',fmt(pd))
 print('H1,H3',fmt(6-(objects(rs[0],D('.5'))[3]+objects(rs[0],D('.5'))[4])/2),fmt(M*objects(rs[1],D('.5'))[3]+kap*objects(rs[1],D('.5'))[4]-6),fmt(6-M*objects(rs[2],D('.5'))[3]-kap*objects(rs[2],D('.5'))[4]))
print('CROSSOVERS')
for r in rs:
 cap=recruit_cap(r); t0,th,tl,gh,gl=objects(r,cap)
 # if weak cap>1 full; if r2 low cap full too
 J=(A*(th-t0)+b*(tl-t0))/2
 L=((th-t0)+(tl-t0))/2
 cross=(t0+J)/(5-L+J)
 print(fmt(r),'cap',fmt(cap),'rho*',fmt(cross),'t0,J,L',*[fmt(x) for x in [t0,J,L]])
print('ZERO RESERVE')
root=m.findroot(lambda r:M*(10-r/2)+kap/(2*r)-6,(D('3.6'),D(4)))
print('ceiling',fmt(root),'r=3.7 margins',fmt(6-M*(10-D('3.7')/2)-kap/(2*D('3.7'))))
print('at p=0 margins',*[fmt(x) for x in [6-(10-D('1.2')/2+1/(2*D('1.2')))/2,M*(10-D(3)/2)+kap/6-6,D('.25')*kap*D(2)/3-D('.02')]])
print('H=9 grid best (new)')
for r in rs:
 vals=[(outcome(r,D(i)/1000,D('.25'),D('.02'),D(9)),D(i)/1000) for i in range(1,9000)]
 vals=[v for v in vals if v[0] is not None]
 print(fmt(r),max(vals,key=lambda x:x[0][0]))
print('WIDE delta p=.5 low U[0,2], high U[9,11]')
for r in rs:
 tl=m.quad(lambda x:kernel(r,D('.5'),x)[0],[0,D('.5'),min(r,2),2]) if r<2 else m.quad(lambda x:kernel(r,D('.5'),x)[0],[0,D('.5'),2])
 tl/=2
 print(fmt(r),fmt(r/2+D('.25')/(2*r)-tl))
print('EXTRA EXACT CANDIDATES')
minrho=1/(40*kap)
print('minimum rho H2',fmt(minrho))
for r in rs[:2]:
 cap=recruit_cap(r); t0,th,tl,_,_=objects(r,cap); J=(A*(th-t0)+b*(tl-t0))/2; L=(th+tl-2*t0)/2
 print('narrow cutoff',fmt((t0+J)/(D('4.975')-L+J)))
print('r2 floor/high crossover',fmt(m.findroot(lambda rho:rs[2]*(rho/4+(1-rho/2)**2/(4-3*rho))-5*rho,(D('.2'),D('.25')))))
r=D('1.2');p=D('.5');rho=D('.25');k=D('.02')
th,gh=kernel(r,p,10)
tl=(m.quad(lambda x:kernel(r,p,x)[0],[0,p,r,2]))/2
gl=(m.quad(lambda x:kernel(r,p,x)[1],[0,p,r,2]))/2
delta=th-tl;tau=(6-gl)/(gh-gl)
print('wide at weak p=.5',*[fmt(x) for x in [delta,gh,gl,tau,delta*(1-tau)-k,2*k/rho-delta,delta*(1-M)-k,rho*delta/2-k]])
print('wide no trade entry',fmt(rho),'informative H buys L abstains entry',fmt(rho+(1-rho)*Q))
print('H9 top at p=0 strong',fmt(M*(9-D(3)/2)+kap/6-6))
def band_objects(r,p,w=D('.05')):
 t0=p*max(0,1-p/r)
 ans=[]
 for center in [D(10),D(1)]:
  lo=center-w;hi=center+w
  cuts=sorted(set([lo,hi]+[z for z in [p,r] if lo<z<hi]))
  tot=[D(0),D(0)]
  for aa,zz in zip(cuts,cuts[1:]):
   mid=(aa+zz)/2
   if mid<p:tot[0]+=t0*(zz-aa)
   elif r<=p:tot[0]+=p*(zz-aa);tot[1]+=(zz*zz-aa*aa)/2-p*(zz-aa)
   elif mid<=r:
    gg=(zz**3-aa**3)/(6*r)-p*p*(zz-aa)/(2*r)
    tot[0]+=(zz*zz-aa*aa)/2-gg;tot[1]+=gg
   else:
    tt=r/2+p*p/(2*r);tot[0]+=tt*(zz-aa);tot[1]+=(zz*zz-aa*aa)/2-tt*(zz-aa)
  ans.extend([v/(2*w) for v in tot])
 return t0,ans[0],ans[2],ans[1],ans[3]
print('NARROW weak transition; rho k p delta bound proceeds upper')
for rho in rhos:
 k=D('.017') if rho==D('.1') else D('.02');r=D('1.2')
 # Delta monotonic in the lower band: bound-ambiguous interval endpoints
 roots=[]
 for target in [k,k/(rho*kap)]:
  if band_objects(r,D('.95'))[1]-band_objects(r,D('.95'))[2]<target:
   lo=D('.95');hi=D('1.05')
   for i in range(100):
    mid=(lo+hi)/2;o=band_objects(r,mid)
    if o[1]-o[2]<target:lo=mid
    else:hi=mid
   roots.append((lo+hi)/2)
  else:roots.append(D(0))
 upper=D(0); bestp=0
 # Universal proceeds upper: high-cost preparation only after purchases, purchase likelihood <= b+lambda in H and <= b+lambda in L.
 # Sharper: low informed trader never buys; hence class-L purchase likelihood b.
 for i in range(1001):
  p=D('.949')+D(i)*D('.000102');t0,th,tl,gh,gl=band_objects(r,p)
  val=t0+((rho+(1-rho)*A)*(th-t0)+(rho+(1-rho)*b)*(tl-t0))/2
  if val>upper:upper=val;bestp=p
 print(fmt(rho),*[fmt(x) for x in roots],fmt(upper),fmt(bestp))
print('NARROW transition informative profiles on grid; best proceeds p xH yL')
for rho in rhos:
 k=D('.017') if rho==D('.1') else D('.02');best=None
 for i in range(2001):
  p=D('.95')+D(i)/20000;r=D('1.2');t0,th,tl,gh,gl=band_objects(r,p);delta=th-tl;tau=(6-gl)/(gh-gl)
  x=min(D(1),b/lam*(delta/k-2));y=min(D(1),max(D(0),b/lam*(rho*delta/k-2)))
  if x<=0 or (b+lam*x)/(2*b+lam*x)<tau:continue
  # Read actual prices and deviations for the proposed profile.
  probsH=[b,1-lam-2*b+lam*(1-x),b+lam*x];probsL=[b+lam*y,1-lam-2*b+lam*(1-y),b]
  mus=[z/(z+w) for z,w in zip(probsH,probsL)]
  es=[rho+(1-rho)*int(gl+mu*(gh-gl)>=6-D('1e-45')) for mu in mus]
  uh=[-es[0]*(1-mus[0])*delta-k,D(0),es[2]*(1-mus[2])*delta-k]
  ul=[es[0]*mus[0]*delta-k,D(0),-es[2]*mus[2]*delta-k]
  # Print only numerical candidates whose used orders maximize the stated payoff, within displayed precision.
  if x<1 and abs(uh[2])>D('1e-40'):continue
  if uh[2]<-D('1e-40'):continue
  if y==0 and ul[0]>D('1e-40'):continue
  if 0<y<1 and abs(ul[0])>D('1e-40'):continue
  if y==1 and ul[0]<0:continue
  eh=sum(z*e for z,e in zip(probsH,es));el=sum(z*e for z,e in zip(probsL,es))
  val=t0+(eh*(th-t0)+el*(tl-t0))/2
  if best is None or val>best[0]:best=(val,p,x,y,(eh+el)/2)
 print(fmt(rho),*[fmt(z) for z in best] if best else ['open'])
