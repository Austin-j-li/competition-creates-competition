"""Print exact examples relevant to the manuscript statements; no assertions."""
from fractions import Fraction as Q

# The fixed-information proposition fixes (class,S), but says nothing about R|S.
# Class values are 12 and 11, the class prior is 1/2, p=1/2, and C is 0 or 6.
# R0 is an equal mixture of U[0,1] and U[8,9]; S reports its component.
# R1 is an equal mixture of U[0,1] and U[9,10]; S is independent of its component.
# Both S and the class are independent fair bits in each economy.
mean_theta=Q(23,2)
low_expected_payment=Q(1,2)**2+Q(1,2)*(1-Q(1,2)**2)
rent0_low=mean_theta-low_expected_payment
rent0_high=mean_theta-Q(17,2)
rent1=mean_theta-(low_expected_payment+Q(19,2))/2
print('CONTROL: E[max(p,R)] for U[0,1]:',low_expected_payment)
print('CONTROL: F0 rents conditional on S:',rent0_low,rent0_high)
print('CONTROL: F1 rent at either S:',rent1)
print('CONTROL: entry with rho=1/4 and high cost=6:',Q(1,4)+Q(3,4)/2,Q(1))

# Jensen gives weak gains. Values all above r lie on the affine profit kernel.
r,p=Q(3),Q(1,2)
tH=r/2+p*p/(2*r)
print('DISPERSION: gross rent of point 10:',10-tH)
print('DISPERSION: mean gross rent of U[199/20,201/20]:',Q(10)-tH)

# A rational witness fills the last logical step of the signal proposition.
# It uses the S(B) vector and the rational slot lambda=1/3, beta=3/10.
a,d,rho,cost,k=Q(7,10),Q(3,4),Q(17,20),Q(357,50),Q(3,200)
M,m=Q(8,11),Q(3,11)
def auction(r):
    t0=p*(1-p/r);th=r/2+p*p/(2*r);tl=1-(1-p*p)/(2*r)
    return th-tl,th-t0,10-th,1-tl
def B(r,mu):
    D,wH,gH,gL=auction(r)
    return gL+mu*(gH-gL)
def phi(mu,yes=True):
    z=d if yes else 1-d
    return z*mu/(z*mu+(1-z)*(1-mu))
r0,r1=Q(11,10),Q(23,10)
muplus=1-a+(2*a-1)*M
D0,wH0,_,_=auction(r0)
D1,_,_,_=auction(r1)
margins=[cost-B(r0,d),B(r1,phi(muplus))-cost,
         k-(2*a-1)*(D0+(1-rho)*(2*d-1)*wH0),
         (2*a-1)*rho*m*D1-k,cost-B(r1,phi(muplus,False))]
print('SIGNAL WITNESS: a_T,d:',a,d,'lambda,beta:',Q(1,3),Q(3,10))
print('SIGNAL WITNESS: private,joint,weak,strong,other-pair margins:',margins)
print('SIGNAL WITNESS: decimal margins:',[float(x) for x in margins])

# The actual signal tuple in A.6 quotes a gross return as a payoff.
ratio=Q(4,3)
gross=Q(1,15)/(2+ratio)
print('SALE: t/b=',ratio,'printed expression=',gross,'net payoff=',gross-Q(1,50))
