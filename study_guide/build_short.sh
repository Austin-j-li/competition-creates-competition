#!/usr/bin/env bash
# Build the short study guide (no more than 50 pages).
#   ./build_short.sh                  the whole guide; copies the PDF to ../output/pdf/
#   ./build_short.sh 07_main_result   one chapter; the PDF is build/short_07_main_result/only.pdf
set -euo pipefail
cd "$(dirname "$0")"

if [ $# -eq 0 ]; then
  out=build/short_full
  mkdir -p "$out/short/chapters"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$out" -jobname=main short/main.tex
  mkdir -p ../output/pdf
  cp "$out/main.pdf" ../output/pdf/Competition_Creates_Competition_Study_Guide_Short.pdf
  echo "PDF: output/pdf/Competition_Creates_Competition_Study_Guide_Short.pdf"
else
  ch="${1%.tex}"
  ch="${ch##*/}"
  [ -f "short/chapters/$ch.tex" ] || { echo "No chapter short/chapters/$ch.tex" >&2; exit 1; }
  out="build/short_$ch"
  mkdir -p "$out/short/chapters"
  printf '\\def\\onlychapter{short/chapters/%s}\\input{short/main}\n' "$ch" > "$out/only.tex"
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir="$out" "$out/only.tex"
  echo "PDF: study_guide/$out/only.pdf"
fi
