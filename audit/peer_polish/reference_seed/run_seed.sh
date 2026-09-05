#!/bin/sh
# Runs the byte-for-byte copy of the legacy certificate seed with assertions enabled.
# The seed relies on `assert` for its acceptance tests, so it must never run under
# Python optimization: refuse if PYTHONOPTIMIZE is set or the interpreter has -O.
set -eu
HERE="$(cd "$(dirname "$0")" && pwd)"
PY="${PYTHON:-$HERE/../../../.venv/bin/python}"
if [ -n "${PYTHONOPTIMIZE:-}" ]; then
  echo "refusing to run: PYTHONOPTIMIZE is set (${PYTHONOPTIMIZE})" >&2
  exit 2
fi
"$PY" - "$HERE/certify_asymmetric.py" <<'PYEOF'
import sys, hashlib, runpy
if sys.flags.optimize > 0:
    sys.exit("refusing to run: sys.flags.optimize = %d (assertions would be stripped)" % sys.flags.optimize)
path = sys.argv[1]
print("seed sha256:", hashlib.sha256(open(path, "rb").read()).hexdigest())
print("python:", sys.version.split()[0], "optimize flag:", sys.flags.optimize)
import mpmath; print("mpmath:", mpmath.__version__)
runpy.run_path(path, run_name="__main__")
print("seed completed: every assertion held")
PYEOF
