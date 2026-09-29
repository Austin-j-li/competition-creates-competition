"""Render talk/build/talk.pptx with LibreOffice and check it against the Beamer PDF.

Run:  <talk venv>/bin/python talk/pptx/render_check.py      (after build_pptx.py)

Writes talk/build/pptx_render/{talk.pdf, s-NN.png (PowerPoint via LibreOffice), b-NN.png (Beamer)}
at 60 dpi (PyMuPDF) for side-by-side review. soffice runs alone, with a private throwaway profile, so a
concurrent LibreOffice instance cannot interfere; the check exits nonzero when the page count
differs from the Beamer PDF or when a rendered page carries no text beyond its footline.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pymupdf

BUILD = Path(__file__).resolve().parent.parent / "build"
PPTX, BEAMER, OUT = BUILD / "talk.pptx", BUILD / "talk.pdf", BUILD / "pptx_render"
FOOTLINE = ("Austin Li", "Competition Creates Competition")


def main() -> int:
    shutil.rmtree(OUT, ignore_errors=True)
    OUT.mkdir(parents=True)
    with tempfile.TemporaryDirectory(prefix="lo_profile_") as prof:
        subprocess.run(["soffice", f"-env:UserInstallation=file://{prof}", "--headless",
                        "--convert-to", "pdf", "--outdir", str(OUT), str(PPTX)],
                       check=True, capture_output=True, timeout=600)
    rendered = OUT / "talk.pdf"
    doc, ref = pymupdf.open(rendered), pymupdf.open(BEAMER)
    # PyMuPDF, not pdftoppm: LibreOffice embeds its Cambria Math substitute (XITS Math) with a
    # font-type mismatch that makes poppler drop whole pages, so pdftoppm shows false blanks
    for src, prefix in ((doc, "s"), (ref, "b")):
        for k, page in enumerate(src, 1):
            page.get_pixmap(dpi=60).save(str(OUT / f"{prefix}-{k:02d}.png"))
    errors = []
    if len(doc) != len(ref):
        errors.append(f"page count {len(doc)} != Beamer {len(ref)}")
    for k, page in enumerate(doc, 1):
        text = page.get_text()
        for f in FOOTLINE:
            text = text.replace(f, "")
        body = "".join(ch for ch in text if ch.isalpha())
        if len(body) < 3:
            errors.append(f"page {k} rendered without body text")
    for e in errors:
        print("FAIL:", e)
    print(f"{len(doc)} pages rendered to {OUT}; {'FAIL' if errors else 'ok'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
