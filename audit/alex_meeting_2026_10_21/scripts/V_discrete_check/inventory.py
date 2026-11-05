"""Print hashes and completion records for the research calculation."""
from pathlib import Path
import hashlib
import json
import time

base=Path(__file__).resolve().parent
audit=base.parent.parent
inputs=[audit/'BRIEF.md']+[audit/'memos'/n for n in ('Q2_discrete_buy_only.md','Q2_discrete_sell_only.md','Q2_discrete_literature.md','LIT_extracts.md')]
def record(path):
    digest=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
    return {'path':str(path),'bytes':path.stat().st_size,'sha256':digest.hexdigest()}
outputs=[p for p in sorted(base.iterdir()) if p.is_file() and p.name!='receipt.json']
complete={}
for name in ('equal_sweep.jsonl','up_sweep.jsonl','down_sweep.jsonl','up_empty_resultants.jsonl'):
    last=None
    with (base/name).open() as f:
        for line in f:last=json.loads(line)
    complete[name]=last
print(json.dumps({'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                  'inputs_at_final_read':[record(p) for p in inputs],
                  'memo':record(audit/'memos'/'V_discrete_check.md'),
                  'outputs':[record(p) for p in outputs],
                  'completion_records':complete,
                  'scope':'Independent print-only research computation. No assertions or test suites.'},indent=2))
