"""Assemble the revised manuscript from the base commit and the drafted fragments.

Run from the repository root with the project interpreter:

    .venv/bin/python audit/revision_v2_2026_10_21/scripts/integrate.py

The script reads main.tex and online_appendix.tex at the base commit of the revision
clone (git -C overleaf/paper-revision show 9b9bf3c:<file>). It then

  1. applies every drafted fragment by its declared line range or anchor, bottom-up,
     after it checks the quoted first and last words of each range against the base;
  2. applies the integrator's recorded edits (integration/ fragments and the edit list
     below), each with an expected count;
  3. substitutes every \\NUM{...} placeholder from reconciliation.csv with the display
     rule of the numerical contract's quantity manifest;
  4. inserts the verified bibliography records at their alphabetical positions;
  5. writes both files into overleaf/paper-revision/ and copies the regenerated tables.

It prints a report of each step. It stops with a message on an overlap, a missing
anchor, an edit whose count differs from the expected count, or a placeholder without a
value. It writes nothing until every step has passed. Print-only: it has no assertions.
"""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REV = ROOT / "audit" / "revision_v2_2026_10_21"
DRAFTS = REV / "drafts"
INTEG = REV / "integration"
CLONE = ROOT / "overleaf" / "paper-revision"
NUMERICS = Path("/home/uctpiaj/work/Projects/ccc-revision-numerics")
BASE_COMMIT = "9b9bf3c"
FILES = ("main.tex", "online_appendix.tex")

# Fragments in application order of the report (application itself is bottom-up).
FRAGMENTS = [
    "A01_intro_ownership_sentence.prose.tex",
    "A02_intro_mechanism.prose.tex",
    "A03_intro_main_result_ownership.prose.tex",
    "A04_intro_robustness_line.prose.tex",
    "A05_intro_selective_entry.prose.tex",
    "A06_model_2_2_to_2_4.prose.tex",
    "A07_section3_payoffs_inference_incentives.prose.tex",
    "A08_section4_1_proposition2.prose.tex",
    "A09_section4_2_benchmark_opening.prose.tex",
    "A10_section4_3_point_mass.prose.tex",
    "A11_section5_2_value_classes.prose.tex",
    "A12_appendix_A1_payoffs_pricing.prose.tex",
    "A13_appendix_A2_trading_main_comparison.prose.tex",
    "A14_appendix_A3_certificate_scope.prose.tex",
    "A15_appendix_nonemptiness_and_many_classes.prose.tex",
    "B01_main_noise.prose.tex",
    "B02_main_class_noise.prose.tex",
    "B03_oa_laplace_extreme.prose.tex",
    "B04_oa_c5_instruction.prose.tex",
    "B05_oa_quality_scope.prose.tex",
    "M1_01_intro_investor_and_noise.tex",
    "M1_02_roles.tex",
    "M1_03_laplace_justification.tex",
    "M1_04_t0_cancellation.tex",
    "M1_05_shareholder_gain.tex",
    "M1_06_empirical_trader.tex",
    "M1_07_literature_blockholders.tex",
    "M1_08_informed_shareholder.tex",
] + [f"M2_{i:02d}_{s}.tex" for i, s in [
    (1, "main_5_1_atomless"), (2, "main_5_3"), (3, "main_6"), (4, "main_7_8"),
    (5, "main_A4_atomless"), (6, "main_A5_signals"), (7, "main_A6_welfare"),
    (8, "main_A7_seller"), (9, "main_A8_parameters"), (10, "oa_A6_atomless"),
    (11, "oa_A7_signals"), (12, "oa_A9_welfare"), (13, "oa_A10_design"),
    (14, "oa_A11_note"), (15, "oa_C0_declarations"), (16, "oa_C6_continuations"),
    (17, "oa_C6b_retire"), (18, "oa_C6c_events"), (19, "oa_C8_registry"),
    (20, "oa_elsewhere")]]

# Fragments placed through anchor comments inside other fragments, not by line number.
# name -> (host fragment, anchor kind)
ANCHORED = {
    "M1_03_laplace_justification.tex": "A06_model_2_2_to_2_4.prose.tex",
    "M1_02_roles.tex": "A06_model_2_2_to_2_4.prose.tex",
    "M1_04_t0_cancellation.tex": "A07_section3_payoffs_inference_incentives.prose.tex",
}

# How an inserted fragment joins the text: a new paragraph, or the end of the paragraph
# that the anchor line closes (the fragment header says which).
INSERT_MODE = {
    "M1_01_intro_investor_and_noise.tex": "paragraph",
    "M1_05_shareholder_gain.tex": "paragraph",
    "M1_06_empirical_trader.tex": "inline",
    "M1_07_literature_blockholders.tex": "inline",
    "M1_08_informed_shareholder.tex": "paragraph",
    "B03_oa_laplace_extreme.prose.tex": "paragraph",
    "B05_oa_quality_scope.prose.tex": "paragraph",
}

# Bodies that the integrator supersedes with a reconciled text (reason in the I-fragment).
SUPERSEDED = {
    ("M2_18_oa_C6c_events.tex", 0): "I03_oa_c6c_events.tex",
}

# Header quotes that are imprecise but whose range is right. Each entry replaces the
# quoted words for the check and states why; the report prints the reason.
ANCHOR_QUOTE_FIX = {
    ("M2_20_oa_elsewhere.tex", 18): (
        "first", "the intervals are nonempty choose",
        'the header quotes "When the intervals ...", but "When" ends line 2582; the range '
        "and the body both start at line 2583"),
}

DIRECTIVE = re.compile(
    r"^%\s*(REPLACES|INSERT AFTER|INSERT BEFORE):\s*(main\.tex|online_appendix\.tex)\s+"
    r"lines?\s+(\d+)(?:\s*[–-]\s*(\d+))?\s*(.*)$")
CONFIRM = re.compile(r'^%\s*INSERT BEFORE:\s*"?(.+?)"?,?\s+at\s+lines?\s+(\d+)')


def stop(msg: str) -> None:
    print(f"\nSTOPPED: {msg}")
    raise SystemExit(1)


def loose(s: str) -> str:
    """Letters and digits only, lower case: a match key that ignores LaTeX markup."""
    s = s.replace("\\(", " ").replace("\\)", " ")
    s = re.sub(r"\\[A-Za-z]+", " ", s)
    return re.sub(r"[^0-9A-Za-z]", "", s).lower()


@dataclass
class Block:
    frag: str
    index: int
    kind: str            # REPLACES, INSERT AFTER, INSERT BEFORE
    file: str
    start: int
    end: int
    quote: str
    body: list[str]
    confirms: list[tuple[str, int]] = field(default_factory=list)

    @property
    def tag(self) -> str:
        return f"{self.frag}#{self.index}"


def strip_comments(lines: list[str]) -> list[str]:
    out = [ln for ln in lines if not ln.lstrip().startswith("%")]
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def parse_fragment(path: Path, pre: dict[str, list[tuple[str, str, int]]]) -> list[Block]:
    text = path.read_text()
    for old, new, count in pre.get(path.name, []):
        n = text.count(old)
        if n != count:
            stop(f"{path.name}: preprocessing expected {count} of {old[:60]!r}, found {n}")
        text = text.replace(old, new)
        print(f"  repaired {path.name}: {old.strip()[:50]!r} -> {new.strip()[:70]!r}")
    lines = text.split("\n")
    blocks: list[Block] = []
    current: Block | None = None
    raw: list[str] = []
    for ln in lines:
        m = DIRECTIVE.match(ln)
        if m:
            if current is not None:
                current.body = raw
                blocks.append(current)
            kind, fname, a, b, quote = m.groups()
            a = int(a)
            b = int(b) if b else a
            current = Block(path.name, len(blocks), kind, fname, a, b, quote.strip(), [])
            raw = []
            continue
        c = CONFIRM.match(ln)
        if c and current is not None and not any(x.strip() for x in raw if not x.lstrip().startswith("%")):
            current.confirms.append((c.group(1), int(c.group(2))))
        raw.append(ln)
    if current is not None:
        current.body = raw
        blocks.append(current)
    if not blocks:
        stop(f"{path.name}: no REPLACES or INSERT directive found")
    return blocks


def quoted_pieces(quote: str) -> tuple[list[str], list[str]]:
    """Split the header quote ("first words ..." to "... last words") into its two ends."""
    q = quote.strip().strip("()")
    parts = re.findall(r'"(.*?)"(?=\s*(?:to\b|\)|$))', q)
    if not parts:
        parts = re.findall(r'"(.*)"', q)
    first = parts[0] if parts else ""
    last = parts[-1] if len(parts) > 1 else ""

    def pieces(s: str) -> list[str]:
        out = [p for p in re.split(r"\.\.\.|…", s)]
        return [loose(p) for p in out if loose(p)]

    return pieces(first), pieces(last)


def check_anchor(block: Block, base: list[str]) -> str:
    """Check the quoted first and last words of a block against the base; stop if absent."""
    a, b = block.start, block.end
    if b < a or b > len(base):
        stop(f"{block.tag}: range {a}-{b} outside {block.file} ({len(base)} lines)")
    # A declared range may begin or end on a blank line; the words sit on the nearest
    # text line inside the range (the blank boundary line is kept when applied).
    while a < b and not base[a - 1].strip():
        a += 1
    while b > a and not base[b - 1].strip():
        b -= 1
    first, last = quoted_pieces(block.quote)
    notes = []
    fix = ANCHOR_QUOTE_FIX.get((block.frag, block.index))
    if fix:
        if fix[0] == "first":
            first = [loose(fix[1])]
        else:
            last = [loose(fix[1])]
        notes.append(f"quote corrected: {fix[2]}")

    def begins_on(i: int, words: str) -> bool:
        cur = loose(base[i - 1])
        two = loose(base[i - 1] + " " + (base[i] if i < len(base) else ""))
        pos = two.find(words)
        return bool(cur) and 0 <= pos < len(cur)

    def ends_on(i: int, words: str) -> bool:
        cur = loose(base[i - 1])
        two = loose((base[i - 2] if i >= 2 else "") + " " + base[i - 1])
        pos = two.rfind(words)
        return bool(cur) and pos >= 0 and pos + len(words) > len(two) - len(cur)

    def tail_after(i: int, words: str) -> str:
        two = loose((base[i - 2] if i >= 2 else "") + " " + base[i - 1])
        return two[two.rfind(words) + len(words):]

    def head_before(i: int, words: str) -> str:
        two = loose(base[i - 1] + " " + (base[i] if i < len(base) else ""))
        return two[:two.find(words)]

    if block.kind == "REPLACES":
        # The quoted words open and close the range. A quote that names the content of
        # a wrapper (a Shaded block or a display) may sit up to two lines inside it.
        if first:
            off = next((o for o in range(3) if a + o <= b and begins_on(a + o, first[0])), None)
            if off is None:
                stop(f"{block.tag}: first words {first[0]!r} do not open {block.file} line {a}:\n"
                     f"    {base[a - 1]!r}")
            if off:
                notes.append(f"first words on line {a + off}")
        if last:
            off = next((o for o in range(3) if b - o >= a and ends_on(b - o, last[-1])), None)
            if off is None:
                stop(f"{block.tag}: last words {last[-1]!r} do not close {block.file} line {b}:\n"
                     f"    {base[b - 1]!r}")
            if off:
                notes.append(f"last words on line {b - off}")
            elif block.kind == "REPLACES" and strip_comments(block.body):
                rest = tail_after(b, last[-1])
                body_end = loose(" ".join(strip_comments(block.body)[-2:]))
                if rest and not body_end.endswith(rest):
                    stop(f"{block.tag}: {block.file} line {b} continues after the quoted last "
                         f"words ({rest!r}), and the body does not keep that text")
        if first and block.kind == "REPLACES" and strip_comments(block.body):
            lead = head_before(a, first[0])
            body_start = loose(" ".join(strip_comments(block.body)[:2]))
            if lead and not body_start.startswith(lead):
                stop(f"{block.tag}: {block.file} line {a} has text before the quoted first "
                     f"words ({lead!r}), and the body does not keep it")
    else:
        span = loose(" ".join(base[a - 1:b]))
        for p in first + last[-1:]:
            if p not in span:
                stop(f"{block.tag}: anchor words {p!r} not in {block.file} lines {a}-{b}")
    for words, line in block.confirms:
        if loose(words) not in loose(base[line - 1]):
            stop(f"{block.tag}: confirmation {words!r} not on {block.file} line {line}")
    if not first and not last:
        notes.append("no quoted words in the header")
    return "anchor words match" + (f" ({'; '.join(notes)})" if notes else "")


def git_show(name: str) -> str:
    return subprocess.run(["git", "-C", str(CLONE), "show", f"{BASE_COMMIT}:{name}"],
                          check=True, capture_output=True, text=True).stdout


# ---------------------------------------------------------------------------
# Stage 1: drafted fragments
# ---------------------------------------------------------------------------

def resolve_anchored(blocks: dict[str, list[Block]], base: dict[str, list[str]]) -> list[str]:
    """Place M1_02, M1_03, M1_04 at the anchor comments of A06 and A07."""
    log = []
    a06 = blocks["A06_model_2_2_to_2_4.prose.tex"][0]
    a07 = blocks["A07_section3_payoffs_inference_incentives.prose.tex"][0]
    m103 = blocks["M1_03_laplace_justification.tex"][0]
    m102 = blocks["M1_02_roles.tex"][0]
    m104 = blocks["M1_04_t0_cancellation.tex"][0]
    main = base["main.tex"]

    # M1_03: the text between the anchors must be base lines 337-340 verbatim.
    body = a06.body
    i0 = next((i for i, ln in enumerate(body) if ln.startswith("% ANCHOR M1_03 BEGIN")), None)
    i1 = next((i for i, ln in enumerate(body) if ln.startswith("% ANCHOR M1_03 END")), None)
    if i0 is None or i1 is None or i1 <= i0:
        stop("A06: anchor comments for M1_03 not found")
    kept = loose(" ".join(body[i0 + 1:i1]))
    want = loose(" ".join(main[m103.start - 1:m103.end]))
    if kept != want:
        stop("A06: text between the M1_03 anchors differs from main.tex lines "
             f"{m103.start}-{m103.end}")
    if not (a06.start <= m103.start <= m103.end <= a06.end):
        stop("M1_03 range lies outside A06")
    body[i0:i1 + 1] = strip_comments(m103.body)
    log.append(f"M1_03 placed between the A06 anchors (verbatim old lines {m103.start}-{m103.end} replaced)")

    # M1_02: anchor line follows the sentence that ends base line 349.
    j = next((i for i, ln in enumerate(body) if ln.startswith("% ANCHOR M1_02")), None)
    if j is None:
        stop("A06: anchor comment for M1_02 not found")
    prev = next(ln for ln in reversed(body[:j]) if ln.strip())
    if loose(main[m102.end - 1])[-40:] not in loose(prev):
        stop("A06: the line before the M1_02 anchor does not end like main.tex line "
             f"{m102.end}")
    if not (a06.start <= m102.end <= a06.end):
        stop("M1_02 anchor line lies outside A06")
    body[j:j + 1] = strip_comments(m102.body)
    log.append(f"M1_02 placed at the A06 anchor (old insert point after line {m102.end})")

    # M1_04: anchor at the end of A07, which ends at base line 564.
    body = a07.body
    k = next((i for i, ln in enumerate(body) if ln.startswith("% ANCHOR M1_04")), None)
    if k is None:
        stop("A07: anchor comment for M1_04 not found")
    if m104.end != a07.end:
        stop(f"M1_04 inserts after line {m104.end}, A07 ends at {a07.end}")
    body[k:k + 1] = strip_comments(m104.body)
    log.append(f"M1_04 placed at the A07 anchor (old insert point after line {m104.end})")
    return log


def apply_blocks(name: str, base: list[str], blocks: list[Block]) -> tuple[list[str], list[str]]:
    ops = []
    for b in blocks:
        if b.kind == "REPLACES":
            ops.append((float(b.start), b))
        elif b.kind == "INSERT AFTER":
            ops.append((b.end + 0.5, b))
        else:
            ops.append((b.start - 0.5, b))
    # Overlap checks.
    reps = [b for b in blocks if b.kind == "REPLACES"]
    for i, x in enumerate(reps):
        for y in reps[i + 1:]:
            if x.start <= y.end and y.start <= x.end:
                stop(f"overlap in {name}: {x.tag} ({x.start}-{x.end}) and {y.tag} ({y.start}-{y.end})")
    for pos, b in ops:
        if b.kind == "REPLACES":
            continue
        after = int(pos - 0.5)  # insertion point lies after this line
        for x in reps:
            if x.start <= after < x.end:
                stop(f"overlap in {name}: insert {b.tag} after line {after} falls inside "
                     f"{x.tag} ({x.start}-{x.end})")
    seen: dict[float, str] = {}
    for pos, b in ops:
        if b.kind != "REPLACES":
            if pos in seen:
                stop(f"two inserts at the same point in {name}: {seen[pos]} and {b.tag}")
            seen[pos] = b.tag

    lines = list(base)
    report = []
    for pos, b in sorted(ops, key=lambda o: -o[0]):
        body = b.final_body
        if b.kind == "REPLACES":
            old_first, old_last = base[b.start - 1], base[b.end - 1]
            before = base[b.start - 2] if b.start >= 2 else ""
            after = base[b.end] if b.end < len(base) else ""
            body = list(body)
            if not old_first.strip() and body and body[0].strip():
                body = [""] + body
            if not old_last.strip() and body and body[-1].strip():
                body = body + [""]
            lines[b.start - 1:b.end] = body
            report.append(
                f"{b.tag:52s} REPLACES {name} {b.start}-{b.end} ({b.end - b.start + 1} -> {len(body)} lines); {b.anchor_note}\n"
                f"      context before: {before[-90:]!r}\n"
                f"      old first:      {old_first[:90]!r}\n"
                f"      new first:      {(body[0] if body else '')[:90]!r}\n"
                f"      old last:       {old_last[-90:]!r}\n"
                f"      new last:       {(body[-1] if body else '')[-90:]!r}\n"
                f"      context after:  {after[:90]!r}")
        else:
            idx = int(pos + 0.5) - 1  # lines kept before the insertion point
            mode = INSERT_MODE.get(b.frag, "paragraph")
            ins = list(body)
            if mode == "paragraph":
                if idx >= 1 and lines[idx - 1].strip():
                    ins = [""] + ins
                if idx < len(lines) and lines[idx].strip():
                    ins = ins + [""]
            lines[idx:idx] = ins
            report.append(
                f"{b.tag:52s} {b.kind} {name} line {idx} ({mode}, {len(body)} lines); {b.anchor_note}\n"
                f"      anchor line:   {base[idx - 1][-90:]!r}\n"
                f"      new first:     {(body[0] if body else '')[:90]!r}\n"
                f"      new last:      {(body[-1] if body else '')[-90:]!r}\n"
                f"      next line:     {(base[idx] if idx < len(base) else '')[:90]!r}")
    return lines, report


def stage_fragments(base: dict[str, list[str]]) -> dict[str, list[str]]:
    print("=" * 78)
    print("STAGE 1. Drafted fragments")
    print("=" * 78)
    blocks: dict[str, list[Block]] = {}
    for fname in FRAGMENTS:
        path = DRAFTS / fname
        if not path.exists():
            stop(f"missing fragment {path}")
        blocks[fname] = parse_fragment(path, FRAGMENT_PREPROCESS)
    # Check anchors against the base before any change.
    for fname, bl in blocks.items():
        for b in bl:
            b.anchor_note = check_anchor(b, base[b.file])
            for words, line in b.confirms:
                print(f"  confirmed {b.tag}: {words!r} on {b.file} line {line}")
    # Superseded bodies.
    for (fname, idx), sub in SUPERSEDED.items():
        sub_text = (INTEG / sub).read_text()
        if f"SUPERSEDES: the body of drafts/{fname}" not in sub_text:
            stop(f"integration/{sub} does not declare that it supersedes {fname}")
        blocks[fname][idx].body = sub_text.split("\n")
        print(f"  {fname}#{idx}: body superseded by integration/{sub} (same range, "
              f"{blocks[fname][idx].file} {blocks[fname][idx].start}-{blocks[fname][idx].end})")
    for line in resolve_anchored(blocks, base):
        print("  " + line)
    out = {}
    for name in FILES:
        todo = []
        for fname, bl in blocks.items():
            if fname in ANCHORED:
                continue
            for b in bl:
                if b.file == name:
                    b.final_body = strip_comments(b.body)
                    todo.append(b)
        lines, report = apply_blocks(name, base[name], todo)
        print(f"\n--- {name}: {len(todo)} blocks applied bottom-up "
              f"({len(base[name])} -> {len(lines)} lines)")
        for r in reversed(report):
            print("  " + r)
        out[name] = lines
    return out


# Repairs to fragment text before parsing: (old, new, expected count). Each one is logged.
FRAGMENT_PREPROCESS: dict[str, list[tuple[str, str, int]]] = {
    # B01: the drafter kept one sentence commented out until both C.9 values existed in
    # reconciliation.csv. They exist (sech_entry_strong, student_t3_entry_strong). The C.9
    # contract labels them fixed-full-order calculations, so the sentence says so.
    "B01_main_noise.prose.tex": [
        ("% OPTIONAL: include the next sentence only after both quantities appear in "
         "reconciliation.csv.\n% At the same score bound, entry is \\NUM{entry_hypsec_r1} "
         "under hyperbolic-secant noise and \\NUM{entry_t3_r1} under Student \\(t_3\\) noise.\n",
         "At the same score bound, with full orders held fixed, entry is "
         "\\NUM{entry_hypsec_r1} under hyperbolic-secant noise and \\NUM{entry_t3_r1} under "
         "Student \\(t_3\\) noise (Online Appendix C.9).\n", 1),
    ],
    "M2_20_oa_elsewhere.tex": [
        # Block 4 ends mid-line: base line 492 continues "For a correctly signed order of"
        # into the display at line 493; the drafted body dropped those words.
        ("A.3} gives the residual upper bound.\n",
         "A.3} gives the residual upper bound. For a correctly signed order of\n", 1),
        # Block 12 ends mid-line: base line 1832 continues "Entry is enclosed by evaluating
        # the exact tail formula" into line 1833; the drafted body dropped those words.
        ("margin at the same\nstrength.\n",
         "margin at the same\nstrength. Entry is enclosed by evaluating the exact tail formula\n", 1),
    ],
}




# ---------------------------------------------------------------------------
# Stage 2: integrator edits. Each edit: (id, file, old, new, expected count, reason).
# The ids are the keys of the integration record (INTEGRATION.md).
# ---------------------------------------------------------------------------

def body(name: str) -> str:
    """Body of an integration fragment: the file without its leading comment header."""
    return "\n".join(strip_comments((INTEG / name).read_text().split("\n")))


def edits() -> list[tuple[str, str, str, str, int, str]]:
    E: list[tuple[str, str, str, str, int, str]] = []
    M, O = "main.tex", "online_appendix.tex"

    # --- X1. Class model wording in the abstract and Section 2.1 (and two stragglers).
    E += [
        ("X1a", M, "Challenger participation and high-value\nchallenger ownership increase.",
         "Challenger participation rises, and so does the\nprobability that a challenger "
         "from the high-value class acquires the target.", 1,
         "abstract: ownership by the high-value class, as in the introduction"),
        ("X1b", M, "The benchmark suppresses\nthe buyer's initial information and gives the "
         "investor perfect\ninformation so that the mechanism is easy to see;",
         "The model suppresses\nthe buyer's initial information and gives the investor "
         "exact knowledge\nof the challenger's quality class, though not of its value, so "
         "that the\nmechanism is easy to see;", 1,
         "Section 2.1: the investor observes the class, not the value"),
        ("X1c", M, "A reserve that excludes a low-value challenger, for instance,",
         "A reserve that excludes the low-value class, for instance,", 1,
         "introduction: class wording, as in Section 6.3"),
        ("X1d", M, "price. A high-value challenger is more likely to receive favorable",
         "price. A challenger from the high-value class is more likely to receive favorable", 1,
         "Section 5.3 (M2_02): class wording, as in the introduction"),
    ]
    # --- X2. Retag (A2)->(A1) and (A3)->(A2): see retag() below (tags and literal text).
    # --- X3. Certificate index j -> i (Proposition 3, Appendix A.3, Online Appendix B.4).
    E += [
        ("X3a", M, "\\((q_H,q_L)=(1,-v_j)\\) at strengths\n\\(r_j\\) whose",
         "\\((q_H,q_L)=(1,-v_i)\\) at strengths\n\\(r_i\\) whose", 1, "Proposition 3"),
        ("X3b", M, "r_j&v_j&\\mathsf E_j\\\\[3pt]", "r_i&v_i&\\mathsf E_i\\\\[3pt]", 1,
         "display (13)"),
        ("X3c", M, "Writing \\(v_{j,-}\\) and \\(v_{j,+}\\) for the endpoints of the bracket at\n"
         "\\(r_j\\), the enclosures",
         "Writing \\(v_{i,-}\\) and \\(v_{i,+}\\) for the endpoints of the bracket at\n"
         "\\(r_i\\), the enclosures", 1, "Appendix A.3, interval signs"),
        ("X3d", M, "On the mesh \\(s_j=j/n\\), interval arithmetic bounds \\(U_H'(s_j)\\)",
         "On the mesh \\(s_i=i/n\\), interval arithmetic bounds \\(U_H'(s_i)\\)", 1,
         "Appendix A.3, high-type cover"),
        ("X3e", M, "\\ge\\min_j\\underline{U_H'(s_j)}-\\frac{L_U}{2n}>0.",
         "\\ge\\min_i\\underline{U_H'(s_i)}-\\frac{L_U}{2n}>0.", 1, "(A.19)"),
        ("X3f", M, "\\(\\rho\\Delta_T(r_j)/2\\le k\\) there",
         "\\(\\rho\\Delta_T(r_i)/2\\le k\\) there", 1, "Appendix A.3, no-trade coexistence"),
        ("X3g", O, "For \\(s_j=j/n\\), evaluate interval enclosures of \\(U_H'(s_j)\\)",
         "For \\(s_i=i/n\\), evaluate interval enclosures of \\(U_H'(s_i)\\)", 1,
         "Online Appendix B.4"),
        ("X3h", O, "\\Gamma_H:=\\min_j\\inf U_H'(s_j;[v_-,v_+])",
         "\\Gamma_H:=\\min_i\\inf U_H'(s_i;[v_-,v_+])", 1, "Online Appendix B.4"),
    ]
    # --- X4. Appendix A.6: W_0, W_theta -> V_0, V_theta (W_H is the win probability).
    E += [
        ("X4a", M, "\\(W_0(R)=R\\mathbf1\\{R\\ge p\\}\\)",
         "\\(\\mathcal V_0(R)=R\\mathbf1\\{R\\ge p\\}\\)", 1, "A.6 allocation value"),
        ("X4b", M, "\\(W_\\theta(R)=\\max\\{R,\\theta\\}\\)",
         "\\(\\mathcal V_\\theta(R)=\\max\\{R,\\theta\\}\\)", 1, "A.6 allocation value"),
        ("X4c", M, "W_\\theta(R)-W_0(R)", "\\mathcal V_\\theta(R)-\\mathcal V_0(R)", 1, "(A.39)"),
    ]
    # --- X5. M1_04 and M1_05: the sign of the entry gains needs its condition.
    E += [
        ("X5a", M, "Each gain is positive, because entry raises expected proceeds with\n"
         "either class.",
         "Each gain is nonnegative, because an admissible challenger raises\nproceeds to at "
         "least the reserve and an inadmissible one leaves them\nunchanged. Both gains are "
         "strictly positive when both class supports\nlie above the reserve, as in the "
         "benchmark.", 1, "M1_04: t_j >= t_0 always; strict under supports above p"),
        ("X5b", M, "\\(V_T\\), not the interim price, and entry raises expected proceeds\n"
         "with either class because \\(t_H>t_0\\) and \\(t_L>t_0\\).",
         "\\(V_T\\), not the interim price. In the benchmark both values lie above\nthe "
         "reserve, so \\(t_H>t_0\\) and \\(t_L>t_0\\), and entry raises expected\nproceeds "
         "with either class.", 1, "M1_05: same condition, stated for the benchmark"),
    ]
    # --- X6. Part (iii) of Proposition 2 in B02: the order bound follows from (A3).
    E += [
        ("X6", M, "\\(\\Delta_T(r_2)\\ge\\Delta_T(r_1)\\) preserves the strict order bound.",
         "\\(\\Delta_T(r_2)\\ge\\Delta_T(r_1)\\) by "
         "\\hyperref[result-proposition-1]{Proposition 1}(b), so the strict order\nbound "
         "of \\eqref{eq:paper-a3} holds at \\(r_2\\) with no separate condition.", 1,
         "B02 proof: name the source of the part (iii) order bound"),
    ]
    # --- X7. M1_03 sentence aligned with the conditions of B01 and B03 (fix round 1).
    E += [
        ("X7", M, "Laplace noise is the extreme member: it is\nthe least dispersed law, and at "
         "the same orders it gives the most\ninformative price.",
         "Laplace noise is the extreme member: among\nlaws with median zero it has the "
         "thinnest tails, and at every pure\norder profile it gives the most informative "
         "flow experiment\n(\\hyperref[sec-noise-and-preparation-costs]{Section 5.1}).", 1,
         "M1_03: same claim and conditions as B01 and the Online Appendix A.6 lemma"),
    ]
    # --- X8. Atomless costs: the declared low law is uniform on [0, 2 eps_C].
    E += [
        ("X8a", M, "supported within\n\\([0,\\varepsilon_C]\\) and",
         "supported within\n\\([0,2\\varepsilon_C]\\) and", 1, "(A.24) supports"),
        ("X8b", M, "\\varepsilon_C<B_{r_1}(m),\\\\", "2\\varepsilon_C<B_{r_1}(m),\\\\", 1,
         "(A.24) first line"),
        ("X8c", M, "The atomless-cost parameter is \\(\\varepsilon_C=\\NUM{atomless_epsilon_C}\\).\n"
         "It measures the low component's support from zero and the high component's\n"
         "support around \\(c_H\\), as in \\eqref{eq:paper-a-24}.",
         "The atomless-cost half-width is \\(\\varepsilon_C=\\NUM{atomless_epsilon_C}\\).\n"
         "The low cost component is uniform on \\([0,2\\varepsilon_C]\\), and the high\n"
         "component is uniform on \\([c_H-\\varepsilon_C,c_H+\\varepsilon_C]\\), as in\n"
         "\\eqref{eq:paper-a-24}.", 1, "Appendix A.8: the declared law of C.0 and C.1"),
        ("X8d", O, "\\([0,\\varepsilon_C]\\) and\n\\([c_H-\\varepsilon_C,c_H+\\varepsilon_C]\\). "
         "Retain (A3) and impose\n\\(\\varepsilon_C<B_{r_1}(m)\\), and",
         "\\([0,2\\varepsilon_C]\\) and\n\\([c_H-\\varepsilon_C,c_H+\\varepsilon_C]\\). "
         "Retain (A3) and impose\n\\(2\\varepsilon_C<B_{r_1}(m)\\), and", 1,
         "Online Appendix A.6 (M2_10), as in the contract"),
        ("X8e", O, "then reads \\(B_{r_1}(m)-\\varepsilon_C\\). Verify all",
         "then reads \\(B_{r_1}(m)-2\\varepsilon_C\\). Verify all", 1, "C.1 margin remark"),
        ("X8f", O, "parameter, and replace cost atoms by the declared atomless components on\n"
         "\\([0,\\NUM{atomless_low_upper}]\\) and\n\\([c_H-\\varepsilon_C,c_H+\\varepsilon_C]\\). "
         "Their mixture weights remain\n\\(\\rho,1-\\rho\\). These replacements define "
         "separate economies.",
         "parameter, and replace cost atoms by a mixture of uniforms on\n"
         "\\([0,2\\varepsilon_C]\\) and \\([c_H-\\varepsilon_C,c_H+\\varepsilon_C]\\).\n"
         "Their mixture weights remain \\(\\rho,1-\\rho\\). The low interval keeps\nwidth "
         "\\(2\\varepsilon_C\\) and has no negative costs. Its upper endpoint\nstays below "
         "the gross-profit floor at every declared baseline strength.\nIts mean is "
         "\\(\\varepsilon_C\\), so its surplus change differs from the\natomic case. These "
         "replacements define separate economies.", 1, "C.1 inputs, from the contract"),
        ("X8g", O, "\\NormalTok{cost\\_halfwidth = \\NUM{atomless_epsilon_C}; cost\\_low\\_support "
         "= [0, \\NUM{atomless_low_upper}]; value\\_band\\_halfwidth = 0.05;}",
         "\\NormalTok{cost\\_halfwidth = \\NUM{atomless_epsilon_C}; "
         "low\\_cost\\_uniform\\_support = [0, 0.2];}\n"
         "\\NormalTok{value\\_band\\_halfwidth = 0.05;}", 1,
         "C.0 benchmark declaration: the contract's key and line breaks"),
    ]
    # --- X9. Online Appendix Section C reconciled with the validated contract.
    E += [
        ("X9a", O, "lower plateau binds only at B(m) = 0;}",
         "lower plateau enters at B(m) = c\\_L;}", 1, "C.0 tie rule: the contract literal"),
        ("X9b", O, "These controls govern the continuation records of C.2 and C.6 and the\n"
         "event exercise C.6c. A price atom is validated by the",
         "These controls govern the continuation records of C.2 and C.6 and the\n"
         "event exercise C.6c. Exercise C.6b is retired because zero-cost\npreparation "
         "never vanishes under the tie rule. A price atom is validated by the", 1,
         "C.0 controls: retirement sentence from the contract"),
        ("X9c", O, "and is recorded, but it accepts nothing on its own. An exact declared",
         "and is recorded, but it accepts nothing on its own. At a zero-spread\n"
         "constant-price node with identical state order laws, Bayes' rule gives\nthe prior "
         "on the full price preimage; the code does not invert a\nconstant map. An exact "
         "declared", 1, "C.0 controls: zero-spread rule from the contract"),
        ("X9d", O, "\\NormalTok{T\\_and\\_Y\\_independent\\_given\\_fundamental = yes.}\n"
         "\\end{Highlighting}\n\\end{Shaded}\n",
         "\\NormalTok{T\\_and\\_Y\\_independent\\_given\\_fundamental = yes.}\n"
         "\\end{Highlighting}\n\\end{Shaded}\n\n" + body("I02_oa_c0_noise_declaration.tex") + "\n",
         1, "C.0: declaration of the C.9 noise laws (integration/I02)"),
        ("X9e", O, "appendix, the endpoint equality \\(p_L=h\\) and the\nexpensive-entry ceiling "
         "equality",
         "appendix, the zero-cost floor equality, which is the endpoint\n\\(p_L=h\\) for "
         "binary values and \\(p_L=h+\\varepsilon_V\\) for uniform\nclasses, and the "
         "expensive-entry ceiling equality", 1, "C.6 event grid: class endpoint"),
        ("X9f", O, "is tested separately. At \\(p_L=h\\) the offsets run only below the endpoint.",
         "is tested separately. The floor endpoint also carries the three\noffsets above "
         "it, beyond the value support, where gross profit and the\nzero cost are equal.", 1,
         "C.6 event grid: offsets above the endpoint are evaluated (event ledger)"),
        ("X9g", O, "zero preparation cost; its equality event inside the reserve domain is the\n"
         "endpoint \\(p_L=h\\).",
         "zero preparation cost; its equality event is the endpoint \\(p_L=h\\) for\n"
         "binary values and \\(p_L=h+\\varepsilon_V\\) for uniform classes.", 1,
         "C.6 data dictionary: class endpoint"),
        ("X9h", O, "additional final-pass nodes. A bounded refinement of near-root\ncandidates "
         "is followed by full revalidation before economically\nidentical continuations are "
         "merged.",
         "additional final-pass nodes. A bounded refinement of near-root\ncandidates is "
         "followed by full revalidation before economically\nidentical continuations are "
         "merged. For interior pure candidates, the\nrefinement solves both held-schedule "
         "first-order equations. It requires\nresidual below \\texttt{1e-10} and movement "
         "within the existing order\nidentity tolerance. Raw candidates and unconverged "
         "starts remain in the\nledger.", 1, "C.6 coverage: bounded refinement, from the contract"),
        ("X9i", O, "Reserve-event endpoints & C.6c & probability; model units \\\\",
         "Gross trade profits and sufficient stake bounds & C.9 & payoff per share;\norder "
         "units \\\\\nEntry under additional noise laws at fixed orders & C.9 & probability "
         "\\\\", 1, "C.8 families: the registry has C.9 rows, no event keys"),
        ("X9j", O, "\\texttt{epsilon\\_V}, \\texttt{r}, and \\texttt{p} exactly; the event keys\n"
         "select on the defining relation of the event. The minimum-margin keys are a",
         "\\texttt{epsilon\\_V}, \\texttt{r}, and \\texttt{p} exactly. The minimum-margin "
         "keys are a", 1, "C.8: no event keys in the registry"),
        ("X9k", O, "used to fill a missing certificate. The keys \\texttt{pool\\_*} from the "
         "retired\nexercise C.6b have no producing row and stay unresolved by design; a\n"
         "manifest that still lists one as required reads a stale contract.",
         "used to fill a missing certificate. The seven registry keys of the\nretired "
         "exercise C.6b are withdrawn and supply no current quantity.", 1,
         "C.8: the C.6b keys are removed from the registry, not left unresolved"),
        ("X9l", O, "the validated exercise outputs in C.1 to C.7. The manifest specifies",
         "the validated exercise outputs in C.1 to C.7 and C.9. The manifest specifies", 1,
         "C.8 opening, from the contract"),
        ("X9m", O, "\\section{D. Institutional pilot and empirical design}\\label{oa-d}",
         body("I01_oa_c9_exercise.tex") + "\n\n"
         "\\section{D. Institutional pilot and empirical design}\\label{oa-d}", 1,
         "new subsection C.9 (integration/I01)"),
        ("X9n", O, "\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c7\\_bargaining.py}",
         "\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c7\\_bargaining.py}\n"
         "\\VariableTok{$PY}\\NormalTok{ numerics/exercises/c9\\_revision.py}", 1,
         "E.1 run list: the C.9 producer, from the contract"),
        ("X9o", O, "\\VariableTok{$PY}\\NormalTok{ numerics/verify.py }\\AttributeTok{{-}{-}final}\n"
         "\\end{Highlighting}\n\\end{Shaded}\n",
         "\\VariableTok{$PY}\\NormalTok{ numerics/verify.py }\\AttributeTok{{-}{-}final}\n"
         "\\end{Highlighting}\n\\end{Shaded}\n\nFor this version, the release gate runs the "
         "producer and presentation\ncommands above and then the release checks in\n"
         "\\texttt{numerics/release\\_checks.py}. The wrappers described next also run a\n"
         "test suite and are not part of that gate.\n", 1,
         "E.1: the release gate of this version (NUMERICS.md), from the contract"),
    ]
    # --- X10. Main-text sentence that the event ledger contradicts (M2_08).
    E += [
        ("X10", M, "Offsets from this event run only below \\(h\\), inside the domain, where the\n"
         "zero-cost comparison is strict.",
         "Offsets below this event lie inside the domain, where the zero-cost\ncomparison "
         "is strict.", 1, "Appendix A.7: offsets above the endpoint are also evaluated"),
    ]
    # --- X11. Lemma OA.2 in the general-prior notation of the main text (M2_20 note).
    E += [
        ("X11a", O, "\\emph{For prior \\(\\pi\\in(0,1)\\), let\n"
         "\\(\\mu_-=\\operatorname{logistic}(\\operatorname{logit}\\pi-2/b)\\),\n"
         "\\(\\mu_+=\\operatorname{logistic}(\\operatorname{logit}\\pi+2/b)\\), and\n"
         "\\(\\omega=\\min\\{\\mu_-,1-\\mu_+\\}\\). Suppose\n"
         "\\(B_{r_0}(\\pi)<c_H<B_{r_1}(\\mu_+)\\) and\n"
         "\\(\\Delta_T(r_0)<k<(1-1/b)\\rho\\omega\\Delta_T(r_1)\\). Then the benchmark\n"
         "entry reversal and unique trading outcomes hold. No condition on the low cost\n"
         "is needed: gross profit at \\(\\mu_-\\) is positive on this support, so the\n"
         "zero-cost realization prepares at every feasible belief.}",
         "\\emph{For prior \\(\\pi\\in(0,1)\\), let \\(m(\\pi)\\) and \\(M(\\pi)\\) be the "
         "posterior\nbounds of the paper, and \\(\\kappa(\\pi)=\\min\\{m(\\pi),1-M(\\pi)\\}\\). "
         "Suppose\n\\(B_{r_0}(\\pi)<c_H<B_{r_1}(M(\\pi))\\) and\n"
         "\\(\\Delta_T(r_0)<k<(1-1/b)\\rho\\kappa(\\pi)\\Delta_T(r_1)\\). Then the benchmark\n"
         "entry reversal and unique trading outcomes hold. No condition on the low cost\n"
         "is needed: gross profit at \\(m(\\pi)\\) is positive on this support, so the\n"
         "zero-cost realization prepares at every feasible belief.}", 1,
         "Lemma OA.2: mu_-=m(pi), mu_+=M(pi), omega=kappa(pi); omega is now the stake of A.12"),
        ("X11b", O, "residual lower bound is therefore \\(\\rho\\omega\\Delta_T\\), while the",
         "residual lower bound is therefore \\(\\rho\\kappa(\\pi)\\Delta_T\\), while the", 1,
         "proof of Lemma OA.2"),
    ]
    # --- X12. Online Appendix A.6 lemma heading as a run-in heading (A.6 has more text).
    E += [
        ("X12", O, "\\subsubsection{Laplace is the extreme member of the class}"
         "\\label{oa-a-laplace-extreme}\n\nWrite",
         "\\protect\\phantomsection\\label{oa-a-laplace-extreme}\n"
         "\\noindent\\textbf{Laplace is the extreme member of the class.}\nWrite", 1,
         "B03: a subsubsection would put the rest of A.6 under the lemma's heading"),
    ]
    # --- X15-X17. Clarity fixes found in the integrated read.
    E += [
        ("X15", M, "Under full orders, its log odds relative to prior odds equal",
         "Under full orders, the Laplace log odds relative to prior odds equal", 1,
         "B01: the pronoun followed a paragraph break and had no antecedent"),
        ("X16", M, "The bracket is nonnegative. A prepared low-value challenger that meets "
         "the reserve\npays \\(\\max\\{p,\\min(R,\\ell)\\}\\ge p\\mathbf1\\{R\\ge p\\}\\) in each "
         "incumbent state, and\none that fails the reserve leaves the no-challenger payment "
         "in place, so",
         "The bracket is nonnegative. With a prepared low-value challenger that meets the\n"
         "reserve, the target receives \\(\\max\\{p,\\min(R,\\ell)\\}\\ge p\\mathbf1\\{R\\ge p\\}\\) "
         "in each\nincumbent state, and one that fails the reserve leaves the no-challenger\n"
         "payment in place, so", 1,
         "M2_08: the inequality is about target proceeds; the challenger does not pay R"),
        ("X17", M, "Each\nposterior stays in \\([m(\\pi),M(\\pi)]\\), so the investor keeps a",
         "Each\nposterior stays in the interval \\([m(\\pi),M(\\pi)]\\) of\n"
         "\\hyperref[sec-inference]{Section 3.2}, so the investor keeps a", 1,
         "M1_03: m(pi), M(pi) are defined in Section 3.2, after this paragraph"),
    ]
    # --- X13. Close the gap that the removed (A.45)-(A.49) leave (labels stay).
    for old_n, new_n in zip(range(50, 58), range(45, 53)):
        E.append((f"X13.{old_n}", M, f"\\tag{{A.{old_n}}}", f"\\tag{{A.{new_n}}}", 1,
                  f"retag (A.{old_n}) as (A.{new_n}); references use \\eqref"))
    return E


def apply_edits(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 2. Integrator edits (expected counts must match)")
    print("=" * 78)
    for eid, name, old, new, count, why in edits():
        n = text[name].count(old)
        if n != count:
            stop(f"edit {eid} ({name}): expected {count} of {old[:70]!r}, found {n}")
        text[name] = text[name].replace(old, new)
        print(f"  {eid:7s} {name:20s} x{count}  {why}")


def scoped_stake_section(text: dict[str, str]) -> None:
    """X14: notation and numbering inside the new Online Appendix A.12 (fragment M1_08)."""
    oa = text["online_appendix.tex"]
    head = "\\subsection{A.12. An informed shareholder}\\label{oa-a-stake}"
    tail = "\\section{B. Computer-assisted equilibrium certificates}"
    if oa.count(head) != 1 or oa.count(tail) != 1:
        stop("A.12 scope markers not found exactly once")
    i, j = oa.index(head), oa.index(tail)
    seg = oa[i:j]
    steps = [
        ("X14a", r"G_([HLj])(?=(?:'?\(q\)|\\ge))", r"\\bar A_\1", 12,
         "G_H(q), G_L(q) -> \\bar A_H(q), \\bar A_L(q): G_j is the class value cdf"),
        ("X14b", r"\\\(D=\\\{x:", r"\\(\\mathcal X_\\tau=\\{x:", 1,
         "entry flow set D -> \\mathcal X_\\tau: D(u) is G_L-G_H"),
        ("X14c", r"\\int_D f\(x-q\)", r"\\int_{\\mathcal X_\\tau}f(x-q)", 1, "same set"),
        ("X14d", r"\\int_\{D\\cap", r"\\int_{\\mathcal X_\\tau\\cap", 2, "same set"),
        ("X14e", r"monotonicity condition on \\\(D\\\)", r"monotonicity condition on \\(\\mathcal X_\\tau\\)",
         1, "same set"),
        ("X14f", r"\\\(D=\[x\^\*,\\infty\)\\\)", r"\\(\\mathcal X_\\tau=[x^*,\\infty)\\)", 1, "same set"),
        ("X14g", r"In the ranked cases \\\(w_H>w_L\\ge 0\\\), with\n\\\(w_H>0\\\) when",
         r"In the ranked cases \\(w_H\\ge w_L\\ge 0\\), with\n\\(w_H>w_L\\) when", 1,
         "w_H >= w_L >= 0 under the ranking, strict exactly when the spread is positive"),
        ("X14h", r"Since \\\(w_H>w_L\\\), the stake bound",
         r"Since \\(w_H\\ge w_L\\ge0\\), the stake bound", 1, "same"),
    ]
    for sid, pat, rep, count, why in steps:
        seg, n = re.subn(pat, rep, seg)
        if n != count:
            stop(f"{sid}: expected {count} matches of {pat!r} in A.12, found {n}")
        print(f"  {sid:7s} online_appendix.tex  x{count}  {why}")
    # Number the eight displays (OA.57)-(OA.64): the tags that A.11 released.
    parts = seg.split("\n\\]")
    if len(parts) - 1 != 8:
        stop(f"X14i: expected 8 displays in A.12, found {len(parts) - 1}")
    seg = parts[0]
    for k, rest in enumerate(parts[1:]):
        n = 57 + k
        seg += f"\n\\tag{{OA.{n}}}\\label{{eq:oa-oa-{n}}}\n\\]" + rest
    print("  X14i    online_appendix.tex  x8   A.12 displays tagged (OA.57)-(OA.64), the "
          "numbers released by A.11")
    text["online_appendix.tex"] = oa[:i] + seg + oa[j:]


def retag(text: dict[str, str]) -> None:
    """X2: conditions (A2), (A3) become (A1), (A2); labels stay."""
    print("\n  X2: retag the surviving conditions")
    m = text["main.tex"]
    for old, new in [("\\tag{A2}\\label{eq:paper-a2}", "\\tag{A1}\\label{eq:paper-a2}"),
                     ("\\tag{A3}\\label{eq:paper-a3}", "\\tag{A2}\\label{eq:paper-a3}")]:
        if m.count(old) != 1:
            stop(f"X2: {old} not found once in main.tex")
        m = m.replace(old, new)
        print(f"  X2      main.tex             x1   {old} -> {new}")
    text["main.tex"] = m
    for name in FILES:
        t = text[name]
        for lit in ("(A1)", "eq:paper-a1}"):
            if t.count(lit):
                stop(f"X2: {name} still contains {lit!r} before the retag")
        n2, n3 = t.count("(A2)"), t.count("(A3)")
        t = t.replace("(A3)", "(A\x002)").replace("(A2)", "(A1)").replace("(A\x002)", "(A2)")
        text[name] = t
        print(f"  X2      {name:20s} literal (A2)->(A1) x{n2}, (A3)->(A2) x{n3}")


# ---------------------------------------------------------------------------
# Stage 3: numbers
# ---------------------------------------------------------------------------

# Placeholder -> reconciliation name. The drafters' names map through the definitions in
# their notes files (M1_00_NOTES, M2_00_NOTES, B00_NOTES).
NUM_MAP = {
    "Pi_acc": "Pi_acc",
    "Pi_hid": "Pi_hid",
    "Delta_R_T": "Delta_R_T",
    "break_even_trade_scale": "break_even_trade_scale",
    "breakeven_scale": "break_even_trade_scale",          # M1_05: W5 ratio, Delta R_T / Pi_acc
    "Omega_U": "Omega_U",
    "Omega_0": "Omega_0",
    "sech_entry_strong": "sech_entry_strong",
    "student_t3_entry_strong": "student_t3_entry_strong",
    "entry_hypsec_r1": "sech_entry_strong",               # B01 optional sentence
    "entry_t3_r1": "student_t3_entry_strong",             # B01 optional sentence
    "atomless_entry_strong_laplace": "cost_mix_laplace_entry_strong",    # M2_01
    "atomless_entry_strong_logistic": "cost_mix_logistic_entry_strong",  # M2_01
    "atomless_epsilon_C": "cost_halfwidth",               # M2_09, M2_15
}


def load_numbers() -> tuple[dict[str, dict], dict[str, dict], dict[str, dict]]:
    recon: dict[str, list[dict]] = {}
    with open(REV / "reconciliation.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            recon.setdefault(row["name"], []).append(row)
    manifest = {}
    with open(NUMERICS / "paper" / "quantity_manifest.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            manifest[row["name"]] = row
    registry = {}
    with open(NUMERICS / "numerics" / "quantity_registry.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            registry[row["name"]] = row
    return recon, manifest, registry


def display(value: str, rule: str) -> str:
    if rule == "exact_input":
        return value
    m = re.fullmatch(r"decimal_(\d+)", rule)
    if not m:
        stop(f"display rule {rule} is not handled here")
    q = Decimal(1).scaleb(-int(m.group(1)))
    return format(Decimal(value).quantize(q, rounding=ROUND_HALF_EVEN), "f")


def substitute(text: dict[str, str]) -> list[tuple]:
    print("\n" + "=" * 78)
    print("STAGE 3. Number placeholders")
    print("=" * 78)
    recon, manifest, registry = load_numbers()
    used = []
    for name in FILES:
        def fill(m: re.Match) -> str:
            ph = m.group(1)
            if ph not in NUM_MAP:
                stop(f"{name}: placeholder \\NUM{{{ph}}} has no mapping")
            key = NUM_MAP[ph]
            rows = recon.get(key, [])
            if len(rows) != 1:
                stop(f"{name}: reconciliation name {key} has {len(rows)} rows")
            value = rows[0]["new_value"]
            rule = manifest[key]["display"]
            shown = display(value, rule)
            reg = registry.get(key, {}).get("value", "n/a")
            used.append((name, ph, key, value, rule, shown, rows[0]["file"], reg))
            return shown
        text[name] = re.sub(r"\\NUM\{([^}]*)\}", fill, text[name])
    for name, ph, key, value, rule, shown, src, reg in used:
        same = "registry agrees" if reg != "n/a" and Decimal(reg) == Decimal(value) else f"registry {reg}"
        print(f"  {name:20s} \\NUM{{{ph}}} -> {shown}   [{key} = {value}; {rule}; {src}; {same}]")
    return used


# ---------------------------------------------------------------------------
# Stage 4: bibliography
# ---------------------------------------------------------------------------

def bib_entries(block: str) -> list[tuple[str, str]]:
    """Split citeproc output into (key, entry text) pairs."""
    out = []
    for chunk in re.split(r"\n(?=\\bibitem\[\\citeproctext\]\{)", block.strip("\n")):
        chunk = chunk.strip("\n")
        m = re.match(r"\\bibitem\[\\citeproctext\]\{(ref-[^}]+)\}", chunk)
        if m:
            out.append((m.group(1), chunk))
    return out


def author_key(entry: str) -> tuple:
    """Author-date sort key: each author's (family, given) in order, then the year.

    The first author is written "Family, Given"; later authors "Given Family". A single
    author sorts before the same author with coauthors, as in the citeproc output."""
    txt = " ".join(entry.split("\n")[1:])
    m = re.search(r"^(.*?)\.\s+(\d{4}[a-z]?)\.", txt)
    authors, year = (m.group(1), m.group(2)) if m else (txt, "")

    def norm(x: str) -> str:
        x = x.replace("{\\o}", "o").replace("\\o", "o")
        x = re.sub(r"\\[\'\"`^~=.]\{?([A-Za-z])\}?", r"\1", x)
        return re.sub(r"[{}\\]", "", x).strip().lower()

    parts = [q.strip() for q in re.split(r",\s+(?:and\s+)?|\s+and\s+", authors) if q.strip()]
    names = [(norm(parts[0]), norm(parts[1]) if len(parts) > 1 else "")]
    for q in parts[2:]:
        w = q.split()
        names.append((norm(w[-1]), norm(" ".join(w[:-1]))))
    return tuple(names) + ((year, ""),)


def merge_bibliography(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 4. Bibliography")
    print("=" * 78)
    raw = (DRAFTS / "F_bibitems.tex").read_text().split("\n")
    new = dict(bib_entries("\n".join(ln for ln in raw if not ln.startswith("%"))))
    oa_only = {"ref-EdmansGoldsteinJiang2015"}
    for name in FILES:
        t = text[name]
        a = t.index("\\begin{CSLReferences}{1}{1}") + len("\\begin{CSLReferences}{1}{1}")
        b = t.index("\\end{CSLReferences}")
        old = bib_entries(t[a:b])
        keys = [k for k, _ in old]
        sorted_ok = all(author_key(x[1]) <= author_key(y[1]) for x, y in zip(old, old[1:]))
        print(f"  {name}: {len(old)} existing entries; existing order "
              f"{'agrees with' if sorted_ok else 'DIFFERS FROM'} the author-year key")
        cited = set(re.findall(r"\\citeproc\{(ref-[^}]+)\}", t))
        if name == "main.tex":
            add = {k: v for k, v in new.items() if k not in oa_only}
        else:
            add = {k: v for k, v in new.items() if k in oa_only or (k in cited and k not in keys)}
        for k in add:
            if k in keys:
                stop(f"{name}: {k} is already in the bibliography")
        merged = sorted(old + list(add.items()), key=lambda kv: author_key(kv[1]))
        t = t[:a] + "\n" + "\n\n".join(e for _, e in merged) + "\n\n" + t[b:]
        text[name] = t
        have = {k for k, _ in merged}
        missing = sorted(cited - have)
        uncited = sorted(have - cited)
        print(f"  {name}: inserted {len(add)}: {', '.join(sorted(add))}")
        print(f"  {name}: final order: {' '.join(k[4:] for k, _ in merged)}")
        print(f"  {name}: cited keys without an entry: {missing or 'none'}")
        print(f"  {name}: entries without a citation: {uncited or 'none'}")
        if missing:
            stop(f"{name}: citations without bibliography entries: {missing}")


# ---------------------------------------------------------------------------
# Stage 5: checks, write, tables
# ---------------------------------------------------------------------------

def check_and_report(text: dict[str, str], base: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 5. Checks")
    print("=" * 78)
    for name in FILES:
        t = text[name]
        for bad in ("\\NUM{", "% ANCHOR", "% REPLACES", "% INSERT", "% FRAGMENT"):
            if bad in t:
                stop(f"{name}: leftover {bad!r}")
        labels = re.findall(r"\\label\{([^}]+)\}", t)
        dup = sorted({x for x in labels if labels.count(x) > 1})
        if dup:
            stop(f"{name}: duplicate labels {dup}")
        refs = set(re.findall(r"\\(?:eq)?ref\{([^}]+)\}", t)) | set(re.findall(r"\\hyperref\[([^\]]+)\]", t))
        undefined = sorted(refs - set(labels))
        old_labels = set(re.findall(r"\\label\{([^}]+)\}", base[name]))
        print(f"  {name}: {len(labels)} labels; removed {sorted(old_labels - set(labels))}; "
              f"added {sorted(set(labels) - old_labels)}")
        print(f"  {name}: references to undefined labels: {undefined or 'none'}")
        if undefined:
            stop(f"{name}: undefined references {undefined}")
        for sym in ("c_L", "c_{L}", "\\lambda", "(A1)", "(A2)", "(A3)", "high-value challenger",
                    "perfect information", "\\tag{A3}"):
            print(f"  {name}: count of {sym!r}: base {base[name].count(sym)}, now {t.count(sym)}")
        tags = re.findall(r"\\tag\{([^}]+)\}", t)
        dup_tags = sorted({x for x in tags if tags.count(x) > 1})
        if dup_tags:
            stop(f"{name}: duplicate tags {dup_tags}")
        seq = [x for x in tags if re.fullmatch(r"(A|OA)\.\d+", x)]
        nums = {}
        for x in seq:
            p, n = x.split(".")
            nums.setdefault(p, []).append(int(n))
        for p, ns in nums.items():
            gaps = sorted(set(range(1, max(ns) + 1)) - set(ns))
            print(f"  {name}: tags ({p}.n) run 1..{max(ns)}; gaps {gaps or 'none'}; "
                  f"in order {'yes' if ns == sorted(ns) else 'NO'}")


def write_and_copy(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 6. Write the clone and copy the tables")
    print("=" * 78)
    for name in FILES:
        (CLONE / name).write_text(text[name])
        print(f"  wrote {CLONE / name} ({text[name].count(chr(10))} lines)")
    recon_hash = {}
    with open(REV / "reconciliation.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            if row["file"].startswith("tables/") and row["file"].endswith(".tex"):
                recon_hash[row["file"]] = row["new_value"]
    for src in sorted((NUMERICS / "tables").glob("*.tex")):
        rel = f"tables/{src.name}"
        dst = CLONE / rel
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        before = hashlib.sha256(dst.read_bytes()).hexdigest() if dst.exists() else None
        if before != h:
            shutil.copyfile(src, dst)
        status = "copied (changed)" if before != h else "unchanged"
        rec = recon_hash.get(rel)
        agree = "matches reconciliation" if rec == h else f"reconciliation {rec}"
        print(f"  {rel:42s} {status:17s} sha256 {h[:16]}... {agree}")


def main() -> None:
    base = {name: git_show(name).split("\n") for name in FILES}
    print(f"Base commit {BASE_COMMIT}: main.tex {len(base['main.tex'])} lines, "
          f"online_appendix.tex {len(base['online_appendix.tex'])} lines")
    lines = stage_fragments(base)
    if "--dump" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--dump") + 1])
        out.mkdir(parents=True, exist_ok=True)
        for name, ls in lines.items():
            (out / name).write_text("\n".join(ls))
        print(f"stage-1 text written to {out}")
    if "--stage1" in sys.argv:
        return
    text = {name: "\n".join(ls) for name, ls in lines.items()}
    apply_edits(text)
    scoped_stake_section(text)
    retag(text)
    substitute(text)
    merge_bibliography(text)
    base_text = {name: "\n".join(ls) for name, ls in base.items()}
    check_and_report(text, base_text)
    if "--check" in sys.argv:
        print("\n--check: nothing written")
        return
    write_and_copy(text)
    print("\nDone.")


if __name__ == "__main__":
    main()
