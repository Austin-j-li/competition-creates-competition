"""Write the calculation receipt and print its location."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import mpmath


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    root=Path.cwd()
    folder=root/'audit/microstructure_search_2026_10_22/scripts/XE2_check'
    team=root/'audit/microstructure_search_2026_10_22'
    sources=[
        team/'TEAM_RULES.md',team/'EXTENSIONS_BRIEF.md',team/'BRIEF.md',
        team/'memos/E2_information_side.md',team/'memos/T2_liquidity_trader.md',
        team/'memos/X_check.md',
    ]+sorted((team/'scripts/E2_information_side').glob('*.py'))
    paper={}
    for name in ('main.tex','online_appendix.tex','tables/table_signal_grid.tex'):
        contents=subprocess.run(['git','-C','overleaf/paper','show',f'01bd5d6:{name}'],capture_output=True,check=True).stdout
        paper[name]={'size':len(contents),'sha256':sha256(contents).hexdigest()}
    results=[team/'memos/XE2_check.md']+sorted(p for p in folder.iterdir() if p.is_file() and p.name!='run_manifest.json')
    declaration={
        'recorded_utc':datetime.now(timezone.utc).isoformat(),
        'paper_commit':'01bd5d6daca14101afb3ef4b0c9e8035ba912181',
        'paper_blobs':paper,
        'inputs':{'h':'10','ell':'1','p':'1/2','rho':'1/4','c_H':'6','k':'1/50','pi':'1/2',
                  'strengths':['6/5','3','18/5'],
                  'cost_law':'rho*U[0,1/5]+(1-rho)*U[59/10,61/10]',
                  'calibration_A':{'lambda':'6/17','beta':'1/3'},
                  'calibration_B':'lambda=(e-1)b; b=(alpha_H(3)+alpha_L(3))/(1+e)',
                  'signals':{'rho':'17/20','c_H':'357/50','k':'3/200','r0':'11/10','r1':'23/10',
                             'a':'7/10','d':'3/4','accuracy_grid':'a=0.68..0.72, d=0.73..0.77, step 0.01'}},
        'method':['exact piecewise auction integration','finite joint law summation',
                  'direct unilateral order payoffs','exact rational root signs',
                  '70-digit arithmetic for calibration B','split cost quadrature and elementary antiderivatives'],
        'numerical_controls':{'decimal_digits':70,'root_sign_endpoints':['1.3939579202792','1.3939579202793'],
                              'coexistence_grid':'1.200 to 1.900, step 0.005',
                              'interval_certificate':False},
        'execution_order':['initial independent.py with all four headline calculations',
                           'E2 common.py, x1_fixed_information.py, x3_atomless_costs.py',
                           'independent.py label correction; domains.py; E2 x4_signals.py',
                           'E2 coexistence_general_prior.py; domains.py antiderivative extension'],
        'software':{'python':platform.python_version(),'mpmath':mpmath.__version__},
        'source_hashes':{str(p.relative_to(root)):digest(p) for p in sources},
        'artifact_hashes':{str(p.relative_to(root)):digest(p) for p in results},
        'outcome':'X1, X3, X4 confirmed; coexistence confirmed with correction',
    }
    path=folder/'run_manifest.json'
    path.write_text(json.dumps(declaration,indent=2)+'\n')
    print(path.relative_to(root))
    print('Artifacts:',len(results),'source files:',len(sources),'paper blobs:',len(paper))
    print('Folder bytes:',sum(p.stat().st_size for p in folder.rglob('*') if p.is_file()))


if __name__=='__main__':
    main()
