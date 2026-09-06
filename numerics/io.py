"""CSV output and run manifests (E.3)."""
from __future__ import annotations

import csv
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = ROOT / "numerics" / "manifests"


def fmt(v, column: str = "") -> str:
    if isinstance(v, (bool, np.bool_)):
        return "true" if v else "false"
    if isinstance(v, (float, np.floating)):
        if column in {"x_star", "x_star_Yplus", "x_star_Yminus"} and not np.isfinite(v):
            return "n/a" if np.isnan(v) else "unattainable" if v > 0 else "always"
        if np.isnan(v):
            return "nan"
        if np.isinf(v):
            return "inf" if v > 0 else "-inf"
        return repr(float(v))
    return str(v)


def write_csv(path: Path | str, columns: list[str], rows: list[dict]) -> Path:
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(columns)
        for r in rows:
            w.writerow([fmt(r.get(c, "n/a"), c) for c in columns])
    return path


def read_csv(path: Path | str) -> list[dict]:
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sha256(path: Path | str) -> str:
    return hashlib.sha256(Path(ROOT / path).read_bytes()).hexdigest()


def software_versions() -> dict:
    import mpmath
    return {"python": sys.version.split()[0], "numpy": np.__version__, "scipy": scipy.__version__,
            "mpmath": mpmath.__version__, "platform": platform.platform()}


def write_manifest(exercise: str, inputs: dict, method: str, tolerances: dict, outputs: list[str],
                   checks: dict, passed: bool, notes: list[str] | None = None) -> Path:
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    man = {
        "exercise": exercise,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": inputs,
        "method": method,
        "tolerances": tolerances,
        "software": software_versions(),
        "outputs": {o: sha256(o) for o in outputs},
        "checks": checks,
        "passed": bool(passed),
        "notes": notes or [],
    }
    path = MANIFEST_DIR / f"{exercise}.json"
    path.write_text(json.dumps(man, indent=1, default=_json_default))
    return path


def _json_default(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)
