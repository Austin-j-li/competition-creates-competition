"""Re-run the author's solver with its output redirected to referee/rerun/ (CSV only)."""
from __future__ import annotations
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import selection_solve as ss  # noqa: E402
ss.HERE = HERE / "rerun"
ss.main()
