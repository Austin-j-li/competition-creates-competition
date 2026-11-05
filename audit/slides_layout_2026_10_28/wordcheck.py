"""Print, page by page, the words that differ between two builds of the deck.

Usage: python3 -I wordcheck.py OLD.pdf NEW.pdf
Each page is read with pdftotext, split into words, and compared as a multiset, so line breaks and
hyphenation do not count. Footline tokens (author, short title, page counters) are dropped.
"""
import collections
import re
import subprocess
import sys
import unicodedata

OLD, NEW = sys.argv[1], sys.argv[2]
FOOT = {"Austin", "Li", "Competition", "Creates", "·", "/", "•"}


def pages(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    out = []
    for p in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"], capture_output=True, text=True).stdout
        t = "".join(c for c in unicodedata.normalize("NFKC", t) if not unicodedata.combining(c))
        words = re.findall(r"\S+", t)
        # join hyphenated line ends: a word ending in '-' followed by the next word
        joined = []
        skip = False
        for i, w in enumerate(words):
            if skip:
                skip = False
                continue
            if w.endswith("-") and i + 1 < len(words) and w != "-":
                joined.append(w[:-1] + words[i + 1])
                skip = True
            else:
                joined.append(w)
        out.append(collections.Counter(x for x in joined if x not in FOOT and not re.fullmatch(r"\d+", x)))
    return out


a, b = pages(OLD), pages(NEW)
print(f"old pages {len(a)}, new pages {len(b)}")
total = 0
for i, (x, y) in enumerate(zip(a, b), 1):
    lost, gained = x - y, y - x
    if lost or gained:
        total += 1
        print(f"page {i}: lost {dict(lost)}  gained {dict(gained)}")
print(f"{total} pages differ in word multiset")
