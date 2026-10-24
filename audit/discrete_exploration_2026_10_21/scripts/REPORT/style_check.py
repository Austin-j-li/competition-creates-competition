"""Print sentences over 25 words and -ing tokens in the report's visible text. Print only."""
import re
import sys
from html.parser import HTMLParser

ALLOW = {"trading", "pooling", "during", "nothing", "something", "anything", "everything",
         "bargaining", "string"}


class Text(HTMLParser):
    BLOCK = {"p", "li", "td", "th", "h1", "h2", "h3", "h4", "div", "figcaption", "tr", "ul", "ol"}

    def __init__(self):
        super().__init__()
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg"):
            self.skip += 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip -= 1
        if tag in self.BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


t = Text()
t.feed(open(sys.argv[1], encoding="utf-8").read())
text = "".join(t.parts)
blocks = [re.sub(r"\s+", " ", b).strip() for b in text.split("\n")]
long_count = 0
for b in blocks:
    if not b:
        continue
    for s in re.split(r"(?<=[.!?:;])\s+(?=[A-Z(\"“])", b):
        words = [w for w in s.split() if re.search(r"[A-Za-z0-9]", w)]
        if len(words) > 25:
            long_count += 1
            print("LONG (%d): %s" % (len(words), s))
print("long sentences:", long_count)
ings = {}
for w in re.findall(r"[A-Za-z-]+ing\b", text):
    if w.lower() not in ALLOW:
        ings[w] = ings.get(w, 0) + 1
print("-ing tokens outside the allowlist:", ings)
