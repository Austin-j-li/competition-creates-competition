"""Print structural facts about the report: unclosed or stray tags, size, forbidden words,
the inline script (written beside this file for a syntax check), and the ids that links use. Print only."""
import os
import re
import sys
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
path = sys.argv[1]
src = open(path, encoding="utf-8").read()


class Stack(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack, self.problems, self.ids, self.hrefs = [], [], set(), []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.add(d["id"])
        if tag == "a" and d.get("href", "").startswith("#"):
            self.hrefs.append(d["href"][1:])
        if tag not in VOID:
            self.stack.append((tag, self.getpos()))

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        names = [t for t, _ in self.stack]
        if tag in names:
            while self.stack and self.stack[-1][0] != tag:
                t, pos = self.stack.pop()
                self.problems.append("unclosed <%s> opened at line %d" % (t, pos[0]))
            self.stack.pop()
        else:
            self.problems.append("stray </%s> at line %d" % (tag, self.getpos()[0]))


p = Stack()
p.feed(src)
p.close()
for t, pos in p.stack:
    p.problems.append("unclosed <%s> opened at line %d" % (t, pos[0]))
print("tag problems:", p.problems if p.problems else "none")
missing = [h for h in p.hrefs if h not in p.ids]
print("internal links:", len(p.hrefs), "missing targets:", missing if missing else "none")
print("size: %d bytes (%.1f KB)" % (os.path.getsize(path), os.path.getsize(path) / 1024))
print("network references:", re.findall(r"(?:src|href)=\"(?:https?:)?//[^\"]+\"|@import|url\(", src) or "none")
# Extra words to scan for come from the environment variable SCAN_WORDS (comma-separated).
words = ["model", "assistant", "agent"] + [w for w in os.environ.get("SCAN_WORDS", "").split(",") if w]
for w in words:
    hits = [m.start() for m in re.finditer(w, src, flags=re.I)]
    print("forbidden-word scan %-10s %d hits" % (w, len(hits)))
    if w != "model":
        for h in hits:
            print("   ...%s..." % src[max(0, h - 50):h + 50].replace("\n", " "))
ctx = sorted({src[max(0, h - 30):h + 20].replace("\n", " ") for h in [m.start() for m in re.finditer("model", src, flags=re.I)]})
print("'model' contexts:")
for c in ctx:
    print("   ", c)
scripts = re.findall(r"<script>(.*?)</script>", src, flags=re.S)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inline_script.js")
open(out, "w", encoding="utf-8").write("\n".join(scripts))
print("inline scripts:", len(scripts), "written to", out)
