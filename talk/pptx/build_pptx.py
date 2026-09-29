"""Build talk/build/talk.pptx: an editable PowerPoint twin of the Beamer deck talk/talk.tex.

Run:  <talk venv>/bin/python talk/pptx/build_pptx.py      (writes talk/build/talk.pptx)

Content lives in declarative modules next to this file: ``content_main.py`` (PDF pages 1-18)
and, when present, ``content_appendix.py`` (pages 19-48). Each exports ``SLIDES``, a list of
``Slide`` records, built from the element records below.

Units. Every coordinate and length in content is in *Beamer points* (the PDF page is
453.54 x 255.12 pt, i.e. 160 x 90 mm), so positions can be read straight off
``talk/build/talk.pdf`` (PyMuPDF bboxes). The engine scales by F = 960/453.54 = 2.1167 to the
13.333 x 7.5 in slide. Sizes are Beamer size names ('tiny' 5.98, 'script' 7.97, 'footnote' 8.97,
'small' 9.96, 'normal' 10.91, 'large' 11.96, 'Large' 14.35, 'Huge' 24.88) or numbers in Beamer pt.

Inline markup (any text field). LaTeX-like, nestable:
  \\b{..} bold   \\i{..} italic   \\key{..} bold structure blue (\\KeyIdea)
  \\info{..} cInfo #AA4B00   \\cost{..} cCost #006F50   \\gray{..} gray text #616161
  \\cite{..} gray footnotesize (\\graycite)   \\status{..} gray scriptsize (\\Status)
  \\statusf{..} gray footnotesize (\\StatusF)   \\color{RRGGBB}{..}
  \\small{..} \\foot{..} \\script{..} \\tiny{..} \\normal{..}  size changes
  $..$  inline math, written as native text (Unicode math italics in Cambria Math,
        real sub/superscripts); supports the LaTeX math subset used by the deck
        (Greek, \\ell, \\le, \\to, \\in, \\approx, \\max, \\Pr, \\mathbb{E}, \\mathsf, \\bar,
        \\boldsymbol, \\text, \\Info{}, \\Cost{}, _{} ^{} ...).
  \\\\ line break inside a paragraph;  ~ non-breaking space;  \\{ \\} \\$ \\% literal characters.

Fonts. Text is Calibri; inline and display math use Cambria Math (Office's math font, installed
with PowerPoint). Renderers without Cambria Math (e.g. LibreOffice on Linux) substitute a heavier
serif for the inline math, which then looks bold although the runs carry b="0"; LibreOffice also
shows the picture fallback of each display equation instead of its native OMML.

Records (all positions in Beamer pt, (x, y) = top-left):
  Slide(label, title, subtitle=None, page=None, kind='frame'|'title'|'divider', body=[...],
        nav=[(button text, target), ...], back=target, notes=None)
      label   Beamer frame label from talk.tex (F0..F16, F10a, F10b, A1..A29; divider 'APPX').
      page    footline counter text, e.g. '7 / 16' or 'A3 / 29' (None on plain slides).
      nav     buttons placed right-aligned above the footline; target = frame label ('A1') or a
              \\hypertarget name ('app:interval', 'main:interval'); resolved after all slides exist.
      back    target of a Back button (same resolution).
      notes   speaker-notes override; by default the notes come from talk/script.tex, matched
              by frame title (main frames, in order) or by '(A<n>)' (Q&A blocks).
  Text(x, y, w, paras, size='normal', h=None, anchor='t', name='Text')
      paras: list of P or markup strings. h=None -> height estimated from Carlito metrics.
  P(text, bullet=None|'ball'|'dot'|'none', level=0, size=None, align='l'|'c'|'r',
    before=0, after=0, color=None, bold=False, line=None, hang=None, line_pt=None)
      'ball' = Madrid itemize ball, 'dot' = Takeaway bullet, 'none' = indented like an item
      without bullet (\\item[] / continuation line). before/after in Beamer pt. line = spacing
      multiple; line_pt = exact line pitch in Beamer pt. hang = (marL, indent) override in Beamer pt.
  Table(x, y, cols, rows, size='small', align='l', row_h=12, rules=True, midrules=(0,),
        valign='m', pad=3, pad_v=0, name='Table', pad_top=None, col_pads=None, line=None, line_pt=None)
      align: one value or one per column; valign: 't'|'m'|'b', one value or one per row;
      pad / pad_v: horizontal / vertical cell padding (Beamer pt); pad_top: top margin, a scalar
      or one per row (default pad_v); col_pads: [(left, right), ...] per-column horizontal margins;
      line / line_pt: line-spacing multiple / exact pitch (Beamer pt) of the cell paragraphs, for
      tables tighter than 1.22 x size or with math (whose font is taller than the text font).
      cols: column widths; rows: list of rows of markup strings or Cell(text, span=1, align=None,
      size=None); booktabs rules: top, midrule below each row index in midrules, bottom.
      rules=False draws no lines. row_h: one value or a list.
  Eq(x, y, latex, size='normal', anchor='l'|'c'|'r', color=None, name='Equation')
      Display equation: native OMML (a14:m, from pandoc) with an xelatex picture fallback, in an
      mc:AlternateContent. \\Info{..} / \\Cost{..} inside latex colour that fragment.
  Figure(x, y, w, h, name, alt='')
      talk/figures/<name>.png, plus <name>.svg as an asvg:svgBlip when it exists.
  Flow(boxes=[Box(...)], arrows=[(i, j), ...], size='footnote', name='Diagram')
  Box(x, y, w, h, text, edge='737373', lw=0.6, align='c', anchor='m', number=None, pad=4)
      Native grouped rounded rectangles + connector arrows (D0, D1). text: markup or list of P.
  ResultBox(x, y, w, h, title, paras, size='small', title_h=15.5)
      tcolorbox ResultBox: structure-blue frame and title band, tinted body.
  Rect(x, y, w, h, fill=None, line=None, lw=0.6, radius=0, name='Shape')   plain helper shape.

Engine helpers (used by build(); callable from content modules for custom work):
  add_text, add_table, add_equation, add_figure, add_flow, add_resultbox, add_rect,
  add_nav_buttons, add_page_number, set_notes, markup_runs, math_runs, measure_paras.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import importlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.package import Part
from pptx.oxml.ns import qn
from pptx.oxml.shapes.autoshape import CT_Shape
from pptx.shapes.autoshape import Shape
from pptx.util import Emu, Pt

# ----------------------------------------------------------------------------------------------
# Paths and constants
# ----------------------------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
TALK = HERE.parent
BUILD = TALK / "build"
FIGDIR = TALK / "figures"
EQDIR = BUILD / "pptx_eq"
OUT = BUILD / "talk.pptx"
TALK_TEX = TALK / "talk.tex"
SCRIPT_TEX = TALK / "script.tex"
def _find_pandoc() -> Path:
    """$PANDOC, then pandoc on PATH, then the binary bundled with the research venv's pypandoc."""
    if os.environ.get("PANDOC"):
        return Path(os.environ["PANDOC"])
    if shutil.which("pandoc"):
        return Path(shutil.which("pandoc"))
    bundled = sorted((TALK.parent / ".venv").glob("lib/python3*/site-packages/pypandoc/files/pandoc"))
    if bundled:
        return bundled[0]
    raise RuntimeError("pandoc not found: set PANDOC, put pandoc on PATH, or install pypandoc in .venv")


PANDOC = _find_pandoc()
EQ_VERSION = "eq-v3"  # bump to invalidate the equation cache

PAGE_W, PAGE_H = 453.54, 255.12          # Beamer page, pt
F = 960.0 / PAGE_W                        # Beamer pt -> slide pt (2.1167)

SIZES = {"tiny": 5.98, "script": 7.97, "footnote": 8.97, "small": 9.96, "normal": 10.91,
         "large": 11.96, "Large": 14.35, "LARGE": 17.28, "huge": 20.74, "Huge": 24.88}

# Colours sampled from talk.pdf with PyMuPDF get_drawings (Madrid) and the deck's aliases.
STRUCT = "3333B2"      # Madrid structure blue: title bar, footline right segment, buttons, KeyIdea
FOOT = ("1A1A59", "262686", "3333B2")   # footline segments left / middle / right
INFO = "AA4B00"        # cInfo
COST = "006F50"        # cCost
GRAY = "616161"        # cGrayText (black!62)
BLACK = "000000"
WHITE = "FFFFFF"
BOX_EDGE = "737373"    # black!55 diagram box edges
ARROW = "666666"       # black!60 diagram arrows
NUM_FILL = "595959"    # black!65 numbered circles (D1)
RB_FRAME = "29298F"    # ResultBox frame / title band (structure!80!black)
RB_BACK = "EFEFF9"     # ResultBox body (structure!8!white)

TEXT_FONT = "Calibri"
MATH_FONT = "Cambria Math"

TITLE_BAR_H = 27.6     # Madrid frametitle band without subtitle (Beamer pt)
SUBTITLE_BAR_H = 39.54
FOOT_Y, FOOT_H = 246.49, 8.63
NAV_Y, NAV_H, NAV_RIGHT, NAV_GAP = 233.0, 7.93, 431.73, 3.82

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "a14": "http://schemas.microsoft.com/office/drawing/2010/main",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "asvg": "http://schemas.microsoft.com/office/drawing/2016/SVG/main",
}
SVG_EXT_URI = "{96DAC541-7B7A-43D3-8B79-37D633B846F1}"
NO_STYLE_TABLE = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"   # built-in "No Style, No Grid"


def Q(tag: str) -> str:
    """Clark-notation name for prefixes python-pptx's qn() does not know (m, a14, mc, w)."""
    pfx, local = tag.split(":")
    return "{%s}%s" % (NS[pfx], local)


def E(v: float) -> Emu:
    """Beamer pt -> EMU on the slide."""
    return Emu(int(round(v * F * 12700)))


def size_pt(size) -> float:
    """Beamer size name or pt -> slide pt, rounded to 0.5 pt."""
    s = SIZES[size] if isinstance(size, str) else float(size)
    return round(s * F * 2) / 2


# ----------------------------------------------------------------------------------------------
# Content records
# ----------------------------------------------------------------------------------------------
@dataclass
class P:
    text: str
    bullet: str | None = None
    level: int = 0
    size: object = None
    align: str = "l"
    before: float = 0.0
    after: float = 0.0
    color: str | None = None
    bold: bool = False
    line: float | None = None
    hang: tuple | None = None
    line_pt: float | None = None   # exact line pitch in Beamer pt (overrides `line`)


@dataclass
class Text:
    x: float
    y: float
    w: float
    paras: list
    size: object = "normal"
    h: float | None = None
    anchor: str = "t"
    name: str = "Text"


@dataclass
class Cell:
    text: str
    span: int = 1
    align: str | None = None
    size: object = None


@dataclass
class Table:
    x: float
    y: float
    cols: list
    rows: list
    size: object = "small"
    align: object = "l"
    row_h: object = 12.0
    rules: bool = True
    midrules: tuple = (0,)
    valign: object = "m"   # 't'|'m'|'b', or one per row
    pad: float = 3.0
    pad_v: float = 0.0
    name: str = "Table"
    pad_top: object = None     # top cell margin (Beamer pt): scalar or one per row; default pad_v
    col_pads: object = None    # [(left, right), ...] per-column horizontal margins; default pad
    line: float | None = None  # line-spacing multiple for all cell paragraphs (dense tables)
    line_pt: float | None = None   # exact line pitch (Beamer pt) for all cell paragraphs


@dataclass
class Eq:
    x: float
    y: float
    latex: str
    size: object = "normal"
    anchor: str = "l"
    color: str | None = None
    name: str = "Equation"


@dataclass
class Figure:
    x: float
    y: float
    w: float
    h: float
    name: str
    alt: str = ""


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float
    text: object
    edge: str = BOX_EDGE
    lw: float = 0.6
    align: str = "c"
    anchor: str = "m"
    number: str | None = None
    pad: object = 4.0      # scalar or (left, top, right, bottom)


@dataclass
class Flow:
    boxes: list
    arrows: list
    size: object = "footnote"
    name: str = "Diagram"
    radius: float = 3.0


@dataclass
class ResultBox:
    x: float
    y: float
    w: float
    h: float
    title: str
    paras: list
    size: object = "small"
    title_h: float = 15.5


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float
    fill: str | None = None
    line: str | None = None
    lw: float = 0.6
    radius: float = 0.0
    name: str = "Shape"


@dataclass
class Slide:
    label: str
    title: str
    subtitle: str | None = None
    page: str | None = None
    kind: str = "frame"
    body: list = field(default_factory=list)
    nav: list = field(default_factory=list)
    back: str | None = None
    notes: str | None = None


# ----------------------------------------------------------------------------------------------
# Runs: inline markup and inline math -> styled runs
# ----------------------------------------------------------------------------------------------
@dataclass
class Run:
    text: str
    b: bool = False
    i: bool = False
    color: str | None = None
    size: object = None
    math: bool = False
    baseline: int = 0
    br: bool = False
    scale: float = 1.0     # extra size factor (second-level scripts)


def _style(run_kw: dict, **upd) -> dict:
    d = dict(run_kw)
    d.update(upd)
    return d


STYLE_CMDS = {
    "b": {"b": True}, "i": {"i": True},
    "key": {"b": True, "color": STRUCT}, "info": {"color": INFO}, "cost": {"color": COST},
    "gray": {"color": GRAY}, "cite": {"color": GRAY, "size": "footnote"},
    "status": {"color": GRAY, "size": "script"}, "statusf": {"color": GRAY, "size": "footnote"},
    "small": {"size": "small"}, "foot": {"size": "footnote"}, "script": {"size": "script"},
    "tiny": {"size": "tiny"}, "normal": {"size": "normal"}, "large": {"size": "large"},
}


def _read_group(s: str, i: int) -> tuple[str, int]:
    """s[i] == '{' -> (content, index after the matching '}')."""
    if i >= len(s) or s[i] != "{":
        raise ValueError(f"expected '{{' at {i} in {s!r}")
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced braces in {s!r}")


def _find_math_end(s: str, i: int) -> int:
    j = i
    while j < len(s):
        if s[j] == "\\":
            j += 2
            continue
        if s[j] == "$":
            return j
        j += 1
    raise ValueError(f"unterminated $ in {s!r}")


def markup_runs(s: str, style: dict | None = None) -> list[Run]:
    """Parse the inline markup (see module docstring) into runs."""
    style = style or {}
    runs: list[Run] = []
    buf: list[str] = []

    def flush():
        if buf:
            runs.append(Run("".join(buf), **style))
            buf.clear()

    i = 0
    while i < len(s):
        c = s[i]
        if c == "$":
            flush()
            j = _find_math_end(s, i + 1)
            runs.extend(math_runs(s[i + 1:j], style))
            i = j + 1
        elif c == "\\":
            if i + 1 < len(s) and s[i + 1] == "\\":
                flush()
                runs.append(Run("", br=True, **style))
                i += 2
                continue
            m = re.match(r"[A-Za-z]+", s[i + 1:])
            if not m:
                buf.append(s[i + 1])
                i += 2
                continue
            cmd = m.group(0)
            i += 1 + len(cmd)
            flush()
            if cmd == "color":
                hexcol, i = _read_group(s, i)
                inner, i = _read_group(s, i)
                runs.extend(markup_runs(inner, _style(style, color=hexcol.strip().lstrip("#"))))
            elif cmd in STYLE_CMDS:
                inner, i = _read_group(s, i)
                runs.extend(markup_runs(inner, _style(style, **STYLE_CMDS[cmd])))
            else:
                raise ValueError(f"unknown markup command \\{cmd} in {s!r}")
        elif c == "{":
            flush()
            inner, i = _read_group(s, i)
            runs.extend(markup_runs(inner, style))
        elif c == "}":
            raise ValueError(f"stray '}}' in {s!r}")
        elif c == "~":
            buf.append("\u00a0")
            i += 1
        else:
            buf.append(c)
            i += 1
    flush()
    return runs


# --- inline math -------------------------------------------------------------------------------
GREEK = {
    "alpha": "𝛼", "beta": "𝛽", "gamma": "𝛾", "delta": "𝛿", "epsilon": "𝜖", "varepsilon": "𝜀",
    "zeta": "𝜁", "eta": "𝜂", "theta": "𝜃", "vartheta": "𝜗", "kappa": "𝜅", "lambda": "𝜆",
    "mu": "𝜇", "nu": "𝜈", "xi": "𝜉", "pi": "𝜋", "rho": "𝜌", "sigma": "𝜎", "tau": "𝜏",
    "phi": "𝜙", "varphi": "𝜑", "chi": "𝜒", "psi": "𝜓", "omega": "𝜔",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π",
    "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}
REL = {"le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "to": "→", "rightarrow": "→",
       "leftarrow": "←", "Rightarrow": "⇒", "in": "∈", "notin": "∉", "sim": "∼", "approx": "≈",
       "ne": "≠", "neq": "≠", "equiv": "≡", "uparrow": "↑", "downarrow": "↓", "mapsto": "↦",
       "subset": "⊂", "subseteq": "⊆", "propto": "∝", "mid": "|", "gg": "≫", "ll": "≪"}
BIN = {"times": "×", "cdot": "⋅", "pm": "±", "mp": "∓", "cup": "∪", "cap": "∩", "setminus": "∖"}
ORD = {"ell": "ℓ", "infty": "∞", "partial": "∂", "nabla": "∇", "ldots": "…", "dots": "…",
       "cdots": "⋯", "prime": "′", "emptyset": "∅", "forall": "∀", "exists": "∃",
       "lvert": "|", "rvert": "|", "vert": "|", "bullet": "•", "neg": "¬"}
OPS = {"max", "min", "Pr", "log", "exp", "sup", "inf", "lim", "arg", "argmax", "det", "sgn"}
SPACES = {",": "\u2009", ";": "\u2005", ":": "\u2005", "!": "", " ": " ", "quad": "\u2003",
          "qquad": "\u2003\u2003", "enspace": "\u2002"}
IGNORE = {"left", "right", "big", "Big", "bigl", "bigr", "Bigl", "Bigr", "displaystyle",
          "textstyle", "limits", "nolimits"}
DOUBLE = {"E": "𝔼", "R": "ℝ", "N": "ℕ", "Z": "ℤ", "Q": "ℚ", "P": "ℙ"}
NBSP = "\u00a0"
SUB_DIGITS = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
SUP_DIGITS = str.maketrans("0123456789+-=()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾")


def _italic(ch: str) -> str:
    if ch == "h":
        return "ℎ"
    if "a" <= ch <= "z":
        return chr(0x1D44E + ord(ch) - ord("a"))
    if "A" <= ch <= "Z":
        return chr(0x1D434 + ord(ch) - ord("A"))
    return ch


@dataclass
class _Atom:
    text: str
    cls: str               # ord, rel, bin, open, close, punct, op, space, text
    b: bool = False
    color: str | None = None
    level: int = 0         # 0 base, +1 sub, -1 sup (sign), depth via abs
    upright: bool = False  # text-font run (\text)


def _math_atoms(s: str, b=False, color=None, level=0) -> list[_Atom]:
    atoms: list[_Atom] = []
    i = 0

    def arg(i):
        # one token or {group}
        while i < len(s) and s[i] == " ":
            i += 1
        if i < len(s) and s[i] == "{":
            return _read_group(s, i)
        if i < len(s) and s[i] == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            return m.group(0), i + len(m.group(0))
        return s[i], i + 1

    while i < len(s):
        c = s[i]
        if c == " ":
            i += 1
            continue
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", s[i:])
            cmd = m.group(1)
            i += len(m.group(0))
            if cmd in GREEK:
                atoms.append(_Atom(GREEK[cmd], "ord", b, color, level))
            elif cmd in ORD:
                atoms.append(_Atom(ORD[cmd], "ord", b, color, level))
            elif cmd in REL:
                atoms.append(_Atom(REL[cmd], "rel", b, color, level))
            elif cmd in BIN:
                atoms.append(_Atom(BIN[cmd], "bin", b, color, level))
            elif cmd in OPS:
                atoms.append(_Atom(cmd, "op", b, color, level, upright=False))
            elif cmd in SPACES:
                atoms.append(_Atom(SPACES[cmd], "space", b, color, level))
            elif cmd in IGNORE:
                pass
            elif cmd in ("{", "}"):
                atoms.append(_Atom(cmd, "open" if cmd == "{" else "close", b, color, level))
            elif cmd in ("%", "$", "&", "#", "_"):
                atoms.append(_Atom(cmd, "ord", b, color, level))
            elif cmd == "mathbb":
                g, i = arg(i)
                atoms.append(_Atom("".join(DOUBLE.get(ch, ch) for ch in g), "ord", b, color, level))
            elif cmd in ("text", "textrm", "mathrm", "mbox", "textnormal", "operatorname"):
                g, i = arg(i)
                cls = "op" if cmd in ("mathrm", "operatorname") else "text"
                atoms.append(_Atom(g.replace("~", "\u00a0"), cls, b, color, level, upright=(cls == "text")))
            elif cmd in ("boldsymbol", "mathbf", "bm", "textbf"):
                g, i = arg(i)
                atoms.extend(_math_atoms(g, True, color, level))
            elif cmd in ("Info", "Cost"):
                g, i = arg(i)
                atoms.extend(_math_atoms(g, b, INFO if cmd == "Info" else COST, level))
            elif cmd == "textcolor":
                col, i = arg(i)
                g, i = arg(i)
                atoms.extend(_math_atoms(g, b, {"cInfo": INFO, "cCost": COST}.get(col, col), level))
            elif cmd == "mathsf":
                g, i = arg(i)
                atoms.append(_Atom(g, "text", b, color, level, upright=True))
            elif cmd in ("bar", "overline", "hat", "tilde", "widehat", "widetilde"):
                g, i = arg(i)
                inner = _math_atoms(g, b, color, level)
                mark = {"bar": "\u0304", "overline": "\u0305", "hat": "\u0302",
                        "widehat": "\u0302", "tilde": "\u0303", "widetilde": "\u0303"}[cmd]
                if inner:
                    inner[0].text += mark
                atoms.extend(inner)
            elif cmd == "frac":
                num, i = arg(i)
                den, i = arg(i)
                atoms.extend(_math_atoms(num, b, color, level))
                atoms.append(_Atom("/", "ord", b, color, level))
                atoms.extend(_math_atoms(den, b, color, level))
            else:
                raise ValueError(f"unsupported math command \\{cmd} in ${s}$")
            continue
        if c in "_^":
            g, i = arg(i + 1)
            sub = -1 if c == "^" else 1
            new_level = (abs(level) + 1) * sub
            atoms.extend(_math_atoms(g, b, color, new_level))
            continue
        if c == "{":
            g, i = _read_group(s, i)
            atoms.extend(_math_atoms(g, b, color, level))
            continue
        i += 1
        if c.isalpha():
            atoms.append(_Atom(_italic(c), "ord", b, color, level))
        elif c.isdigit() or c == ".":
            atoms.append(_Atom(c, "ord", b, color, level))
        elif c in "=<>":
            atoms.append(_Atom(c, "rel", b, color, level))
        elif c == "-":
            atoms.append(_Atom("−", "bin", b, color, level))
        elif c in "+*":
            atoms.append(_Atom("+" if c == "+" else "∗", "bin", b, color, level))
        elif c in "([":
            atoms.append(_Atom(c, "open", b, color, level))
        elif c in ")]":
            atoms.append(_Atom(c, "close", b, color, level))
        elif c in ",;":
            atoms.append(_Atom(c, "punct", b, color, level))
        elif c == "'":
            atoms.append(_Atom("′", "ord", b, color, level))
        elif c == "~":
            atoms.append(_Atom(" ", "space", b, color, level))
        else:
            atoms.append(_Atom(c, "ord", b, color, level))
    return atoms


def math_runs(src: str, style: dict | None = None) -> list[Run]:
    """Inline LaTeX math -> native runs (Unicode math italics, real sub/superscripts)."""
    style = dict(style or {})
    base_color = style.get("color")
    atoms = _math_atoms(src)
    # TeX-like spacing: no-break spaces around binary operators (not unary) and before relations;
    # after a relation the space is breakable when another relation follows in the same formula
    # (a chain such as B(1/2) = 4.80 < c_H = 6 < B(M) may wrap, a short x = 0.015 never does);
    # a narrow no-break space follows commas (TeX never breaks inline math at a comma, so a set
    # such as {H, L} stays on one line)
    out: list[_Atom] = []
    prev = None
    for k, a in enumerate(atoms):
        if a.level == 0 and a.cls == "rel":
            if prev is not None and prev.cls not in ("open", "space"):
                out.append(_Atom(NBSP, "space", a.b, a.color, 0))
            out.append(a)
            if k + 1 < len(atoms) and atoms[k + 1].cls not in ("close", "punct"):
                chain = any(b.level == 0 and b.cls == "rel" for b in atoms[k + 1:])
                out.append(_Atom(" " if chain else NBSP, "space", a.b, a.color, 0))
        elif a.level == 0 and a.cls == "bin":
            unary = prev is None or prev.cls in ("bin", "rel", "open", "punct", "op")
            if unary:
                out.append(a)
            else:
                out.append(_Atom(NBSP, "space", a.b, a.color, 0))
                out.append(a)
                out.append(_Atom(NBSP, "space", a.b, a.color, 0))
        elif a.level == 0 and a.cls == "punct":
            out.append(a)
            if k + 1 < len(atoms) and a.text == ",":
                out.append(_Atom("\u202f", "space", a.b, a.color, 0))
        elif a.cls == "op" and k + 1 < len(atoms) and atoms[k + 1].cls in ("ord",) and atoms[k + 1].level == 0:
            out.append(a)
            out.append(_Atom("\u2009", "space", a.b, a.color, 0))
        else:
            out.append(a)
        if a.cls != "space":
            prev = a
    # collapse double spaces
    cleaned: list[_Atom] = []
    for a in out:
        if a.cls == "space" and cleaned and cleaned[-1].cls == "space" and a.text in (" ", NBSP) \
                and cleaned[-1].text in (" ", NBSP):
            continue
        cleaned.append(a)
    runs: list[Run] = []
    for a in cleaned:
        text = a.text
        baseline = 0
        scale = 1.0
        if a.level:
            depth = abs(a.level)
            baseline = -25000 if a.level > 0 else 30000
            if depth >= 2:  # second-level scripts: smaller and further offset (TeX scriptscript)
                scale = 0.75
                baseline = -32000 if a.level > 0 else 36000
        kw = dict(style)
        kw["color"] = a.color or base_color
        kw["b"] = style.get("b", False) or a.b
        kw["i"] = False
        kw["math"] = not a.upright
        kw["baseline"] = baseline
        kw["scale"] = scale
        r = Run(text, **kw)
        if runs and not runs[-1].br and all(getattr(runs[-1], f) == getattr(r, f) for f in
                                            ("b", "i", "color", "size", "math", "baseline", "scale")):
            runs[-1].text += r.text
        else:
            runs.append(r)
    return runs


# ----------------------------------------------------------------------------------------------
# Measurement (Carlito = metric-identical Calibri) for height estimates and button widths
# ----------------------------------------------------------------------------------------------
_FONTS: dict = {}


def _font_file(pattern: str) -> str | None:
    try:
        out = subprocess.run(["fc-match", "-f", "%{file}", pattern], capture_output=True, text=True, check=True)
        return out.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def _font(bold: bool, math: bool):
    from PIL import ImageFont
    key = ("math" if math else "text", bold)
    if key not in _FONTS:
        pattern = "XITS Math" if math else ("Carlito:bold" if bold else "Carlito")
        path = _font_file(pattern)
        _FONTS[key] = ImageFont.truetype(path, 1000) if path else None
    return _FONTS[key]


def text_width(text: str, size_bp: float, bold=False, math=False) -> float:
    """Width in Beamer pt of text at size_bp Beamer pt."""
    f = _font(bold, math)
    if f is None:
        return 0.5 * size_bp * len(text)
    return f.getlength(text) / 1000.0 * size_bp


def _size_bp(size) -> float:
    return SIZES[size] if isinstance(size, str) else float(size)


def _para_obj(p) -> P:
    return p if isinstance(p, P) else P(p)


def _para_geometry(p: P, size) -> tuple[float, float]:
    """(marL, indent) in Beamer pt for a paragraph."""
    if p.hang is not None:
        return p.hang
    base = 21.8 + 16.0 * p.level
    if p.bullet == "ball":
        return base, -10.6
    if p.bullet == "none":
        return base, 0.0
    if p.bullet == "dot":
        return 10.2, -10.2
    return 0.0, 0.0


def measure_paras(paras, width: float, size="normal") -> float:
    """Estimated height (Beamer pt) of paragraphs laid out in a box of the given width."""
    total = 0.0
    for k, p in enumerate(paras):
        p = _para_obj(p)
        psize = _size_bp(p.size or size)
        runs = markup_runs(p.text, {"size": p.size or size, "b": p.bold})
        marl, _ = _para_geometry(p, psize)
        avail = max(width - marl, 10)
        lines, cur, line_max = 1, 0.0, psize
        for r in runs:
            if r.br:
                lines += 1
                cur = 0.0
                continue
            rs = _size_bp(r.size or size) * (0.7 if r.baseline else 1.0)
            for tok in re.split(r"([ \t\u2002\u2003\u2005\u2009]+)", r.text):
                if not tok:
                    continue
                w = text_width(tok, rs, r.b, r.math)
                if cur + w > avail and not tok.isspace() and cur > 0:
                    lines += 1
                    cur = w
                else:
                    cur += w
        spacing = (p.line or 1.0) * 1.2207 * psize
        total += lines * spacing + (p.before if k else 0) + p.after
    return total


# ----------------------------------------------------------------------------------------------
# Low-level XML helpers
# ----------------------------------------------------------------------------------------------
def _a(tag: str) -> str:
    return qn("a:" + tag)


def _srgb(parent, hexcol: str):
    fill = etree.SubElement(parent, _a("solidFill"))
    etree.SubElement(fill, _a("srgbClr"), val=hexcol)
    return fill


def _apply_run(r, run: Run, default_size, slide_color=None):
    """Write explicit character properties on a python-pptx run."""
    r.text = run.text
    rPr = r._r.get_or_add_rPr()
    for k in list(rPr.attrib):
        del rPr.attrib[k]
    for ch in list(rPr):
        rPr.remove(ch)
    rPr.set("lang", "en-US")
    rPr.set("sz", str(int(round(size_pt(run.size or default_size) * run.scale * 100))))
    rPr.set("b", "1" if run.b else "0")
    rPr.set("i", "1" if run.i else "0")
    if run.baseline:
        rPr.set("baseline", str(run.baseline))
    rPr.set("dirty", "0")
    _srgb(rPr, run.color or slide_color or BLACK)
    face = MATH_FONT if run.math else TEXT_FONT
    etree.SubElement(rPr, _a("latin"), typeface=face)
    etree.SubElement(rPr, _a("ea"), typeface=face)
    etree.SubElement(rPr, _a("cs"), typeface=face)


def _set_ppr(p_el, p: P, size, bullet_color=STRUCT):
    """Paragraph properties: alignment, indents, spacing, bullets (schema order kept)."""
    pPr = p_el.get_or_add_pPr()
    for ch in list(pPr):
        pPr.remove(ch)
    marl, indent = _para_geometry(p, size)
    pPr.set("marL", str(int(E(marl))))
    pPr.set("indent", str(int(E(indent))))
    pPr.set("algn", {"l": "l", "c": "ctr", "r": "r", "j": "just"}[p.align])
    if p.line_pt:
        ln = etree.SubElement(pPr, _a("lnSpc"))
        etree.SubElement(ln, _a("spcPts"), val=str(int(round(p.line_pt * F * 100))))
    elif p.line:
        ln = etree.SubElement(pPr, _a("lnSpc"))
        etree.SubElement(ln, _a("spcPct"), val=str(int(p.line * 100000)))
    sb = etree.SubElement(pPr, _a("spcBef"))
    etree.SubElement(sb, _a("spcPts"), val=str(int(round(p.before * F * 100))))
    sa = etree.SubElement(pPr, _a("spcAft"))
    etree.SubElement(sa, _a("spcPts"), val=str(int(round(p.after * F * 100))))
    if p.bullet in ("ball", "dot"):
        bc = etree.SubElement(pPr, _a("buClr"))
        etree.SubElement(bc, _a("srgbClr"), val=bullet_color)
        etree.SubElement(pPr, _a("buSzPct"), val="90000" if p.bullet == "ball" else "100000")
        etree.SubElement(pPr, _a("buFont"), typeface=TEXT_FONT)
        etree.SubElement(pPr, _a("buChar"), char="●" if p.bullet == "ball" else "•")
    else:
        etree.SubElement(pPr, _a("buNone"))


def fill_text_frame(tf, paras, size="normal", color=None):
    """Write paragraphs (P or markup) into a text frame, replacing its content."""
    paras = [_para_obj(p) for p in paras]
    txBody = tf._txBody
    for p_el in txBody.findall(_a("p"))[1:]:
        txBody.remove(p_el)
    first = tf.paragraphs[0]
    for r in list(first._p):
        if r.tag != _a("pPr"):
            first._p.remove(r)
    for k, p in enumerate(paras):
        para = first if k == 0 else tf.add_paragraph()
        psize = p.size or size
        _set_ppr(para._p, p, psize)
        runs = markup_runs(p.text, {"size": p.size or None, "b": p.bold, "color": p.color or color})
        for run in runs:
            if run.br:
                # a:br carries the run size, else PowerPoint sizes the break at the 18 pt default
                br = etree.SubElement(para._p, _a("br"))
                etree.SubElement(br, _a("rPr"), lang="en-US",
                                 sz=str(int(round(size_pt(run.size or psize) * 100))))
                continue
            if run.text == "":
                continue
            _apply_run(para.add_run(), run, psize)
        # end-of-paragraph properties keep the size so empty lines have the right height
        end = etree.SubElement(para._p, _a("endParaRPr"), lang="en-US",
                               sz=str(int(size_pt(psize) * 100)), dirty="0")
        etree.SubElement(end, _a("latin"), typeface=TEXT_FONT)


def _frame_setup(tf, anchor="t", wrap=True, insets=(0, 0, 0, 0)):
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = (E(v) for v in insets)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]


def _no_line(shape):
    shape.line.fill.background()


def _set_line(shape, hexcol, width_bp):
    shape.line.color.rgb = RGBColor.from_string(hexcol)
    shape.line.width = Pt(width_bp * F)


def _set_fill(shape, hexcol):
    if hexcol is None:
        shape.fill.background()
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(hexcol)


def _round_adj(shape, radius_bp, w, h):
    if shape.adjustments and len(shape.adjustments):
        shape.adjustments[0] = min(0.5, radius_bp / max(min(w, h), 1e-6))


def _no_shadow(shape):
    """Drop the theme style reference (whose effectRef draws a shadow) and state no effects."""
    el = shape._element
    style = el.find(qn("p:style"))
    if style is not None:
        el.remove(style)
    spPr = el.spPr
    if spPr.find(_a("effectLst")) is None:
        eff = etree.SubElement(spPr, _a("effectLst"))
        ln = spPr.find(_a("ln"))
        if ln is not None:
            ln.addnext(eff)


# ----------------------------------------------------------------------------------------------
# Element builders
# ----------------------------------------------------------------------------------------------
def add_text(shapes, el: Text):
    h = el.h if el.h is not None else measure_paras(el.paras, el.w, el.size) + 2.0
    tb = shapes.add_textbox(E(el.x), E(el.y), E(el.w), E(h))
    tb.name = el.name
    _frame_setup(tb.text_frame, el.anchor)
    fill_text_frame(tb.text_frame, el.paras, el.size)
    return tb


def add_rect(shapes, el: Rect):
    prst = MSO_SHAPE.ROUNDED_RECTANGLE if el.radius else MSO_SHAPE.RECTANGLE
    sh = shapes.add_shape(prst, E(el.x), E(el.y), E(el.w), E(el.h))
    sh.name = el.name
    _set_fill(sh, el.fill)
    if el.line:
        _set_line(sh, el.line, el.lw)
    else:
        _no_line(sh)
    if el.radius:
        _round_adj(sh, el.radius, el.w, el.h)
    _no_shadow(sh)
    return sh


def _cell_borders(cell, top, bottom):
    """top/bottom: None or width in Beamer pt. Left/right never drawn (booktabs)."""
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("lnL", "lnR", "lnT", "lnB", "noFill", "solidFill"):
        for old in tcPr.findall(_a(tag)):
            tcPr.remove(old)
    for tag, w in (("lnL", None), ("lnR", None), ("lnT", top), ("lnB", bottom)):
        ln = etree.SubElement(tcPr, _a(tag))
        if w is None:
            ln.set("w", "0")
            etree.SubElement(ln, _a("noFill"))
        else:
            ln.set("w", str(int(round(w * F * 12700))))
            ln.set("cap", "flat")
            ln.set("cmpd", "sng")
            ln.set("algn", "ctr")
            _srgb(ln, BLACK)
            etree.SubElement(ln, _a("prstDash"), val="solid")
    etree.SubElement(tcPr, _a("noFill"))


def add_table(shapes, el: Table):
    nrows, ncols = len(el.rows), len(el.cols)
    row_h = el.row_h if isinstance(el.row_h, (list, tuple)) else [el.row_h] * nrows
    gf = shapes.add_table(nrows, ncols, E(el.x), E(el.y), E(sum(el.cols)), E(sum(row_h)))
    gf.name = el.name
    tbl = gf.table
    tblPr = tbl._tbl.tblPr
    for attr in ("firstRow", "bandRow", "firstCol", "lastRow", "lastCol", "bandCol"):
        if attr in tblPr.attrib:
            del tblPr.attrib[attr]
    sid = tblPr.find(_a("tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, _a("tableStyleId"))
    sid.text = NO_STYLE_TABLE
    for j, w in enumerate(el.cols):
        tbl.columns[j].width = E(w)
    for i, h in enumerate(row_h):
        tbl.rows[i].height = E(h)
    aligns = el.align if isinstance(el.align, (list, tuple)) else [el.align] * ncols
    heavy, light = 0.87, 0.55
    rule_below = {i: light for i in el.midrules} if el.rules else {}
    for i, row in enumerate(el.rows):
        j = 0
        for c in row:
            c = c if isinstance(c, Cell) else Cell(c)
            cell = tbl.cell(i, j)
            if c.span > 1:
                cell.merge(tbl.cell(i, j + c.span - 1))
            if el.col_pads is not None:
                cell.margin_left = E(el.col_pads[j][0])
                cell.margin_right = E(el.col_pads[j + c.span - 1][1])
            else:
                cell.margin_left = cell.margin_right = E(el.pad)
            ptop = el.pad_top[i] if isinstance(el.pad_top, (list, tuple)) else el.pad_top
            cell.margin_top = E(el.pad_v if ptop is None else ptop)
            cell.margin_bottom = E(el.pad_v)
            va = el.valign[i] if isinstance(el.valign, (list, tuple)) else el.valign
            cell.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[va]
            al = c.align or aligns[j]
            # an empty paragraph ignores an exact line pitch (its height is the end-of-paragraph
            # font's), so exact-pitch tables get a no-break space instead
            txt = "\u00a0" if (el.line_pt and c.text == "") else c.text
            paras = [P(txt, align=al, line=el.line, line_pt=el.line_pt) for part in [c.text]]
            fill_text_frame(cell.text_frame, paras, c.size or el.size)
            j += c.span
        while j < ncols:  # short row: blank cells
            fill_text_frame(tbl.cell(i, j).text_frame,
                            [P("\u00a0" if el.line_pt else "", line_pt=el.line_pt)], el.size)
            j += 1
    for i in range(nrows):
        top = bottom = None
        if el.rules:
            if i == 0:
                top = heavy
            elif (i - 1) in rule_below:
                top = rule_below[i - 1]
            if i == nrows - 1:
                bottom = heavy
            elif i in rule_below:
                bottom = rule_below[i]
        for j in range(ncols):
            _cell_borders(tbl.cell(i, j), top, bottom)
    return gf


def add_figure(shapes, slide_part, el: Figure):
    png = FIGDIR / f"{el.name}.png"
    pic = shapes.add_picture(str(png), E(el.x), E(el.y), E(el.w), E(el.h))
    pic.name = f"Figure {el.name}"
    pic._element.nvPicPr.cNvPr.set("descr", el.alt or el.name)
    svg = FIGDIR / f"{el.name}.svg"
    if svg.exists():
        package = slide_part.package
        partname = package.next_image_partname("svg")
        svg_part = Part(partname, "image/svg+xml", package, svg.read_bytes())
        rid = slide_part.relate_to(svg_part, RT.IMAGE)
        blip = pic._element.blipFill.find(_a("blip"))
        ext_lst = blip.find(_a("extLst"))
        if ext_lst is None:
            ext_lst = etree.SubElement(blip, _a("extLst"))
        ext = etree.SubElement(ext_lst, _a("ext"), uri=SVG_EXT_URI)
        sb = etree.SubElement(ext, "{%s}svgBlip" % NS["asvg"], nsmap={"asvg": NS["asvg"]})
        sb.set(qn("r:embed"), rid)
    return pic


def _connector(shapes, x1, y1, x2, y2, color=ARROW, width=0.7):
    cx = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, E(x1), E(y1), E(x2), E(y2))
    cx.line.color.rgb = RGBColor.from_string(color)
    cx.line.width = Pt(width * F)
    ln = cx.line._get_or_add_ln()
    etree.SubElement(ln, _a("tailEnd"), type="triangle", w="med", len="med")
    _no_shadow(cx)
    return cx


def add_flow(shapes, el: Flow):
    grp = shapes.add_group_shape()
    grp.name = el.name
    made = []
    for k, bx in enumerate(el.boxes):
        sh = grp.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(bx.x), E(bx.y), E(bx.w), E(bx.h))
        sh.name = f"{el.name} box {k + 1}"
        _set_fill(sh, WHITE)
        _set_line(sh, bx.edge, bx.lw)
        _round_adj(sh, el.radius, bx.w, bx.h)
        _no_shadow(sh)
        tf = sh.text_frame
        pad = bx.pad if isinstance(bx.pad, (tuple, list)) else (bx.pad,) * 4
        _frame_setup(tf, bx.anchor, insets=pad)
        paras = bx.text if isinstance(bx.text, list) else [P(bx.text, align=bx.align)]
        fill_text_frame(tf, paras, el.size)
        made.append(sh)
    for (i, j) in el.arrows:
        a, b = el.boxes[i], el.boxes[j]
        y = a.y + a.h / 2
        cx = _connector(grp.shapes, a.x + a.w + a.lw / 2, y, b.x - b.lw / 2 - 0.3, y)
        cx.begin_connect(made[i], 3)
        cx.end_connect(made[j], 1)
        cx.name = f"{el.name} arrow {i + 1}-{j + 1}"
    for k, bx in enumerate(el.boxes):
        if bx.number:
            d = 11.0
            c = grp.shapes.add_shape(MSO_SHAPE.OVAL, E(bx.x - 3.8), E(bx.y - 4.8), E(d), E(d))
            c.name = f"{el.name} step {bx.number}"
            _set_fill(c, NUM_FILL)
            _no_line(c)
            _no_shadow(c)
            _frame_setup(c.text_frame, "m")
            fill_text_frame(c.text_frame, [P(r"\b{%s}" % bx.number, align="c", color=WHITE, size="script")], "script")
    return grp


def add_resultbox(shapes, el: ResultBox):
    grp = shapes.add_group_shape()
    grp.name = "ResultBox"
    body = grp.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(el.x), E(el.y), E(el.w), E(el.h))
    body.name = "ResultBox body"
    _set_fill(body, RB_BACK)
    _set_line(body, RB_FRAME, 0.8)
    _round_adj(body, 1.5, el.w, el.h)
    _no_shadow(body)
    _frame_setup(body.text_frame, "t", insets=(9.1, el.title_h + 3.3, 6.8, 3.0))
    fill_text_frame(body.text_frame, el.paras, el.size)
    band = grp.shapes.add_shape(MSO_SHAPE.ROUND_2_SAME_RECTANGLE, E(el.x), E(el.y), E(el.w), E(el.title_h))
    band.name = "ResultBox title"
    _set_fill(band, RB_FRAME)
    _set_line(band, RB_FRAME, 0.8)
    band.adjustments[0] = min(0.5, 1.5 / el.title_h)
    band.adjustments[1] = 0.0
    _no_shadow(band)
    _frame_setup(band.text_frame, "m", insets=(9.1, 0, 6.8, 0))
    fill_text_frame(band.text_frame, [P(r"\b{%s}" % el.title, color=WHITE)], el.size)
    return grp


# --- equations ---------------------------------------------------------------------------------
EQ_PREAMBLE = r"""\documentclass[border=0.6pt]{standalone}
\usepackage{amsmath,amssymb,mathtools,xcolor,fontspec}
\setmainfont{Latin Modern Sans}
\definecolor{cInfo}{HTML}{AA4B00}\definecolor{cCost}{HTML}{006F50}
\newcommand{\Info}[1]{\textcolor{cInfo}{#1}}
\newcommand{\Cost}[1]{\textcolor{cCost}{#1}}
\begin{document}
"""


def _strip_color_macros(latex: str) -> tuple[str, list[tuple[str, str]]]:
    """Remove \\Info{..}/\\Cost{..} wrappers; return (plain latex, [(fragment, colour)])."""
    frags = []
    out, i = [], 0
    while i < len(latex):
        m = re.match(r"\\(Info|Cost)(?![A-Za-z])", latex[i:])
        if m:
            j = i + len(m.group(0))
            inner, j = _read_group(latex, j)
            inner_plain, sub = _strip_color_macros(inner)
            frags.extend(sub)
            frags.append((inner_plain, INFO if m.group(1) == "Info" else COST))
            out.append("{" + inner_plain + "}")
            i = j
        else:
            out.append(latex[i])
            i += 1
    return "".join(out), frags


def _pandoc_omml(latex: str) -> etree._Element:
    """LaTeX display math -> m:oMath element via pandoc (docx writer)."""
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "eq.tex"
        src.write_text("\\[" + latex + "\\]\n", encoding="utf-8")
        dst = Path(td) / "eq.docx"
        subprocess.run([str(PANDOC), str(src), "-f", "latex", "-t", "docx", "-o", str(dst)], check=True)
        xml = zipfile.ZipFile(dst).read("word/document.xml")
    root = etree.fromstring(xml)
    om = root.xpath("//m:oMath", namespaces=NS)
    if not om:
        raise RuntimeError(f"pandoc produced no OMML for {latex!r}")
    return om[0]


def _omml_texts(el) -> str:
    return "".join(el.xpath(".//m:t/text()", namespaces=NS))


OMML_STRUCTS = ("f", "sSub", "sSup", "sSubSup", "d", "func", "acc", "bar", "nary", "rad", "limLow",
                "limUpp", "eqArr", "groupChr", "box", "borderBox", "sPre", "phant")


def _style_omml(omath, size, color, frags):
    """Add a:rPr (size, italics, colour, Cambria Math) to every m:r, as PowerPoint does."""
    sz = str(int(round(size_pt(size) * 100)))
    run_color = {}
    targets = []
    if frags:
        frag_texts = []
        for frag, col in frags:
            try:
                frag_texts.append((frag, _omml_texts(_pandoc_omml(frag)), col))
            except (subprocess.CalledProcessError, RuntimeError) as exc:
                print(f"warning: colour fragment {frag!r} could not be converted to OMML ({exc})")
        for frag, ftxt, col in frag_texts:
            if not ftxt:
                print(f"warning: colour fragment {frag!r} has no OMML text")
                continue
            n_before = len(targets)
            cand = omath.xpath(".//m:sSub|.//m:sSup|.//m:sSubSup|.//m:d|.//m:r", namespaces=NS)
            hit = [c for c in cand if _omml_texts(c) == ftxt]
            if hit:
                targets.append((hit, col))
            else:
                # contiguous run sequence at top level
                kids = list(omath)
                texts = [_omml_texts(k) for k in kids]
                for s in range(len(kids)):
                    acc = ""
                    for e in range(s, len(kids)):
                        acc += texts[e]
                        if acc == ftxt:
                            targets.append((kids[s:e + 1], col))
                            break
                        if not ftxt.startswith(acc):
                            break
            if len(targets) == n_before:
                print(f"warning: colour fragment not matched in OMML: {frag!r}")
        for els, col in targets:
            for e in els:
                for r in ([e] if e.tag == Q("m:r") else e.xpath(".//m:r", namespaces=NS)):
                    run_color[r] = col
    for r in omath.xpath(".//m:r", namespaces=NS):
        for w in r.xpath("./w:rPr", namespaces=NS):
            r.remove(w)
        mrpr = r.find(Q("m:rPr"))
        nor = mrpr is not None and mrpr.find(Q("m:nor")) is not None   # \text{..}: text font
        if nor:
            # CT_RPR: m:nor and (m:scr?, m:sty?) are alternatives; m:nor already means upright text
            for alt in mrpr.findall(Q("m:sty")) + mrpr.findall(Q("m:scr")):
                mrpr.remove(alt)
        t = r.find(Q("m:t"))
        if t is not None and t.text and t.text != t.text.strip():
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        upright = nor or (mrpr is not None and any(s.get(Q("m:val")) in ("p", "b")
                                                   for s in mrpr.findall(Q("m:sty"))))
        bold = mrpr is not None and any(s.get(Q("m:val")) in ("b", "bi") for s in mrpr.findall(Q("m:sty")))
        rpr = etree.Element(_a("rPr"), lang="en-US", sz=sz)
        rpr.set("i", "0" if upright else "1")
        if bold:
            rpr.set("b", "1")
        col = run_color.get(r, color or BLACK)
        _srgb(rpr, col)
        if nor:
            for tag in ("latin", "ea", "cs"):
                etree.SubElement(rpr, _a(tag), typeface=TEXT_FONT)
        else:
            etree.SubElement(rpr, _a("latin"), typeface=MATH_FONT, panose="02040503050406030204",
                             pitchFamily="18", charset="0")
            etree.SubElement(rpr, _a("ea"), typeface=MATH_FONT)
            etree.SubElement(rpr, _a("cs"), typeface=MATH_FONT)
        if mrpr is not None:
            mrpr.addnext(rpr)
        else:
            r.insert(0, rpr)
    # Structure properties carry m:ctrlPr/a:rPr, as PowerPoint writes them, so fraction bars,
    # scripts and text typed into a slot take the equation's size and colour when edited.
    for st in list(omath.iter(*(Q("m:" + t) for t in OMML_STRUCTS))):
        first = st.find(".//" + Q("m:r") + "/" + _a("rPr"))
        if first is None:
            continue
        pr_tag = st.tag + "Pr"
        pr = st.find(pr_tag)
        if pr is None:
            pr = etree.Element(pr_tag)
            st.insert(0, pr)
        for old in pr.findall(Q("m:ctrlPr")):
            pr.remove(old)
        rpr = copy.deepcopy(first)
        rpr.set("i", "1")
        # colour of the structure (fraction bar, fence): the runs' colour when they all share
        # one, else the equation colour (a fraction whose numerator starts with c_H stays black)
        cols = set(st.xpath(".//m:r/a:rPr/a:solidFill/a:srgbClr/@val", namespaces=NS))
        for f in rpr.findall(_a("solidFill")):
            rpr.remove(f)
        fill = _srgb(rpr, cols.pop() if len(cols) == 1 else (color or BLACK))
        rpr.remove(fill)
        rpr.insert(0, fill)
        for tag in ("latin", "ea", "cs"):
            for f in rpr.findall(_a(tag)):
                rpr.remove(f)
        etree.SubElement(rpr, _a("latin"), typeface=MATH_FONT, panose="02040503050406030204",
                         pitchFamily="18", charset="0")
        etree.SubElement(rpr, _a("ea"), typeface=MATH_FONT)
        etree.SubElement(rpr, _a("cs"), typeface=MATH_FONT)
        etree.SubElement(pr, Q("m:ctrlPr")).append(rpr)


_RECIPE: list = []


def _eq_recipe() -> str:
    """Hash of everything besides the snippet that shapes an equation: preamble, OMML styling
    code and the pandoc version, so a change to any of them invalidates the cache."""
    if not _RECIPE:
        ver = subprocess.run([str(PANDOC), "--version"], capture_output=True, text=True,
                             check=True).stdout.splitlines()[0]
        src = EQ_PREAMBLE + ver + "".join(inspect.getsource(f) for f in (
            _style_omml, _strip_color_macros, _pandoc_omml, compile_equation)) + repr(OMML_STRUCTS)
        _RECIPE.append(hashlib.sha256(src.encode()).hexdigest())
    return _RECIPE[0]


def compile_equation(latex: str, size, color=None) -> dict:
    """Cached: fallback PNG (600 dpi, transparent), natural size in Beamer pt, OMML xml."""
    EQDIR.mkdir(parents=True, exist_ok=True)
    key = hashlib.sha256(json.dumps([EQ_VERSION, _eq_recipe(), latex, _size_bp(size), color])
                         .encode()).hexdigest()[:16]
    meta_p = EQDIR / f"{key}.json"
    png_p = EQDIR / f"{key}.png"
    omml_p = EQDIR / f"{key}.omml.xml"
    if meta_p.exists() and png_p.exists() and omml_p.exists():
        meta = json.loads(meta_p.read_text())
        meta.update(png=str(png_p), omml=omml_p.read_bytes())
        return meta
    import pymupdf
    s = _size_bp(size)
    body = latex if color is None else r"\textcolor[HTML]{%s}{%s}" % (color, latex)
    tex = EQ_PREAMBLE + r"\fontsize{%.2f}{%.2f}\selectfont$\displaystyle %s$" % (s, 1.25 * s, body) + "\n\\end{document}\n"
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "eq.tex").write_text(tex, encoding="utf-8")
        res = subprocess.run(["xelatex", "-interaction=nonstopmode", "-halt-on-error", "eq.tex"],
                             cwd=td, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"xelatex failed for {latex!r}:\n{res.stdout[-2000:]}")
        shutil.copy(Path(td) / "eq.pdf", EQDIR / f"{key}.pdf")
        (EQDIR / f"{key}.tex").write_text(tex, encoding="utf-8")
    doc = pymupdf.open(EQDIR / f"{key}.pdf")
    page = doc[0]
    w, h = page.rect.width, page.rect.height
    page.get_pixmap(dpi=600, alpha=True).save(str(png_p))
    plain, frags = _strip_color_macros(latex)
    omath = _pandoc_omml(plain)
    _style_omml(omath, size, color, frags)
    para = etree.Element(Q("m:oMathPara"), nsmap={"m": NS["m"]})
    ppr = etree.SubElement(para, Q("m:oMathParaPr"))
    etree.SubElement(ppr, Q("m:jc")).set(Q("m:val"), "left")   # set per placement in add_equation
    para.append(omath)
    omml = etree.tostring(para)
    omml_p.write_bytes(omml)
    meta = {"w": w, "h": h, "latex": latex}
    meta_p.write_text(json.dumps(meta))
    meta.update(png=str(png_p), omml=omml)
    return meta


def add_equation(shapes, el: Eq):
    """Native OMML text box in mc:Choice(a14), picture in mc:Fallback."""
    meta = compile_equation(el.latex, el.size, el.color)
    w, h = meta["w"], meta["h"]
    x = {"l": el.x, "c": el.x - w / 2, "r": el.x - w}[el.anchor]
    pic = shapes.add_picture(meta["png"], E(x), E(el.y), E(w), E(h))
    pic.name = f"{el.name} (picture)"
    pic._element.nvPicPr.cNvPr.set("descr", el.latex)
    tb = shapes.add_textbox(E(x), E(el.y), E(w), E(h))
    tb.name = el.name
    tf = tb.text_frame
    _frame_setup(tf, "m", wrap=False)
    p_el = tf.paragraphs[0]._p
    ppr = p_el.get_or_add_pPr()
    # native math is set in Cambria Math, wider than the Latin Modern fallback: justify it on the
    # anchor so a centred equation overflows symmetrically about the fallback image's centre
    ppr.set("algn", {"l": "l", "c": "ctr", "r": "r"}[el.anchor])
    etree.SubElement(ppr, _a("buNone"))
    a14m = etree.SubElement(p_el, Q("a14:m"), nsmap={"a14": NS["a14"]})
    omml = etree.fromstring(meta["omml"])
    for jc in omml.iter(Q("m:jc")):
        jc.set(Q("m:val"), {"l": "left", "c": "center", "r": "right"}[el.anchor])
    a14m.append(omml)
    # PowerPoint writes an end-of-paragraph run after an equation: text typed after it keeps the size
    etree.SubElement(p_el, _a("endParaRPr"), lang="en-US",
                     sz=str(int(round(size_pt(el.size) * 100))), dirty="0")
    sp_tree = shapes._spTree
    ac = etree.Element(Q("mc:AlternateContent"), nsmap={"mc": NS["mc"]})
    choice = etree.SubElement(ac, Q("mc:Choice"), nsmap={"a14": NS["a14"]})
    choice.set("Requires", "a14")
    fallback = etree.SubElement(ac, Q("mc:Fallback"))
    idx = list(sp_tree).index(pic._element)
    sp_tree.remove(pic._element)
    sp_tree.remove(tb._element)
    choice.append(tb._element)
    fallback.append(pic._element)
    sp_tree.insert(idx, ac)
    return ac


# ----------------------------------------------------------------------------------------------
# Chrome: layouts, title bar, footline, page number, navigation
# ----------------------------------------------------------------------------------------------
def _next_id(sp_tree) -> int:
    ids = [int(v) for v in sp_tree.xpath("//@id") if str(v).isdigit()]
    return max(ids + [1]) + 1


def _layout_shape(sp_tree, name, x, y, w, h, fill=None, prst="rect", text=None, size="tiny",
                  align="c", color=WHITE):
    sp = CT_Shape.new_autoshape_sp(_next_id(sp_tree), name, prst, E(x), E(y), E(w), E(h))
    sp_tree.append(sp)
    sh = Shape(sp, None)
    _set_fill(sh, fill)
    _no_line(sh)
    nvpr = sp.find(qn("p:nvSpPr")).find(qn("p:nvPr"))
    nvpr.set("userDrawn", "1")
    # plain shapes: drop the style block so no theme shadow/outline applies
    style = sp.find(qn("p:style"))
    if style is not None:
        sp.remove(style)
    if text is not None:
        _frame_setup(sh.text_frame, "m")
        fill_text_frame(sh.text_frame, [P(text, align=align, color=color)], size)
    return sh


def _style_placeholder(ph_el, x, y, w, h, size, color, align="l", bold=False, anchor="t", line=None):
    spPr = ph_el.find(qn("p:spPr"))
    for ch in list(spPr):
        spPr.remove(ch)
    xfrm = etree.SubElement(spPr, _a("xfrm"))
    etree.SubElement(xfrm, _a("off"), x=str(int(E(x))), y=str(int(E(y))))
    etree.SubElement(xfrm, _a("ext"), cx=str(int(E(w))), cy=str(int(E(h))))
    txBody = ph_el.find(qn("p:txBody"))
    body_pr = txBody.find(_a("bodyPr"))
    for k in list(body_pr.attrib):
        del body_pr.attrib[k]
    for ch in list(body_pr):
        body_pr.remove(ch)
    body_pr.set("vert", "horz")
    body_pr.set("wrap", "square")
    for ins in ("lIns", "tIns", "rIns", "bIns"):
        body_pr.set(ins, "0")
    body_pr.set("anchor", {"t": "t", "m": "ctr", "b": "b"}[anchor])
    etree.SubElement(body_pr, _a("noAutofit"))
    lst = txBody.find(_a("lstStyle"))
    for ch in list(lst):
        lst.remove(ch)
    l1 = etree.SubElement(lst, _a("lvl1pPr"), marL="0", indent="0",
                          algn={"l": "l", "c": "ctr", "r": "r"}[align])
    if line:
        ln = etree.SubElement(l1, _a("lnSpc"))
        etree.SubElement(ln, _a("spcPct"), val=str(int(line * 100000)))
    etree.SubElement(l1, _a("buNone"))
    d = etree.SubElement(l1, _a("defRPr"), sz=str(int(size_pt(size) * 100)), b="1" if bold else "0")
    _srgb(d, color)
    etree.SubElement(d, _a("latin"), typeface=TEXT_FONT)


def setup_layouts(prs):
    """Three layouts: 'Madrid Title', 'Madrid Frame' (title bar + footline), 'Madrid Plain'."""
    layouts = list(prs.slide_layouts)
    title_l, frame_l, plain_l = layouts[0], layouts[5], layouts[1]
    for lay in layouts:
        if lay not in (title_l, frame_l, plain_l):
            prs.slide_layouts.remove(lay)

    def drop_ph(lay, keep_types):
        tree = lay.shapes._spTree
        for ph in list(lay.placeholders):
            if ph.placeholder_format.type not in keep_types:
                tree.remove(ph._element)

    from pptx.enum.shapes import PP_PLACEHOLDER as PH
    master = prs.slide_master._element          # template bullets declare Arial: use Calibri
    for bf in master.iter(_a("buFont")):
        for k in list(bf.attrib):
            del bf.attrib[k]
        bf.set("typeface", TEXT_FONT)
    # Madrid Frame
    frame_l._element.cSld.set("name", "Madrid Frame")
    drop_ph(frame_l, {PH.TITLE})
    tree = frame_l.shapes._spTree
    title_ph = frame_l.placeholders[0]._element
    bar = _layout_shape(tree, "Title bar", 0, 0, PAGE_W, TITLE_BAR_H, fill=STRUCT)
    tree.remove(bar._element)
    title_ph.addprevious(bar._element)
    _style_placeholder(title_ph, 8.5, 7.2, PAGE_W - 17, 17.5, "Large", WHITE, anchor="t")
    seg_w = PAGE_W / 3
    for k, (col, txt) in enumerate(zip(FOOT, ("Austin Li", "Competition Creates Competition", None))):
        _layout_shape(tree, f"Footline {k + 1}", k * seg_w, FOOT_Y, seg_w, FOOT_H, fill=col,
                      text=txt, size="tiny")
    # Madrid Title
    title_l._element.cSld.set("name", "Madrid Title")
    drop_ph(title_l, {PH.CENTER_TITLE, PH.SUBTITLE})
    tree = title_l.shapes._spTree
    box = _layout_shape(tree, "Title box", 6.91, 55.05, 439.73, 57.89, fill=STRUCT, prst="roundRect")
    box.adjustments[0] = 4.0 / 57.89
    spPr = box._element.spPr
    eff = etree.SubElement(spPr, _a("effectLst"))
    sh = etree.SubElement(eff, _a("outerShdw"), blurRad=str(int(E(3.0))), dist=str(int(E(3.2))),
                          dir="2700000", algn="tl", rotWithShape="0")
    clr = etree.SubElement(sh, _a("srgbClr"), val="000000")
    etree.SubElement(clr, _a("alpha"), val="45000")
    tree.remove(box._element)
    first_ph = title_l.placeholders[0]._element
    first_ph.addprevious(box._element)
    for ph in title_l.placeholders:
        if ph.placeholder_format.type == PH.CENTER_TITLE:
            _style_placeholder(ph._element, 12, 58, PAGE_W - 24, 52, "Large", WHITE, align="c",
                               anchor="m", line=1.13)
        else:
            _style_placeholder(ph._element, 12, 128.5, PAGE_W - 24, 18, "normal", BLACK, align="c")
    # Madrid Plain (appendix divider)
    plain_l._element.cSld.set("name", "Madrid Plain")
    drop_ph(plain_l, {PH.TITLE})
    _style_placeholder(plain_l.placeholders[0]._element, 12, 81.8, PAGE_W - 24, 55, "Huge", BLACK,
                       align="c", bold=True, anchor="m")
    return {"title": title_l, "frame": frame_l, "divider": plain_l}


_PLAIN_ITALIC = {_italic(c): c for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"}


def set_title(slide, markup: str, size="Large", color=WHITE, bold=False, align="l", line=None):
    """Title placeholder. Inline math is written as ordinary italic letters in the text font (the
    subscript stays a baseline-shifted run), so the outline and navigator read plain 'r1' rather
    than Unicode math alphanumerics."""
    ph = slide.shapes.title
    fill_text_frame(ph.text_frame, [P(markup, color=color, bold=bold, align=align, line=line)], size)
    for r in ph._element.iter(_a("r")):
        rpr, t = r.find(_a("rPr")), r.find(_a("t"))
        if rpr is None or t is None or rpr.find(_a("latin")).get("typeface") != MATH_FONT:
            continue
        t.text = "".join(_PLAIN_ITALIC.get(ch, ch) for ch in t.text)
        if any(ch.isalpha() for ch in t.text):
            rpr.set("i", "1")
        for tag in ("latin", "ea", "cs"):
            rpr.find(_a(tag)).set("typeface", TEXT_FONT)
    return ph


def add_subtitle(shapes, markup: str):
    """Subtitle band: extends the layout's title bar to Madrid's two-line height."""
    sh = shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, E(TITLE_BAR_H), E(PAGE_W), E(SUBTITLE_BAR_H - TITLE_BAR_H))
    sh.name = "Subtitle"
    _set_fill(sh, STRUCT)
    _no_line(sh)
    _no_shadow(sh)
    _frame_setup(sh.text_frame, "t", insets=(8.5, 0, 8.5, 0))
    fill_text_frame(sh.text_frame, [P(markup, color=WHITE)], "footnote")
    return sh


def add_page_number(shapes, text: str):
    tb = shapes.add_textbox(E(2 * PAGE_W / 3), E(FOOT_Y), E(PAGE_W / 3 - 5.5), E(FOOT_H))
    tb.name = "Frame number"
    _frame_setup(tb.text_frame, "m")
    fill_text_frame(tb.text_frame, [P(text, align="r", color=WHITE)], "tiny")
    return tb


def _button(shapes, label: str, x_right: float, back=False):
    """Beamer \\beamergotobutton / \\beamerreturnbutton: blue rounded pill, small triangle, white text."""
    tw = text_width(label, SIZES["tiny"])
    w = tw + 16.0          # Beamer's pill padding; Calibri sets the label ~8% narrower than LM Sans
    x = x_right - w
    sh = shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, E(x), E(NAV_Y), E(w), E(NAV_H))
    sh.name = f"Nav: {label}"
    _set_fill(sh, STRUCT)
    _set_line(sh, STRUCT, 0.8)
    sh.adjustments[0] = 0.5    # Beamer's pill: corner radius half the height
    _no_shadow(sh)
    _frame_setup(sh.text_frame, "m", wrap=False, insets=(4.4, 0, 3.2, 0))
    fill_text_frame(sh.text_frame, [P("\u2009" + label, color=WHITE)], "tiny")
    para = sh.text_frame.paragraphs[0]
    tri = etree.Element(_a("r"))
    rpr = etree.SubElement(tri, _a("rPr"), lang="en-US", sz=str(int(size_pt("tiny") * 60)), dirty="0")
    _srgb(rpr, WHITE)
    for tag in ("latin", "ea", "cs"):
        etree.SubElement(rpr, _a(tag), typeface=TEXT_FONT)
    etree.SubElement(tri, _a("t")).text = "\u25c4" if back else "\u25ba"
    para._p.find(_a("r")).addprevious(tri)
    return sh, x


def add_nav_buttons(shapes, nav: list, back: str | None):
    """Right-aligned button row; returns [(shape, target)] for later link resolution."""
    out = []
    items = list(nav) + ([("Back", back, True)] if back else [])
    x_right = NAV_RIGHT
    for it in reversed(items):
        label, target = it[0], it[1]
        is_back = len(it) > 2
        sh, x = _button(shapes, label, x_right, back=is_back)
        out.append((sh, target))
        x_right = x - NAV_GAP
    return out


# ----------------------------------------------------------------------------------------------
# talk.tex frame index and script.tex notes
# ----------------------------------------------------------------------------------------------
def frame_index() -> tuple[list[tuple[str, str]], dict]:
    """[(label, title)] in deck order, and {hypertarget name: label}."""
    tex = TALK_TEX.read_text(encoding="utf-8")
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    frames, targets = [], {}
    for m in re.finditer(r"\\begin\{frame\}(\[[^\]]*\])?", tex):
        opts = m.group(1) or ""
        lab = re.search(r"label=([A-Za-z0-9]+)", opts)
        j = m.end()
        title = ""
        if j < len(tex) and tex[j] == "{":
            title, j = _read_group(tex, j)
        end = tex.find("\\end{frame}", j)
        body = tex[j:end]
        if lab:
            frames.append((lab.group(1), title))
            for t in re.findall(r"\\hypertarget\{([^}]*)\}", body):
                targets[t] = lab.group(1)
    return frames, targets


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("$", "")).strip()


def latex_to_plain(s: str) -> str:
    # LaTeX comment semantics: a comment eats its newline and the next line's leading blanks,
    # so a "% source:" line inside a paragraph does not split it; blank lines stay breaks
    s = re.sub(r"(?<!\\)%[^\n]*\n[ \t]*(?=\S)", "", s)
    s = re.sub(r"(?<!\\)%[^\n]*", "", s)
    s = s.replace("\\PaperTitle", "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders")
    s = s.replace("\\PaperShortTitle", "Competition Creates Competition")
    s = re.sub(r"\\Pause(\{\})?", "[pause]", s)
    s = re.sub(r"\\Advance(\{\})?", "[advance]", s)

    s = re.sub(r"\\Cue\{", lambda m: "\n\nLive cue: {", s)

    def math(m):
        t = m.group(1)
        for k, v in {"\\Delta": "Δ", "\\ell": "ℓ", "\\rho": "ρ", "\\theta": "θ", "\\mu": "μ",
                     "\\tau": "τ", "\\eta": "η", "\\le": "≤", "\\ge": "≥", "\\to": "→", "\\in": "∈",
                     "\\approx": "≈", "\\times": "×", "\\infty": "∞", "\\,": " ", "\\ ": " "}.items():
            t = t.replace(k, v)
        t = re.sub(r"_\{?([0-9])\}?", lambda mm: mm.group(1).translate(SUB_DIGITS), t)
        t = re.sub(r"_\{([^}]*)\}", r"\1", t)
        t = t.replace("_", "").replace("{", "").replace("}", "")
        return t
    s = re.sub(r"\$([^$]*)\$", math, s)
    s = s.replace("---", "—").replace("--", "–").replace("``", "“").replace("''", "”")
    s = s.replace("~", " ").replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")
    s = re.sub(r"\\[,;: ]", " ", s)
    for _ in range(4):
        s = re.sub(r"\\[A-Za-z]+\*?(\[[^\]]*\])?\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\\[A-Za-z]+\*?", "", s)
    s = s.replace("{", "").replace("}", "")
    paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", s)]
    return "\n".join(p for p in paras if p)


def script_notes() -> dict:
    """{frame label: notes text} from script.tex."""
    tex = SCRIPT_TEX.read_text(encoding="utf-8")
    body = tex[tex.find("\\begin{document}"):]
    frames, _ = frame_index()
    notes, used = {}, set()
    i = 0
    while True:
        m = re.search(r"\\script(frame|opening)\{", body[i:])
        if not m:
            break
        j = i + m.start() + len(m.group(0)) - 1
        if m.group(1) == "opening":
            timing, j = _read_group(body, j)
            text, j = _read_group(body, j)
            notes.setdefault("F0", f"Opening ({latex_to_plain(timing)})\n" + latex_to_plain(text))
            i = j
            continue
        title, j = _read_group(body, j)
        timing, j = _read_group(body, j)
        text, j = _read_group(body, j)
        i = j
        am = re.search(r"\((A\d+)\)", timing)
        label = None
        if am:
            label = am.group(1)
        else:
            for lab, t in frames:
                if lab not in used and _norm(t) == _norm(title):
                    label = lab
                    break
        if label is None:
            print(f"warning: script block without a frame: {title!r}")
            continue
        used.add(label)
        notes[label] = f"{latex_to_plain(title)} ({latex_to_plain(timing)})\n" + latex_to_plain(text)
    # Standing Q&A answers keyed to a backup: \textit{question} (... A<n> ...)[: answer]
    sec = body.find("\\section*{Standing Q")
    if sec >= 0:
        stance = re.sub(r"(?<!\\)%[^\n]*", "", body[sec:body.find("\\end{document}")])
        for m in re.finditer(r"\\textit\{", stance):
            question, j = _read_group(stance, m.end() - 1)
            pm = re.match(r"\s*\(([^()]*)\)", stance[j:])
            if not pm or not re.search(r"\bA\d+\b", pm.group(1)):
                continue
            j += pm.end()
            nxt = re.search(r"\\textit\{|\n\s*\n", stance[j:])
            answer = stance[j:j + nxt.start() if nxt else len(stance)].strip().lstrip(":").strip()
            if answer in ("", "."):
                answer = re.sub(r"^.*?\bA\d+\b\s*:?\s*", "", pm.group(1))
            answer = latex_to_plain(answer)
            answer = answer[:1].upper() + answer[1:]
            if answer and answer[-1] not in ".?!":
                answer += "."
            for lab in dict.fromkeys(re.findall(r"\bA\d+\b", pm.group(1))):
                qa = f"Q: {latex_to_plain(question)}\nA: {answer}"
                notes[lab] = (notes[lab] + "\n\n" + qa) if lab in notes else ("Standing Q&A\n" + qa)
    return notes


def set_notes(slide, text: str):
    tf = slide.notes_slide.notes_text_frame
    tf.text = text


# ----------------------------------------------------------------------------------------------
# Build
# ----------------------------------------------------------------------------------------------
def add_element(slide, el):
    shapes = slide.shapes
    if isinstance(el, Text):
        return add_text(shapes, el)
    if isinstance(el, Table):
        return add_table(shapes, el)
    if isinstance(el, Eq):
        return add_equation(shapes, el)
    if isinstance(el, Figure):
        return add_figure(shapes, slide.part, el)
    if isinstance(el, Flow):
        return add_flow(shapes, el)
    if isinstance(el, ResultBox):
        return add_resultbox(shapes, el)
    if isinstance(el, Rect):
        return add_rect(shapes, el)
    if callable(el):
        return el(slide)
    raise TypeError(f"unknown element {el!r}")


def load_slides() -> list:
    sys.path.insert(0, str(HERE))
    slides = list(importlib.import_module("content_main").SLIDES)
    # ---- HOOK: appendix pages 19-48 -----------------------------------------------------------
    # content_appendix.py (same API, exports SLIDES starting with the 'Appendix' divider) is
    # appended automatically once it exists; nav targets into the appendix then resolve.
    if (HERE / "content_appendix.py").exists():
        slides += list(importlib.import_module("content_appendix").SLIDES)
    # --------------------------------------------------------------------------------------------
    return slides


def renumber_ids(slide):
    """Unique, sequential shape ids per slide; connector references are remapped."""
    tree = slide.shapes._spTree
    mapping, nxt = {}, 2
    for el in tree.iter():
        if el.tag in (qn("p:cNvPr"),):
            old = el.get("id")
            mapping.setdefault(old, str(nxt))
            el.set("id", str(nxt))
            nxt += 1
    for tag in ("a:stCxn", "a:endCxn"):
        for el in tree.iter(qn(tag)):
            if el.get("id") in mapping:
                el.set("id", mapping[el.get("id")])


DOC_TITLE = "Competition Creates Competition: Stock Prices and the Discovery of Takeover Bidders"
DOC_AUTHOR = "Austin Li"
DOC_DATE = datetime.datetime(2026, 9, 29, 12, 0, 0)   # fixed, so rebuilds carry identical metadata


def finish_package(prs):
    """Package-level parts PowerPoint writes but python-pptx leaves as template boilerplate."""
    # p:notesMasterIdLst (after p:sldMasterIdLst), which consumers use to find the notes master
    pres = prs.part._element
    for old in pres.findall(qn("p:notesMasterIdLst")):
        pres.remove(old)
    rid = next((r.rId for r in prs.part.rels.values() if r.reltype == RT.NOTES_MASTER), None)
    if rid:
        lst = etree.Element(qn("p:notesMasterIdLst"))
        etree.SubElement(lst, qn("p:notesMasterId")).set(qn("r:id"), rid)
        pres.find(qn("p:sldMasterIdLst")).addnext(lst)
    # core properties
    cp = prs.core_properties
    cp.title, cp.author, cp.last_modified_by = DOC_TITLE, DOC_AUTHOR, DOC_AUTHOR
    cp.subject, cp.keywords, cp.comments = "Conference talk", "", ""
    cp.revision = 1
    cp.created = cp.modified = DOC_DATE
    # app properties: slide and notes counts, custom (widescreen) format
    n_notes = sum(1 for sl in prs.slides if sl.has_notes_slide)
    pkg = prs.part.package
    for rel in list(pkg._rels.values()):
        if rel.reltype == RT.THUMBNAIL:          # generic python-pptx thumbnail: drop it
            pkg.drop_rel(rel.rId)
        elif rel.reltype == RT.EXTENDED_PROPERTIES:
            rel.target_part._blob = (
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/'
                'extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/'
                '2006/docPropsVTypes"><TotalTime>0</TotalTime><Application>python-pptx '
                '(talk/pptx/build_pptx.py)</Application><PresentationFormat>Custom'
                f'</PresentationFormat><Slides>{len(prs.slides)}</Slides><Notes>{n_notes}</Notes>'
                '<HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop>'
                '<LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc>'
                '<HyperlinksChanged>false</HyperlinksChanged></Properties>').encode()


def build(out: Path = OUT) -> Path:
    slides_spec = load_slides()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    prs.part._element.sldSz.attrib.pop("type", None)   # widescreen: PowerPoint writes no type
    layouts = setup_layouts(prs)
    frames, targets = frame_index()
    labels = {lab for lab, _ in frames}
    notes = script_notes()
    by_label, pending = {}, []
    for spec in slides_spec:
        layout = layouts[spec.kind]
        slide = prs.slides.add_slide(layout)
        by_label[spec.label] = slide
        if spec.kind == "title":
            set_title(slide, spec.title, "Large", WHITE, align="c", line=1.13)
            for ph in list(slide.placeholders):
                if ph.placeholder_format.idx == 1:
                    fill_text_frame(ph.text_frame, [P(spec.subtitle or "", align="c")], "normal")
        elif spec.kind == "divider":
            set_title(slide, spec.title, "Huge", BLACK, bold=True, align="c")
        else:
            set_title(slide, spec.title)
            if spec.subtitle:
                add_subtitle(slide.shapes, spec.subtitle)
        for el in spec.body:
            add_element(slide, el)
        if spec.page:
            add_page_number(slide.shapes, spec.page)
        pending += [(spec.label, sh, tgt) for sh, tgt in add_nav_buttons(slide.shapes, spec.nav, spec.back)]
        text = spec.notes if spec.notes is not None else notes.get(spec.label)
        if text:
            set_notes(slide, text)
        # remove empty placeholders
        for ph in list(slide.placeholders):
            if not ph.has_text_frame or not ph.text_frame.text.strip():
                ph._element.getparent().remove(ph._element)
        if spec.label not in labels and spec.kind != "divider":
            print(f"warning: slide label {spec.label} is not a frame label in talk.tex")
    unresolved = []
    for src, sh, tgt in pending:
        lab = targets.get(tgt, tgt)
        if lab in by_label:
            sh.click_action.target_slide = by_label[lab]
        else:
            unresolved.append((src, tgt))
    # Madrid footline: the author and title segments link to the title page on every counted page
    for sh in layouts["frame"].shapes:
        if sh.name in ("Footline 1", "Footline 2"):
            sh.click_action.target_slide = by_label["F0"]
    for slide in prs.slides:
        renumber_ids(slide)
    finish_package(prs)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"wrote {out} ({len(prs.slides)} slides)")
    if unresolved:
        print(f"nav targets not yet in the deck ({len(unresolved)}): " +
              ", ".join(f"{s}->{t}" for s, t in unresolved))
    return out


def main():
    build()


if __name__ == "__main__":
    # Run under the module name 'build_pptx' so content modules share these record classes.
    sys.path.insert(0, str(HERE))
    importlib.import_module("build_pptx").main()
