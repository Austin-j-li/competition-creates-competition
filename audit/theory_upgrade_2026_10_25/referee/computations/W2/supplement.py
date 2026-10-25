from recompute import *
# Fixed full-information control at the benchmark.
v=evaluate(H,L,U(0,'1.6'),B)
lam=B['cap']; b=B['beta']*(1-lam); m=b/(2*b+lam)
efix=B['rho']+(1-B['rho'])*(b+lam)
show('FROZEN FULL ORDERS',dict(efix=efix,branch_ratio=v['eH']/efix,L_sale_payoff=B['rho']*v['Delta']*m-B['k'],H_purchase_payoff=v['Delta']*m-B['k']))
# Exact equality in the takeover finite sufficient condition written with >=.
z=D('.99'); delta1=9*(1-z)
lam1,_,_=research(delta1,B); e1=B['rho']+(1-B['rho'])*(B['beta']+(1-B['beta'])*lam1)
delta0=mp.findroot(lambda dd:B['rho']+(1-B['rho'])*(B['beta']+(1-B['beta'])*research(dd,B)[0])-z*e1,(D('.08'),D('.089')))
center=1+delta0/(1-z)
F0=mix((z,U(0,1)),(1-z,U(center-D('.001'),center+D('.001'))))
F1=mix((z,U(0,1)),(1-z,U('10.1','10.2')))
x0=evaluate(H,L,F0,B); x1=evaluate(H,L,F1,B)
show('TAKEOVER equality construction',dict(z=z,center=center,delta0=delta0,delta1=delta1,entryratio=x1['eH']/x0['eH'],bound=9/(9-delta1),ownership_difference=x1['OH']-x0['OH']))
show('TAKEOVER equality F0',x0);show('TAKEOVER equality F1',x1)
# Counterexample branch endpoint and scales.
upper=mp.findroot(lambda rr:evaluate(H,L,U(0,rr),C)['phi'],(D(13),D('13.5')))
show('COUNTEREXAMPLE branch endpoints',dict(lower=(D('24.75')+D('.375'))/D('2.5'),upper=upper))
# Wide-class Proposition 2 row, general prior .7.
wh0=cw(U(1,19),U(0,1)); wh1=cw(U(1,19),U(0,'4.5'))
show('WIDE CLASSES P2',dict(WH0=wh0,WH1=wh1,OH0=D('.7')*D('.25')*wh0,OH1=D('.7')*efix*wh1))
# Solver B upper proof coefficient wording: larger root positive despite g>=0 on [0,1].
s=mp.sqrt(D('.25')); beta=D('.01')
y=(1+s)*beta-s
c0=2*(1-s)/(1+s)*y*y
c1=(1-s*s)*(1-beta)*(1+s+4*y)/(1+s)
c2=(1-s*s)*(1-beta)*(1-2*beta)
show('Solver B polynomial',dict(c0=c0,c1=c1,c2=c2,discriminant=c1*c1-4*c0*c2))
P=params(cH='2.734',rho='.25',k='1.7',beta='.2',a='.001',cap='.9')
for r in ['9.5','10','10.1']:
    v=evaluate(H,L,U(0,r),P)
    show('FINITE comparison at r='+r,{k:v[k] for k in ['branch','tau','lam','buy_margin','OH','WH']})
# Every value in the benchmark's displayed loss and response margins.
show('SMALL benchmark margins',dict(delta_derivative_min=D(11)/72,counterexample_slope_upper=D(57)/880,h_over_max=D(10)/D('3.6'),h_over_branchcap=D(10)/D('1.677632834385081')))
for label,P,r in [('benchmark',B,D('1.6')),('counterexample',C,D(11))]:
    v=evaluate(H,L,U(0,r),P)
    show('SCALE ratios '+label,dict(k_Delta=P['k']/v['Delta'],a_Delta=P['a']/v['Delta'],rhoDelta_2k=P['rho']*v['Delta']/(2*P['k']),cost_gH=P['cH']/v['gH']))
show('RESTRICTED uniform DA family',dict(gH20=cg(H,U(0,20)),gH25=cg(H,U(0,25)),cost=D(3),full_family_bound=cg(H,U(0,10))))
