exec(open('/tmp/ccc_wa/w3.py').read().split("# Counterexample")[0])
import random
random.seed(1)
found=0
for it in range(20000):
    rho=random.uniform(.02,.9); k=random.uniform(.01,1); beta=random.uniform(.05,.45)
    a=10**random.uniform(-3,1); cap=random.uniform(.05,.95); cH=random.uniform(.5,8.5)
    Ds=[0.01+9*i/900 for i in range(899)]
    rec=[]
    for D in Ds:
        tau=cH/(9-D)
        if tau<=.5 or tau>=1 or D<=2*k: rec.append(0); continue
        L=Lam(D,rho,k,beta,a,cap)
        rec.append(1 if M_(L,beta)>=tau else 0)
    comps=sum(1 for i in range(1,len(rec)) if rec[i]==1 and rec[i-1]==0)+(rec[0]==1)
    if comps>=2:
        found+=1
        if found<=5:
            segs=[];st=None
            for i,v in enumerate(rec):
                if v and st is None: st=Ds[i]
                if not v and st is not None: segs.append((round(st,3),round(Ds[i-1],3))); st=None
            if st is not None: segs.append((round(st,3),round(Ds[-1],3)))
            print(dict(rho=round(rho,3),k=round(k,3),beta=round(beta,3),a=round(a,4),cap=round(cap,3),cH=round(cH,3)),segs)
print('found',found)
