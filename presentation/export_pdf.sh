#!/bin/sh
# Export dist/presentation.pdf with headless Chrome: every slide, every reveal, projector theme.
# Serve dist first:  python3 -m http.server 8766 --bind 127.0.0.1 --directory presentation/dist
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
URL="${1:-http://127.0.0.1:8766/}"
PROFILE=$(mktemp -d)
"$CHROME" --headless=new --disable-gpu --no-first-run --user-data-dir="$PROFILE" \
  --window-size=1600,956 --virtual-time-budget=8000 --no-pdf-header-footer \
  --print-to-pdf="$HERE/dist/presentation.pdf" "$URL" 2>/dev/null
rm -rf "$PROFILE"
python3 - "$HERE/dist/presentation.pdf" <<'PY'
import sys
from pypdf import PdfReader
r = PdfReader(sys.argv[1]); w = float(r.pages[0].mediabox.width) / 72; h = float(r.pages[0].mediabox.height) / 72
print(f"{sys.argv[1]}: {len(r.pages)} pages at {w:g} x {h:g} in")
PY
