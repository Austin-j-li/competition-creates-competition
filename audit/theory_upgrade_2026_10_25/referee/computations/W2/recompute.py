"""Consumer calculations for the W2 referee. Print numerical outputs; no assertions."""
from mpmath import mp
import json
mp.dps = 60
D = mp.mpf

def U(lo,hi):
    return [(D(1),D(lo),D(hi))]
def atom(v):
    return U(v,v)
def mix(*items):
    return [(D(w)*v,a,b) for w,law in items for v,a,b in law]
def epow(law,t,n):
    return sum(w*(max(a-t,0)**n if a==b else (max(b-t,0)**(n+1)-max(a-t,0)**(n+1))/((n+1)*(b-a))) for w,a,b in law)
def mean(law):
    return sum(w*(a+b)/2 for w,a,b in law)
def cw(law,F):
    return sum(w*(epow(law,a,1)-epow(law,b,1))/(b-a) for w,a,b in F)
def cg(law,F,p=D('.5')):
    return sum(w*(epow(law,a,2)-epow(law,b,2)-max(p-a,0)**2+max(p-b,0)**2)/(2*(b-a)) for w,a,b in F)
def auction(H,L,F,p=D('.5')):
    gh,gl=cg(H,F,p),cg(L,F,p)
    return dict(Delta=mean(H)-mean(L)-gh+gl,gamma=gh-gl,gH=gh,gL=gl,WH=cw(H,F),WL=cw(L,F))
def params(**kw):
    return {k:D(v) for k,v in kw.items()}
B=params(cH=6,rho='.25',k='.02',beta='.294655',a='.025')
B['cap']=(mp.e-1)*B['beta']/(1+(mp.e-1)*B['beta'])
C=params(cH='2.5',rho='.05',k='.2',beta='.2',a=5,cap='.9')
H,L=atom(10),atom(1)
def research(delta,P):
    b,a,k=P['beta'],P['a'],P['k']
    aa=2*a*(1-2*b); bb=4*a*b+k*(1-2*b)+b*delta; cc=b*(2*k-delta)
    lam=-2*cc/(bb+mp.sqrt(bb*bb-4*aa*cc))
    den=2*b+(1-2*b)*lam
    m=b*(1-lam)/den
    lp=m/(2*a+delta*b/den**2)
    return lam,m,lp

def evaluate(H,L,F,P):
    v=auction(H,L,F); delta=v['Delta']; gam=v['gamma']
    rho,b,a,k=P['rho'],P['beta'],P['a'],P['k']
    tau=(P['cH']-v['gL'])/gam
    lam,m,lp=research(delta,P)
    le=b*(2*tau-1)/(b+(1-2*b)*(1-tau))
    eh=rho+(1-rho)*(b+(1-b)*lam); el=rho+(1-rho)*b*(1-lam)
    oh=eh*v['WH']/2; ol=el*v['WL']/2
    v.update(tau=tau,lam=lam,lamE=le,M=1-m,eH=eh,eL=el,entry=(eh+el)/2,OH=oh,OL=ol,OZ=rho*v['WH']/2,mult=eh/rho,difference=(eh-rho)*v['WH']/2,entrant=eh/(eh+el),winshare=oh/(oh+ol),buy_margin=1-m-tau,sale_margin=k-rho*delta/2,phi=delta*(1-tau)-k-2*a*le,cap_margin=P['cap']-lam,lambda_prime=lp,epsilon=delta*(1-rho)*(1-b)*lp/eh,research_cost=a*lam**2/2)
    v['branch']=bool(delta>2*k and D('.5')<tau<1 and v['buy_margin']>=-D('1e-50') and v['sale_margin']>=0 and 0<lam<P['cap'])
    return v

def show(label,v):
    print(label)
    print(json.dumps({k:(v if isinstance(v,bool) else mp.nstr(v,16)) for k,v in v.items()},sort_keys=True))

if __name__=='__main__':
    bm=[]; ce=[]
    for r in ['1.55','1.6','1.65']:
        v=evaluate(H,L,U(0,r),B); bm.append(v)
        dp=(1-1/D(r)**2)/2
        v.update(log_slope_r=v['epsilon']*dp/v['Delta'],elasticity_r=v['epsilon']*D(r)*dp/v['Delta'],mean_prepared=1+9*v['entrant'])
        show('BENCHMARK r='+r,v)
    for r in [11,12]:
        v=evaluate(H,L,U(0,r),C); ce.append(v)
        v.update(elasticity_r=v['epsilon']*v['gamma']/v['Delta']-1)
        show('KNOWN COUNTEREXAMPLE r='+str(r),v)
    show('COUNTEREXAMPLE CHANGES',{k:100*(ce[1][k]/ce[0][k]-1) for k in ['lam','entry','eH','WH','OH']})
    show('COUNTEREXAMPLE DECOMPOSITION',dict(frozenOH=ce[0]['eH']*ce[1]['WH']/2,information=(ce[1]['eH']-ce[0]['eH'])*ce[1]['WH']/2,auction=ce[0]['eH']*(ce[1]['WH']-ce[0]['WH'])/2,conservative_margin=ce[0]['M']-ce[1]['tau'],logOH=mp.log(ce[1]['OH']/ce[0]['OH']),loge=mp.log(ce[1]['eH']/ce[0]['eH']),logW=mp.log(ce[1]['WH']/ce[0]['WH'])))
    rstart=mp.findroot(lambda r:evaluate(H,L,U(0,r),B)['phi'],(D('1.4'),D('1.6')))
    rcap=mp.findroot(lambda r:evaluate(H,L,U(0,r),B)['cap_margin'],(D('1.6'),D('1.8')))
    rn=mp.findroot(lambda r:evaluate(H,L,U(0,r),B)['sale_margin'],(D('1.6'),D('1.8')))
    start=evaluate(H,L,U(0,rstart),B); end=evaluate(H,L,U(0,rcap),B)
    show('BENCHMARK ENDPOINTS',dict(rstart=rstart,rcap=rcap,rN=rn,lam_start=start['lam'],cap=B['cap'],eH_start=start['eH'],eH_end=end['eH'],eL_start=start['eL'],eL_end=end['eL'],entry_start=start['entry'],entry_end=end['entry'],eH_gain_pct=100*(end['eH']/start['eH']-1),tolerated_W_loss_pct=100*(1-start['eH']/end['eH']),P2_OH=end['eH']/2,P2_mult=end['eH']/B['rho'],P2_loss_pct=100*(1-B['rho']/end['eH'])))
    rt=4+mp.sqrt(63)/2
    show('DA',dict(r_tau1=rt,cost_bound=(100-D('.25'))/20,cost_margin=6-(100-D('.25'))/20,rt_gap=10-rt,h_gap=10-D('3.6'),research_gap=10-rcap,branch_Wloss_bound=2*B['k']/(B['rho']*9),eH_gain_sufficient=1/(1-2*B['k']/(B['rho']*9))-1,rho_limit=((1+mp.sqrt(3))/(3*mp.sqrt(3)-1))**2))
    for r in ['11','11.1']:
        show('solver_A rising beyond h r='+r,evaluate(H,L,U(0,r),params(cH='2.4',rho='.05',k=2,beta='.2',a='.025',cap='.9')))
    for s in ['2.9','3']:
        show('solver_A constant WH s='+s,evaluate(mix(('.5',atom(1)),('.5',atom(10))),L,U(D(s)-D('.1'),D(s)+D('.1')),params(cH=2,rho='.25',k='.2',beta='.2',a=1,cap='.9')))
    for z in ['9.8','10.2']:
        show('solver_A conditional share fall z='+z,evaluate(H,L,mix(('.5',U(0,1)),('.5',U(D(z)-D('.1'),D(z)+D('.1')))),dict(C,cH=D('2.7'))))
    for z in ['9.99','10.01']:
        show('TAKEOVER benchmark mixture z='+z,evaluate(H,L,mix(('.996',U(0,'1.5')),('.004',U(D(z)-D('.01'),D(z)+D('.01')))),B))
    for rho in ['.01','.25']:
        for r in ['10.5','11.2']:
            v=evaluate(H,L,U(0,r),params(cH='2.734',rho=rho,k='1.7',beta='.2',a='.001',cap='.9'))
            v.update(eta=v['Delta']/v['gamma'],elasticity_r=v['epsilon']*v['gamma']/v['Delta']-1,trade_cost_share=D('1.7')/(D('1.7')+2*D('.001')*v['lam']))
            show('Solver B low rho='+rho+' r='+r,v)
    HP=U(8,12); PP=params(cH=3,rho='.05',k='.6',beta='.2',a='.01',cap='.95')
    for r in ['8.07','10.07','12']:
        v=evaluate(HP,L,U(0,r),PP)
        slope=mp.diff(lambda rr:evaluate(HP,L,U(0,rr),PP)['OH'],D(r))
        show('Solver B continuous r='+r,dict(v,slope=slope))
    peak=mp.findroot(lambda rr:mp.diff(lambda rr2:evaluate(HP,L,U(0,rr2),PP)['OH'],rr),(D(10),D('10.2')))
    show('Solver B continuous exact peak',dict(r=peak,**evaluate(HP,L,U(0,peak),PP)))
    for r in ['4.5','9','15']:
        wh=cw(U(1,19),U(0,r)); risk=1-(19-D(r))/18/wh
        show('TAKEOVER at risk r='+r,dict(WH=wh,risk=risk))
    for aa in ['.01','.02','.05','.1','.25','.5','1','2','5']:
        v=evaluate(H,L,U(0,'11.5'),dict(C,a=D(aa)))
        show('RESEARCH COST sweep a='+aa,dict(branch=v['branch'],lam=v['lam'],epsilon=v['epsilon'],elasticity_r=v['epsilon']*v['gamma']/v['Delta']-1))
    for rho in ['.01','.05','.1','.15','.2','.25','.3','.5','.9']:
        s=mp.sqrt(D(rho)); show('ELASTICITY ceiling rho='+rho,dict(bound=2*(1-s)/(1+s),qopt=s/(1+s)))
    for delta,P in [(D('.1'),B),(D('.12'),B),(D('4.5'),C)]:
        lam,m,lp=research(delta,P)
        show('LAMBDA derivative delta='+str(delta),dict(analytic=lp,numerical=mp.diff(lambda dd:research(dd,P)[0],delta)))
    for i,F in enumerate([U(0,2),mix(('.5',U(0,1)),('.5',U(3,4)))]):
        v=auction(atom(3),L,F)
        show('HAZARD COUNTEREXAMPLE '+str(i),dict(v,ratio=v['WL']/v['WH']))
    for i,F in enumerate([U('2.1','2.4'),U('2.6',9)]):
        v=auction(mix(('.49',atom('2.5')),('.51',atom(10))),mix(('.5',atom(2)),('.5',atom(10))),F)
        show('Solver F ratio example '+str(i),dict(v,ratio=v['WL']/v['WH']))
    for r in ['2','2.5']:
        v=auction(mix(('.5',atom('1.5')),('.5',atom(3))),mix(('.5',atom(1)),('.5',atom(3))),U(0,r))
        show('Solver B FOSD class ratio r='+r,dict(v,ratio_HL=v['WH']/v['WL']))
