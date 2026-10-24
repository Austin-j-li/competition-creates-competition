"""Round 4: correct the note field of two P5 registry rows (referee findings 3 and 9).

Values, displays and statuses stay unchanged. The script prints each old and new note.
Run from the repository root:
    .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/W1/r4_registry_notes.py
"""
import csv
import io

PATH = "audit/slot_manuscript_2026_10_23/registry/P5_observables.csv"

NEW_NOTES = {
    "vol_full_B": (
        "Volume 2b+lambda: two-sided full informed trade. The value is a point rounded to nearest "
        "at 20 digits, not an enclosure. Outward enclosure [0.7273518492757511245590493, "
        "0.7273518492757511245590494] (scripts/R_referee/recompute.log); a wider certificate is in "
        "scripts/XP5/registry_recompute.csv."
    ),
    "theta_max_full_eq_r1_B": (
        "1 - 2k/(rho Delta_T(r_1)) = 19/25. Under rule IM, full two-sided trade with share theta' is "
        "an equilibrium at r_1 iff theta' <= this value; at equality the low-class sale earns exactly "
        "zero. Strict incentives, and rule I0, need theta' < this value."
    ),
}

with open(PATH, newline="") as fh:
    rows = list(csv.reader(fh))
header = rows[0]
key_i, note_i = header.index("key"), header.index("note")
for row in rows[1:]:
    if row[key_i] in NEW_NOTES:
        print("key:", row[key_i])
        print("  old note:", row[note_i])
        row[note_i] = NEW_NOTES[row[key_i]]
        print("  new note:", row[note_i])
buf = io.StringIO()
csv.writer(buf, lineterminator="\r\n").writerows(rows)
with open(PATH, "w", newline="") as fh:
    fh.write(buf.getvalue())
