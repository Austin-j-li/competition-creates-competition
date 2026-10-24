#!/usr/bin/env python3
"""Run the guide's print-only chapter programs and save their output."""

from pathlib import Path
import os
import subprocess
from time import perf_counter


def main() -> None:
    folder = Path(__file__).resolve().parent
    output = folder / "output"
    output.mkdir(exist_ok=True)
    programs = sorted(
        path for path in folder.glob("*.py")
        if path.name not in {"run_all.py", "A_crosscheck.py"}
    )
    failures = 0
    for path in programs:
        start = perf_counter()
        try:
            result = subprocess.run(
                ["python3", str(path)], cwd=folder.parent,
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, errors="replace", check=False,
            )
            code, content = result.returncode, result.stdout
        except OSError as error:
            code, content = 127, f"Could not start python3: {error}\n"
        destination = output / f"{path.stem}.txt"
        destination.write_text(content, encoding="utf-8")
        failures += code != 0
        print(f"{path.name}: exit={code}, seconds={perf_counter() - start:.3f}, "
              f"output=verify/output/{destination.name}", flush=True)
    print(f"Chapter programs: {len(programs)}; nonzero exits: {failures}.")
    print("This runner prints results. It does not certify their correctness.")


if __name__ == "__main__":
    main()
