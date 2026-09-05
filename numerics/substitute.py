"""Placeholder substitution (C.8, E.3): writes paper/*_filled.md from the validated registry."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from numerics.io import ROOT, read_csv  # noqa: E402

PLACEHOLDER = re.compile(r"\[\[([A-Za-z0-9_]+)\]\]")


def substitute(strict: bool = True) -> tuple[bool, dict]:
    registry = {r["name"]: r for r in read_csv("numerics/quantity_registry.csv")}
    manifest = {m["name"]: m for m in read_csv("paper/quantity_manifest.csv")}
    report = {"filled": [], "unresolved": [], "unknown": []}
    ok = True
    for src, dst in (("paper/main.md", "paper/main_filled.md"), ("paper/online_appendix.md", "paper/online_appendix_filled.md")):
        text = (ROOT / src).read_text(encoding="utf-8")
        keys = sorted(set(PLACEHOLDER.findall(text)))
        for k in keys:
            if k not in manifest:
                report["unknown"].append((src, k))
                ok = False
                continue
            row = registry.get(k)
            if row is None or row["status"] == "open" or row["display"] == "[[unresolved]]":
                report["unresolved"].append((src, k, row["branch"] if row else "not in registry"))
                ok = False
                continue
            text = text.replace(f"[[{k}]]", row["display"])
            report["filled"].append((src, k))
        if ok or not strict:
            (ROOT / dst).write_text(text, encoding="utf-8")
    return ok, report


if __name__ == "__main__":
    ok, rep = substitute(strict="--force" not in sys.argv)
    print(f"filled {len(rep['filled'])} placeholders; unresolved {len(rep['unresolved'])}; unknown {len(rep['unknown'])}")
    for item in rep["unresolved"] + rep["unknown"]:
        print("  ", item)
    sys.exit(0 if ok else 1)
