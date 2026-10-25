"""Print the labels of a LaTeX .aux file with their printed numbers and pages, and compare two maps.

  python3 label_map.py AUX [--before FILE]

Without --before: a markdown table, one row per \\newlabel, in document order:  | label | printed number | page |
With --before FILE: the earlier map is read and only the differences are printed:
  changed      labels whose printed number differs
  appeared     labels in AUX that the earlier map does not have
  disappeared  labels of the earlier map that AUX does not have
FILE is either this tool's own table or the markdown table of a label map that has the columns "printed" and
"label" (the label in backticks); the columns are found by their headings. Only the kinds of labels that the
earlier map contains (the text before the first colon: prop, tab, fig, ...) are compared; the kinds of AUX that
the earlier map does not contain are listed with their counts and are not compared.
It only prints. Exit status: 0 when the run reached its end, 1 when AUX or FILE cannot be read, AUX holds no label,
the earlier map holds no labelled row, or the program stopped (the output then says so), 2 for a usage error.
"""
import argparse
import collections
import pathlib
import re
import sys


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


def top_groups(text):
    """The top-level {...} groups of text, as strings without their outer braces."""
    groups = []
    i = 0
    while i < len(text):
        if text[i] == "{":
            j = match_brace(text, i)
            groups.append(text[i + 1:j])
            i = j + 1
        else:
            i += 1
    return groups


def clean(s):
    return re.sub(r"\s+", " ", s.replace("{", "").replace("}", "")).strip()


def read_aux(path, seen=None):
    """Ordered dict label -> (printed number, page) from an .aux file and the .aux files it inputs."""
    seen = seen or set()
    path = pathlib.Path(path).resolve()
    labels = collections.OrderedDict()
    if path in seen or not path.exists():
        return labels
    seen.add(path)
    text = path.read_text(errors="replace")
    for m in re.finditer(r"\\newlabel\{|\\@input\{", text):
        i = m.end() - 1
        j = match_brace(text, i)
        if m.group(0).startswith("\\@input"):
            for k, v in read_aux(path.parent / text[i + 1:j], seen).items():
                labels[k] = v
            continue
        label = text[i + 1:j]
        k = j + 1
        if k >= len(text) or text[k] != "{":
            continue
        end = match_brace(text, k)
        groups = top_groups(text[k + 1:end])
        if len(groups) < 2:
            continue
        labels[label] = (clean(groups[0]), clean(groups[1]))
    return labels


def read_before(path):
    """label -> printed number from this tool's table or from a markdown label map with 'printed' and 'label' columns."""
    text = pathlib.Path(path).read_text(errors="replace")
    label_col = number_col = page_col = None
    out = collections.OrderedDict()
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c) and any(cells):
            continue
        low = [c.lower() for c in cells]
        if label_col is None and any(c == "label" for c in low) and any("printed" in c for c in low):
            label_col = low.index("label")
            number_col = next(i for i, c in enumerate(low) if "printed" in c)
            page_col = next((i for i, c in enumerate(low) if c == "page"), None)
            continue
        if label_col is None or label_col >= len(cells) or number_col >= len(cells):
            continue
        m = re.fullmatch(r"`([^`]*)`", cells[label_col])
        label = m.group(1) if m else cells[label_col]
        if not label:
            continue  # a numbered object without a label
        page = cells[page_col] if page_col is not None and page_col < len(cells) else ""
        out[label] = (cells[number_col].strip("`").strip(), page)
    return out


def kind(label):
    return label.split(":", 1)[0] if ":" in label else label


def main(argv=None):
    ap = argparse.ArgumentParser(description="Print the labels of an .aux file; with --before, the labels whose printed number changed.")
    ap.add_argument("aux", metavar="AUX", help="the .aux file")
    ap.add_argument("--before", metavar="FILE", default=None, help="an earlier label map (this tool's output or a markdown label table)")
    args = ap.parse_args(argv)

    if not pathlib.Path(args.aux).is_file():
        print(f"{args.aux}: not found")
        return 1
    now = read_aux(args.aux)
    if not now:
        print(f"no \\newlabel found in {args.aux}")
        return 1
    if args.before is None:
        print(f"label map of {args.aux}: {len(now)} labels")
        print()
        print("| label | printed number | page |")
        print("|---|---|---|")
        for label, (num, page) in now.items():
            print(f"| `{label}` | {num} | {page} |")
        return 0

    try:
        before = read_before(args.before)
    except OSError as exc:
        print(f"cannot read {args.before}: {exc}")
        return 1
    print(f"comparison of {args.aux} ({len(now)} labels) with {args.before} ({len(before)} labels)")
    if not before:
        print("no labelled rows found in the earlier map (a table with the headings 'printed' and 'label' is needed)")
        return 1
    scope = {kind(l) for l in before}
    outside = collections.Counter(kind(l) for l in now if kind(l) not in scope)
    compared = [l for l in now if kind(l) in scope]

    changed = [(l, before[l][0], now[l][0], now[l][1]) for l in compared if l in before and before[l][0] != now[l][0]]
    appeared = [(l, now[l][0], now[l][1]) for l in compared if l not in before]
    gone = [(l, before[l][0]) for l in before if l not in now]
    same = sum(1 for l in compared if l in before and before[l][0] == now[l][0])

    print()
    print(f"changed ({len(changed)}): label, printed number before -> now, page now")
    for l, a, b, pg in changed:
        print(f"  {l}: {a} -> {b}  (page {pg})")
    if not changed:
        print("  (none)")
    print(f"appeared ({len(appeared)}): label, printed number, page")
    for l, b, pg in appeared:
        print(f"  {l}: {b}  (page {pg})")
    if not appeared:
        print("  (none)")
    print(f"disappeared ({len(gone)}): label, printed number before")
    for l, a in gone:
        print(f"  {l}: {a}")
    if not gone:
        print("  (none)")
    print()
    print(f"unchanged {same}; compared {len(compared)} labels of the kinds {', '.join(sorted(scope)) or '(none)'}")
    if outside:
        print("not compared (kinds the earlier map does not contain): " +
              ", ".join(f"{k} {n}" for k, n in sorted(outside.items())))
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except BrokenPipeError:  # the reader closed the pipe (for example "| head"): stop without a traceback
        import os
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        status = 1
    except Exception as exc:  # the program itself stopped: say so on the stream that is read, and exit 1
        import traceback
        print(f"label_map stopped: {type(exc).__name__}: {exc}")
        traceback.print_exc(file=sys.stdout)
        status = 1
    sys.exit(status)
