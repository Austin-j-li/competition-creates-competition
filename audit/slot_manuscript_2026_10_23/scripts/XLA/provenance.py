"""Print local Git evidence for the manuscript and numerical layers.

The program reads committed files. It does not run an exercise or contact a remote.
"""
import csv
import hashlib
import io
import json
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT/'overleaf/paper'
REF = 'revision/alex-2026-10-21'


def git(repo, *args):
    return subprocess.check_output(['git','-C',str(repo),*args])


def source(repo, ref, file):
    return git(repo,'show',f'{ref}:{file}')


def rows(ref, file):
    return list(csv.DictReader(io.StringIO(source(ROOT,ref,file).decode())))


print('Parent main',git(ROOT,'rev-parse','main').decode().strip())
print('Numerical revision',git(ROOT,'rev-parse',REF).decode().strip())
print('Manuscript pin',git(PAPER,'rev-parse','01bd5d6').decode().strip())
for ref in ('main',REF):
    print('\nREF',ref)
    paths = git(ROOT,'ls-tree','-r','--name-only',ref,'numerics/manifests').decode().splitlines()
    for path in paths:
        if path.endswith('.json'):
            doc=json.loads(source(ROOT,ref,path))
            if doc.get('exercise','').startswith('c'):
                costs = {key:value['c_L'] for key,value in doc.get('inputs',{}).items()
                         if isinstance(value,dict) and 'c_L' in value}
                print(path,doc.get('timestamp_utc'), 'passed',doc.get('passed'), 'low costs',costs)
    for row in rows(ref,'tables/equilibrium_controls.csv'):
        if (Fraction(row['r'])==3 and row['experiment']=='feedback' and row['accepted']=='true'
                and row['noise']=='Laplace' and row['cost_law']=='atoms'):
            print('Feedback r=3', {key:row[key] for key in ('E','O_H','R_T','W','expected_preparation_cost')})

print('\nPinned tables versus numerical revision: SHA256')
paths=git(PAPER,'ls-tree','-r','--name-only','01bd5d6','tables').decode().splitlines()
for path in paths:
    old=source(PAPER,'01bd5d6',path)
    new=source(ROOT,REF,path)
    print(path,hashlib.sha256(old).hexdigest(),hashlib.sha256(new).hexdigest(),'same_bytes',old==new)

print('\nCertificate field differences: parent main versus numerical revision')
old,new=rows('main','numerics/certificates.csv'),rows(REF,'numerics/certificates.csv')
for a,b in zip(old,new):
    print('r',a['r'],{key:(a.get(key),b.get(key)) for key in a.keys()|b.keys() if a.get(key)!=b.get(key)})

print('\nAncestry, local refs only')
for parent in ('main','origin/main'):
    status=subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',REF,parent],check=False).returncode
    print(f'{REF} ancestor of {parent}:', status==0)
print('Remote tracking refs that contain the revision:',git(ROOT,'branch','-r','--contains',REF).decode().strip())
print('Manuscript top level:',git(PAPER,'ls-tree','--name-only','01bd5d6').decode().strip())
