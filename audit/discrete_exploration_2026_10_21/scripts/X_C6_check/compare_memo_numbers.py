# Print-only helper: list every long decimal in the memo and say whether my output or the author's output holds it.
# A match means: the absolute value of some printed number, rounded to the memo's digits, equals the memo's number within one unit of the last digit.
# Absolute values are used because the memo states losses as positive amounts.
# Run: .venv/bin/python audit/discrete_exploration_2026_10_21/scripts/X_C6_check/compare_memo_numbers.py
import re
from decimal import Decimal, ROUND_HALF_UP, getcontext

getcontext().prec = 120

BASE = "audit/discrete_exploration_2026_10_21/"
MEMO = BASE + "memos/C6_info_acquisition.md"
FILES = {"mine": BASE + "scripts/X_C6_check/output.txt", "author": BASE + "scripts/C6_info_acquisition/results.txt"}

num_re = re.compile(r"-?\d+\.\d+(?:[eE][-+]?\d+)?")
pool = {}
for tag, path in FILES.items():
    vals = []
    for line in open(path):
        for tok in num_re.findall(line):
            try:
                vals.append(Decimal(tok))
            except Exception:
                pass
    pool[tag] = vals

memo_lines = open(MEMO).read().splitlines()
long_re = re.compile(r"(?<![\d.])(\d+\.\d{8,})")
sci_re = re.compile(r"(\d\.\d+)\\times10\^\{-(\d+)\}")

def found_in(tag, x, d):
    unit = Decimal(10) ** (-d)
    for y in pool[tag]:
        y = abs(y)
        yr = y.quantize(unit, rounding=ROUND_HALF_UP) if y < 10 ** 6 else y
        if abs(yr - x) <= unit:
            return True
    return False


def found_sci(tag, mant, ex):
    x = Decimal(mant) * Decimal(10) ** (-int(ex))
    d = len(mant.split(".")[1])
    return any(y != 0 and abs(y - x) <= Decimal(10) ** (-int(ex) - d) for y in pool[tag])


rows = []
for i, line in enumerate(memo_lines, 1):
    for tok in long_re.findall(line):
        x, d = Decimal(tok), len(tok.split(".")[1])
        rows.append((i, tok, {tag: found_in(tag, x, d) for tag in pool}))
    for mant, ex in sci_re.findall(line):
        rows.append((i, mant + "e-" + ex, {tag: found_sci(tag, mant, ex) for tag in pool}))

print(f"long decimals in the memo: {len(rows)}")
for tag in pool:
    print(f"   found in the {tag} output: {sum(1 for r in rows if r[2][tag])}")
print(f"   found in either: {sum(1 for r in rows if any(r[2].values()))}")
for i, tok, hit in rows:
    if not hit["author"]:
        print(f"   not in the author's output: line {i}: {tok}  (in mine: {hit['mine']})")
