"""W4 referee calculations: read inputs, evaluate formulas, print numbers only."""
import csv
import importlib.util
import math
import sys
from decimal import Decimal as Dec, getcontext
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path.cwd()
getcontext().prec = 70
with (ROOT/'audit/slot_manuscript_2026_10_23/registry/registry.csv').open() as fh:
    registry = {row['key']: row for row in csv.DictReader(fh)}

def decimal_input(key):
    f = Fraction(registry[key]['value'])
    return Dec(f.numerator)/Dec(f.denominator)

h, ell, p, rho, cH, k = [decimal_input('prim_'+x) for x in ('h','ell','p','rho','cH','k')]
beta = decimal_input('beta_B')
u = Dec(1).exp()-1
lam = u*beta/(1+u*beta)
b = (1-lam)*beta
M, m = (1+u)/(2+u), 1/(2+u)
vartheta, fbar = M-m, b+lam/2
calc = {'lambda_B':lam, 'theta_B':vartheta, 'vol_full_B':2*fbar, 'd_slot_B':fbar}
a = M*h-cH
rC = (a+(a*a+M*((1-M)*ell*ell-p*p)).sqrt())/M
dS = k/(rho*m)
rS = ell+dS+(dS*dS+2*ell*dS).sqrt()
calc.update(rC_B=rC, rS_B=rS, margin_obs_r2_above_rC_B=decimal_input('prim_r2')-rC)
print('BENCHMARK, INDEPENDENT DECIMAL CALCULATION')
print('M,m,b,rho*lambda/2:',M,m,b,rho*lam/2)
for tag in ('r1','r2'):
    r = decimal_input('prim_'+tag)
    omega = 1-ell/r
    delta = (r-ell)**2/(2*r)
    gL, gH = (ell*ell-p*p)/(2*r), h-r/2-p*p/(2*r)
    BM = gL+M*(gH-gL)
    chi = int(BM>=cH)
    wplus, wzero, wminus = ell/r+M*omega, ell/r+omega/2, ell/r+m*omega
    entryplus = rho+(1-rho)*chi
    classcov = rho*lam/2*omega
    recruitmentcov = fbar*(1-rho)*chi*wplus
    yplus, yzero, yminus = entryplus*wplus, rho*wzero, rho*wminus
    calc['wgap_'+tag+'_B']=wplus-wminus
    calc['cov_win_'+tag+'_B']=classcov+recruitmentcov
    calc['cov_entry_'+tag+'_B']=fbar*(1-rho)*chi
    calc['ba_'+tag+'_B']=rho*delta*vartheta+(1-rho)*chi*(ell-p+(p*p-ell*ell)/(2*r)+p*p/r+delta*M)
    print(tag,'omega,w+,w0,w-:',omega,wplus,wzero,wminus)
    print(tag,'BM,chi,classcov,recruitmentcov,share:',BM,chi,classcov,recruitmentcov,recruitmentcov/(classcov+recruitmentcov))
    print(tag,'winner buy impact,sale impact,second difference:',yplus-yzero,yzero-yminus,yplus-2*yzero+yminus)
    print(tag,'RR,OR:',wplus/wminus,wplus*(1-wminus)/(wminus*(1-wplus)))
    print(tag,'winner frequency gap,price spread,ratio:',yplus-yminus,calc['ba_'+tag+'_B'],(yplus-yminus)/calc['ba_'+tag+'_B'])
print('REGISTRY COMPARISON: key | recomputed | registry stored value | numeric difference')
for key, value in calc.items():
    print(key,format(value,'.24f'),registry[key]['value'],format(value-decimal_input(key),'.3E'),sep=' | ')

# Use the existing numerical program's functions without invoking its export main.
src = ROOT/'audit/slot_manuscript_2026_10_23/scripts/P5_observables/p5_observables.py'
spec = importlib.util.spec_from_file_location('p5_consumer',src)
program = importlib.util.module_from_spec(spec)
spec.loader.exec_module(program)
P = program.Prim(False)
S = program.Slot(P,program.iv.exp(1)-1,program.I(Fraction(294655,1000000)))
print('EXISTING P5 PROGRAM, DIRECT FUNCTION CONSUMER')
for rf in (Fraction(3),Fraction(18,5)):
    out = program.outcome(P,S,program.I(rf),'F')
    for label, value in [('wgap',out['w'][1]-out['w'][-1]),('cov_win',out['cov_win']),('cov_entry',out['cov_entry']),('spread',out['spread'])]:
        print(rf,label,value)

Mf, mf, tf = float(M),float(m),float(vartheta)
def risks(WH, WL, top=Mf, bottom=mf):
    wp, wm = WL+top*(WH-WL), WL+bottom*(WH-WL)
    return WH-WL,wp-wm,wp/wm,wp*(1-wm)/(wm*(1-wp)) if wp<1 and wm>0 else float('nan')

def point_profit(theta,r,reserve=.5):
    if r<=reserve: return theta-reserve
    return (theta*theta-reserve*reserve)/(2*r) if theta<=r else theta-r/2-reserve*reserve/(2*r)

def bisect(fn,lo,hi):
    flo,fhi=fn(lo),fn(hi)
    if flo*fhi>0: return float('nan')
    for _ in range(100):
        mid=(lo+hi)/2
        if flo*fn(mid)<=0: hi=mid
        else: lo,flo=mid,fn(mid)
    return (lo+hi)/2

print('POINT BENCHMARK EXTENSION: r | omega,gap,RR,OR')
for r in (1.2,3,3.6,5,8,10,12,20): print(r,risks(min(10/r,1),min(1/r,1)))
print('POINT 1/2 CLASSES AT BENCHMARK SLOT')
for r in (2,3,10,100): print(r,risks(2/r,1/r))
print('Solver C EQUILIBRIUM EXAMPLE')
for r in (2,3,4):
    delta=1-1.5/r
    BM=point_profit(1,r)+.7*(point_profit(2,r)-point_profit(1,r))
    print(r,'omega,gap,RR,OR',risks(2/r,1/r,.7,.3),'Delta,BM,gross correct order,cov',delta,BM,.15*delta,1/(16*r))
print('Solver E RECRUITMENT WINDOWS')
def B(r,mu): return (1-mu)*point_profit(1,r)+mu*point_profit(10,r)
print('B_h(M), fraction of h, benchmark cost multiple',B(10,Mf),B(10,Mf)/10,6/B(10,Mf))
for cost in (4,3,2):
    lo=bisect(lambda r:B(r,.5)-cost,1,60)
    hi=bisect(lambda r:B(r,Mf)-cost,1,60)
    print('cost,window,ceiling gap',cost,lo,hi,risks(min(10/hi,1),1/hi)[1])
print('solver_A MAXIMUM B(M), r<=p:',.5+(5/7), 'at r>2 bound:',(3/8+(5/7)*1.5)/2)

def atom_w(atoms,r): return sum(prob*min(theta/r,1) for theta,prob in atoms)
print('Solver C NONMONOTONE D, RISING UNIFORM GAP')
for r in (2,3,3.6,5,9):
    WH=atom_w([(1.5,.4),(10,.6)],r);WL=atom_w([(1,.5),(2,.5)],r)
    print(r,WH-WL,.6-.9/r)
print('MULTIPLE PEAKS UNDER RANKED CLASSES')
for r in (2,5,10,20):
    WH=atom_w([(2,.5),(10,.5)],r);WL=atom_w([(1,.5),(5,.5)],r)
    print(r,risks(WH,WL,.7,.3))
print('RELATIVE RISK CAN FALL UNDER CLASS FOSD ALONE')
for r in (2,4,10):
    WH=atom_w([(2,.5),(10,.5)],r);WL=atom_w([(1,.5),(10,.5)],r)
    print(r,'WH,WL,Q,omega,gap,RR,OR',WH,WL,WH/WL,risks(WH,WL,.7,.3))
print('GENERAL INCUMBENT FOSD CAN LOWER RR WITH POINT CLASSES')
for WH,WL in ((1,.1),(.2,.1)): print(WH,WL,risks(WH,WL,.7,.3))
print('ASYMMETRIC PRIOR, NO RECRUITMENT: pi=.25,lambda=beta=rho=.25 except rho=.5,r=3,cH=1')
top,bottom=.4375,.125
WH,WL=2/3,1/3
wx=[WL+mu*(WH-WL) for mu in (bottom,.25,top)]
print('m,pi,M,second difference',bottom,.25,top,.5*(wx[2]-2*wx[1]+wx[0]),'KH,KL',.5*.5*(1-top),.5*.5*bottom)
print('SAME REDUCED AUCTION COORDINATES, DIFFERENT OMEGA')
L=(15+math.sqrt(331))/8; H=L+.75; r=.75*(2*L+.75)
print('first economy: delta=.25,gL=1.25,gH=1.75,omega=0')
print('second: L,H,r,delta,gL,gH,omega',L,H,r,.75-(point_profit(H,r)-point_profit(L,r)),point_profit(L,r),point_profit(H,r),(H-L)/r)

class Law:
    def __init__(self,mean,cdf,m1,m2): self.mean,self.cdf,self.m1,self.m2=mean,cdf,m1,m2
    def win(self,r): return self.m1(r)/r+1-self.cdf(r)
    def profit(self,r): return (self.m2(r)+2*r*(self.mean-self.m1(r))-r*r*(1-self.cdf(r))-.25)/(2*r)

def uniform(lo,hi):
    def q(r): return max(lo,min(hi,r))
    return Law((lo+hi)/2,lambda r:(q(r)-lo)/(hi-lo),lambda r:(q(r)**2-lo**2)/(2*(hi-lo)),lambda r:(q(r)**3-lo**3)/(3*(hi-lo)))

Phi=lambda z:.5*math.erfc(-z/math.sqrt(2))
def lognormal(scale,sigma):
    def moment(n,r):
        if r<=.5:return 0.
        return scale**n*math.exp(n*n*sigma*sigma/2)*Phi((math.log((r-.5)/scale)-n*sigma*sigma)/sigma)
    return Law(.5+scale*math.exp(sigma*sigma/2),lambda r:moment(0,r),lambda r:.5*moment(0,r)+moment(1,r),lambda r:.25*moment(0,r)+moment(1,r)+moment(2,r))

def exponential(scale):
    def moment(n,r):
        z=max(0.,(r-.5)/scale)
        return math.factorial(n)*scale**n*(1-math.exp(-z)*sum(z**j/math.factorial(j) for j in range(n+1)))
    return Law(.5+scale,lambda r:moment(0,r),lambda r:.5*moment(0,r)+moment(1,r),lambda r:.25*moment(0,r)+moment(1,r)+moment(2,r))

def smooth_result(label,GL,GH,peak_lo,density_peak):
    def omega(r):return GH.win(r)-GL.win(r)
    def margin(r):return GL.cdf(r)-GH.cdf(r)-omega(r)
    peak=bisect(margin,peak_lo,100)
    ceiling=bisect(lambda r:(1-Mf)*GL.profit(r)+Mf*GH.profit(r)-6,.501,200)
    gp=GH.profit(ceiling)-GL.profit(ceiling)
    delta=GH.mean-GL.mean-gp
    floor_return=.25*mf*delta
    print(label,'means',GL.mean,GH.mean,'D peak',density_peak,'winner peak',peak,'incumbent beats H at peak',1-GH.win(peak),'ceiling',ceiling,'full order return at ceiling',floor_return)
    for r in (1.2,3,3.6): print('  r,omega,D-omega,WH',r,omega(r),margin(r),GH.win(r))

print('SMOOTH CLASS CALIBRATIONS: EXACT TAIL MOMENTS, NO TRUNCATION')
for sigma in (.1,.3,.5,1.):
    smooth_result('literal Solver B lognormal sigma='+str(sigma),lognormal(.5,sigma),lognormal(9.5,sigma),2.7,.5+math.sqrt(4.75))
    fac=math.exp(-sigma*sigma/2)
    smooth_result('actual means (1,10), sigma='+str(sigma),lognormal(.5*fac,sigma),lognormal(9.5*fac,sigma),.5+math.sqrt(4.75)*fac,.5+math.sqrt(4.75)*fac)
for width in (.2,.5,.9):
    smooth_result('Solver B uniform width='+str(width),uniform(1-.5*width,1+.5*width),uniform(10*(1-width),10*(1+width)),max(1+.5*width,10*(1-width)),max(1+.5*width,10*(1-width)))
cross=.5+math.log(19)/(2-1/9.5)
smooth_result('shifted exponential',exponential(.5),exponential(9.5),cross,cross)
print('PAPER TABLE A6, UNIFORM CLASSES')
for label,GL,GH in [('narrow',uniform(.95,1.05),uniform(9.95,10.05)),('wide',uniform(.6,1.4),uniform(1,19))]:
    omega=lambda r:GH.win(r)-GL.win(r)
    peak=bisect(lambda r:GL.cdf(r)-GH.cdf(r)-omega(r),9.95 if label=='narrow' else 1.4,20)
    print(label,'peak,omega at peak',peak,omega(peak))
    for r in (1,3,3.6,4.5,5.5,19):
        print(' r,WH,WL,Q,omega,D,margin',r,GH.win(r),GL.win(r),GH.win(r)/GL.win(r),omega(r),GL.cdf(r)-GH.cdf(r),GL.cdf(r)-GH.cdf(r)-omega(r))
