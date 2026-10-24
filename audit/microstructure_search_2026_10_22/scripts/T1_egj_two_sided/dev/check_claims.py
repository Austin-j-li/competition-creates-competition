"""Print-only check of three memo statements against the bench scan."""
import sys
from fractions import Fraction as F
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from t1_summarize import load
data, und = load('bench')
r1 = F(3)
none_Z = {(k[0], k[1]) for k, e in data.items() if k[2] == r1 and k[3] == 'ZE_IC' and not e}
uniqM = {(k[0], k[1]): e[0]['label'] for k, e in data.items() if k[2] == r1 and k[3] == 'MX_IC' and len(e) == 1}
mixing_unique = {key for key, lab in uniqM.items() if 'partial' in lab}
print('rule Z, r1: points without equilibrium:', len(none_Z))
print('rule M, r1: points whose unique equilibrium has a mixing class:', len(mixing_unique))
print('identical sets:', none_Z == mixing_unique)
print('labels in the mixing set:', sorted({uniqM[k] for k in mixing_unique}))
print('Z-empty points outside the mixing set:', sorted((float(a), float(b)) for a, b in none_Z - mixing_unique))
R3 = (F(31, 20), F(8, 5), F(33, 20))
part = []
for th in sorted({k[0] for k in data}):
    if th < F(13, 50):
        continue
    for lam in sorted({k[1] for k in data}):
        co = [any(q['label'] == 'NT' for q in data[(th, lam, r, 'MX_IC')]) and any(q['label'] != 'NT' for q in data[(th, lam, r, 'MX_IC')]) for r in R3]
        if any(co):
            part.append((float(th), float(lam), co))
print('theta >= 0.26 with coexistence at some of 1.55/1.60/1.65:', part)
