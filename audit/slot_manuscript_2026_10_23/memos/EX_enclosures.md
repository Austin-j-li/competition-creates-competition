# EX: outward decimal enclosures

Status: **open**. One protected display differs in the P2 candidate. Neither registry was replaced.

## Export repair

Both exporters retain interval arithmetic at 60 decimal digits. The economic calculations remain unchanged.
The export reads each binary endpoint as an exact `Fraction`.
Decimal division uses `ROUND_FLOOR` for the lower endpoint and `ROUND_CEILING` for the upper endpoint.
P2 prints 60 significant digits. P5 retains 20 significant digits in registry notes.
Each package also writes the exact rational endpoints to `EX_exact_enclosures.json` beside its script.

The repaired files are:

- `scripts/P2_auction/derive.py`
- `scripts/P5_observables/p5_observables.py`

Both scripts accept `--registry-output` for a candidate export before registry replacement.
The P5 source preserves the complete manual notes for `vol_full_B` and `theta_max_full_eq_r1_B`.
The comparison confirms that both notes remain identical to the baseline.

## Runs and comparison

Both scripts ran through `scripts/_slots/run_slot.sh` with `.venv/bin/python`.
The successful runs wrote `EX_candidate.csv` and `EX_candidate_run.log` in each package folder.
The first candidate runs reached export but failed on relative paths. The corrected interface resolves the supplied path.
The logs from those failed runs remain as `EX_candidate_failed.log` in each package folder.

The baseline registry, source, and log remain in each package folder as:

- `EX_before.csv`
- `EX_before_source.txt`
- `EX_before_run.log`

The print-only comparison is `scripts/P2_auction/EX_compare.py`.
Its full output is `scripts/P2_auction/EX_candidate_comparison.log`.
It compares every column and reads the exact endpoint records. It contains no assertions.

**Computer-assisted:** P2 retains all 3,386 keys, their order, values, statuses, source paths, and log paths.
The candidate changes 2,136 notes and one display:

```text
key:     p2_reserve_points_deter_r0_two
value:   unchanged
display: '0' -> '0.000000'
status:  unchanged
```

**Computer-assisted:** P5 retains all 135 keys and their order. Every column except `note` remains identical.
The candidate changes 126 notes. Both manual notes remain identical.

## Enclosure counts

**Computer-assisted:** All 2,269 P2 candidate notes with enclosures contain their complete exact endpoint intervals.
The 334 equal-endpoint enclosures equal exact decimal values. They therefore satisfy the permitted exception.

**Computer-assisted:** All 128 P5 candidate notes with enclosures contain their complete exact endpoint intervals.
Two enclosures have equal endpoints. Both equal exact decimal values.

The current P5 baseline contains 125 equal-endpoint notes, compared with 121 in the task description.
Equal decimal endpoints alone do not establish an invalid certificate. The P2 candidates demonstrate the exact-value exception.

These counts describe the candidates. The two registries retain their original bytes because the protected display condition requires a stop.

## Open work and coordinator output

**Open:** Resolve the P2 display difference before either registry replacement.
The required coordinator command was not run after the stop condition. It therefore produced no output for this repair.
No claim in the brief or an earlier memo was refuted.
No tests ran. No commit or push occurred.
