"""Build/package the peer revision, or reproduce it from a fresh source copy."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
ENV = {**os.environ, **{key: "1" for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")},
       "SOURCE_DATE_EPOCH": "1788652800", "TZ": "UTC", "PYTHONHASHSEED": "0"}
ENV["PATH"] = str(Path(sys.executable).parent) + os.pathsep + ENV.get("PATH", "")
PRODUCERS = ("c1_baseline", "c2_correspondence", "c3_signals", "c4_moderate", "c5_noise", "c6_reserve",
             "c6b_price_pools", "c6c_reserve_events", "c7_bargaining")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes(root: Path) -> dict:
    paths = list((root / "numerics").rglob("*.py")) + [root / p for p in
            ("paper/main.md", "paper/online_appendix.md", "paper/quantity_manifest.csv", "references.bib", "replication/release.py", "Makefile",
             "audit/peer_polish/independent_checks.py", "audit/peer_polish/verify_core_bindings.py", "audit/peer_polish/certificate_checks.py",
             "audit/peer_polish/reference_seed/certify_asymmetric.py")]
    return {str(p.relative_to(root)): digest(p) for p in sorted(paths)}


def run(root: Path, arguments: list[str], records: list[dict]) -> None:
    start = time.monotonic()
    label = Path(arguments[0]).stem
    log = root / "audit/peer_polish/logs" / f"release_{label}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    command = [sys.executable, *arguments]
    print("RUN", " ".join(arguments), flush=True)
    with log.open("w") as stream:
        result = subprocess.run(command, cwd=root, env=ENV, stdout=stream, stderr=subprocess.STDOUT)
    records.append({"command": command, "cwd": str(root), "exit_code": result.returncode,
                    "elapsed_seconds": round(time.monotonic() - start, 3), "log": str(log.relative_to(root))})
    if result.returncode:
        raise RuntimeError(f"command failed: {arguments}; see {log}")


def text_of(pdf: Path) -> str:
    return subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)


def pdf_checks(root: Path) -> dict:
    result = {}
    for name in ("main", "online_appendix"):
        pdf = root / f"paper/{name}_filled.pdf"
        text = text_of(pdf)
        if re.search(r"\[\[[A-Za-z0-9_]+\]\]|\?\?|/Users/|/home/uctpiaj|�|■", text):
            raise ValueError(f"unresolved field/reference, missing glyph, or local path in {pdf}")
        log = root / f"paper/build/{name}_filled.log"
        if log.exists() and re.search(r"undefined references|Citation .+ undefined|Missing character:", log.read_text(errors="replace")):
            raise ValueError(f"unresolved typesetting issue in {log}")
        result[name] = {"pdf_sha256": digest(pdf), "text_sha256": hashlib.sha256(" ".join(text.split()).encode()).hexdigest()}
    return result


def build(root: Path, records: list[dict]) -> dict:
    sources = source_hashes(root)
    run(root, ["numerics/verify.py", "--stage", "c1", "c2", "c3", "c4", "c5", "c6", "c6b", "c6c", "c7"], records)
    run(root, ["numerics/release_checks.py"], records)
    run(root, ["audit/peer_polish/verify_core_bindings.py", "--reserve-comparisons=tables/reserve_comparisons.csv"], records)
    run(root, ["-m", "pytest", "-q", "numerics/tests"], records)
    run(root, ["numerics/check_registry.py"], records)
    run(root, ["numerics/registry.py"], records)
    run(root, ["numerics/substitute.py"], records)
    run(root, ["numerics/render/render_all.py"], records)
    run(root, ["numerics/verify.py", "--final"], records)
    run(root, ["numerics/render/latex.py"], records)
    run(root, ["numerics/verify.py", "--final"], records)
    pdfs = pdf_checks(root)
    if sources != source_hashes(root):
        raise ValueError("source changed during build; rebuild from stable sources")
    (root / "replication/build_manifest.json").write_text(json.dumps({"commands": records, "source_sha256": sources, "pdfs": pdfs}, indent=2) + "\n")
    return pdfs


def copy_source(destination: Path) -> None:
    skip = shutil.ignore_patterns(".*", "__pycache__", "*.pyc", "*.pdf", "build", "drafts", "*.aux", "*.fls", "*.fdb_latexmk", "*.out", "*.toc", "*.synctex.gz", "*.bbl", "*.blg",
                                 "*credentials*", "*secret*", "auth.json", "token.json", "*.pem", "*.key")
    def ignore(directory: str, names: list[str]) -> set[str]:
        ignored = set(skip(directory, names))
        for name in set(names) - ignored:
            if (Path(directory) / name).is_symlink():
                raise ValueError(f"symlink excluded from replication package: {Path(directory) / name}")
        return ignored
    for name in ("paper", "numerics", "tables", "figures_data", "verification", "replication", "audit/peer_polish"):
        shutil.copytree(ROOT / name, destination / name, ignore=ignore)
    for name in ("Makefile", "references.bib", "CLAUDE.md"):
        shutil.copy2(ROOT / name, destination / name)
    (destination / "figures").mkdir(exist_ok=True)


def canonical_csv(path: Path) -> list:
    with path.open(newline="") as stream:
        data = list(csv.DictReader(stream))
    ignore = {"run_id", "candidate_id", "duplicate_of"}
    def value(cell: str):
        cell = re.sub(r"\b(c6c?)_\d{8}T\d{12}Z", r"\1_RUN", cell)
        try:
            number = Decimal(cell)
            if not number.is_finite():
                return cell
            if number == 0:
                return "0"
            fixed = format(number, "f")
            return fixed.rstrip("0").rstrip(".") if "." in fixed else fixed
        except InvalidOperation:
            return cell
    return sorted(tuple(sorted((key, value(cell)) for key, cell in row.items() if key not in ignore)) for row in data)


def reproduce(workers: int) -> None:
    destination = Path(tempfile.mkdtemp(prefix="ccc-peer-reproduce-"))
    records: list[dict] = []
    copy_source(destination)
    output_paths = set()
    for manifest in (destination / "numerics/manifests").glob("*.json"):
        data = json.loads(manifest.read_text())
        if data.get("exercise") == "handout":
            continue
        output_paths.update(data.get("outputs", {}))
    # These are only files inside the disposable fresh copy, never source inputs.
    for relative in output_paths:
        path = destination / relative
        if not path.resolve().is_relative_to(destination.resolve()):
            raise ValueError(f"producer manifest output escapes fresh copy: {relative}")
        if path.is_file():
            path.unlink()
    for name in ("c1_baseline", "c3_signals", "c4_moderate", "c5_noise", "c7_bargaining", "c6b_price_pools"):
        run(destination, [f"numerics/exercises/{name}.py"], records)
    with ThreadPoolExecutor(max_workers=2) as executor:
        jobs = [executor.submit(run, destination, [f"numerics/exercises/{name}.py", f"--workers={workers}"], records)
                for name in ("c2_correspondence", "c6_reserve")]
        for job in jobs:
            job.result()
    run(destination, ["numerics/exercises/c6c_reserve_events.py", f"--workers={min(workers,8)}"], records)
    pdfs = build(destination, records)
    compare_reproduction(destination, records, pdfs)


def compare_reproduction(destination: Path, records: list[dict], pdfs: dict) -> None:
    """Compare a completed isolated build, including a presentation-only rebuild."""
    mismatches = []
    compared = []
    for manifest in (ROOT / "numerics/manifests").glob("*.json"):
        data = json.loads(manifest.read_text())
        if data.get("exercise") == "handout":
            continue
        for relative in data.get("outputs", {}):
            if relative.endswith(".csv") and relative not in compared:
                if canonical_csv(ROOT / relative) != canonical_csv(destination / relative):
                    mismatches.append(relative)
                compared.append(relative)
    original = json.loads((ROOT / "replication/build_manifest.json").read_text())["pdfs"]
    for name in original:
        if original[name]["text_sha256"] != pdfs[name]["text_sha256"]:
            mismatches.append(f"{name} substantive manuscript text")
    report = {"directory": str(destination), "commands": records, "compared_csvs": compared,
              "mismatches": mismatches, "pdfs": pdfs, "passed": not mismatches}
    (ROOT / "audit/peer_polish/reproduction.json").write_text(json.dumps(report, indent=2) + "\n")
    if mismatches:
        raise ValueError(f"fresh reproduction differs: {mismatches}; outputs preserved at {destination}")
    print(f"Fresh reproduction passed: {destination}")


def package(pdfs: dict, records: list[dict]) -> None:
    built = json.loads((ROOT / "replication/build_manifest.json").read_text())
    if built["source_sha256"] != source_hashes(ROOT) or built["pdfs"] != pdfs:
        raise ValueError("sources or PDFs differ from validated build")
    records = built["commands"] + records
    inspection = ROOT / "audit/peer_polish/visual_checks/inspection.json"
    if not inspection.exists():
        raise ValueError("Full PDF inspection record required before packaging")
    reviewed = json.loads(inspection.read_text())
    if not reviewed.get("passed") or any(reviewed["pdfs"][name]["pdf_sha256"] != data["pdf_sha256"] for name, data in pdfs.items()):
        raise ValueError("PDFs differ from the completed visual inspection")
    for name in pdfs:
        info = subprocess.check_output(["pdfinfo", str(ROOT / f"paper/{name}_filled.pdf")], text=True)
        page_count = int(re.search(r"Pages:\s+(\d+)", info).group(1))
        if sorted(reviewed["pages"][name]) != list(range(1, page_count + 1)):
            raise ValueError(f"incomplete page inspection: {name}")
    for required in ("audit/peer_polish/completion_report.md", "audit/peer_polish/issue_ledger.csv", "replication/README.md", "replication/requirements.txt"):
        if not (ROOT / required).is_file():
            raise FileNotFoundError(required)
    release = ROOT / "peer_release"
    release.mkdir(exist_ok=True)
    for name in pdfs:
        shutil.copy2(ROOT / f"paper/{name}_filled.pdf", release / f"{name}.pdf")
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True)
    revision = git.stdout.strip() if git.returncode == 0 else json.loads((ROOT / "replication/run_manifest.json").read_text())["revision"]
    date = datetime.now(timezone.utc).date().isoformat()
    (release / "README.md").write_text(
        "# Competition Creates Competition\n\nStock Prices and the Discovery of Takeover Bidders\n\n"
        f"Austin Li. Peer-circulation revision, {date}. Source base {revision}.\n\n"
        "main.pdf contains the theory working paper and its paper appendix. online_appendix.pdf supplies the detailed proofs, "
        "numerical methods and additional results. The empirical section is a research design scaffold.\n")
    manifest = {"revision": revision, "date_utc": date, "source_sha256": built["source_sha256"], "commands": records, "environment": {k:ENV[k] for k in
                ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "SOURCE_DATE_EPOCH")}, "pdfs": pdfs}
    (ROOT / "replication/run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    destination = ROOT / "source_and_replication"
    if destination.exists():
        raise FileExistsError(f"preserve existing archive directory before replacing: {destination}")
    copy_source(destination)
    with tarfile.open(ROOT / "source_and_replication.tar.gz", "w:gz") as archive:
        archive.add(destination, arcname="source_and_replication")
    print(f"Peer PDFs: {release}; source archive: {ROOT / 'source_and_replication.tar.gz'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=20)
    parser.add_argument("--reproduce", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--package-only", action="store_true")
    args = parser.parse_args()
    if args.workers < 1:
        parser.error("workers must be positive")
    if args.reproduce:
        reproduce(args.workers)
    else:
        records = []
        if args.package_only:
            run(ROOT, ["numerics/verify.py", "--final"], records)
            run(ROOT, ["numerics/release_checks.py"], records)
            run(ROOT, ["audit/peer_polish/verify_core_bindings.py", "--reserve-comparisons=tables/reserve_comparisons.csv"], records)
            pdfs = pdf_checks(ROOT)
        else:
            pdfs = build(ROOT, records)
        if not args.build_only:
            package(pdfs, records)
