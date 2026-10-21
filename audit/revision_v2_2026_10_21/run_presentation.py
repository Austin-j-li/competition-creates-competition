"""Run the project presentation sequence and numerical release gates."""
from pathlib import Path
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
(HERE / 'logs').mkdir(parents=True, exist_ok=True)
label = sys.argv[1] if len(sys.argv) > 1 else 'first'
env = dict(os.environ)
env.update({key:'1' for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
env.update(SOURCE_DATE_EPOCH='1788652800',PYTHONHASHSEED='0',TZ='UTC')
import pypandoc
env['PATH'] = str(Path(pypandoc.get_pandoc_path()).parent) + os.pathsep + env.get('PATH','')
commands = [
    ['numerics/check_registry.py'],
    ['numerics/registry.py'],
    ['numerics/substitute.py'],
    ['numerics/render/render_all.py'],
    ['numerics/render/latex.py'],
    ['audit/revision_v2_2026_10_21/reconcile.py'],
    ['numerics/verify.py','--final'],
    ['numerics/release_checks.py'],
]
records = []
for arguments in commands:
    command = [sys.executable,*arguments]
    start = time.monotonic()
    log = HERE/'logs'/f'{label}_{Path(arguments[0]).stem}.log'
    print('RUN', ' '.join(command), flush=True)
    with log.open('w') as stream:
        result = subprocess.run(command,cwd=ROOT,env=env,stdout=stream,stderr=subprocess.STDOUT)
    record = {'command':command,'cwd':str(ROOT),'exit_code':result.returncode,
              'elapsed_seconds':time.monotonic()-start,'log':str(log.relative_to(ROOT))}
    records.append(record)
    (HERE/f'presentation_{label}_runs.json').write_text(json.dumps(records,indent=2)+'\n')
    print(record,flush=True)
    if result.returncode:
        sys.exit(result.returncode)
print('Presentation sequence and both numerical gates passed.',flush=True)
