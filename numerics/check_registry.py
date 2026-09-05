"""Run with .venv/bin/python numerics/check_registry.py."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    # Separate processes exercise both import orders as well as ambient precision.
    script = """
import json
from decimal import getcontext, ROUND_DOWN
{imports}
getcontext().prec = {precision}
getcontext().rounding = ROUND_DOWN
rows, problems = build_registry()
assert not problems, problems
assert getcontext().prec == {precision}
assert getcontext().rounding == ROUND_DOWN
print(json.dumps(rows, sort_keys=True))
"""
    baseline = None
    for imports in (
        "from numerics.registry import build_registry",
        "import numerics.thresholds\nfrom numerics.registry import build_registry",
        "from numerics.registry import build_registry\nimport numerics.thresholds",
    ):
        for precision in (12, 28, 60, 80):
            result = subprocess.check_output(
                [sys.executable, "-c", script.format(imports=imports, precision=precision)],
                cwd=ROOT,
            )
            if baseline is None:
                baseline = result
            assert result == baseline, (imports, precision)
    print("Registry is identical across 12 precision/import-order combinations.")


if __name__ == "__main__":
    main()
