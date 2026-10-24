"""Print a second computation of interior roots through quadratic resultants.

This is a numerical elimination calculation, not a symbolic certificate.
It supplements the simplex grid on cases where no conventional root was found.
"""
from __future__ import annotations
import argparse
from itertools import permutations
import json
import numpy as np
from scipy.optimize import root
from solver import Params,Game,regions,cleared_equations


def minimal_equations(g,e,k,a,b):
    v=np.array([1.,a,b]);h=g.H@v;l=g.L@v;d=h+l
    out=[]
    for flows,weights,num in (((0,1),g.buy,l),((-1,0),g.sell,h)):
        ix=[i for i,x in enumerate(g.flows) if x in flows and e[i]*weights[i]>0]
        if not ix:
            out.append(k)
        elif len(ix)==1:
            i=ix[0];out.append(k*d[i]-g.delta*weights[i]*e[i]*num[i])
        else:
            i,j=ix
            out.append(k*d[i]*d[j]-g.delta*(weights[i]*e[i]*num[i]*d[j]+weights[j]*e[j]*num[j]*d[i]))
    return np.array(out)


def trim(v):
    out=np.asarray(v,dtype=float)
    while len(out)>1 and abs(out[-1])<1e-11:
        out=out[:-1]
    return out


def coefficients(fn):
    z=fn(0.,0.)
    pa,ma=fn(1.,0.),fn(-1.,0.)
    pb,mb=fn(0.,1.),fn(0.,-1.)
    a,aa=(pa-ma)/2,(pa+ma)/2-z
    b,bb=(pb-mb)/2,(pb+mb)/2-z
    ab=fn(1.,1.)-z-a-b-aa-bb
    scale=max(abs(z),abs(a),abs(b),abs(aa),abs(ab),abs(bb),1e-20)
    return [trim(np.array([z,a,aa])/scale),trim(np.array([b,ab])/scale),trim(np.array([bb])/scale)]


def determinant(matrix):
    n=len(matrix); value=np.array([0.])
    for perm in permutations(range(n)):
        inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
        term=np.array([(-1.)**inversions])
        for i,j in enumerate(perm):
            term=np.polynomial.polynomial.polymul(term,matrix[i][j])
        value=np.polynomial.polynomial.polyadd(value,term)
    return trim(value)


def real_roots(c):
    c=trim(c)
    if len(c)<2: return []
    return [float(v.real) for v in np.polynomial.polynomial.polyroots(c) if abs(v.imag)<2e-5 and -1e-7<=v.real<=1+1e-7]


def interior_roots(g,e,k):
    p=coefficients(lambda a,b:minimal_equations(g,e,k,a,b)[0])
    q=coefficients(lambda a,b:minimal_equations(g,e,k,a,b)[1])
    while len(p)>1 and np.max(abs(p[-1]))<1e-11: p.pop()
    while len(q)>1 and np.max(abs(q[-1]))<1e-11: q.pop()
    m,n=len(p)-1,len(q)-1
    if m==0 and n==0:
        return [],"degenerate_vertical_curve"
    matrix=[[np.array([0.]) for _ in range(m+n)] for _ in range(m+n)]
    for i in range(n):
        for j,v in enumerate(p[::-1]): matrix[i][i+j]=v
    for i in range(m):
        for j,v in enumerate(q[::-1]): matrix[n+i][i+j]=v
    resultant=determinant(matrix)
    if np.max(abs(resultant))<1e-10:
        return [],"zero_resultant"
    result=[]
    for a in real_roots(resultant):
        ps=np.array([np.polynomial.polynomial.polyval(a,v) for v in p])
        qs=np.array([np.polynomial.polynomial.polyval(a,v) for v in q])
        for b in real_roots(ps)+real_roots(qs):
            sol=root(lambda v:minimal_equations(g,e,k,float(v[0]),float(v[1])),[a,b],tol=1e-12)
            u,v=map(float,sol.x)
            if not(-1e-8<=u<=1+1e-8 and -1e-8<=v<=1+1e-8): continue
            u,v=float(np.clip(u,0,1)),float(np.clip(v,0,1))
            if max(abs(float(w)-k) for w in g.gross_at(u,v,e))>2e-9: continue
            if not g.rates_feasible(u,v,e): continue
            if any(max(abs(u-x),abs(v-y))<1e-7 for x,y in result):continue
            result.append((u,v))
    return result,"isolated"


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('input')
    args=parser.parse_args()
    total=0
    for line in open(args.input):
        x=json.loads(line)
        if x.get('kind')!='config':continue
        p=Params(**{**x['params'],'noise':tuple(x['params']['noise'])})
        for m in x['menus']:
            if m['menu']!='M3':continue
            missing=[r['k'] for r in m['grid'] if not r['equilibria']]
            if not missing:continue
            g=Game(p,'M3'); regs=regions(g)
            for k in missing:
                found=[]; degeneracies=[]
                for e,poly in regs:
                    pairs,status=interior_roots(g,e,k)
                    if status!='isolated':degeneracies.append({'rates':e.tolist(),'status':status})
                    for a,b in pairs:
                        for s in g.full_partitions(a,b):
                            ok,strict,regret=g.optimal(a,b,k,s)
                            if ok:found.append({'a':a,'b':b,'strict':strict,'E':s['E'],'O_H':s['O_H'],'self_pool':s['self_pool'],'regret':regret})
                total+=1
                print(json.dumps({'params':x['params'],'k':k,'extra_roots':found,'degeneracies':degeneracies}),flush=True)
    print(json.dumps({'kind':'complete','cases':total}),flush=True)


if __name__=='__main__': main()
