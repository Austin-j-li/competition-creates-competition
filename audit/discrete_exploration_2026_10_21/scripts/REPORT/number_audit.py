"""Print every decimal number in the report that does not appear in the memos, the ledger,
or the chart-value output. Print only."""
import glob
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))
team = os.path.dirname(os.path.dirname(here))
page = open(sys.argv[1], encoding="utf-8").read()
srcs = []
for f in sorted(glob.glob(os.path.join(team, "memos", "*.md"))) + [os.path.join(team, "LEDGER.md"),
                                                                    os.path.join(team, "BRIEF.md"),
                                                                    os.path.join(here, "chart_values.out.txt")]:
    srcs.append(open(f, encoding="utf-8").read())
corpus = "\n".join(srcs)
nums = sorted(set(re.findall(r"(?<![\w.])\d+\.\d+", page)), key=float)
missing = [x for x in nums if not re.search(r"(?<![\d.])" + re.escape(x), corpus)]
print("decimal numbers on the page:", len(nums))
print("not found in any source:", missing if missing else "none")
for x in missing:
    for m in re.finditer(r"(?<![\d.])" + re.escape(x), page):
        print("   %s: ...%s..." % (x, re.sub(r"<[^>]+>", "", page[max(0, m.start() - 90):m.end() + 30]).replace("\n", " ")))
