#!/bin/sh
# Print the self-contained talk. Optional: input HTML, output PDF, mode (1 or main).
set -eu
TALK_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
INPUT=${1:-"$TALK_DIR/dist/index.html"}
OUTPUT=${2:-"$TALK_DIR/dist/talk.pdf"}
MODE=${3:-1}
CHROME=${CHROME_BIN:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
if [ ! -x "$CHROME" ]; then
  CHROME=$(command -v google-chrome || command -v chromium || command -v chromium-browser)
fi
if [ ! -f "$INPUT" ]; then
  printf 'Missing input HTML: %s\n' "$INPUT" >&2
  exit 1
fi
case "$MODE" in 1|main) ;; *) printf 'Print mode must be 1 or main\n' >&2; exit 1 ;; esac
mkdir -p "$TALK_DIR/dist"
PROFILE=$(mktemp -d "$TALK_DIR/dist/.pdf-chrome.XXXXXX")
trap 'rm -rf "$PROFILE"' EXIT HUP INT TERM
mkdir -p "$(dirname -- "$OUTPUT")"
URL=$(python3 - "$INPUT" "$MODE" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve().as_uri() + '?print=' + sys.argv[2])
PY
)
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --allow-file-access-from-files --run-all-compositor-stages-before-draw \
  --virtual-time-budget=6000 --user-data-dir="$PROFILE" \
  --print-to-pdf="$PROFILE/talk.pdf" "$URL"
if [ ! -s "$PROFILE/talk.pdf" ]; then
  printf 'Chrome did not produce a PDF\n' >&2
  exit 1
fi
mv "$PROFILE/talk.pdf" "$OUTPUT"
printf '%s\n' "$OUTPUT"
