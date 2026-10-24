"""Replay the independently derived profiles through the source interfaces."""
from fractions import Fraction as F
from pathlib import Path
import sys

sys.path.insert(0,str(Path('audit/microstructure_search_2026_10_22/scripts/N4_strategic_traders').resolve()))
from common import objects, LAM, BETA
from n41_holder import verify
from n42_challenger import enumerate_all, eta_fixed_b, chall_types
from slot3 import engine, informed_ok, third_ok, chall_ok

print('PARTIAL INFORMED PURCHASES OMITTED BY THE HOLDER CANDIDATE LIST')
for r,s,e in [(F(31,20),F(5093,10026),F(195548,336985)),
              (F(8,5),F(517,999),F(2528,4995)),
              (F(33,20),F(38819,73638),F(1545852,3456895))]:
    ev,h,l,u,c=verify(objects(r),LAM,BETA,F(7,50),s,F(0),F(0),F(0),{1:e},'IM','CM')
    print('r',r,'best responses H,L,holder,challenger:',h,l,u,c,'entry',ev['E'])

print('\nPARTIAL INFORMED PURCHASES OMITTED BY THE CHALLENGER SEARCH')
chi=F(9,100);s=F(84493,172800);t=F(1);o=objects(F(3))
types=chall_types(o,1,-1)
ev=engine(o,LAM,chi,eta_fixed_b(LAM,chi,BETA),s,t,types)
print('best responses H,L:',informed_ok(ev,s,t))
print('best responses of challenger types:',third_ok(ev,types))
print('preparation condition:',chall_ok(o,ev))
print('entry:',ev['E'])
print('source enumeration at the same presence:')
enumerate_all(F(3),LAM,chi,BETA)
