"""Read solver output and print compact research summaries. No assertions."""
import json
from pathlib import Path
from collections import Counter,defaultdict

HERE=Path(__file__).parent


def configs(name):
    for line in (HERE/name).open():
        x=json.loads(line)
        if x.get("kind")=="config":
            yield x


def brief(eq):
    return {k:eq[k] for k in ("a","b","strict","E","O_H","self_pool","beliefs")}


for name in ("equal_sweep.jsonl","up_sweep.jsonl","down_sweep.jsonl"):
    if not (HERE/name).exists(): continue
    count=Counter(); max_regret=0.; examples={}
    for x in configs(name):
        count['parameter_configs']+=1
        p=x['params']
        for m in x['menus']:
            count['local_root_calls']+=m['search']['local_root_calls']
            for row in m['grid']:
                count['games']+=1
                eq=row['equilibria']; strict=[v for v in eq if v['strict']]
                count['strict_equilibria']+=len(strict)
                count['conventional_equilibria']+=len(eq)
                count['games_no_strict']+=not strict
                count['games_no_conventional_found']+=not eq
                count['games_multiple_strict']+=len(strict)>1
                count['games_with_self_pool']+=any(v['self_pool'] for v in eq)
                for v in eq:
                    max_regret=max(max_regret,v['regret'])
                    for rule in ('all_L','all_H','max_deviation','prior'):
                        count['unsupported_'+rule]+=not v['beliefs'][rule]
                if not strict and 'no_strict' not in examples:
                    examples['no_strict']={'params':p,'menu':m['menu'],'k':row['k'],'equilibria':[brief(v) for v in eq]}
                if not eq and 'no_conventional_found' not in examples:
                    examples['no_conventional_found']={'params':p,'menu':m['menu'],'k':row['k']}
    print(json.dumps({'file':name,'counts':dict(count),'max_regret':max_regret,'examples':examples}))

for x in configs('equal_sweep.jsonl'):
    p=x['params']
    if p['r'] not in (1.2,3.,3.6,8.5): continue
    print(json.dumps({'benchmark':p,'menus':{m['menu']:[brief(v) for row in m['grid'] if abs(row['k']-.02)<1e-10 for v in row['equilibria']] for m in x['menus']}}))

# Consecutive grid segments at the benchmark trade cost. Each row preserves
# every distinct strict outcome, including alternative price pools.
groups=defaultdict(list)
for x in configs('equal_sweep.jsonl'):
    p=x['params']
    for m in x['menus']:
        row=next(z for z in m['grid'] if abs(z['k']-.02)<1e-10)
        sig=tuple(sorted((round(v['a'],6),round(v['b'],6),round(v['E'],9),round(v['O_H'],9),v['self_pool']) for v in row['equilibria'] if v['strict']))
        groups[(p['c_L'],p['lam'],m['menu'])].append((p['r'],sig))
for key,rows in groups.items():
    segments=[]
    for r,sig in sorted(rows):
        if not segments or segments[-1]['outcomes']!=sig:
            segments.append({'r_first':r,'r_last':r,'outcomes':sig})
        else:
            segments[-1]['r_last']=r
    print(json.dumps({'segments':{'c_L':key[0],'lambda':key[1],'menu':key[2]},'grid_intervals':segments}))
