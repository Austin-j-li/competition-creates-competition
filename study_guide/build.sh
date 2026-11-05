#!/usr/bin/env bash
# Build the study guide.
#   ./build.sh                  the whole guide; copies the PDF to ../output/pdf/
#   ./build.sh 07_main_result   one chapter; the PDF is build/07_main_result/only.pdf
# Each build has its own folder under build/, so builds can run at the same time.
set -euo pipefail
cd "$(dirname "$0")"

if [ $# -eq 0 ]; then
  out=build/full
  mkdir -p "$out/chapters"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$out" main.tex
  mkdir -p ../output/pdf
  cp "$out/main.pdf" ../output/pdf/Competition_Creates_Competition_Study_Guide.pdf
  echo "PDF: output/pdf/Competition_Creates_Competition_Study_Guide.pdf"
else
  ch="${1%.tex}"
  ch="${ch#chapters/}"
  [ -f "chapters/$ch.tex" ] || { echo "No chapter chapters/$ch.tex" >&2; exit 1; }
  out="build/$ch"
  mkdir -p "$out/chapters"
  printf '\\def\\onlychapter{chapters/%s}\\input{main}\n' "$ch" > "$out/only.tex"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$out" "$out/only.tex"
  echo "PDF: study_guide/$out/only.pdf"
fi
