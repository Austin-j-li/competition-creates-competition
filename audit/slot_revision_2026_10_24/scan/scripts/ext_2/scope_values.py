import runpy,itertools
ns=runpy.run_path('scripts/ext_2/recompute.py')
globals().update({k:v for k,v in ns.items() if not k.startswith('__')})
def display(label,value):
 l,h=endpoints(value); print(label,mp.nstr(l,28),mp.nstr(h,28))
cap=I('0.33')
alo=(D('1.65')*mlam(cap)-k)/(2*cap)
display('cap .33 minus lower strip',cap-lamE(3))
display('upper strip minus cap .33',lamE('3.6')-cap)
display('a .025 minus lower cost at cap .33',a-alo)
display('upper cost minus a .025',aup-a)
display('r1 entry with cap .33',entryR(cap))
display('zero research purchase payoff at r=1.55',rho*D('1.55')/2-k)
# Every hypothesis for the tabulated class examples.
for name,case in cases.items():
 hl,hh,ll,lh,pi,c,fee,rs=case; pi,c,fee=map(I,(pi,c,fee)); mm=pi/(pi+(1-pi)*E); top=pi*E/(1-pi+pi*E)
 ob0=nodes[name,0]; ob1=nodes[name,1]
 margins={'weak cost':c-ob0[2][1]-pi*(ob0[1][1]-ob0[2][1]),'strong top':ob1[2][1]+top*(ob1[1][1]-ob1[2][1])-c,'weak trade':fee-ob0[3],'strong trade':rho*imin([mm,1-top])*ob1[3]-fee,'ownership':(rho+(1-rho)*(b+lam))*ob1[1][2]-rho*ob0[1][2]}
 if len(rs)==3:
  ob2=nodes[name,2]; margins['return']=c-ob2[2][1]-top*(ob2[1][1]-ob2[2][1])
 for key,value in margins.items(): display(name+' '+key,value)
# Three-class collision and its perturbed, strict choices.
for eps in ['-.001','0','.001']:
 ww=weight+I(eps); ts=[I(1),1+I('49/16')*ww,I('65/16')]; means=[]
 for qi,base in enumerate([b,b0,b]):
  joint=[p*(base+(lam if j==qi else 0)) for j,p in enumerate(priors)]; means.append(sum(x*t for x,t in zip(joint,ts))/sum(joint))
 display('price zero minus plus, perturbation '+eps,rho*(means[1]-means[2]))
 choices=[]
 for j,t in enumerate(ts):
  pays=[q*rho*(t-mn)-I('1/8')*abs(q) for q,mn in zip([-1,0,1],means)]
  choices.extend(pays[j]-p for i,p in enumerate(pays) if i!=j)
 display('smallest choice margin, perturbation '+eps,imin(choices))
# Declared private-signal grid.
accepted=[]; margins=[]
for ai,di in itertools.product(range(68,73),range(73,78)):
 out=signal_margin('grid','1.1','2.3','.85','7.14','.015',str(Q(ai,100)),str(Q(di,100)))
 if all(positive(out[k]) for k in ['private','joint','weak','strong']):
  accepted.append((ai,di)); margins.extend(out.values())
print('Grid pairs',accepted)
display('grid smallest margin',imin(margins))
# Analytic reserve and signed-shortfall values.
display('positive shortfall at prior .3',-val['p2_fixed_prior_three_tenths_r1_cost_sign_plus'])
# Under the baseline F1>F0, F1(p) need not be positive.
# Continuous U[p,r] examples with p=.5, r=.5+width and h=10, ell=1.
def supported(r):
 rr=I(r); width=rr-half; gl=(1-half)**2/(2*width); gh=10-(rr+half)/2; dd=(rr-1)**2/(2*width)
 return gl,gh,dd
for rr in ['1.1','3','3.6']:
 gl,gh,dd=supported(rr)
 display('U[.5,'+rr+'] prior profit',gl+half*(gh-gl))
 display('U[.5,'+rr+'] top profit',gl+M*(gh-gl))
 display('U[.5,'+rr+'] spread',dd)
