import sys; sys.path.insert(0,'/tmp/ccc_wa')
from own import *
import itertools
# point masses h=10,l=1,p=.5, U[0,r]; scan r in (h, 40]; count branch points with W_H<1 and sign of dO/dr
rows=[];tot=0;fall=0;rise=0
for rho,k,a,beta,cH in itertools.product([.02,.05,.1,.25],[.02,.05,.1,.2,.5,1,2],[.01,.1,.5,1,5],[.1,.2,.3,1/3],[1,2,2.5,3,4,5,6]):
    P=dict(h=10,l=1,p=.5,cH=cH,rho=rho,k=k,beta=beta,a=a,cap=.9)
    pts=[10+0.25*i for i in range(1,121)]
    for r in pts:
        s=state(r,P)
        if not s.get('branch'): continue
        s2=state(r+1e-4,P)
        if not s2.get('branch'): continue
        tot+=1
        d=s2['own']-s['own']
        if d<0: fall+=1
        else: rise+=1
        rows.append((rho,k,a,beta,cH,r,d>0,s['lamR'],s['WH']))
print('branch pts r>h:',tot,'fall',fall,'rise',rise)
# which parameter combos have rising ownership beyond h?
ups=[x for x in rows if x[6]]
import collections
print(collections.Counter((x[0],x[1],x[2]) for x in ups).most_common(15))
print('min k/rho among branch pts r>h:',min(x[1]/x[0] for x in rows))
