"""Print-only scan of the manuscript, the comparison note, the slides, figure labels and project documents
for the four language rules and the house rules. It prints; it asserts nothing. The hits never change the exit
status: 0 when the scan ran to the end, 1 when it stopped or a requested source could not be read (the output then
ends with a line that says so), 2 for a usage error.

  python3 language_scan.py [--doc DIR] [--extra PATH ...] [--pdf FILE ...] [--no-figcode] [--no-doc]

Default scope: main.tex, sections/*.tex, appendix/*.tex, comparison.tex and slides.tex in DIR (default
slot/manuscript of this repository), plus the string literals of scripts/F_figures/make_figures.py, where the
in-figure labels and annotations live (docstrings and the arguments of log() and print() are skipped).
  --doc DIR       folder that holds the documents
  --extra PATH    more files or folders (.tex, .md; a folder is searched for both); several allowed
  --pdf FILE      the text of built PDFs (pdftotext): captions, figure PDFs and printed labels; also reports
                  "??" and "in preparation"
  --no-figcode    leave out the string literals of make_figures.py
  --no-doc        leave out the documents of DIR; scan only the --extra and --pdf files (and the figure program)

Categories
  status           rule 1: status labels (analytical, computer-assisted, numerical diagnostic, certified,
                   "open" as a status, "not characterized" and kin)
  defensive        rule 2: hedges, caveats, limitation endings, "may" outside the tie-rule phrases
  history          rule 3: narration of the paper's own changes
  process          rule 3: registry, script, run, verification, file names, keys, workstream codes, rule codes
  example naming   rule 4: benchmark, calibration, main case, "at B", S(B), Value at B
  names            tool, agent, model, account and host names, and home-directory paths (also inside the
                   comments and docstrings of Python files)
  house            we/our/us; \\textbf outside table cells, theorem heads and item labels; dashes in running
                   text; paragraph openers that count (also after a run-in heading); decimals, percentages and
                   multi-digit fractions typed outside \\reg, and single-digit fractions typed right after "=";
                   lemma, definition and remark environments, untitled propositions and corollaries, and the
                   counts of propositions and corollaries in sections/*.tex; "this section"
  interval claim   "interval of strengths" (each hit needs its condition)
  placeholder      "??" and "in preparation"
  allowed          the tie-rule phrases "may mix" and "may prepare with any probability": printed, not counted
                   in the total

Every hit prints as file:line, category, the matched text and the trimmed line. The run ends with counts by
category (with the kinds inside each) and by file.
"""
import argparse
import ast
import bisect
import collections
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DEFAULT_DOC = ROOT / "slot" / "manuscript"
FIGCODE = pathlib.Path(__file__).resolve().parents[1] / "F_figures" / "make_figures.py"

CATEGORY_ORDER = ["status", "defensive", "history", "process", "example naming", "names", "house",
                  "interval claim", "placeholder", "allowed"]


# ------------------------------------------------------------------ patterns
WS = r"(?:\s|~)+"
DASHES = r"\-\u2010-\u2014"  # hyphen, en and em dashes, as the inside of a character class


def W(pattern):
    """Let a space (and \\s+) in a pattern match any run of white space or ~, so that a phrase broken over two
    lines or tied with ~ is found."""
    return pattern.replace(r"\s+", WS).replace(" ", WS)


TEX, MD, PDF, PY = "tex", "md", "pdf", "py"
ALL = {TEX, MD, PDF, PY}
TEXT = {TEX, MD, PDF}

# (category, kind, regex, flags, applies to)
PATTERNS = []


def add(category, kind, regex, applies=ALL, flags=re.IGNORECASE):
    PATTERNS.append((category, kind, re.compile(regex, flags), set(applies)))


# --- rule 1: status
add("status", "analytical", r"\banalytical(ly)?\b")
# pdftotext drops a hyphen at the end of a line and glues the two halves, so the separator may be empty
add("status", "computer-assisted", r"\bcomputer[\s~" + DASHES + r"]*assisted\b")
add("status", "numerical diagnostic", W(r"\bnumerical(ly)? diagnostics?\b"))
add("status", "certified", r"\bcertif(y|ies|ied|ying|icate|icates|ication|ications)\b")
add("status", "open as a status", W(r"\b(remains? open|is open|are open|left open|leaves? \w+ open|open (question|problem|item|items|result|results|case|cases|issue|issues))\b(?![" + DASHES + r"]\w)"))
# A bare "open" that the pattern above does not already report: not before a noun it lists, not before a hyphenated
# word (open-set, open-ended), not in "relatively open" and the like, not before a topological noun.
add("status", "open (bare)", r"(?<!relatively\s)(?<!remains\s)(?<!remain\s)(?<!is\s)(?<!are\s)(?<!left\s)\bopen\b(?![" + DASHES + r"]\w)(?!\s+(interval|intervals|set|sets|ball|cover|subset|neighbou?rhood|contest|contests|marker|markers|half|region|regions|segment|segments|circle|circles|disk|disc|square|bracket|brackets|end|ends|band|bands|window|windows|at|from|question|problem|item|items|result|results|case|cases|issue|issues))")
add("status", "not characterized", W(r"\b(not (yet )?(characteri[sz]ed|established|proved|proven|claimed|resolved)|uncharacteri[sz]ed|unresolved|unproved|unproven|conjectures?)\b"))

# --- rule 2: defensive writing
add("defensive", "hedge", W(r"\b(arguably|should be noted|it is worth noting|it is worth|of course|to be clear|we do not claim|I do not claim|this is not to say|in some cases|not necessarily|could be argued|admittedly|perhaps|possibly|somewhat|to some extent|strictly speaking|one might|note that)\b"))
add("defensive", "hedge (soft)", W(r"\b(seems?|seemingly|appears? to|likely|could|need not|beyond the scope|future work|is not meant to|are not meant to|illustrative)\b"))
add("defensive", "caveat", r"\b(caveats?|limitations?|reassur\w*)\b")
add("defensive", "disclaimer", W(r"\b(only in the (benchmark|example)|is not needed|does not rise|cannot be weakened|not only)\b"))
add("defensive", "may/might", r"\bmight\b")
add("defensive", "may", W(r"\bmay\b(?!\s+mix\b)(?!\s+prepare with any probability\b)"))
add("allowed", "tie rule: may mix", W(r"\bmay mix\b"))
add("allowed", "tie rule: may prepare with any probability", W(r"\bmay prepare with any probability\b"))

# --- rule 3: development log
add("history", "now", r"\bnow\b")
add("history", "no longer", W(r"\bno longer\b"))
add("history", "new", r"\b(new|newly)\b")
add("history", "updated", r"\bupdat(e|es|ed|ing)\b")
add("history", "revised", r"\brevis(e|es|ed|ion|ions|ing)\b")
add("history", "corrected", r"\bcorrect(ed|ion|ions|s)\b")
add("history", "replaces", r"\breplac(e|es|ed|ement|ements|ing)\b")
add("history", "in this version", W(r"\b(in this version|earlier (draft|version|versions|result|results|paper|manuscript)|previous (draft|version|versions|paper|manuscript))\b"))
add("history", "previously", r"\bprevious(ly)?\b")
add("history", "upgrade", r"\bupgrad\w*")
add("history", "originally", r"\b(originally|formerly)\b")
add("history", "this draft", W(r"\b(this draft|the (current|present) (draft|version)|this revision)\b"))
add("history", "generalizes the earlier", W(r"generali[sz]\w* (the )?(earlier|previous)|restriction is removed|\bis removed\b|(has|have) been (added|changed|removed|replaced|dropped|extended|strengthened|weakened|relaxed|sharpened)"))
add("history", "generalizes", r"\bgenerali[sz](es|ed|ing|ation|ations)\b(?!\s+(the\s+)?(earlier|previous))")

# --- rule 3: process words
add("process", "registry", r"\bregistr(y|ies)\b")
add("process", "script", r"\bscripts?\b")
add("process", "exercise", r"\bexercises?\b")
add("process", "checker", r"\bcheckers?\b")
add("process", "run", r"(?<!long\s)(?<!short\s)(?<!medium\s)\brun\b(?!\s+logs?\b)")
add("process", "run log", W(r"\brun logs?\b"))
add("process", "runs/ran/rerun", r"(?<!long\s)(?<!short\s)(?<!medium\s)\b(?:runs|ran|re-?runs?)\b"
    r"(?!\s+(?:from|on|over|through|to|between|along|up|down|across)\b)")
add("process", "program/code/pipeline", r"\b(?:programs?|codes?|pipelines?)\b")
add("process", "check", r"\b(?:cross-?)?check(?:s|ed|ing)?\b")
add("process", "scan", r"\bscan(?:s|ned|ning)?\b")
add("process", "digits", r"\bdigits\b")
add("process", "enters no proof", W(r"\b(?:enters?|entered) no (?:step |part |line |argument )?(?:of (?:the |any |a )?)?(?:proof|argument|derivation)s?\b"))
add("process", "verified", r"\bverifi(ed|cation|cations)\b")
add("process", "recomputed", r"\brecomput\w*")
add("process", "method words", W(r"\b(Sturm|enclosures?|interval arithmetic|bisection|workstreams?)\b"))
add("process", "key/file", r"\b(keys?|files?)\b")
add("process", "file name", r"\.(py|csv|json|log|txt|md|sh|png)\b|\\nolinkurl", applies={TEX, MD, PDF})
add("process", "file name (tex/pdf)", r"\b[\w-]+\.(tex|pdf)\b", applies={TEX, MD, PDF})
add("process", "texttt with underscore", r"\\texttt\{[^}]*_", applies={TEX})
add("process", "texttt", r"\\texttt\{[^}_]*\}", applies={TEX})
add("process", "workstream code", r"\b(XP[1-5][b]?|P[1-5]|W[1-5]|LA|XLA)\b", flags=0)
add("process", "tie-rule code", r"\b(?:[Rr]ules?\s+)?(?:IM|I0|C1|CM)\b", flags=0)
add("process", "plan code", r"(?<!\()\b(?:O[1-9]|D[1-9]|S(?:1[0-3]|[0-9]))\b(?!\))", flags=0)

# --- rule 4: the example is neutral
add("example naming", "benchmark", r"\bbench-?marks?\b")
# The example's internal label B, written bare, as $B$ or as \(B\), after a plain space or a tie ~. B is also the
# symbol of gross profit, so every hit of the label kinds needs reading.
_B_BARE = r"B\b(?![\w(])"
_B_MATH = r"(?:\$B\$|\\\(B\\\))"
_B_ANY = r"(?:" + _B_BARE + "|" + _B_MATH + ")"
_LABEL_WORDS = ["at", "of", "in", "under", "for", "calibration", "economy", "example", "specification", "scenario",
                "benchmark", "baseline"]
_NOT_AFTER_LABEL_WORD = "".join(rf"(?<!\b(?i:{w}){sep})" for w in _LABEL_WORDS for sep in (r"\s", "~"))
add("example naming", "calibration B", r"\b(?i:calibration)" + WS + _B_ANY, flags=0)
add("example naming", "calibration", r"\bcalibrat\w*\b(?!" + WS + _B_ANY + ")")
add("example naming", "main case", W(r"\bmain case\b"))
add("example naming", "at B", r"(?<![Vv]alue(?:\s|~))\b(?:(?i:at)" + WS + _B_ANY + r"|(?i:of|in|under|for)" + WS + _B_MATH + ")",
    flags=0)
add("example naming", "label B", r"\b(?i:economy|example|specification|scenario|benchmark|baseline|"
    r"parametri[sz]ation)" + WS + _B_ANY, flags=0)
add("example naming", "symbol B", _NOT_AFTER_LABEL_WORD + _B_MATH, flags=0)
add("example naming", "S(B)", r"\bS\(B\)|\\mathbf\{S\}\(B\)", flags=0)
add("example naming", "Value at B", r"\b[Vv]alue" + WS + r"(?:at|of|in)" + WS + _B_ANY, flags=0)
add("example naming", "baseline", r"\bbaseline\b")

# --- names of tools, agents, models, accounts
# The names are written in pieces, so that no project text holds a tool, agent or model name in one piece.
_NAMES = ["Clau" "de", "Anthro" "pic", "Open" "AI", "Chat" "G" "PT", "G" "PT(?:-?[\\w.]+)?", "Co" "dex", "Op" "us",
          "Son" "net", "Fa" "ble", "Hai" "ku", "Gem" "ini", "Co" "pilot", "Ast" "ra", "Mist" "ral", "Gr" "ok",
          "Deep" "Seek"]
add("names", "model/tool name", r"\b(?:" + "|".join(_NAMES) + r")\b")
# Capitalised only: these are also ordinary words or macro names in lower case.
add("names", "model / host name", r"\b(?:S" r"ol|Con" r"denser|My" r"riad)\b", flags=0)
add("names", "account name", r"\b(?:uct" r"piaj|austin" r"li)\b")
add("names", "home path", r"(?:/home|/Users)/[\w.-]+")
add("names", "agent / assistant term", W(r"\b(?:sub-?" r"agents?|language " r"models?|L" r"LMs?|AI " r"assistants?)\b"))

# --- house rules
add("house", "we/our/us", r"\b(we|We|our|Our|ours|ourselves|us)\b", flags=0)
add("house", "dash ---", r"---|\u2014", applies={TEX, PDF, PY})
add("house", "dash \u2014", r"\u2014", applies={MD})
add("house", "dash spaced --", r"(?<=\s)--(?=\s)", applies={TEX})
add("house", "this section", W(r"\bthis section\b"), applies={TEX, MD, PDF})

# --- other
add("interval claim", "interval of strengths", W(r"\binterval of (strengths|slots|incumbent strengths)\b"))
add("placeholder", "??", r"\?\?", applies={TEX, PDF, MD})
add("placeholder", "in preparation", W(r"\bin preparation\b"))

COUNT_WORDS = "Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve"


# ------------------------------------------------------------------ helpers for LaTeX text
def strip_comments(text):
    """Replace every LaTeX comment (an unescaped % to the end of the line), every comment environment and every
    \\iffalse ... \\fi block with spaces; keep the newlines."""
    out = []
    for line in text.split("\n"):
        i, n = 0, len(line)
        while i < n:
            c = line[i]
            if c == "\\":
                i += 2
                continue
            if c == "%":
                line = line[:i] + " " * (n - i)
                break
            i += 1
        out.append(line)
    text = "\n".join(out)
    for m in list(re.finditer(r"\\begin\{comment\}.*?\\end\{comment\}", text, re.S)):
        text = blank(text, m.start(), m.end())
    return blank_iffalse(text)


def blank_iffalse(text):
    """Blank each \\iffalse ... \\fi block; conditionals opened inside it are counted, so that the right \\fi ends it."""
    opener = re.compile(r"\\iffalse\b")
    tokens = re.compile(r"\\if[A-Za-z@]*\b|\\fi\b")
    pos = 0
    while True:
        m = opener.search(text, pos)
        if not m:
            return text
        depth, end = 1, len(text)
        for t in tokens.finditer(text, m.end()):
            depth += -1 if t.group(0) == "\\fi" else 1
            if depth == 0:
                end = t.end()
                break
        text = blank(text, m.start(), end)
        pos = end


def match_brace(text, i):
    """Index of the } that closes the { at text[i]; len(text)-1 if it never closes."""
    depth = 0
    n = len(text)
    j = i
    while j < n:
        c = text[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    return n - 1


def blank(text, a, b):
    """Replace text[a:b] by spaces, keeping newlines."""
    return text[:a] + re.sub(r"[^\n]", " ", text[a:b]) + text[b:]


# commands whose first braced argument is a label, key, path or length and never prose
OPAQUE_ARG = re.compile(
    r"\\(reg|label|ref|eqref|autoref|cref|Cref|pageref|nameref|cite[a-zA-Z]*|input|include|includegraphics|"
    r"bibliography|bibliographystyle|usepackage|usetikzlibrary|url|nolinkurl|hypertarget|hyperlink|setcounter|"
    r"newcounter|addtocounter|href)\*?\s*(\[[^\]]*\]\s*)*\{")


def mask_opaque(text):
    """Blank the arguments of \\reg, \\label, \\ref, \\cite, \\input and similar commands: keys and paths are not prose."""
    pos = 0
    while True:
        m = OPAQUE_ARG.search(text, pos)
        if not m:
            return text
        i = m.end() - 1
        j = match_brace(text, i)
        text = blank(text, i + 1, j)
        pos = j + 1


TABULAR = re.compile(r"\\begin\{(tabular\*?|tabularx|longtable|array|supertabular)\}")


def tabular_spans(text):
    spans = []
    for m in TABULAR.finditer(text):
        end = text.find("\\end{" + m.group(1) + "}", m.end())
        spans.append((m.start(), len(text) if end < 0 else end))
    return spans


def in_spans(spans, pos):
    return any(a <= pos < b for a, b in spans)


class Source:
    """One text to scan: a display name, a kind and the text with offsets that map back to lines."""

    def __init__(self, name, kind, text, first_line=1, label=None):
        self.name, self.kind, self.text = name, kind, text
        self.label = label or name
        self.first_line = first_line
        self.starts = [0]
        for m in re.finditer("\n", text):
            self.starts.append(m.end())

    def line_of(self, pos):
        return bisect.bisect_right(self.starts, pos) - 1

    def line_text(self, idx):
        a = self.starts[idx]
        b = self.starts[idx + 1] - 1 if idx + 1 < len(self.starts) else len(self.text)
        return self.text[a:b]


Hit = collections.namedtuple("Hit", "src line category kind match context")

PROBLEMS = []  # sources that could not be scanned: the run ends with a line that says so, and the exit status is 1


def skipped(name, reason):
    print(f"skipped {name}: {reason}")
    PROBLEMS.append(name)


def shorten(line, a, b, width=150):
    """Trim the line; when it is long keep a window around the match span [a, b)."""
    stripped = line.strip()
    lead = len(line) - len(line.lstrip())
    a2, b2 = max(a - lead, 0), max(b - lead, 0)
    if len(stripped) <= width:
        return stripped
    lo = max(0, a2 - width // 2)
    hi = min(len(stripped), lo + width)
    lo = max(0, hi - width)
    return ("..." if lo > 0 else "") + stripped[lo:hi] + ("..." if hi < len(stripped) else "")


def collapse(s, limit=70):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 3] + "..."


# ------------------------------------------------------------------ scans
def scan_patterns(src, scan_text, hits):
    seen = set()
    tikz = [(m.start(), m.end()) for m in re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", scan_text, re.S)] \
        if src.kind == TEX else []
    for category, kind, rx, applies in PATTERNS:
        if src.kind not in applies:
            continue
        for m in rx.finditer(scan_text):
            if m.end() == m.start():
                continue
            if kind == "dash ---" and src.kind == TEX and is_table_dash(scan_text, m.start(), m.end()):
                continue
            if kind == "dash spaced --" and in_spans(tikz, m.start()):
                continue
            key = (category, kind, m.start())
            if key in seen:
                continue
            seen.add(key)
            idx = src.line_of(m.start())
            line = src.line_text(idx)
            col = m.start() - src.starts[idx]
            hits.append(Hit(src, idx + src.first_line, category, kind, collapse(m.group(0)),
                            shorten(line, col, col + len(m.group(0)))))


def is_table_dash(text, a, b):
    """A cell that holds only --- (an empty table entry) is not a dash in running text."""
    i = a - 1
    while i >= 0 and text[i] in " \t":
        i -= 1
    j = b
    while j < len(text) and text[j] in " \t":
        j += 1
    before_ok = i < 0 or text[i] in "&\n{" or text[max(i - 1, 0): i + 1] == "\\\\"
    after_ok = j >= len(text) or text[j] in "&\n}" or text[j: j + 2] == "\\\\"
    return before_ok and after_ok


MACRO_DEF = re.compile(r"\\(newcommand|renewcommand|providecommand|def|edef|gdef|newenvironment|renewenvironment|"
                       r"setbeamertemplate|setbeamercolor|setbeamerfont|DeclareRobustCommand)\b")


def is_head_prefix(prefix, content):
    """True when the bold text opens a table head, item label or theorem head: only macro names, braces and
    short labels such as (i) precede it on its line, and it is short."""
    p = re.sub(r"\\begin\{[^}]*\}", " ", prefix)
    p = re.sub(r"\{[^{}]{0,12}\}", " ", p)
    p = re.sub(r"\\[A-Za-z@]+\*?", " ", p)
    p = re.sub(r"[{}\[\]\s*|&:]", " ", p)
    return not re.findall(r"[A-Za-z]{2,}", p) and len(content.split()) <= 6


def scan_bold(src, scan_text, hits):
    spans = tabular_spans(scan_text)
    for m in re.finditer(r"\\textbf\s*\{", scan_text):
        i = m.end() - 1
        j = match_brace(scan_text, i)
        content = scan_text[i + 1:j]
        if "#" in content or in_spans(spans, m.start()):
            continue
        idx = src.line_of(m.start())
        ls = src.starts[idx]
        prefix = scan_text[ls:m.start()]
        if MACRO_DEF.search(prefix) or is_head_prefix(prefix, content):
            continue
        line = src.line_text(idx)
        hits.append(Hit(src, idx + src.first_line, "house", "textbf", collapse("\\textbf{" + content + "}"),
                        shorten(line, m.start() - ls, j - ls)))


def scan_openers(src, scan_text, hits):
    """Paragraph openers that count: Two ..., Three ... at the start of a paragraph, also right after a run-in
    heading on the same line (\\paragraph{Winners.} Two forces ...)."""
    rx = re.compile(r"^[ \t]*(?P<run>\\(?:sub)*paragraph\*?\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}[ \t]*)?"
                    r"(?:\\noindent\s*)?(?:\\(?:emph|textit)\{)?(" + COUNT_WORDS + r")\b")
    section_line = re.compile(r"^\s*\\(sub)*(section|paragraph|subparagraph)\*?\s*(\[[^\]]*\])?\{.*\}\s*(\\label\{[^}]*\})?\s*$"
                              r"|^\s*\\(begin|end)\{[^}]*\}\s*(\[.*\])?\s*$")
    n = len(src.starts)
    prev_blank = True
    prev_head = False
    for idx in range(n):
        line = scan_text[src.starts[idx]: (src.starts[idx + 1] - 1 if idx + 1 < n else len(scan_text))]
        if not line.strip():
            prev_blank = True
            continue
        m = rx.match(line)
        if m and (prev_blank or prev_head or m.group("run")):
            hits.append(Hit(src, idx + src.first_line, "house", "count opener", m.group(2),
                            shorten(src.line_text(idx), m.start(2), m.end(2))))
        prev_blank = False
        prev_head = bool(section_line.match(line))


# masks for typed numbers
# The bracket that follows a layout macro (an item label, a length, a TikZ or beamer option, a citation note) holds
# no data. The bracket after any other macro opens a mathematical interval or a delimiter, as in \in[0.25,0.75],
# \DT[1-0.37] or \Bigl[...\Bigr], and stays visible; so does the title of a theorem-like environment.
_RESULT_ENVS = ("theorem|proposition|lemma|corollary|claim|remark|definition|assumption|conjecture|example|proof|"
                "namedresult|ResultBox")
OPT_ARG = re.compile(
    r"(\\(?:item|makebox|framebox|parbox|raisebox|node|draw|fill|filldraw|path|coordinate|clip|shade|useasboundingbox|"
    r"Takeaway[A-Za-z]*|includegraphics|usepackage|documentclass|usebeamercolor|usebeamerfont|usefonttheme|usetheme|"
    r"usecolortheme|cite[A-Za-z]*)\*?"
    r"|\\begin\{(?!(?:" + _RESULT_ENVS + r")\*?\})[^}]*\}|\\\\\*?)\s*\[[^\]\n]*\]")
LENGTH = re.compile(r"-?\d*\.?\d+(?:pt|em|ex|cm|mm|in|bp|sp|mu|px)\b"
                    r"|-?\d*\.?\d+\s*\\[A-Za-z]*(?:width|height|skip|sep|indent|size|stretch)\b"
                    r"|\\[A-Za-z]+\s*=\s*-?\d*\.?\d+(?:pt|em|ex|cm|mm|in|bp)\b")
OVERLAY = re.compile(r"<[0-9,\-+|:. ]*>")
TYPED_DECIMAL = re.compile(r"(?<![\w.\\])(?:\d+\.\d+|\.\d+)(?![\w])(?!\.\d)")
TYPED_PERCENT = re.compile(r"(?<![\w.\\])\d+(?:\.\d+)?\s*\\%")
TYPED_FRAC_SLASH = re.compile(r"(?<![\d./\\])(\d+)/(\d+)(?![\d/!])")
TYPED_FRAC_TEX = re.compile(r"\\(?:[dt]?frac|nicefrac)\s*\{\s*-?\s*(\d+)\s*\}\s*\{\s*(\d+)\s*\}")
TYPED_FRAC_OVER = re.compile(r"\{\s*-?\s*(\d+)\s*\\over\s*(\d+)\s*\}")
# A single-digit fraction typed as the value of a symbol ("\rho=1/4", "\tau(1)=5/8") is a typed example value;
# one that goes on into a product or a macro ("=\tfrac12\sum") is a weight and is left alone.
_FRAC_VALUE = (r"(?:(\d)/(\d)|\\[dt]?frac\s*\{\s*(\d)\s*\}\s*\{\s*(\d)\s*\}|\\[dt]?frac\s*(\d)\s*(\d))(?!\d)")
_FRAC_VALUE_END = (r"(?!\s*[A-Za-z0-9(\[{/^_*+\-]|\s*\\(?!le\b|ge\b|leq\b|geq\b|ne\b|neq\b|approx\b|to\b|in\b|quad\b|"
                   r"qquad\b|text\b|mathrm\b|[,;:)\]\\!\s]))")
TYPED_FRAC_VALUE = re.compile(r"(?:=|\\approx|\\equiv|:=|\\coloneqq)\s*(?:\\[,;:! ])*\s*-?\s*" + _FRAC_VALUE + _FRAC_VALUE_END)


NUMBER_OPAQUE = re.compile(r"\\(setstretch|linespread|scalebox|rotatebox|arraystretch|baselinestretch)\b\}?(\s*\{[^{}]*\}){1,2}")
TYPED_REFERENCE = re.compile(r"(?:Sections?|Appendix|Appendices|Tables?|Figures?|Propositions?|Corollar(?:y|ies)|Lemmas?|Remarks?|"
                             r"Theorems?|Parts?|Steps?|Equations?|Eq\.)(?:~|\s)+(?:[A-Z]?[\d.]+(?:\(\w+\))?(?:,|;|\s|~|and|or|to|--)*)*$")


def number_text(scan_text):
    """The text in which typed numbers are looked for: the body only, without optional arguments, lengths,
    overlay specifications and the arguments of opaque commands."""
    body = scan_text.find("\\begin{document}")
    t = scan_text if body < 0 else blank(scan_text, 0, body)
    for rx in (OPT_ARG,):
        for m in list(rx.finditer(t)):
            a = m.end() - len(m.group(0)) + len(m.group(1))
            t = blank(t, a, m.end())
    for m in list(LENGTH.finditer(t)):
        t = blank(t, m.start(), m.end())
    for m in list(OVERLAY.finditer(t)):
        t = blank(t, m.start(), m.end())
    for m in list(NUMBER_OPAQUE.finditer(t)):
        t = blank(t, m.start(), m.end())
    return t


MAIN_TEXT_COUNTS = collections.Counter()
EXPECTED_COUNTS = {"proposition": 4, "corollary": 3}


def scan_structure(src, scan_text, hits):
    """House rules for the main text (sections/*.tex): no lemma, definition or remark environments, every proposition
    and corollary carries a descriptive title, and the counts of propositions and corollaries are kept."""
    for m in re.finditer(r"\\begin\{(lemma|definition|remark|claim|assumption|conjecture)\*?\}", scan_text):
        idx = src.line_of(m.start())
        hits.append(Hit(src, idx + src.first_line, "house", "lemma/definition/remark in the main text",
                        collapse(m.group(0)), shorten(src.line_text(idx), m.start() - src.starts[idx], m.end() - src.starts[idx])))
    for m in re.finditer(r"\\begin\{(proposition|corollary)\}(?P<title>\s*\[[^\]\n]*\])?", scan_text):
        MAIN_TEXT_COUNTS[m.group(1)] += 1
        if not m.group("title"):
            idx = src.line_of(m.start())
            hits.append(Hit(src, idx + src.first_line, "house", "result without a title", collapse(m.group(0)),
                            shorten(src.line_text(idx), m.start() - src.starts[idx], m.end() - src.starts[idx])))


def main_text_count_hits(src, hits):
    """One hit for each result type whose count in sections/*.tex differs from the house rule."""
    for kind, expected in EXPECTED_COUNTS.items():
        found = MAIN_TEXT_COUNTS[kind]
        if found != expected:
            plural = "corollaries" if kind == "corollary" else kind + "s"
            hits.append(Hit(src, 0, "house", "main-text count", f"{plural} {found}",
                            f"sections/*.tex hold {found} {kind} environment(s); the house rule is {expected}"))


def scan_numbers(src, scan_text, hits):
    t = number_text(scan_text)
    found = []
    for m in TYPED_DECIMAL.finditer(t):
        found.append((m.start(), m.end(), "typed decimal"))
    for m in TYPED_FRAC_SLASH.finditer(t):
        if len(m.group(1)) > 1 or len(m.group(2)) > 1:
            found.append((m.start(), m.end(), "typed fraction"))
    for rx in (TYPED_FRAC_TEX, TYPED_FRAC_OVER):
        for m in rx.finditer(t):
            if len(m.group(1)) > 1 or len(m.group(2)) > 1:
                found.append((m.start(), m.end(), "typed fraction"))
    for m in TYPED_PERCENT.finditer(t):
        found.append((m.start(), m.end(), "typed percentage"))
    for m in TYPED_FRAC_VALUE.finditer(t):
        found.append((m.start(), m.end(), "typed fraction after ="))
    for a, b, kind in found:
        if kind == "typed decimal" and TYPED_REFERENCE.search(scan_text[max(0, a - 80):b]):
            kind = "typed reference"
        idx = src.line_of(a)
        ls = src.starts[idx]
        hits.append(Hit(src, idx + src.first_line, "house", kind, collapse(scan_text[a:b]),
                        shorten(src.line_text(idx), a - ls, b - ls)))


def scan_tex(path, name, hits, kind=TEX, main_text=False):
    raw = path.read_text(errors="replace")
    text = strip_comments(raw) if kind == TEX else raw
    src = Source(name, kind, text)
    scan_text = mask_opaque(text) if kind == TEX else text
    scan_patterns(src, scan_text, hits)
    if kind == TEX:
        scan_bold(src, scan_text, hits)
        scan_numbers(src, scan_text, hits)
        if main_text:
            scan_structure(src, scan_text, hits)
    scan_openers(src, scan_text, hits)
    return src


def join_hyphenated(page):
    """The page text with every line that ends in a letter and a hyphen joined to the next line, which starts with a
    lower-case letter (bench- / mark gives benchmark). The line count is kept: the joined text sits on the first
    line and the second line is left empty."""
    lines = page.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if i + 1 < len(lines) and re.search(r"[A-Za-z]-$", line) and re.match(r"\s*[a-z]", lines[i + 1]):
            out.append(line[:-1] + lines[i + 1].lstrip())
            out.append("")
            i += 2
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def scan_pdf(path, name, hits):
    try:
        res = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        skipped(name, "pdftotext not found")
        return None
    if res.returncode != 0:
        skipped(name, f"pdftotext failed: {res.stderr.strip()[:100]}")
        return None
    pages = res.stdout.split("\f")
    # one source per page; the line number is the line on the page, and the page goes into the name
    for p, page in enumerate(pages, 1):
        if not page.strip():
            continue
        text = page.replace("\u00ad", "")
        src = Source(name, PDF, text, label=f"{name} p.{p}")
        found = []
        scan_patterns(src, src.text, found)
        # a second pass over the text with hyphenated line breaks joined; a hit that both passes find prints once
        joined = Source(name, PDF, join_hyphenated(text), label=src.label)
        again = []
        scan_patterns(joined, joined.text, again)

        def key(h):
            return (h.category, h.kind, h.line, re.sub(r"[\s\-]", "", h.match.lower()))

        seen = {key(h) for h in found}
        for h in found + [h for h in again if key(h) not in seen]:
            hits.append(h._replace(src=src))
    return True


def docstring_ids(tree):
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
                    and isinstance(body[0].value.value, str):
                ids.add(id(body[0].value))
    return ids


def key_like(value):
    """A single token that reads as a path, a column name or a dictionary key: lower case or with _ / . : - in it.
    A token such as P3 or (CM), which a figure could print as a label, does not."""
    return bool(re.fullmatch(r"[a-z0-9_./:\-]+", value) or re.fullmatch(r"[\w./:\-]+", value) and re.search(r"[_./:]", value))


def scan_pycode(path, name, hits):
    """String literals of a Python file, except docstrings and the arguments of log() and print()."""
    source = path.read_text(errors="replace")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        skipped(name, str(exc))
        return None
    skip = docstring_ids(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg in ("help", "description", "epilog", "metavar", "prog"):
                    for sub in ast.walk(kw.value):
                        if isinstance(sub, ast.Constant):
                            skip.add(id(sub))
            fn = node.func
            fname = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
            if fname in ("log", "print", "open", "write_text", "read_text", "mkdir", "run", "get", "addfont"):
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Constant):
                        skip.add(id(sub))
    lines = source.split("\n")
    src = Source(name, PY, source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in skip:
            value = node.value
            if not value.strip():
                continue
            for category, kind, rx, applies in PATTERNS:
                if PY not in applies:
                    continue
                if category == "names":
                    continue  # the names are searched in the whole text of the file below
                if category == "process" and not re.search(r"\s", value) and key_like(value):
                    continue  # a path, a column name or a key in code, not a label
                for m in rx.finditer(value):
                    if m.end() == m.start():
                        continue
                    line_no = node.lineno
                    line = lines[min(line_no, len(lines)) - 1] if lines else ""
                    ctx = line if line.strip() else value.replace("\n", " / ")
                    hits.append(Hit(src, line_no, category, kind, collapse(m.group(0)), shorten(ctx, 0, 0)))
    # tool, agent, model, account and host names are searched in the whole text, comments and docstrings included
    for category, kind, rx, applies in PATTERNS:
        if category != "names" or PY not in applies:
            continue
        for m in rx.finditer(source):
            idx = src.line_of(m.start())
            hits.append(Hit(src, idx + 1, category, kind, collapse(m.group(0)),
                            shorten(src.line_text(idx), m.start() - src.starts[idx], m.end() - src.starts[idx])))
    return src


# ------------------------------------------------------------------ driver
def display(path, base):
    path = pathlib.Path(path)
    for root in (base, ROOT):
        try:
            return str(path.resolve().relative_to(root.resolve()))
        except ValueError:
            continue
    return str(path)


def expand_extra(paths):
    files = []
    for p in paths:
        p = pathlib.Path(p).expanduser()
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.suffix in (".tex", ".md") and not any(part in (".git", "__pycache__", "build") for part in f.parts):
                    files.append(f)
        elif p.exists():
            files.append(p)
        else:
            skipped(str(p), "not found")
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print-only language scan (rules 1 to 4 and house rules).")
    ap.add_argument("--doc", default=str(DEFAULT_DOC), help="folder that holds the documents (default slot/manuscript)")
    ap.add_argument("--extra", nargs="+", action="extend", default=[], metavar="PATH", help="more files or folders (.tex, .md)")
    ap.add_argument("--pdf", nargs="+", action="extend", default=[], metavar="FILE", help="built PDFs to scan as text")
    ap.add_argument("--no-figcode", action="store_true", help="leave out the string literals of make_figures.py")
    ap.add_argument("--no-doc", action="store_true", help="leave out the documents of --doc; scan only --extra and --pdf")
    args = ap.parse_args(argv)

    doc = pathlib.Path(args.doc).expanduser()
    hits = []
    scanned = []

    files = [] if args.no_doc else [doc / "main.tex"] + sorted((doc / "sections").glob("*.tex")) \
        + sorted((doc / "appendix").glob("*.tex")) + [doc / "comparison.tex", doc / "slides.tex"]
    structure = Source("sections/*.tex (structure)", TEX, "")
    for f in files:
        if not f.exists():
            skipped(display(f, doc), "not found")
            continue
        name = display(f, doc)
        try:
            scan_tex(f, name, hits, main_text=name.startswith("sections/"))
            scanned.append(name)
        except Exception as exc:  # one source that fails does not stop the others; the run says so at its end
            skipped(name, f"{type(exc).__name__}: {exc}")
    if any(n.startswith("sections/") for n in scanned):
        main_text_count_hits(structure, hits)
        scanned.append(structure.name)

    if not args.no_figcode:
        if FIGCODE.exists():
            name = display(FIGCODE, ROOT) + " (strings)"
            try:
                scan_pycode(FIGCODE, name, hits)
                scanned.append(name)
            except Exception as exc:
                skipped(name, f"{type(exc).__name__}: {exc}")
        else:
            skipped("figure code", f"{FIGCODE} not found")

    for f in expand_extra(args.extra):
        name = display(f, ROOT)
        try:
            if f.suffix == ".py":
                name += " (strings)"
                scan_pycode(f, name, hits)
            elif f.suffix == ".tex":
                scan_tex(f, name, hits, TEX)
            else:
                scan_tex(f, name, hits, MD)
            scanned.append(name)
        except Exception as exc:
            skipped(name, f"{type(exc).__name__}: {exc}")

    for f in args.pdf:
        f = pathlib.Path(f).expanduser()
        if not f.exists():
            skipped(str(f), "not found")
            continue
        name = display(f, ROOT)
        try:
            if scan_pdf(f, name, hits):
                scanned.append(name)
        except Exception as exc:
            skipped(name, f"{type(exc).__name__}: {exc}")

    # ---- print the hits, file by file in scope order, line by line
    order = {}
    for h in hits:
        order.setdefault(h.src.label, len(order))
    cat_rank = {c: i for i, c in enumerate(CATEGORY_ORDER)}
    hits.sort(key=lambda h: (order[h.src.label], h.line, cat_rank[h.category], h.kind))
    print(f"language scan: {len(scanned)} sources; doc folder {display(doc, ROOT)}")
    print()
    for h in hits:
        print(f"{h.src.label}:{h.line}  [{h.category}: {h.kind}]  {h.match!r}  |  {h.context}")

    # ---- counts
    print()
    print("=" * 78)
    print("Counts by category (kinds inside each category indented)")
    by_cat = collections.Counter(h.category for h in hits)
    by_kind = collections.defaultdict(collections.Counter)
    for h in hits:
        by_kind[h.category][h.kind] += 1
    counted = 0
    for c in CATEGORY_ORDER:
        if by_cat[c] == 0:
            print(f"  {c:<16}{0:>6}")
            continue
        tag = "  (allowed, printed, not in the total)" if c == "allowed" else ""
        print(f"  {c:<16}{by_cat[c]:>6}{tag}")
        for kind, n in sorted(by_kind[c].items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"      {kind:<44}{n:>6}")
        if c != "allowed":
            counted += by_cat[c]
    print(f"  {'total':<16}{counted:>6}   (all categories except allowed)")
    print()
    print("Counts by file (hits, allowed phrases excluded; the allowed count follows in brackets)")
    per_file = collections.Counter()
    per_file_allowed = collections.Counter()
    per_file_cat = collections.defaultdict(collections.Counter)
    for h in hits:
        if h.category == "allowed":
            per_file_allowed[h.src.name] += 1
        else:
            per_file[h.src.name] += 1
            per_file_cat[h.src.name][h.category] += 1
    short = {"status": "stat", "defensive": "def", "history": "hist", "process": "proc", "example naming": "ex",
             "names": "names", "house": "house", "interval claim": "intv", "placeholder": "plc"}
    for name in scanned:
        row = ", ".join(f"{short[c]} {per_file_cat[name][c]}" for c in CATEGORY_ORDER[:-1] if per_file_cat[name][c])
        print(f"  {name:<78}{per_file[name]:>6}  [{per_file_allowed[name]}]  {row}")
    print()
    if PROBLEMS:
        print(f"scan INCOMPLETE: {len(PROBLEMS)} source(s) skipped: " + "; ".join(PROBLEMS))
        return 1
    print(f"scan complete: {len(scanned)} sources")
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BrokenPipeError:  # the reader closed the pipe (for example "| head"): stop without a traceback
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        status = 1
    except Exception as exc:  # the scan itself stopped: say so on the stream that is read, and exit 1
        import traceback
        print(f"scan INCOMPLETE: language_scan stopped: {type(exc).__name__}: {exc}")
        traceback.print_exc(file=sys.stdout)
        status = 1
    sys.exit(status)
