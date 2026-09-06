"""Fresh-copy comparison must preserve scientific precision and ignore only run metadata."""
import csv
from pathlib import Path
import tempfile
from subprocess import CompletedProcess
from unittest.mock import patch

from replication.release import canonical_csv


def test_canonical_data_preserves_exact_decimals() -> None:
    with tempfile.TemporaryDirectory() as directory:
        first, second = (Path(directory) / name for name in ("first.csv", "second.csv"))
        def write(path, number, run):
            with path.open("w", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(["value", "branch", "run_id"])
                writer.writerow([number, f"{run}:full_orders", run])
        write(first, "0.1234567890123456789012345678901", "c6_20260905T233647072695Z")
        write(second, "0.1234567890123456789012345678902", "c6_20260906T233647072695Z")
        assert canonical_csv(first) != canonical_csv(second)
        write(second, "0.12345678901234567890123456789010", "c6_20260906T233647072695Z")
        assert canonical_csv(first) == canonical_csv(second)


def test_statement_space_precedes_its_heading() -> None:
    from numerics.render import latex
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root / "input.md").write_text("#### Posterior bounds\n\n[**Proposition A.1.**]{#result}\n\nBody.\n\n**Lemma 2.** Other statement.\n\n**Input declaration: signals.**\n\n```text\nh = 10\n```\n")
        with patch.object(latex, "ROOT", root), patch.object(latex.subprocess, "run", return_value=CompletedProcess([], 0, "", "")):
            assert latex.convert("input.md", "output.tex", pdf=False)
        converted = (root / "output.tex.md").read_text()
        assert "\\Needspace{10\\baselineskip}\n```\n\n#### Posterior bounds\n\n[**Proposition" in converted
        assert "\\Needspace{8\\baselineskip}\n```\n\n**Lemma 2" in converted
        assert "\\Needspace{5\\baselineskip}\n```\n\n**Input declaration: signals.**" in converted
