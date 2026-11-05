exec(open('/tmp/ccc_wa/w3.py').read().split("# Counterexample")[0])
import math
beta=0.294655; u=math.e-1; cap=u*beta/(1+u*beta)
print('cap',cap,'M_cap',M_(cap,beta))
scan('bench',6.,.25,.02,beta,1/40,cap,[1.5+0.05*i for i in range(60)])
