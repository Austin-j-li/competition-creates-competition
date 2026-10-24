"""Print every \\reg key used in the three documents, flag keys missing from the registry,
and list decimal numbers typed directly in the source (outside \\reg) for review."""
import csv
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[4]
DOC = ROOT / "slot/manuscript"
REG = ROOT / "audit/slot_manuscript_2026_10_23/registry/registry.csv"

keys = {r["key"]: r for r in csv.DictReader(REG.open())}
files = sorted([DOC / "main.tex", DOC / "slides.tex", DOC / "comparison.tex"]
               + list((DOC / "sections").glob("*.tex")) + list((DOC / "appendix").glob("*.tex"))
               + list((DOC / "comparison").glob("*.tex")) if (DOC / "comparison").exists() else
               [DOC / "main.tex", DOC / "slides.tex", DOC / "comparison.tex"]
               + list((DOC / "sections").glob("*.tex")) + list((DOC / "appendix").glob("*.tex")))
reg_re = re.compile(r"\\reg\{([^}]*)\}")
dec_re = re.compile(r"(?<![\w.{])(\d+\.\d{2,})(?![\w}])")
used, missing, literals = {}, [], []
for f in files:
    if not f.exists():
        continue
    for n, line in enumerate(f.read_text().splitlines(), 1):
        code = line.split("%", 1)[0] if not line.lstrip().startswith("%") else ""
        for k in reg_re.findall(code):
            used.setdefault(k, set()).add(f.name)
            if k not in keys:
                missing.append((f.name, n, k))
        stripped = reg_re.sub("", code)
        for d in dec_re.findall(stripped):
            if re.search(r"\\(hspace|vspace|includegraphics|resizebox|scalebox|setlength|addtolength)|width|height|pt|cm|mm|em\b|ex\b", stripped):
                continue
            literals.append((f.name, n, d, stripped.strip()[:110]))
print(f"files scanned: {sum(1 for f in files if f.exists())}; distinct keys used: {len(used)}; missing keys: {len(missing)}")
for m in missing:
    print("MISSING", *m)
print(f"literal decimals outside \\reg: {len(literals)}")
for l in literals:
    print("LITERAL", *l)
