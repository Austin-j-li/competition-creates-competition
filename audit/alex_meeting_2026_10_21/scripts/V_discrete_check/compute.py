"""Print-only consumer interface for the independent finite-game solver.

Examples:
  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py point --r 3 --lam .8
  .venv/bin/python audit/alex_meeting_2026_10_21/scripts/V_discrete_check/compute.py sweep --jobs 5

Standard output is JSON Lines. Redirect it only inside this script directory.
"""
from __future__ import annotations
import argparse
from dataclasses import asdict, replace
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np
import scipy
from solver import Params, Game, full_simplex_audit, equilibrium_candidates, auction

NOISE={"equal":(1/3,1/3,1/3),"up":(.1,.2,.7),"down":(.7,.2,.1)}
RULES=("directional","all_L","all_H","max_deviation","prior")


def print_record(x):
    print(json.dumps(x,separators=(",",":"),allow_nan=False),flush=True)


def compact_equilibrium(g:Game,k:float,row:dict,details:bool=False) -> dict:
    a,b=row["a"],row["b"]
    belief={}
    on=~np.isin(g.flows,row["off"])
    for rule in RULES:
        supported=[]
        for s in g.full_partitions(a,b,rule):
            if not np.allclose(np.asarray(s["entry_rates"])[on],np.asarray(row["entry_rates"])[on],atol=1e-12,rtol=0):
                continue
            ok,strict,_=g.optimal(a,b,k,s)
            if ok:
                supported.append({"strict":strict,"off_prices":[s["price"][i] for i in np.flatnonzero(~on)]})
        belief[rule]=supported if details else bool(supported)
    out={"a":a,"b":b,"strict":row["strict"],"E":row["E"],"O_H":row["O_H"],
         "entry_rates":row["entry_rates"],"self_pool":row["self_pool"],"beliefs":belief,"regret":row["regret"]}
    if details:
        out.update({key:row[key] for key in ("partition","price_beliefs","mu","price","gross","off")})
        out["net_payoffs"]=(np.asarray(row["gross"])-k*np.abs(g.actions)[None,:]).tolist()
    return out


def one_config(task):
    p,ks,mesh,detail,menus=task
    started=time.monotonic(); result=[]
    for menu in menus:
        g=Game(p,menu)
        eq,continua,search=equilibrium_candidates(g,np.array(ks),mesh)
        rows=[]
        for k,equilibria in eq.items():
            # Off-path partitions can differ without a different on-path outcome.
            seen=set(); outcomes=[]
            for row in equilibria:
                key=(round(row["a"],8),round(row["b"],8),tuple(row["entry_rates"][i] for i,x in enumerate(g.flows) if x not in row["off"]))
                if key in seen: continue
                seen.add(key)
                outcomes.append(compact_equilibrium(g,k,row,detail))
            rows.append({"k":k,"equilibria":outcomes})
        result.append({"menu":menu,"flows":g.flows.tolist(),"search":search,"grid":rows,"continua":continua})
    return {"kind":"config","params":asdict(p),"menus":result,"seconds":time.monotonic()-started}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode",choices=("point","sweep","simplex","special"))
    parser.add_argument("--r",type=float,default=3.)
    parser.add_argument("--lam",type=float,default=1.)
    parser.add_argument("--cl",type=float,default=1.)
    parser.add_argument("--ch",type=float,default=6.)
    parser.add_argument("--k",type=float,nargs="+",default=[.02])
    parser.add_argument("--noise",choices=NOISE,default="equal")
    parser.add_argument("--mesh",type=int,default=40)
    parser.add_argument("--rstep",type=float,default=.05)
    parser.add_argument("--jobs",type=int,default=1)
    parser.add_argument("--menus",nargs="+",default=["M1","M2","M3"])
    args=parser.parse_args()
    p=Params(r=args.r,lam=args.lam,c_L=args.cl,c_H=args.ch,noise=NOISE[args.noise])
    print_record({"kind":"manifest","arguments":vars(args),"numpy":np.__version__,"scipy":scipy.__version__,
                  "python":sys.version,"utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
                  "source_sha256":{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in Path(__file__).parent.glob("*.py")},
                  "status":"numerical diagnostic","payoff_tolerance":2e-9,
                  "entry_equality_roundoff":2e-13,"full_simplex_mesh":args.mesh,
                  "root_method":"fine grid; all entry regimes and price partitions; quadratic edge roots; local interior roots",
                  "limit":"local root search is not an algebraic completeness certificate"})
    if args.mode=="simplex":
        for lam in (1.,.5,.7,.8,.9):
            for noise in NOISE.values():
                for menu in args.menus:
                    print_record({"kind":"full_simplex",**full_simplex_audit(replace(p,lam=lam,noise=noise),menu,args.mesh)})
        return
    if args.mode=="point":
        print_record(one_config((p,args.k,args.mesh,True,args.menus)))
        return
    if args.mode=="special":
        # Independent counterexamples and exact boundary calculations.
        rt=1+.24+np.sqrt(.24**2+.48)
        rc=4+np.sqrt(16-.25)
        cases=[("buy_cutoff",replace(p,r=rt,lam=1.),[.02]),
               ("two_sided_cutoff",replace(p,r=3,lam=1.),[1/36,1/18,.04]),
               ("price_pool",replace(p,r=3,lam=.8),[.02,.04,.05]),
               ("highcost_crossing",replace(p,r=rc,lam=1.),[.02]),
               ("highcost_after",replace(p,r=rc+1e-6,lam=1.),[.02]),
               ("floor_crossing",replace(p,r=3,lam=1.,c_L=.125),[.02]),
               ("buy_pool",replace(p,r=3,lam=1.,c_L=3.),[.02]),
               ("buy_pool_later",replace(p,r=3.1,lam=1.,c_L=3.),[.02]),
               ("up_noise",replace(p,r=2+np.sqrt(3),lam=1.,c_L=.02,noise=NOISE["up"]),[.045]),
               ("down_noise",replace(p,r=2+np.sqrt(3),lam=1.,c_L=.02,c_H=12.,noise=NOISE["down"]),[.08])]
        for name,cp,ks in cases:
            result=one_config((cp,ks,args.mesh,True,args.menus)); result["case"]=name
            print_record(result)
        return
    ks=list(np.round(np.arange(.0025,.100001,.0025),8))+[.125,.15,.2,.25,.5]
    rs=np.round(np.arange(1.05,9.950001,args.rstep),8)
    rs=np.unique(np.r_[rs,1.2,3.,3.6,8.5])
    tasks=[(replace(p,r=float(r),lam=lam,c_L=cl),ks,args.mesh,False,args.menus)
           for cl in (1.,.02) for lam in (1.,.5,.7,.8,.9) for r in rs]
    print_record({"kind":"grid_declaration","r":rs.tolist(),"k":ks,"lambda":[1.,.5,.7,.8,.9],
                  "c_L":[1.,.02],"noise":p.noise,"configurations":len(tasks),"menus":args.menus})
    if args.jobs>1:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            for result in pool.map(one_config,tasks,chunksize=1):
                print_record(result)
    else:
        for task in tasks:
            print_record(one_config(task))
    print_record({"kind":"complete","configurations":len(tasks)})


if __name__=="__main__":
    main()
