"""Verification gate: reruns acceptance checks and the placeholder substitution; exits nonzero on any breach.

Usage:
    python numerics/verify.py                 # gate for the completed stages recorded in manifests
    python numerics/verify.py --stage c1 c2   # gate only the named exercises (used between commits)
    python numerics/verify.py --final         # additionally require every placeholder to be resolved
    python numerics/verify.py --rerun         # re-execute the cheap exercises before checking (C.1, C.3, C.4, C.5, C.7)

Checks: (1) every named manifest exists and passed, and the SHA-256 of each output file matches
the manifest (no hand edits); (2) the declared C.1 nodes and the three certificates are
re-validated directly against the C.0 tolerances; (3) the threshold residuals; (4) the registry is
rebuilt and every key belonging to a completed stage resolves with a non-open status; (5) with
--final, the substitution runs strictly.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from numerics.auction import payoffs_closed_form  # noqa: E402
from numerics.certificates import certify  # noqa: E402
from numerics.io import MANIFEST_DIR, ROOT, read_csv, sha256  # noqa: E402
from numerics.params import BENCHMARK, CERTIFICATE_BRACKETS, CONTROLS  # noqa: E402
from numerics.search import full_order_candidate, pooling_candidate  # noqa: E402
from numerics.thresholds import compute_thresholds  # noqa: E402
from numerics.validation import validate  # noqa: E402

STAGES = {
    "c1": ("c1_baseline", ["C.1", "C.1/C.5"]),
    "c2": ("c2_correspondence", ["C.2"]),
    "c3": ("c3_signals", ["C.3"]),
    "c4": ("c4_moderate", ["C.4"]),
    "c5": ("c5_noise", ["C.5"]),
    "c6": ("c6_reserve", ["C.6", "C.0/C.6"]),
    "c6b": ("c6b_price_pools", ["C.6b"]),
    "c6c": ("c6c_reserve_events", ["C.6c"]),
    "c7": ("c7_bargaining", ["C.7"]),
    "c8": ("c8_registry", ["C.8"]),
    "render": ("render", []),
}
RERUN = {"c1": "numerics/exercises/c1_baseline.py", "c3": "numerics/exercises/c3_signals.py", "c4": "numerics/exercises/c4_moderate.py",
         "c5": "numerics/exercises/c5_noise.py", "c7": "numerics/exercises/c7_bargaining.py", "render": "numerics/render/render_all.py"}


def check(cond: bool, msg: str, failures: list[str]) -> None:
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", nargs="*", default=None)
    ap.add_argument("--final", action="store_true")
    ap.add_argument("--rerun", action="store_true")
    args = ap.parse_args()
    failures: list[str] = []
    stages = args.stage or [s for s, (m, _) in STAGES.items() if (MANIFEST_DIR / f"{m}.json").exists()]
    want_handout = bool(args.stage and "handout" in args.stage)
    stages = [s for s in stages if s != "handout"]
    if args.final:
        stages = list(STAGES)
    if args.rerun:
        for s in stages:
            if s in RERUN:
                r = subprocess.run([sys.executable, str(ROOT / RERUN[s])], cwd=ROOT)
                check(r.returncode == 0, f"rerun {RERUN[s]}", failures)

    # (1) manifests and output hashes
    for s in stages:
        mname, _ = STAGES[s]
        path = MANIFEST_DIR / f"{mname}.json"
        if not path.exists():
            check(False, f"manifest {mname} present", failures)
            continue
        man = json.loads(path.read_text())
        check(man["passed"] is True, f"manifest {mname} passed", failures)
        for out, h in man["outputs"].items():
            check((ROOT / out).exists() and sha256(out) == h, f"output hash unchanged: {out}", failures)

    # (2) direct re-validation of the declared benchmark nodes and the certificates
    if "c1" in stages:
        for rs, mk in (("1.2", pooling_candidate), ("3", full_order_candidate), ("3.6", full_order_candidate)):
            pay = payoffs_closed_form(BENCHMARK, float(rs))
            v = validate(mk(BENCHMARK, pay).sched, CONTROLS)
            check(v.accepted, f"declared node r={rs} {mk.__name__} accepted (eps_q={max(v.epsilon_q, v.epsilon_q_refined):.2e})", failures)
    if "c2" in stages:
        for r_s, vl, vr in CERTIFICATE_BRACKETS:
            rec = certify(BENCHMARK, r_s, vl, vr, CONTROLS)
            check(rec.accepted, f"certificate r={r_s} all predicates true", failures)
        for row in compute_thresholds(BENCHMARK):
            if row["boundary"] in ("pooling_unique_sufficient", "pooling_existence", "full_orders_unique_sufficient", "high_cost_ceiling"):
                check(abs(float(row["defining_residual"])) <= CONTROLS.independent_formula_acceptance,
                      f"threshold {row['boundary']} residual {row['defining_residual']:.1e}", failures)

    # (3) registry: rebuild and check stage keys
    from numerics.registry import build_registry
    registry, problems = build_registry()
    from numerics.io import write_csv
    from numerics.registry import REGISTRY_COLUMNS
    write_csv("numerics/quantity_registry.csv", REGISTRY_COLUMNS, registry)
    manifest = read_csv("paper/quantity_manifest.csv")
    done_exercises = {e for s in stages for e in STAGES[s][1]} | {"C.0", "E"}
    if {"c1", "c3", "c4"} <= set(stages):
        done_exercises.add("C.1/C.3/C.4")
    source_stage = {"figures_data/posterior_tails.csv": "c5", "numerics/two_signals.csv": "c3", "numerics/moderate_values.csv": "c4",
                    "tables/reserve_comparisons.csv": "c6", "numerics/certificates.csv": "c2", "numerics/thresholds.csv": "c2"}
    for m in manifest:
        need = source_stage.get(m["source_file"])
        if m["exercise"] in done_exercises and (need is None or need in stages):
            row = next(r for r in registry if r["name"] == m["name"])
            check(row["status"] != "open", f"registry {m['name']} = {row['display']} [{row['status']}]", failures)

    # (4) strict substitution
    if args.final:
        from numerics.substitute import substitute
        ok, rep = substitute(strict=True)
        check(ok, f"substitution: {len(rep['filled'])} filled, {len(rep['unresolved'])} unresolved, {len(rep['unknown'])} unknown", failures)
        for item in rep["unresolved"] + rep["unknown"]:
            print("     ", item)

    # (5) handout build (docs/index.html from the same CSVs and registry); not an exercise stage
    if want_handout:
        r = subprocess.run([sys.executable, str(ROOT / "handout" / "build.py"), "--quiet"], cwd=ROOT)
        check(r.returncode == 0, "handout build passed", failures)

    print("\nVERIFY", "PASSED" if not failures else f"FAILED ({len(failures)} failures)")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
