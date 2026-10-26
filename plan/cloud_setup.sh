#!/usr/bin/env bash
# Install document-build and numerical dependencies.
set -euo pipefail

# Append to an existing setup script; preserve its earlier commands and settings.
# The setup process must run as root in its Linux environment.
if [ "$(id -u)" -ne 0 ]; then
  printf '%s\n' 'Run this installer as root in the build environment.' >&2
  exit 1
fi
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates fontconfig ghostscript poppler-utils \
  latexmk texlive-latex-base texlive-latex-recommended texlive-latex-extra \
  texlive-fonts-recommended texlive-fonts-extra texlive-xetex texlive-science texlive-bibtex-extra \
  python3 python3-pip python3-venv

python3 -m pip install --break-system-packages \
  numpy scipy mpmath matplotlib fonttools sympy

# Make the distribution's Fira OpenType faces visible to the slide compiler.
fira_source="$(kpsewhich FiraSans-Regular.otf)"
if [ -n "$fira_source" ]; then
  install -d /usr/local/share/fonts/ccc-fira
  cp "$(dirname "$fira_source")"/FiraSans-*.otf /usr/local/share/fonts/ccc-fira/
  fc-cache -f /usr/local/share/fonts/ccc-fira
else
  printf '%s\n' 'FiraSans-Regular.otf is missing from the installed font collection.' >&2
  exit 1
fi

# Read installed versions and package locations without changing project files.
latexmk -v
pdflatex --version
xelatex --version
python3 --version
for dependency in newtxtext.sty newtxmath.sty natbib.sty aer.bst fontspec.sty \
  beamer.cls tikz.sty mathtools.sty microtype.sty setspace.sty enumitem.sty \
  needspace.sty caption.sty geometry.sty booktabs.sty array.sty tabularx.sty \
  longtable.sty graphicx.sty xcolor.sty hyperref.sty; do
  kpsewhich "$dependency"
done
python3 -c 'import numpy, scipy, mpmath, matplotlib, fontTools, sympy; print("Numerical and font packages import successfully.")'
printf '%s\n' 'Dependencies installed. The figure program retains its original font path until S2.'
