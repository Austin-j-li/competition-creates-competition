"""Exact profiles at the two stake endpoints and the pure-purchase example."""
from fractions import Fraction as F
from independent import auction, holder_profile, holder_thresholds, L, B, C, RHO, K, show

left=holder_thresholds(F(33,20))[0]
right=holder_thresholds(F(31,20))[3]
print('LOWER STAKE ENDPOINT: TWO FULL-PURCHASE INFORMATIVE OUTCOMES AT 1.65')
r=F(33,20);a=auction(r);cap=holder_thresholds(r)[2]
e=(K+RHO*left*a['w'])/(left*a['w']-a['d']*(a['tau']-F(1,2)))
holder_profile(r,left,F(1),F(0),F(0),F(1))
holder_profile(r,left,F(1),F(0),cap,e)

print('\nUPPER STAKE ENDPOINT: THREE POINTS ON THE CONTINUUM AT 1.55')
r=F(31,20);a=auction(r)
s0=B*(2*a['tau']-1)/(L*(1-a['tau']))
e=K/(a['d']*(1-a['tau']))
for s in [s0,(s0+1)/2,F(1)]:
    m=(L*s*(1-a['tau'])/(2*a['tau']-1)-B)/C
    holder_profile(r,right,s,F(0),m,e)

print('\nI0: BOTH FREE ABSTENTION AND PURE PURCHASE AT STAKE 0.1, STRENGTH 1.47')
r=F(147,100)
show('Omega1',holder_thresholds(r)[0])
show('Omega2',holder_thresholds(r)[1])
holder_profile(r,F(1,10),F(1),F(0),F(0),F(1))
holder_profile(r,F(1,10),F(1),F(0),F(1),F(1))
