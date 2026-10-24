"""Apply the round-2 review corrections to the revised manuscript.

Run from the repository root with the project interpreter:

    .venv/bin/python audit/revision_v2_2026_10_21/scripts/round2.py            # writes the clone
    .venv/bin/python audit/revision_v2_2026_10_21/scripts/round2.py --check    # checks only

The script reads main.tex and online_appendix.tex at commit ac4e37e of the revision clone
(the round-1 integration, git -C overleaf/paper-revision show ac4e37e:<file>) and applies,
in order:

  1. content edits to main.tex and online_appendix.tex (round2_edits_main.py and
     round2_edits_oa.py). Each edit is an exact replacement with an expected count, a block
     replacement between two unique anchors, or a set of replacements scoped to a region;
  2. two block moves from Appendix A of the paper to the new Online Appendix subsections
     A.13 (more than two classes) and A.14 (exact reserve events), with their own edits;
  3. equation retagging and label renames in main.tex;
  4. checks: labels, references, tags, citations, and leftover notation;
  5. the write of both files and the copy of the round-2 tables and Figure 4, each checked
     against the hash recorded in round2_artifacts.csv.

Every review item that an edit serves is named in the edit's note; the report prints them.
It stops with a message on any mismatch and writes nothing until every step has passed.
Print-only: it has no assertions.
"""

from __future__ import annotations

import csv
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import round2_edits_main as EM  # noqa: E402
import round2_edits_oa as EO  # noqa: E402

ROOT = HERE.parents[2]
REV = ROOT / "audit" / "revision_v2_2026_10_21"
CLONE = ROOT / "overleaf" / "paper-revision"
NUMERICS = Path("/home/uctpiaj/work/Projects/ccc-revision-numerics")
BASE_COMMIT = "ac4e37e"
FILES = ("main.tex", "online_appendix.tex")


class Stop(Exception):
    pass


def stop(msg: str) -> None:
    raise Stop(msg)


def git_show(name: str) -> str:
    return subprocess.run(["git", "-C", str(CLONE), "show", f"{BASE_COMMIT}:{name}"],
                          check=True, capture_output=True, text=True).stdout


# --- edit primitives -------------------------------------------------------------------

def replace(text: str, old: str, new: str, count: int, eid: str) -> str:
    n = text.count(old)
    if n != count:
        stop(f"{eid}: expected {count} of {old[:90]!r}, found {n}")
    return text.replace(old, new)


def block(text: str, start: str, end: str, new: str, eid: str) -> str:
    n = text.count(start)
    if n != 1:
        stop(f"{eid}: start anchor occurs {n} times: {start[:90]!r}")
    i = text.find(start)
    j = text.find(end, i)
    if j < 0:
        stop(f"{eid}: end anchor not found after start: {end[:90]!r}")
    return text[:i] + new + text[j + len(end):]


def scoped(text: str, rstart: str, rend: str, pairs: list, eid: str) -> str:
    n = text.count(rstart)
    if n != 1:
        stop(f"{eid}: region start occurs {n} times: {rstart[:90]!r}")
    i = text.find(rstart)
    j = text.find(rend, i)
    if j < 0:
        stop(f"{eid}: region end not found: {rend[:90]!r}")
    seg = text[i:j]
    for old, new, count in pairs:
        seg = replace(seg, old, new, count, eid)
    return text[:i] + seg + text[j:]


def apply(text: str, edits: list, label: str) -> str:
    for e in edits:
        kind = e["kind"]
        if kind == "R":
            text = replace(text, e["old"], e["new"], e["count"], e["id"])
            what = f"x{e['count']}"
        elif kind == "B":
            text = block(text, e["start"], e["end"], e["new"], e["id"])
            what = "block"
        elif kind == "S":
            text = scoped(text, e["start"], e["end"], e["pairs"], e["id"])
            what = f"scoped {sum(c for _, _, c in e['pairs'])}"
        else:
            stop(f"{e['id']}: unknown kind {kind}")
        print(f"  {e['id']:8s} {label:4s} {what:11s} {e['why']}")
    return text


def cut(text: str, start: str, end: str, eid: str) -> tuple[str, str]:
    """Remove [start, end) and return (remaining text, removed block)."""
    n = text.count(start)
    if n != 1:
        stop(f"{eid}: cut start occurs {n} times")
    i = text.find(start)
    j = text.find(end, i)
    if j < 0:
        stop(f"{eid}: cut end not found")
    return text[:i] + text[j:], text[i:j]


# --- stages ----------------------------------------------------------------------------

def stage_content(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 1. Content edits (expected counts must match)")
    print("=" * 78)
    text["main.tex"] = apply(text["main.tex"], EM.edits(), "main")
    text["online_appendix.tex"] = apply(text["online_appendix.tex"], EO.edits(), "OA")


def stage_moves(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 2. Moves from Appendix A to the Online Appendix")
    print("=" * 78)
    main, oa = text["main.tex"], text["online_appendix.tex"]
    moved = []
    for mv in EM.moves():
        main, blk = cut(main, mv["start"], mv["end"], mv["id"])
        print(f"  {mv['id']:8s} cut {blk.count(chr(10))} lines from main.tex ({mv['why']})")
        blk = apply(blk, mv["edits"], "mv")
        if mv.get("stub"):
            main = main.replace(mv["end"], mv["stub"] + mv["end"], 1)
            print(f"  {mv['id']:8s} left a summary in main.tex before {mv['end'][:40]!r}")
        moved.append(blk.rstrip("\n") + "\n\n")
    anchor = EO.MOVE_ANCHOR
    if oa.count(anchor) != 1:
        stop("move anchor in online_appendix.tex is not unique")
    oa = oa.replace(anchor, "".join(moved) + anchor)
    print(f"  inserted {len(moved)} subsections before {anchor[:50]!r}")
    text["main.tex"], text["online_appendix.tex"] = main, oa


def stage_retag(text: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 3. Retag and relabel main.tex")
    print("=" * 78)
    t = text["main.tex"]
    for old, new in EM.RETAG:
        t = replace(t, f"\\tag{{{old}}}", f"\\tag{{{new}}}", 1, f"tag {old}")
        print(f"  tag ({old}) -> ({new})")
    for old, new in EM.RELABEL:
        n = t.count("{" + old + "}")
        if n == 0:
            stop(f"label {old} not found")
        if t.count("{" + new + "}"):
            stop(f"label target {new} already in use")
        t = t.replace("{" + old + "}", "{" + new + "}")
        print(f"  label {old} -> {new} ({n} occurrences, definition included)")
    text["main.tex"] = t


def bib_check(t: str, name: str) -> None:
    cited = set(re.findall(r"\\citeproc\{ref-([^}]+)\}", t))
    records = re.findall(r"\\bibitem\[\\citeproctext\]\{ref-([^}]+)\}", t)
    missing = sorted(cited - set(records))
    uncited = sorted(set(records) - cited)
    print(f"  {name}: {len(records)} records, {len(cited)} cited keys; "
          f"missing records {missing or 'none'}; uncited records {uncited or 'none'}")
    if missing:
        stop(f"{name}: citations without a record {missing}")
    if uncited:
        stop(f"{name}: records without a citation {uncited}")


def stage_checks(text: dict[str, str], base: dict[str, str]) -> None:
    print("\n" + "=" * 78)
    print("STAGE 4. Checks")
    print("=" * 78)
    for name in FILES:
        t = text[name]
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
        tags = re.findall(r"\\tag\{([^}]+)\}", t)
        dup_tags = sorted({x for x in tags if tags.count(x) > 1})
        if dup_tags:
            stop(f"{name}: duplicate tags {dup_tags}")
        seq = [x for x in tags if re.fullmatch(r"(A|OA)\.\d+", x)]
        nums: dict[str, list[int]] = {}
        for x in seq:
            p, n = x.split(".")
            nums.setdefault(p, []).append(int(n))
        for p, ns in nums.items():
            gaps = sorted(set(range(1, max(ns) + 1)) - set(ns))
            ordered = ns == sorted(ns)
            print(f"  {name}: tags ({p}.n) run 1..{max(ns)}; gaps {gaps or 'none'}; "
                  f"in order {'yes' if ordered else 'NO'}")
            if gaps or not ordered:
                stop(f"{name}: tag sequence ({p}.n) has gaps or is out of order")
        print(f"  {name}: conditions tagged {[x for x in tags if re.fullmatch(r'A[12]', x)]}")
        for sym, allowed in EM.LEFTOVER if name == "main.tex" else EO.LEFTOVER:
            n = t.count(sym)
            flag = "" if n <= allowed else "  <-- above allowance"
            print(f"  {name}: count of {sym!r}: base {base[name].count(sym)}, now {n} "
                  f"(allowed {allowed}){flag}")
            if n > allowed:
                stop(f"{name}: {sym!r} occurs {n} times, allowance {allowed}")
    bib_check(text["main.tex"], "main.tex")
    bib_check(text["online_appendix.tex"], "online_appendix.tex")


def artifact_hashes() -> dict[str, str]:
    with open(REV / "round2_artifacts.csv", newline="") as fh:
        return {r["file"]: r["after_sha256"] for r in csv.DictReader(fh)}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stage_artifacts(write: bool) -> None:
    print("\n" + "=" * 78)
    print("STAGE 5. Round-2 tables and figures")
    print("=" * 78)
    rec = artifact_hashes()
    # Only tables the manuscript already uses. A new worktree table (the class exhibit of a
    # later round) is not copied.
    items = [f"tables/{p.name}" for p in sorted((CLONE / "tables").glob("*.tex"))]
    skipped = sorted({p.name for p in (NUMERICS / "tables").glob("*.tex")}
                     - {p.name for p in (CLONE / "tables").glob("*.tex")})
    print(f"  worktree tables not used by the manuscript, not copied: {skipped or 'none'}")
    items += [f"figures/{n}.pdf" for n in ("bargaining_weight", "equilibrium_correspondence",
                                            "posterior_tail_entry", "two_returns")]
    for rel in items:
        src, dst = NUMERICS / rel, CLONE / rel
        h = sha(src)
        if rel in rec and rec[rel] != h:
            stop(f"{rel}: worktree hash {h[:16]} differs from round2_artifacts.csv {rec[rel][:16]}")
        before = sha(dst) if dst.exists() else None
        status = "unchanged"
        if before != h:
            status = "copied (changed)" if write else "would copy (changed)"
            if write:
                shutil.copyfile(src, dst)
        listed = "listed in round2_artifacts.csv" if rel in rec else "not a round-2 change"
        print(f"  {rel:44s} {status:22s} sha256 {h[:16]}  {listed}")


def main() -> None:
    base = {name: git_show(name) for name in FILES}
    print(f"Base commit {BASE_COMMIT}: main.tex {base['main.tex'].count(chr(10))} lines, "
          f"online_appendix.tex {base['online_appendix.tex'].count(chr(10))} lines")
    text = dict(base)
    try:
        stage_content(text)
        stage_moves(text)
        stage_retag(text)
        stage_checks(text, base)
        write = "--check" not in sys.argv
        stage_artifacts(write)
    except Stop as exc:
        print(f"\nSTOPPED: {exc}")
        sys.exit(1)
    if not write:
        print("\n--check: nothing written")
        return
    for name in FILES:
        (CLONE / name).write_text(text[name])
        print(f"  wrote {CLONE / name} ({text[name].count(chr(10))} lines)")
    print("\nDone.")


if __name__ == "__main__":
    main()
