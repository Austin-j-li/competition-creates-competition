"""Figures of the order-slot manuscript (workstream F).

Writes beliefs.pdf, coexistence.pdf, research.pdf and the three slide versions
into slot/manuscript/figures/, a run log (run_log.txt) and PNG previews (png/).

Every curve comes from a closed form of the proof packages at calibration B:
  P1_core: tau, Delta, J, the thresholds r_A, r_F, r_N, r_J, r_S, r_C and the entry of each branch
           (Proposition 3, Step 7);
  P3_research: the research polynomial F_r, the recruitment intensity, r_R, r_R-bar, r_U.
Boundaries use mpmath at 40 digits; the plotted curves use floating point.
The log prints each boundary beside the registry display value. Nothing is asserted.

Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py
"""
import csv
import hashlib
import math
import pathlib
import subprocess

import numpy as np
from mpmath import mp, mpf, sqrt as mpsqrt

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.gridspec import GridSpec

HERE = pathlib.Path(__file__).resolve().parent
TEAM = HERE.parents[1]
ROOT = TEAM.parents[1]
OUT = ROOT / "slot" / "manuscript" / "figures"
PNG = HERE / "png"
REGISTRY = TEAM / "registry" / "registry.csv"
LOGFILE = HERE / "run_log.txt"
FIRA = pathlib.Path("/home/uctpiaj/work/texlive/2026/texmf-dist/fonts/opentype/public/fira")

mp.dps = 40
LOG = []


def log(*args):
    line = " ".join(str(a) for a in args)
    LOG.append(line)
    print(line)


# ============================================================ number layer
class Prm:
    """Benchmark primitives of calibration B in one number type (mpmath or float)."""

    def __init__(self, num, euler, sqrt):
        self.sqrt = sqrt
        self.h, self.ell, self.p = num(10), num(1), num(1) / 2
        self.rho, self.cH, self.k = num(1) / 4, num(6), num(1) / 50
        self.beta = num(294655) / num(1000000)
        self.a = num(1) / 40
        self.e = euler
        self.u = euler - 1                                   # 1 + u = e
        self.lam = self.u * self.beta / (1 + self.u * self.beta)   # presence probability, also the cap
        self.b = self.beta / (1 + self.u * self.beta)        # b = (1 - lambda) beta
        self.M = euler / (1 + euler)                         # M(1/2)
        self.m = 1 / (1 + euler)                             # m(1/2)


PM = Prm(mpf, mp.e, mpsqrt)
PF = Prm(float, math.e, math.sqrt)


def gH(P, r):
    return P.h - r / 2 - P.p * P.p / (2 * r)


def gL(P, r):
    return (P.ell * P.ell - P.p * P.p) / (2 * r)


def Delta(P, r):
    return (r - P.ell) ** 2 / (2 * r)


def tau(P, r):
    return (P.cH - gL(P, r)) / (gH(P, r) - gL(P, r))


def J(P, r):
    return Delta(P, r) * (1 - tau(P, r))


def frak(P, d):
    """Root above ell of Delta(r) = d."""
    return P.ell + d + P.sqrt(d * d + 2 * P.ell * d)


def lamE(P, r):
    t = tau(P, r)
    return P.beta * (2 * t - 1) / (P.beta + (1 - 2 * P.beta) * (1 - t))


def phi(P, r):
    return Delta(P, r) * (1 - tau(P, r)) - P.k - 2 * P.a * lamE(P, r)


def lamR(P, r):
    """Positive root of the research polynomial F_r (P3, equation (F)); r with Delta > 2k."""
    D = Delta(P, r)
    A = 2 * P.a * (1 - 2 * P.beta)
    Bc = 4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * D
    C = P.beta * (2 * P.k - D)
    return (-Bc + np.sqrt(Bc * Bc - 4 * A * C)) / (2 * A)


def ent_branch_R(P, r):
    """Entry on the mixed purchase R (P1, Proposition 3, Step 7)."""
    return P.rho + (1 - P.rho) * P.b * Delta(P, r) / (2 * P.k)


def ent_plateau(P):
    return P.rho + (1 - P.rho) * (P.b + P.lam / 2)


def ent_threshold(P, r):
    """Entry on the threshold branch T under rule CM (P1, Step 7)."""
    D, t = Delta(P, r), tau(P, r)
    return P.rho + (P.b / 2) * (P.k - P.rho * J(P, r)) / (D * (1 - t) ** 2)


def bisect(f, lo, hi, n=160):
    lo, hi = mpf(lo), mpf(hi)
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def boundaries():
    P = PM
    B = {}
    B["rA"] = bisect(lambda r: J(P, r) - P.k, mpf("1.3"), mpf("1.6"))
    B["rF"] = frak(P, P.k / P.m)
    B["rN"] = frak(P, 2 * P.k / P.rho)
    B["rJ"] = bisect(lambda r: P.rho * J(P, r) - P.k, mpf("1.8"), mpf("2.2"))
    B["rS"] = frak(P, P.k / (P.rho * P.m))
    Mh = P.M * P.h - P.cH
    B["rC"] = (Mh + mpsqrt(Mh * Mh + P.M * ((1 - P.M) * P.ell ** 2 - P.p ** 2))) / P.M
    B["rR"] = bisect(lambda r: phi(P, r), mpf("1.4"), mpf("1.7"))
    B["rRbar"] = frak(P, (2 * P.a * P.lam + P.k) / P.m)
    B["rU"] = frak(P, (P.k + P.a * P.lam) / (P.rho * P.m))
    return B


BD = boundaries()
BF = {k_: float(v) for k_, v in BD.items()}
R0, R1, R2 = 1.2, 3.0, 3.6
RHO = 0.25
ENT1 = float(ent_plateau(PM))
CAP = float(PM.lam)
NODES = [1.55, 1.60, 1.65]


# ============================================================ registry comparison
def read_registry():
    rows = {}
    if REGISTRY.exists():
        with REGISTRY.open(newline="") as fh:
            for row in csv.DictReader(fh):
                rows[row["key"]] = row["display"]
    return rows


REG = read_registry()


def d6(x):
    return f"{float(x):.6f}"


def same(comp, reg):
    """True when the registry display equals the computed string as a number."""
    try:
        from fractions import Fraction
        return abs(float(Fraction(reg)) - float(comp)) < 5e-7
    except (ValueError, ZeroDivisionError):
        return False


def regd(key, computed):
    """Registry display string for a key; falls back to the computed string."""
    return REG.get(key, computed)


# ============================================================ style
NAVY, BRICK, GREY, INK = "#1f3a6e", "#b4472e", "#6c6c6c", "#222222"
BAND_BLUE, BAND_GREY = "#e5eaf4", "#ececec"
DASH_R = (0, (5.0, 2.2))
DASH_Q = (0, (6.0, 2.0, 1.5, 2.0))
DASH_T = (0, (3.0, 2.0))


def fira_truetype(src, dst):
    """Convert the CFF outlines of an OpenType font to TrueType outlines (fontTools recipe), so that the
    PDF embeds a plain TrueType font (Type 42). Needed because matplotlib embeds CFF fonts in a wrapper that
    some PDF readers reject."""
    from fontTools.ttLib import TTFont, newTable
    from fontTools.pens.cu2quPen import Cu2QuPen
    from fontTools.pens.ttGlyphPen import TTGlyphPen

    font = TTFont(str(src))
    order = font.getGlyphOrder()
    gset = font.getGlyphSet()
    glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = {}
    for name in order:
        pen = TTGlyphPen(gset)
        gset[name].draw(Cu2QuPen(pen, 1.0, reverse_direction=True))
        glyf.glyphs[name] = pen.glyph()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]
    glyf.compile(font)
    hmtx = font["hmtx"]
    for name, glyph in glyf.glyphs.items():
        if hasattr(glyph, "xMin"):
            hmtx[name] = (hmtx[name][0], glyph.xMin)
    maxp = font["maxp"] = newTable("maxp")
    maxp.tableVersion = 0x00010000
    maxp.maxZones, maxp.maxTwilightPoints, maxp.maxStorage = 1, 0, 0
    maxp.maxFunctionDefs, maxp.maxInstructionDefs, maxp.maxStackElements = 0, 0, 0
    maxp.maxSizeOfInstructions, maxp.maxComponentElements = 0, max(
        (len(g.components) if hasattr(g, "components") else 0) for g in glyf.glyphs.values())
    maxp.maxPoints = maxp.maxContours = maxp.maxCompositePoints = maxp.maxCompositeContours = 0
    maxp.maxComponentDepth = 0
    maxp.numGlyphs = len(order)
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = order
    for rec in list(font["name"].names):
        if rec.nameID in (1, 4, 16):
            rec.string = "Fira Sans TT" if rec.nameID != 4 else "Fira Sans TT Regular"
    font.sfntVersion = "\000\001\000\000"
    font.save(str(dst))


def register_fira():
    src = FIRA / "FiraSans-Regular.otf"
    dst = HERE / ".mpl" / "FiraSans-Regular-tt.ttf"
    if not src.exists():
        return False
    if not dst.exists():
        dst.parent.mkdir(exist_ok=True)
        fira_truetype(src, dst)
    fm.fontManager.addfont(str(dst))
    return True


FIRA_OK = register_fira()


class Style:
    def __init__(self, talk):
        self.talk = talk
        if talk:
            self.fs, self.fl, self.ft, self.fm_, self.fn = 11.0, 12.0, 10.5, 10.0, 10.5
            self.lw, self.lwt, self.lwd, self.ms = 2.9, 1.3, 1.1, 6.5
            self.family = "Fira Sans TT" if FIRA_OK else "DejaVu Sans"
            self.math = "cm"
        else:
            self.fs, self.fl, self.ft, self.fm_, self.fn = 8.0, 9.0, 8.0, 8.0, 7.5
            self.lw, self.lwt, self.lwd, self.ms = 1.9, 0.8, 0.7, 4.6
            self.family = "STIXGeneral"
            self.math = "stix"

    def apply(self):
        plt.rcdefaults()
        plt.rcParams.update({
            "pdf.fonttype": 42, "ps.fonttype": 42,
            "font.family": "serif" if not self.talk else "sans-serif",
            "font.serif": ["STIXGeneral"], "font.sans-serif": [self.family, "DejaVu Sans"],
            "mathtext.fontset": self.math,
            "font.size": self.fs, "axes.labelsize": self.fl,
            "xtick.labelsize": self.ft, "ytick.labelsize": self.ft,
            "axes.linewidth": 0.8 if not self.talk else 1.1,
            "xtick.major.width": 0.8 if not self.talk else 1.1, "ytick.major.width": 0.8 if not self.talk else 1.1,
            "xtick.major.size": 3.0 if not self.talk else 4.0, "ytick.major.size": 3.0 if not self.talk else 4.0,
            "axes.spines.top": False, "axes.spines.right": False,
            "axes.unicode_minus": False, "savefig.dpi": 300,
        })


def panel_label(ax, text, S, dx=-0.085, dy=1.02):
    ax.text(dx, dy, text, transform=ax.transAxes, fontsize=S.fl, ha="left", va="bottom")


def mark_x(ax, x, tex, S, level=0, value=None, color="0.3", lvl=0.075, full=True):
    """Dotted vertical line with a label above the axes (two lines when a value is given)."""
    y = 1.015 + level * lvl
    ax.axvline(x, 0, 1, color=color, ls=":", lw=S.lwd, zorder=1)
    if level > 0:
        ax.plot([x, x], [1.0, y], transform=ax.get_xaxis_transform(), color=color, ls=":", lw=S.lwd,
                clip_on=False, zorder=1)
    txt = tex if value is None else tex + "\n" + value
    ax.text(x, y, txt, transform=ax.get_xaxis_transform(), ha="center", va="bottom", fontsize=S.fm_,
            color=color, linespacing=1.0, clip_on=False)


def lab(ax, x, y, s, S, color=INK, ha="left", va="center", size=None, **kw):
    ax.text(x, y, s, color=color, ha=ha, va=va, fontsize=size or S.fn, **kw)


def dot(ax, x, y, S, color="k", open_=False, size=None, z=6):
    ax.plot([x], [y], "o", ms=size or S.ms, mfc="white" if open_ else color, mec=color, mew=1.0, clip_on=False,
            zorder=z, ls="none")


def save(fig, name):
    path = OUT / name
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None, "Creator": "make_figures.py"})
    plt.close(fig)
    return path


# ============================================================ figure 1: beliefs
def fig_beliefs(talk):
    S = Style(talk)
    S.apply()
    size = (7.4, 3.1) if talk else (6.5, 3.05)
    fig = plt.figure(figsize=size)
    gs = GridSpec(1, 2, width_ratios=[1.75, 1.0], wspace=0.42,
                  left=0.105 if not talk else 0.085, right=0.985, bottom=0.17 if not talk else 0.225,
                  top=0.88 if not talk else 0.83, figure=fig)
    axa, axb = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
    Mv, mv = float(PM.M), float(PM.m)
    rC = BF["rC"]

    # --- (a) tau(r) against r
    rr = np.linspace(R0, R2, 600)
    axa.axhspan(mv, Mv, color=BAND_GREY, lw=0, zorder=0)
    axa.axhline(0.5, color=GREY, ls=(0, (1.5, 2.0)), lw=S.lwt * 1.4, zorder=1)
    axa.axhline(Mv, color=NAVY, ls=(0, (6, 2)), lw=S.lwt * 1.4, zorder=1)
    axa.axhline(mv, color=NAVY, ls=(0, (6, 2)), lw=S.lwt * 1.4, zorder=1)
    axa.plot(rr, tau(PF, rr), color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    for x in (R0, R1, R2):
        axa.axvline(x, color="0.3", ls=":", lw=S.lwd, zorder=1)
        dot(axa, x, float(tau(PF, x)), S, color=BRICK)
    sec = axa.secondary_xaxis("top")
    sec.set_xticks([R0, R1, R2])
    sec.set_xticklabels([r"$r_0$", r"$r_1$", r"$r_2$"], fontsize=S.fm_)
    sec.tick_params(length=2.5, pad=1.5)
    sec.spines["top"].set_visible(False)
    axa.set_xlim(R0, R2)
    axa.set_ylim(0.2, 0.84)
    axa.set_xticks([1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6])
    axa.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    axa.set_xlabel(r"incumbent strength, $r$")
    axa.set_ylabel(r"threshold belief, $\tau(r)$")
    xl = 1.27
    lab(axa, xl, Mv + 0.022, r"top posterior $M(1/2)=%s$" % regd("M_half_B", d6(PM.M)), S, color=NAVY, va="bottom")
    lab(axa, xl, mv + 0.022, r"bottom posterior $m(1/2)=%s$" % regd("m_half_B", d6(PM.m)), S, color=NAVY, va="bottom")
    lab(axa, xl, 0.5 + 0.022, r"prior $1/2$", S, color="0.35", va="bottom")
    lab(axa, 1.9 if not talk else 2.0, 0.60 if not talk else 0.585, r"threshold $\tau(r)$", S, color=BRICK, va="center")
    axa.annotate("", xy=(2.0 if not talk else 2.1, float(tau(PF, 2.0 if not talk else 2.1)) - 0.012),
                 xytext=(2.0 if not talk else 2.1, 0.62 if not talk else 0.605),
                 arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=0, shrinkB=0))
    dot(axa, rC, Mv, S, color="k", open_=True)
    axa.annotate(r"ceiling $r_C$", xy=(rC, Mv), xytext=(3.27, 0.60), fontsize=S.fn,
                 ha="center", va="top", color="k",
                 arrowprops=dict(arrowstyle="-", lw=S.lwt, color="0.3", shrinkA=1, shrinkB=3.5))
    panel_label(axa, "(a)", S, dx=-0.17 if not talk else -0.145, dy=1.075)

    # --- (b) the band for M(1/2)
    r2x = np.linspace(R1, R2, 400)
    t1, t2 = float(tau(PF, R1)), float(tau(PF, R2))
    axb.axhspan(t1, t2, color=BAND_BLUE, lw=0, zorder=0)
    axb.axhline(t1, color=NAVY, lw=S.lwt, zorder=1)
    axb.axhline(t2, color=NAVY, lw=S.lwt, zorder=1)
    axb.axhline(Mv, color=NAVY, ls=(0, (6, 2)), lw=S.lwt * 1.7, zorder=2)
    axb.plot(r2x, tau(PF, r2x), color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    axb.axvline(rC, color="0.3", ls=":", lw=S.lwd, zorder=1)
    dot(axb, rC, Mv, S, color="k", open_=True)
    dot(axb, R1, t1, S, color=BRICK)
    dot(axb, R2, t2, S, color=BRICK)
    axb.set_xlim(R1, R2)
    axb.set_ylim(0.7000, 0.7350)
    axb.set_xticks([3.0, 3.2, 3.4, 3.6])
    axb.set_xticklabels([r"$r_1$", "3.2", "3.4", r"$r_2$"])
    axb.set_yticks([0.700, 0.710, 0.720, 0.730])
    axb.set_xlabel(r"incumbent strength, $r$")
    axb.set_ylabel(r"belief, $\tau(r)$ and $M(1/2)$")
    lab(axb, 3.02, t2 + 0.0010, r"$\tau(r_2)=%s$" % regd("tau_r2", d6(t2)), S, color=NAVY, va="bottom")
    lab(axb, 3.02, Mv - 0.0009, r"$M(1/2)=%s$" % regd("M_half_B", d6(PM.M)), S, color=NAVY, va="top")
    lab(axb, 3.585, t1 + 0.0010, r"$\tau(r_1)=%s$" % regd("tau_r1", d6(t1)), S, color=NAVY, ha="right", va="bottom")
    lab(axb, 3.585, 0.7105 if talk else 0.7095, r"band for $M(1/2)$", S, color=NAVY, ha="right", va="center")
    lab(axb, rC - 0.012, 0.7022, r"$r_C=%s$" % regd("rC_B", d6(rC)), S, color="0.2", ha="right", va="center")
    panel_label(axb, "(b)", S, dx=-0.34 if not talk else -0.36, dy=1.075)
    return fig


# ============================================================ figure 2: coexistence
def draw_branches(ax, S, markers=True):
    """All branches of the benchmark path at prior 1/2, rules IM and C1, and T under CM."""
    rA, rF, rN, rJ, rS, rC = (BF[k_] for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC"))
    lo, hi = ax.get_xlim()

    def mk(x, y, color, open_=False, z=6, size=None):
        if markers and lo <= x <= hi:
            dot(ax, x, y, S, color=color, open_=open_, z=z, size=size)

    # T: threshold branch under rule CM (thin dashed)
    rt = np.linspace(rA, rJ, 300)
    ax.plot(rt, ent_threshold(PF, rt), color="k", ls=DASH_T, lw=S.lwt * 1.15, zorder=3)
    # N: no informed trade, closed at r_N
    ax.plot([R0, rN], [RHO, RHO], color=NAVY, lw=S.lw, solid_capstyle="butt", zorder=4)
    mk(rN, RHO, NAVY)
    # Q: mixed orders at the entry floor, open at both ends
    ax.plot([rN, rJ], [RHO, RHO], color=GREY, ls=DASH_Q, lw=S.lw, zorder=4)
    mk(rN, RHO, GREY, open_=True, z=7)
    mk(rJ, RHO, GREY, open_=True, z=7)
    # R: mixed purchase that recruits, closed at r_A, joins F at r_F
    rr = np.linspace(rA, rF, 200)
    ax.plot(rr, ent_branch_R(PF, rr), color=BRICK, ls=DASH_R, lw=S.lw, zorder=4)
    mk(rA, float(ent_branch_R(PF, rA)), BRICK)
    # F: full purchase, then full trade; entry plateau up to r_C (closed), floor above r_C (open)
    ax.plot([rF, rC], [ENT1, ENT1], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    mk(rF, ENT1, BRICK)
    mk(rC, ENT1, BRICK)
    ax.plot([rC, R2], [RHO, RHO], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    mk(rC, RHO, BRICK, open_=True, z=7)


def fig_coexistence(talk):
    S = Style(talk)
    S.apply()
    rA, rF, rN, rJ, rS, rC = (BF[k_] for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC"))
    ZLO, ZHI = 1.25, 2.35
    ylo, yhi = 0.15, 0.62
    ylob = 0.12
    if talk:
        fig = plt.figure(figsize=(7.6, 3.3))
        axa = fig.add_axes([0.105, 0.335, 0.285, 0.475])
        axb = fig.add_axes([0.53, 0.335, 0.455, 0.475])
    else:
        fig = plt.figure(figsize=(6.5, 5.9))
        axa = fig.add_axes([0.095, 0.675, 0.885, 0.255])
        axb = fig.add_axes([0.095, 0.085, 0.885, 0.40])
    for ax, yl in ((axa, ylo), (axb, ylob)):
        ax.set_ylim(yl, yhi)
        ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6])
        ax.set_xlabel(r"incumbent strength, $r$")
        ax.axvspan(rA, rN, color=BAND_BLUE, lw=0, zorder=0)
    axa.set_ylabel(r"total entry, $E$")
    axb.set_ylabel(r"total entry, $E$") if not talk else None
    axa.set_xlim(R0, R2)
    axb.set_xlim(ZLO, ZHI)
    axa.set_xticks([1.2, 2.0, 2.8, 3.6] if talk else [1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6])
    axb.set_xticks([1.4, 1.6, 1.8, 2.0, 2.2] if not talk else [1.4, 1.8, 2.2])
    draw_branches(axa, S, markers=False)
    draw_branches(axb, S, markers=True)
    dot(axa, rC, ENT1, S, color=BRICK)
    dot(axa, rC, RHO, S, color=BRICK, open_=True, z=7)
    for x in (rA, rN, rC):
        axa.axvline(x, color="0.3", ls=":", lw=S.lwd, zorder=1)
    mark_x(axa, rC, r"$r_C$", S, level=0, lvl=0.1)
    # --- (a): the whole path
    axa.annotate("", xy=(ZLO, 0.585), xytext=(ZHI, 0.585),
                 arrowprops=dict(arrowstyle="<->", lw=S.lwt * 1.2, color="0.35", shrinkA=0, shrinkB=0))
    lab(axa, ZHI + 0.06, 0.585, r"zoom in (b)" if not talk else r"(b)", S, color="0.35", ha="left", va="center")
    lab(axa, 1.27, RHO + 0.025, r"N", S, color=NAVY, va="bottom", size=S.fn + 1)
    lab(axa, 2.85, ENT1 + 0.025, r"F", S, color=BRICK, va="bottom", size=S.fn + 1, ha="center")
    lab(axa, 3.545, RHO + 0.026, r"F above $r_C$", S, color=BRICK, ha="right", va="bottom")
    panel_label(axa, "(a)", S, dx=-0.098 if not talk else -0.30, dy=1.05)
    # --- (b): the zoom with every boundary
    for key, tex, level in (("rA", r"$r_A$", 1), ("rF", r"$r_F$", 0), ("rN", r"$r_N$", 1), ("rJ", r"$r_J$", 0),
                            ("rS", r"$r_S$", 1)):
        mark_x(axb, BF[key], tex, S, level=level, lvl=0.085 if not talk else 0.095)
    panel_label(axb, "(b)", S, dx=-0.098 if not talk else -0.19, dy=1.17 if not talk else 1.05)
    # direct labels (zoom)
    if not talk:
        lab(axb, ZLO + 0.012, RHO - 0.024, r"N: no informed trade", S, color=NAVY, va="top")
        axb.annotate(r"Q: mixed orders at the floor", xy=(1.857, RHO), xytext=(1.857, RHO - 0.05),
                     fontsize=S.fn, color="0.35", ha="center", va="top",
                     arrowprops=dict(arrowstyle="-", lw=S.lwt, color="0.5", shrinkA=0, shrinkB=3))
        axb.annotate(r"R: mixed" "\n" r"purchase" "\n" r"that recruits", xy=(1.428, float(ent_branch_R(PF, 1.428))),
                     xytext=(1.38, 0.47), fontsize=S.fn, color=BRICK, ha="right", va="center",
                     arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=1, shrinkB=2.5))
        axb.annotate(r"T: threshold branch" "\n" r"(rule CM)", xy=(1.62, float(ent_threshold(PF, 1.62))),
                     xytext=(1.74, 0.385), fontsize=S.fn, color="k", ha="left", va="center",
                     arrowprops=dict(arrowstyle="-", lw=S.lwt, color="0.2", shrinkA=1, shrinkB=2.5))
        lab(axb, (rF + rN) / 2, ENT1 + 0.016, r"F: full purchase", S, color=BRICK, ha="center", va="bottom")
        lab(axb, (rJ + rS) / 2, ENT1 + 0.016, r"mixed sales", S, color=BRICK, ha="center", va="bottom")
        lab(axb, (rS + ZHI) / 2, ENT1 + 0.016, r"full trade", S, color=BRICK, ha="center", va="bottom")
        lab(axb, (rA + rN) / 2, ylob + 0.012, r"coexistence", S, color=NAVY, ha="center", va="bottom")
    else:
        lab(axb, ZLO + 0.012, RHO - 0.018, r"N", S, color=NAVY, va="top", size=S.fn + 1)
        lab(axb, 1.857, RHO - 0.02, r"Q", S, color="0.35", va="top", ha="center", size=S.fn + 1)
        lab(axb, 1.38, 0.50, r"R", S, color=BRICK, va="center", ha="right", size=S.fn + 1)
        lab(axb, 1.78, 0.34, r"T", S, color="k", va="center", ha="left", size=S.fn + 1)
        lab(axb, 2.25, ENT1 + 0.02, r"F", S, color=BRICK, ha="center", va="bottom", size=S.fn + 1)
        lab(axb, (rA + rN) / 2, ylob + 0.012, r"coexistence", S, color=NAVY, ha="center", va="bottom")
        # key below the panels
        from matplotlib.lines import Line2D
        hs = [Line2D([], [], color=NAVY, lw=S.lw), Line2D([], [], color=BRICK, ls=DASH_R, lw=S.lw),
              Line2D([], [], color=BRICK, lw=S.lw), Line2D([], [], color=GREY, ls=DASH_Q, lw=S.lw),
              Line2D([], [], color="k", ls=DASH_T, lw=S.lwt * 1.15)]
        ls_ = [r"N no trade", r"R mixed purchase", r"F full purchase", r"Q mixed orders", r"T threshold (CM)"]
        fig.legend(hs, ls_, loc="lower center", ncol=5, frameon=False, fontsize=S.fn - 1.0, handlelength=1.7,
                   columnspacing=1.1, handletextpad=0.5, bbox_to_anchor=(0.5, -0.015))
        axa.set_xlabel(r"incumbent strength, $r$")
        axb.set_xlabel(r"incumbent strength, $r$")
    return fig


# ============================================================ figure 3: research
def research_curves():
    rR, rRb = BF["rR"], BF["rRbar"]
    rb = np.linspace(rR, rRb, 300)
    lam_b = lamR(PF, rb)
    ent_b = RHO + (1 - RHO) * (PF.beta + (0.5 - PF.beta) * lam_b)
    return rb, lam_b, ent_b


def entry_at(lam):
    return RHO + (1 - RHO) * (PF.beta + (0.5 - PF.beta) * lam)


def fig_research(talk):
    S = Style(talk)
    S.apply()
    rR, rRb, rN, rU, rC = (BF[k_] for k_ in ("rR", "rRbar", "rN", "rU", "rC"))
    rb, lam_b, ent_b = research_curves()
    if talk:
        fig = plt.figure(figsize=(7.4, 3.1))
        gs = GridSpec(1, 2, left=0.085, right=0.985, bottom=0.205, top=0.83, wspace=0.30, figure=fig)
        axs = [(fig.add_subplot(gs[0]), None), (fig.add_subplot(gs[1]), None)]
        xr = (1.2, 2.0)
    else:
        fig = plt.figure(figsize=(6.5, 5.5))
        gs = GridSpec(2, 2, width_ratios=[3.1, 1.25], left=0.105, right=0.975, bottom=0.095, top=0.925,
                      wspace=0.075, hspace=0.26, figure=fig)
        a1 = fig.add_subplot(gs[0, 0])
        a2 = fig.add_subplot(gs[0, 1], sharey=a1)
        b1 = fig.add_subplot(gs[1, 0])
        b2 = fig.add_subplot(gs[1, 1], sharey=b1)
        axs = [(a1, a2), (b1, b2)]
        xr = (1.2, 2.0)
    xr2 = (2.4, 3.6)

    def common(axl, axr, ylim, yticks, ylabel, panel):
        axl.set_xlim(*xr)
        axl.set_ylim(*ylim)
        axl.set_yticks(yticks)
        axl.set_ylabel(ylabel)
        axl.set_xticks([1.2, 1.4, 1.6, 1.8, 2.0])
        axl.axvspan(rN, xr[1], color=BAND_GREY, lw=0, zorder=0)
        if axr is not None:
            axr.set_xlim(*xr2)
            axr.set_xticks([2.4, 2.8, 3.2, 3.6])
            axr.spines["left"].set_visible(False)
            axr.tick_params(axis="y", left=False, labelleft=False)
            axr.axvspan(xr2[0], rU, color=BAND_GREY, lw=0, zorder=0)
            axl.spines["right"].set_visible(False)
            for ax_, sx in ((axl, 1.0), (axr, 0.0)):
                ax_.plot([sx - 0.012, sx + 0.012], [-0.028, 0.028], transform=ax_.transAxes, color="k", lw=0.8,
                         clip_on=False)
        panel_label(axl, panel, S, dx=-0.105 if not talk else -0.20, dy=1.10 if not talk else 1.06)

    # ---------------- panel (a): research intensity
    al, ar = axs[0]
    common(al, ar, (-0.025, 0.40), [0.0, 0.1, 0.2, 0.3, 0.4], r"research intensity, $\lambda$", "(a)")
    al.axhline(CAP, xmin=0, xmax=(rRb - xr[0]) / (xr[1] - xr[0]), color="0.55", ls=(0, (1.2, 2.2)), lw=S.lwt, zorder=1)
    al.plot([R0, rN], [0, 0], color=NAVY, lw=S.lw, solid_capstyle="butt", zorder=4, clip_on=False)
    dot(al, rN, 0.0, S, color=NAVY)
    al.plot(rb, lam_b, color=BRICK, ls=DASH_R, lw=S.lw, zorder=4)
    dot(al, rR, float(lam_b[0]), S, color=BRICK)
    al.plot([rRb, rN], [CAP, CAP], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    dot(al, rRb, CAP, S, color=BRICK, size=S.ms * 0.8)
    dot(al, rN, CAP, S, color=BRICK, open_=True, z=7)
    if ar is not None:
        ar.plot([rU, R2], [CAP, CAP], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
        dot(ar, rU, CAP, S, color=BRICK, open_=True, z=7)
        dot(ar, R1, CAP, S)
        dot(ar, R2, CAP, S)
    for x in NODES:
        dot(al, x, float(lamR(PF, x)), S)
        dot(al, x, 0.0, S)
    dot(al, R0, 0.0, S)
    lv = 0.085 if not talk else 0.1
    for ax_, x, tex, level in ((al, rR, r"$r_R$", 1), (al, rRb, r"$\bar r_R$", 0), (al, rN, r"$r_N$", 1)):
        mark_x(ax_, x, tex, S, level=level, lvl=lv)
    if ar is not None:
        mark_x(ar, rU, r"$r_U$", S, level=0, lvl=lv)
        mark_x(ar, rC, r"$r_C$", S, level=1, lvl=lv)
    lab(al, 1.21, 0.02, r"zero research", S, color=NAVY, va="bottom")
    if talk:
        al.annotate(r"research" "\n" r"branch", xy=(1.548, float(lamR(PF, 1.548)) - 0.006), xytext=(1.215, 0.27), fontsize=S.fn,
                    color=BRICK, ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=14, shrinkB=4))
        lab(al, 1.21, CAP + 0.026, r"cap $\bar\lambda=%s$" % regd("res_cap", d6(CAP)), S, color="0.3", va="bottom")
    else:
        al.annotate(r"research branch", xy=(1.555, float(lamR(PF, 1.555)) - 0.004), xytext=(1.30, 0.20), fontsize=S.fn,
                    color=BRICK, ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=1, shrinkB=4))
        lab(al, 1.21, CAP + 0.018, r"cap $\bar\lambda=%s$" % regd("res_cap", d6(CAP)), S, color="0.3", va="bottom")
        lab(ar, 3.55, CAP + 0.018, r"research at the cap", S, color=BRICK, ha="right", va="bottom")
    lab(al, (rN + xr[1]) / 2, 0.20, r"beyond $r_N$" if talk else r"equilibrium" "\n" r"set not" "\n" r"characterized", S,
        color="0.35", ha="center", va="center")

    # ---------------- panel (b): entry
    bl, br = axs[1]
    common(bl, br, (0.20, 0.58), [0.2, 0.3, 0.4, 0.5], r"total entry, $E$", "(b)")
    bl.plot([R0, rN], [RHO, RHO], color=NAVY, lw=S.lw, solid_capstyle="butt", zorder=4)
    dot(bl, rN, RHO, S, color=NAVY)
    bl.plot(rb, ent_b, color=BRICK, ls=DASH_R, lw=S.lw, zorder=4)
    dot(bl, rR, float(ent_b[0]), S, color=BRICK)
    bl.plot([rRb, rN], [ENT1, ENT1], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    dot(bl, rRb, ENT1, S, color=BRICK, size=S.ms * 0.8)
    dot(bl, rN, ENT1, S, color=BRICK, open_=True, z=7)
    if br is not None:
        br.plot([rU, rC], [ENT1, ENT1], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
        dot(br, rU, ENT1, S, color=BRICK, open_=True, z=7)
        dot(br, rC, ENT1, S, color=BRICK, open_=True, z=7)
        br.plot([rC, R2], [RHO, RHO], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
        dot(br, rC, RHO, S, color=BRICK, open_=True, z=7)
        dot(br, R1, ENT1, S)
        dot(br, R2, RHO, S, size=S.ms * 0.8, z=9)
    for x in NODES:
        dot(bl, x, float(entry_at(lamR(PF, x))), S)
        dot(bl, x, RHO, S)
    dot(bl, R0, RHO, S)
    lab(bl, 1.21, RHO - 0.014, r"zero research", S, color=NAVY, va="top")
    lab(bl, (rN + xr[1]) / 2, 0.40, r"beyond $r_N$" if talk else r"equilibrium" "\n" r"set not" "\n" r"characterized", S,
        color="0.35", ha="center", va="center")
    if talk:
        lab(bl, rR - 0.012, float(ent_b[0]) - 0.022, regd("res_entry_rR", d6(ent_b[0])), S, color=BRICK, ha="center", va="top")
        lab(bl, rRb - 0.005, ENT1 + 0.022, regd("res_entry_cap", d6(ENT1)), S, color=BRICK, ha="center", va="bottom")
    else:
        lab(br, 3.55, ENT1 + 0.02, r"research at the cap", S, color=BRICK, ha="right", va="bottom")
        lab(br, 3.55, RHO + 0.022, r"entry at the floor", S, color=BRICK, ha="right", va="bottom")
        ins = bl.inset_axes([0.075, 0.37, 0.40, 0.40])
        ins.plot(rb, ent_b, color=BRICK, ls=DASH_R, lw=S.lw * 0.85)
        ins.plot([rRb, 1.74], [ENT1, ENT1], color=BRICK, lw=S.lw * 0.85)
        for x in NODES:
            ins.plot([x], [float(entry_at(lamR(PF, x)))], "o", ms=S.ms * 0.85, color="k", clip_on=False)
        ins.plot([rR], [float(ent_b[0])], "o", ms=S.ms * 0.85, color=BRICK, clip_on=False)
        ins.plot([rRb], [ENT1], "o", ms=S.ms * 0.7, color=BRICK, clip_on=False)
        ins.set_xlim(1.49, 1.74)
        ins.set_ylim(0.4985, 0.5260)
        ins.set_xticks([1.5, 1.6, 1.7])
        ins.set_yticks([0.50, 0.51, 0.52])
        ins.tick_params(labelsize=S.ft - 1.0, length=2.2, pad=1.5)
        ins.patch.set_alpha(0.0)
        ins.text(1.495, 0.5248, r"entry along the branch", fontsize=S.fn - 0.5, color=BRICK, va="center", ha="left")
    if talk:
        for ax_ in (al, bl):
            ax_.set_xlabel(r"incumbent strength, $r$")
    else:
        fig.text(0.5, 0.012, r"incumbent strength, $r$", ha="center", va="bottom", fontsize=S.fl)
    return fig


# ============================================================ build
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    log("make_figures.py: figures of the order-slot manuscript, calibration B")
    log(f"fonts: Fira Sans registered: {FIRA_OK}; matplotlib {matplotlib.__version__}; mpmath dps {mp.dps}")
    log("")
    log("Primitives: h=10 ell=1 p=1/2 rho=1/4 c_H=6 k=1/50 pi=1/2; 1+u=e, beta=0.294655; research a=1/40, cap=lambda_B")
    log(f"u={float(PM.u):.10f}  lambda_B={float(PM.lam):.10f}  b_B={float(PM.b):.10f}  "
        f"M(1/2)={float(PM.M):.10f}  m(1/2)={float(PM.m):.10f}")
    log("")
    log("Boundaries used (40-digit values, 12 shown) beside the registry display value")
    log(f"{'name':<8}{'value':<22}{'computed':<12}{'registry key':<14}{'registry':<12}match")
    rows = [("r_A", "rA", "rA"), ("r_F", "rF", "rF_B"), ("r_N", "rN", "rN"), ("r_J", "rJ", "rJ"),
            ("r_S", "rS", "rS_B"), ("r_C", "rC", "rC_B"), ("r_R", "rR", "res_rR"), ("r_R-bar", "rRbar", "res_rcap"),
            ("r_U (r_U^R)", "rU", "res_rUR")]
    for name, key, rk in rows:
        v = BD[key]
        comp, reg = d6(v), REG.get(rk, "(no row)")
        log(f"{name:<8}{mp.nstr(v, 14):<22}{comp:<12}{rk:<14}{reg:<12}{'yes' if same(comp, reg) else 'DIFFERENT'}")
    log("")
    log("Other values used, computed beside the registry")
    P = PM
    checks = [
        ("M(1/2)", P.M, "M_half_B"), ("m(1/2)", P.m, "m_half_B"), ("lambda_B (cap)", P.lam, "res_cap"),
        ("tau(r_0)", tau(P, mpf(6) / 5), "tau_r0"), ("tau(r_1)", tau(P, mpf(3)), "tau_r1"),
        ("tau(r_2)", tau(P, mpf(18) / 5), "tau_r2"),
        ("entry plateau, F", ent_plateau(P), "entry_r1_B"), ("entry at r_A, branch R", ent_branch_R(P, BD["rA"]), "entry_rA_B"),
        ("entry on R at 1.40", ent_branch_R(P, mpf("1.40")), "entry_mb_r140_B"),
        ("entry on R at 1.45", ent_branch_R(P, mpf("1.45")), "entry_mb_r145_B"),
        ("entry on T at 1.55", ent_threshold(P, mpf("1.55")), "entry_th_r155_B"),
        ("entry on T at 1.60", ent_threshold(P, mpf("1.60")), "entry_th_r160_B"),
        ("entry on T at 1.65", ent_threshold(P, mpf("1.65")), "entry_th_r165_B"),
        ("entry on T at r_A (= R at r_A)", ent_threshold(P, BD["rA"]), "entry_rA_B"),
        ("entry on T at r_J (= rho)", ent_threshold(P, BD["rJ"]), "entry_floor_obs"),
    ]
    for r_, tag in ((mpf("1.55"), "155"), (mpf("1.60"), "160"), (mpf("1.65"), "165")):
        lam_ = mpf(float(lamR(PF, float(r_))))
        # research intensity with the 40-digit root of F_r by bisection
        D = Delta(P, r_)
        f = lambda z: 2 * P.a * (1 - 2 * P.beta) * z * z + (4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * D) * z + P.beta * (2 * P.k - D)
        lam_hp = bisect(f, mpf(0), mpf(1))
        ent_hp = P.rho + (1 - P.rho) * (P.beta + (mpf(1) / 2 - P.beta) * lam_hp)
        checks.append((f"research lambda_R at {float(r_):.2f}", lam_hp, f"res_lambda_r{tag}"))
        checks.append((f"entry on branch R at {float(r_):.2f}", ent_hp, f"res_entry_r{tag}"))
    lam_rR = bisect(lambda z: 2 * P.a * (1 - 2 * P.beta) * z * z + (4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * Delta(P, BD["rR"])) * z + P.beta * (2 * P.k - Delta(P, BD["rR"])), mpf(0), mpf(1))
    checks.append(("research at r_R", lam_rR, "res_lambda_rR"))
    checks.append(("research at r_R, recruitment intensity lambda_E(r_R)", lamE(P, BD["rR"]), "res_lambda_rR"))
    checks.append(("entry at r_R", P.rho + (1 - P.rho) * (P.beta + (mpf(1) / 2 - P.beta) * lam_rR), "res_entry_rR"))
    checks.append(("entry at the cap", ent_plateau(P), "res_entry_cap"))
    log(f"{'quantity':<52}{'computed':<12}{'registry key':<20}{'registry':<12}match")
    for name, v, rk in checks:
        comp, reg = d6(v), REG.get(rk, "(no row)")
        log(f"{name:<52}{comp:<12}{rk:<20}{reg:<12}{'yes' if same(comp, reg) else 'DIFFERENT'}")
    log("")
    log("Order of the boundaries (coexistence figure): r_A < r_F < r_N < r_J < r_S < r_C: " +
        " < ".join(f"{BF[k_]:.6f}" for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC")))
    log("Research branch: r_R < r_R-bar < r_N < r_U: " + " < ".join(f"{BF[k_]:.6f}" for k_ in ("rR", "rRbar", "rN", "rU")))
    log("Line breaks: no curve crosses an open interval. Coexistence: R ends at r_F where F starts at the same value;")
    log("  F ends at r_C (closed), the floor segment starts at r_C (open). Q is open at r_N and r_J.")
    log("  Research: Z closed at r_N; the cap line ends open at r_N and restarts open at r_U; (r_N, r_U) is shaded, no line.")
    log("  Research: the plateau ends open at r_C and the floor segment starts open at r_C (P3 excludes M = tau(r)).")
    log("  Markers: filled = the value is attained at that strength; open = approached, not attained or not claimed.")
    log("  Nodes (black): r_0, 1.55, 1.60, 1.65, r_1 = 3, r_2 = 18/5 (the six strengths of P3).")
    log("Fonts: manuscript figures use STIXGeneral text and STIX math (TrueType, Type 42).")
    log("  Slide figures use Fira Sans (Regular) with Computer Modern math; the CFF outlines of Fira Sans are converted")
    log("  to TrueType outlines with fontTools (cu2qu, error bound 1 font unit) so that the PDF embeds a TrueType font.")
    log("")

    made = []
    for talk in (False, True):
        sfx = "_talk" if talk else ""
        for name, fn in (("beliefs", fig_beliefs), ("coexistence", fig_coexistence), ("research", fig_research)):
            fig = fn(talk)
            path = save(fig, f"{name}{sfx}.pdf")
            made.append(path)

    log("SHA-256 of each PDF")
    for path in made:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        log(f"  {sha}  slot/manuscript/figures/{path.name}  ({path.stat().st_size} bytes)")
    log("")
    log("Fonts (pdffonts)")
    for path in made:
        try:
            res = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True, check=False)
            log(f"--- {path.name}")
            log(res.stdout.rstrip())
        except FileNotFoundError:
            log("pdffonts not found")
    for path in made:
        try:
            subprocess.run(["pdftoppm", "-r", "110", "-png", str(path), str(PNG / path.stem)], check=False)
        except FileNotFoundError:
            pass
    LOGFILE.write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
