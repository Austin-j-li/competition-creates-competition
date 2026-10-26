"""Figures of the order-slot manuscript.

Writes beliefs.pdf, coexistence.pdf, research.pdf and the three slide versions
into slot/manuscript/figures/, a run log (run_log.txt) and PNG previews (png/).

Every curve comes from a closed form of the proof packages at the primitives of the example:
  P1_core: tau, Delta, J, the marked strengths r_A, r_F, r_N, r_J, r_S, r_C and the entry of each coexistence form
           (Proposition 3, Step 7), and the coexistence region of Proposition 3(a) at prior 1/2;
  P3_research: the research polynomial Lambda_r, the recruitment intensity, r_R, r_lambda-bar, r_U;
  O1 (floor-entry research): the floor root lambda_Q and the floor margin, whose zero is r_Q.
Boundaries use mpmath at 40 digits; the plotted curves use floating point.
The log prints each boundary beside the registry display value. Nothing is asserted.

Run from the repository root:
  .venv/bin/python audit/slot_manuscript_2026_10_23/scripts/F_figures/make_figures.py
Optional argument --out DIR: the six PDFs, the PNG previews and the run log go to DIR (created if needed). Without
it the PDFs go to slot/manuscript/figures/, and the PNG previews (png/) and the run log (run_log.txt) go beside
this script.
The slide versions set their text in Archivo: the TrueType files in slot/manuscript/fonts/ (the static Archivo
faces as served by Google Fonts, with OFL.txt beside them). The paths used are printed when the program starts.
The manuscript versions keep STIXGeneral text and STIX math.
"""
import argparse
import csv
import hashlib
import math
import os
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
MPL_CACHE = HERE / ".mpl"
OUT_LABEL = "slot/manuscript/figures"

mp.dps = 40
LOG = []


def log(*args):
    line = " ".join(str(a) for a in args)
    LOG.append(line)
    print(line)


# ============================================================ number layer
class Prm:
    """Primitives of the example in one number type (mpmath or float)."""

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
    """Positive root of the research polynomial Lambda_r (P3); r with Delta > 2k."""
    D = Delta(P, r)
    A = 2 * P.a * (1 - 2 * P.beta)
    Bc = 4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * D
    C = P.beta * (2 * P.k - D)
    return (-Bc + np.sqrt(Bc * Bc - 4 * A * C)) / (2 * A)


def lamQ(P, D):
    """Floor-entry research lambda_Q(Delta): the root in [0, 1) of a lambda = rho Delta m_lambda - k, rho Delta >= 2k.
    After clearing 2 beta + (1 - 2 beta) lambda: a(1 - 2beta) lambda^2 + [rho Delta beta + k(1 - 2beta) + 2a beta] lambda
    + beta(2k - rho Delta) = 0; the root is -2C/(B + sqrt(B^2 - 4AC))."""
    sq = np.sqrt if P is PF else P.sqrt
    A = P.a * (1 - 2 * P.beta)
    Bc = P.rho * D * P.beta + P.k * (1 - 2 * P.beta) + 2 * P.a * P.beta
    C = P.beta * (2 * P.k - P.rho * D)
    return -2 * C / (Bc + sq(Bc * Bc - 4 * A * C))


def phi_rho(P, r):
    """Floor margin rho Delta (1 - tau) - k - a lambda_E; its zero on the path is r_Q."""
    return P.rho * Delta(P, r) * (1 - tau(P, r)) - P.k - P.a * lamE(P, r)


def ent_branch_R(P, r):
    """Entry on the mixed purchase R (P1, Proposition 3, Step 7)."""
    return P.rho + (1 - P.rho) * P.b * Delta(P, r) / (2 * P.k)


def ent_plateau(P):
    return P.rho + (1 - P.rho) * (P.b + P.lam / 2)


def ent_threshold(P, r):
    """Entry on the threshold pair T, when an indifferent high-cost challenger may prepare with any probability (P1, Step 7)."""
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
    B["rQ"] = bisect(lambda r: phi_rho(P, r), B["rN"], B["rU"])
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
# Manuscript palette: navy and brick for the two kinds of branch, grey for the floor branches.
NAVY, BRICK, GREY, INK = "#1f3a6e", "#b4472e", "#6c6c6c", "#222222"
BAND_BLUE, BAND_GREY = "#e5eaf4", "#ececec"
PAPER_PALETTE = (NAVY, BRICK, GREY, INK, BAND_BLUE, BAND_GREY)
# Slide palette: the ruled-document tokens of DESIGN.md. Ink carries the quiet branch and the
# region boundaries, the information colour the branches a purchase recruits along and the belief
# band, the cost colour the preparation threshold, the muted grey the floor branches. The bands are
# the information tint and the neutral tint on the slide paper colour.
INK_T, MUTED_T, INFO_T, COST_T = "#1e2530", "#5b6573", "#b54b00", "#006459"
BAND_INFO_T, BAND_GREY_T = "#f5ece5", "#ebedee"
TALK_PALETTE = (INK_T, INFO_T, MUTED_T, INK_T, BAND_INFO_T, BAND_GREY_T)


def set_palette(talk):
    """Bind the drawing colours to the manuscript palette or to the slide palette."""
    global NAVY, BRICK, GREY, INK, BAND_BLUE, BAND_GREY
    NAVY, BRICK, GREY, INK, BAND_BLUE, BAND_GREY = TALK_PALETTE if talk else PAPER_PALETTE
DASH_R = (0, (5.0, 2.2))
DASH_Q = (0, (6.0, 2.0, 1.5, 2.0))
DASH_T = (0, (3.0, 2.0))


FONTS_DIR = ROOT / "slot" / "manuscript" / "fonts"


def register_archivo():
    """Register the Archivo TrueType files of slot/manuscript/fonts/ with matplotlib, so that the slide
    figures embed Archivo (TrueType, Type 42). Prints the paths used; returns True when Archivo-Regular
    is present."""
    files = sorted(FONTS_DIR.glob("Archivo-*.ttf"))
    if not (FONTS_DIR / "Archivo-Regular.ttf").exists():
        print(f"Archivo: Archivo-Regular.ttf not found in {FONTS_DIR}; slide figures use DejaVu Sans")
        return False
    for f in files:
        fm.fontManager.addfont(str(f))
        print(f"Archivo: {f}")
    return True


ARCHIVO_OK = False


class Style:
    def __init__(self, talk):
        self.talk = talk
        if talk:
            self.fs, self.fl, self.ft, self.fm_, self.fn = 11.0, 12.0, 10.5, 10.0, 10.5
            self.lw, self.lwt, self.lwd, self.ms = 2.9, 1.3, 1.1, 6.5
            self.family = "Archivo" if ARCHIVO_OK else "DejaVu Sans"
            self.math = "stix"
        else:
            self.fs, self.fl, self.ft, self.fm_, self.fn = 8.0, 9.0, 8.0, 8.0, 7.5
            self.lw, self.lwt, self.lwd, self.ms = 1.9, 0.8, 0.7, 4.6
            self.family = "STIXGeneral"
            self.math = "stix"

    def apply(self):
        set_palette(self.talk)
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
        if self.talk:
            # Slide figures in the ruled-document tokens: in-figure text and
            # axes in ink, tick labels in the muted grey. Curve colours are
            # set by the drawing calls and stay as they are.
            plt.rcParams.update({
                "text.color": "#1e2530", "axes.edgecolor": "#1e2530",
                "axes.labelcolor": "#1e2530",
                "xtick.color": "#5b6573", "ytick.color": "#5b6573",
                "xtick.labelcolor": "#5b6573", "ytick.labelcolor": "#5b6573",
                # The slide paper colour, so a figure shows no box on the slide.
                "figure.facecolor": "#fbfcfc", "axes.facecolor": "#fbfcfc",
                "savefig.facecolor": "#fbfcfc",
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


def lab(ax, x, y, s, S, color=None, ha="left", va="center", size=None, **kw):
    ax.text(x, y, s, color=INK if color is None else color, ha=ha, va=va, fontsize=size or S.fn, **kw)


def dot(ax, x, y, S, color="k", open_=False, size=None, z=6):
    ax.plot([x], [y], "o", ms=size or S.ms, mfc="white" if open_ else color, mec=color, mew=1.0, clip_on=False,
            zorder=z, ls="none")


def save(fig, name):
    path = OUT / name
    fig.savefig(path, metadata={"CreationDate": None, "ModDate": None, "Creator": "Competition Creates Competition"})
    plt.close(fig)
    return path


# ============================================================ figure 1: beliefs
def fig_beliefs(talk):
    global NAVY, BRICK
    S = Style(talk)
    S.apply()
    if talk:
        # On the slides the posterior band is information and the threshold is a cost.
        NAVY, BRICK = INFO_T, COST_T
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
    axa.set_ylabel(r"preparation threshold, $\tau(r)$")
    xl = 1.27
    lab(axa, xl, Mv + 0.022, r"top posterior $M(1/2)\approx %s$" % regd("M_half_B", d6(PM.M)), S, color=NAVY, va="bottom")
    lab(axa, xl, mv + 0.022, r"bottom posterior $m(1/2)\approx %s$" % regd("m_half_B", d6(PM.m)), S, color=NAVY, va="bottom")
    lab(axa, xl, 0.5 + 0.022, r"prior $1/2$", S, color="0.35", va="bottom")
    lab(axa, 1.9 if not talk else 2.0, 0.60 if not talk else 0.585, r"threshold $\tau(r)$", S, color=BRICK, va="center")
    axa.annotate("", xy=(2.0 if not talk else 2.1, float(tau(PF, 2.0 if not talk else 2.1)) - 0.012),
                 xytext=(2.0 if not talk else 2.1, 0.62 if not talk else 0.605),
                 arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=0, shrinkB=0))
    dot(axa, rC, Mv, S, color="k", open_=True)
    axa.annotate(r"entry ceiling $r_C$", xy=(rC, Mv), xytext=(3.27, 0.60), fontsize=S.fn,
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
    lab(axb, 3.02, t2 + 0.0010, r"$\tau(r_2)\approx %s$" % regd("tau_r2", d6(t2)), S, color=NAVY, va="bottom")
    lab(axb, 3.02, Mv - 0.0009, r"$M(1/2)\approx %s$" % regd("M_half_B", d6(PM.M)), S, color=NAVY, va="top")
    lab(axb, 3.585, t1 + 0.0010, r"$\tau(r_1)=%s$" % regd("tau_r1", d6(t1)), S, color=NAVY, ha="right", va="bottom")
    lab(axb, 3.585, 0.7105 if talk else 0.7095, r"band for $M(1/2)$", S, color=NAVY, ha="right", va="center")
    lab(axb, rC - 0.012, 0.7022, r"$r_C\approx %s$" % regd("rC_B", d6(rC)), S, color="0.2", ha="right", va="center")
    panel_label(axb, "(b)", S, dx=-0.34 if not talk else -0.36, dy=1.075)
    return fig


# ============================================================ figure 2: coexistence
def draw_branches(ax, S, markers=True):
    """All coexistence forms along the example's path at prior 1/2, when an indifferent investor may mix and an
    indifferent high-cost challenger prepares; the threshold pair T when that challenger may prepare with any probability."""
    rA, rF, rN, rJ, rS, rC = (BF[k_] for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC"))
    lo, hi = ax.get_xlim()

    def mk(x, y, color, open_=False, z=6, size=None):
        if markers and lo <= x <= hi:
            dot(ax, x, y, S, color=color, open_=open_, z=z, size=size)

    # T: threshold pair (thin dashed)
    rt = np.linspace(rA, rJ, 300)
    ax.plot(rt, ent_threshold(PF, rt), color="k", ls=DASH_T, lw=S.lwt * 1.15, zorder=3)
    # N: quiet market, closed at r_N
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


def axes_in(fig, left, bottom, w, h):
    """Axes placed in inches."""
    W, H = fig.get_size_inches()
    return fig.add_axes([left / W, bottom / H, w / W, h / H])


def draw_region(ax, S, talk):
    """The coexistence region of Proposition 3(a) in the (Delta_T, tau) plane at prior 1/2 and the example's slot:
    1/2 < tau <= M(1/2) and k/(1 - tau) <= Delta_T <= 2k/rho, with the example's path (Delta_T(r), tau(r))."""
    P = PF
    Mv = float(PM.M)
    DN = 2 * P.k / P.rho                       # Delta^N at prior 1/2
    DF = P.k / (1 - Mv)                        # Delta^F at prior 1/2
    xlo, xhi, ylo, yhi = 0.0, 0.20, 0.45, 0.765
    ax.set_xlim(xlo, xhi)
    ax.set_ylim(ylo, yhi)
    tt = np.linspace(0.5, Mv, 200)
    left = P.k / (1 - tt)
    xs = np.concatenate([left, [DN, DN]])
    ys = np.concatenate([tt, [Mv, 0.5]])
    ax.fill(xs, ys, color=BAND_BLUE, lw=0, zorder=0)
    ax.plot(left, tt, color=NAVY, lw=S.lwt * 1.4, zorder=2)                       # Delta = k/(1 - tau), closed
    ax.plot([DN, DN], [0.5, Mv], color=NAVY, lw=S.lwt * 1.4, zorder=2)             # Delta = 2k/rho, closed
    ax.plot([left[-1], DN], [Mv, Mv], color=NAVY, lw=S.lwt * 1.4, zorder=2)        # tau = M(1/2), closed
    ax.axhline(0.5, color=GREY, ls=(0, (1.5, 2.0)), lw=S.lwt * 1.4, zorder=1)     # tau = pi, open
    ax.plot([DF, DF], [0.5, Mv], color=NAVY, ls=(0, (4.0, 2.0)), lw=S.lwt, zorder=2)  # Delta = k/(1 - M)
    ax.plot([xlo, left[-1]], [Mv, Mv], color=NAVY, ls=(0, (1.5, 2.0)), lw=S.lwt * 1.4, zorder=1)  # tau = M(1/2)
    # the example's path from r_0 until it leaves the window
    r_out = float(frak(PF, xhi))
    rr = np.linspace(R0, r_out, 400)
    ax.plot(Delta(PF, rr), tau(PF, rr), color=BRICK, lw=S.lw * 0.8, solid_capstyle="butt", zorder=4, clip_on=False)
    ax.annotate("", xy=(xhi + 0.006, float(tau(PF, frak(PF, xhi + 0.006)))),
                xytext=(xhi - 0.004, float(tau(PF, frak(PF, xhi - 0.004)))),
                arrowprops=dict(arrowstyle="-|>", lw=S.lw * 0.8, color=BRICK, mutation_scale=7 if not talk else 10,
                                shrinkA=0, shrinkB=0), annotation_clip=False, zorder=5)
    dot(ax, float(Delta(PF, R0)), float(tau(PF, R0)), S)
    for key in ("rA", "rF", "rN"):
        r_ = BF[key]
        dot(ax, float(Delta(PF, r_)), float(tau(PF, r_)), S, color=BRICK, z=7)
    ax.set_xlabel(r"target-payoff spread, $\Delta_T$")
    ax.set_ylabel(r"preparation threshold, $\tau$" if not talk else r"threshold, $\tau$")
    if talk:
        ax.set_xticks([0.0, 0.1, 0.2])
    else:
        ax.set_xticks([0.0, 0.05, 0.10, 0.15, 0.20])
    ax.set_yticks([0.5, 0.6, 0.7])
    yoff = 0.016 if not talk else 0.02
    def plabel(key, tex, dx, dy, ha):
        r_ = BF[key]
        lab(ax, float(Delta(PF, r_)) + dx, float(tau(PF, r_)) + dy, tex, S, color=BRICK, ha=ha, va="center")
    lab(ax, float(Delta(PF, R0)) - 0.002, float(tau(PF, R0)) - yoff * 1.3, r"$r_0$", S, color="k", ha="left", va="center")
    plabel("rA", r"$r_A$", -0.004, yoff * 1.3, "right")
    plabel("rF", r"$r_F$", 0.003, yoff * 1.3, "left")
    plabel("rN", r"$r_N$", 0.004, -yoff * 1.3, "left")
    lab(ax, 0.006, Mv + 0.012, r"$M(1/2)$", S, color=NAVY, ha="left", va="bottom")
    lab(ax, 0.006, 0.5 - 0.012, r"prior $\pi=1/2$" if not talk else r"$\pi=1/2$", S, color="0.35", ha="left", va="top")
    if not talk:
        lab(ax, 0.117, 0.705, r"coexistence" "\n" r"region", S, color=NAVY, ha="center", va="center", linespacing=1.0)
        lab(ax, 0.063, 0.545, r"R", S, color=NAVY, ha="center", va="center", size=S.fn + 1)
        lab(ax, 0.117, 0.545, r"F", S, color=NAVY, ha="center", va="center", size=S.fn + 1)
    else:
        lab(ax, 0.118, 0.70, r"coexistence", S, color=NAVY, ha="center", va="center", size=S.fn - 1.5)


def fig_coexistence(talk):
    S = Style(talk)
    S.apply()
    rA, rF, rN, rJ, rS, rC = (BF[k_] for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC"))
    ZLO, ZHI = 1.25, 2.35
    ylo, yhi = 0.15, 0.62
    ylob = 0.12
    if talk:
        fig = plt.figure(figsize=(10.2, 3.3))
        axa = axes_in(fig, 0.75, 1.10, 2.25, 1.55)
        axr = axes_in(fig, 3.85, 1.10, 1.95, 1.55)
        axb = axes_in(fig, 6.55, 1.10, 3.55, 1.55)
    else:
        fig = plt.figure(figsize=(6.5, 5.85))
        axa = axes_in(fig, 0.62, 3.66, 3.20, 1.78)
        axr = axes_in(fig, 4.50, 3.66, 1.80, 1.78)
        axb = axes_in(fig, 0.62, 0.50, 5.80, 2.15)
    for ax, yl in ((axa, ylo), (axb, ylob)):
        ax.set_ylim(yl, yhi)
        ax.set_yticks([0.2, 0.3, 0.4, 0.5, 0.6])
        ax.set_xlabel(r"incumbent strength, $r$")
        ax.axvspan(rA, rN, color=BAND_BLUE, lw=0, zorder=0)
    axa.set_ylabel(r"entry, $\mathsf{E}$")
    axb.set_ylabel(r"entry, $\mathsf{E}$") if not talk else None
    axa.set_xlim(R0, R2)
    axb.set_xlim(ZLO, ZHI)
    axa.set_xticks([1.2, 2.0, 2.8, 3.6] if talk else [1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6])
    axb.set_xticks([1.4, 1.6, 1.8, 2.0, 2.2] if not talk else [1.4, 1.8, 2.2])
    draw_branches(axa, S, markers=False)
    draw_branches(axb, S, markers=True)
    draw_region(axr, S, talk)
    dot(axa, rC, ENT1, S, color=BRICK)
    dot(axa, rC, RHO, S, color=BRICK, open_=True, z=7)
    for x in (rA, rN, rC):
        axa.axvline(x, color="0.3", ls=":", lw=S.lwd, zorder=1)
    mark_x(axa, rC, r"$r_C$", S, level=0, lvl=0.1)
    # --- (a): the whole path
    axa.annotate("", xy=(ZLO, 0.585), xytext=(ZHI, 0.585),
                 arrowprops=dict(arrowstyle="<->", lw=S.lwt * 1.2, color="0.35", shrinkA=0, shrinkB=0))
    lab(axa, ZHI + 0.06, 0.585, r"zoom in (c)" if not talk else r"(c)", S, color="0.35", ha="left", va="center")
    lab(axa, 1.27, RHO + 0.025, r"N", S, color=NAVY, va="bottom", size=S.fn + 1)
    lab(axa, 2.85, ENT1 + 0.025, r"F", S, color=BRICK, va="bottom", size=S.fn + 1, ha="center")
    lab(axa, 3.545, RHO + 0.026, r"F above $r_C$" if not talk else r"F", S, color=BRICK, ha="right", va="bottom")
    pdx = -0.19 if not talk else -0.30
    panel_label(axa, "(a)", S, dx=pdx, dy=1.06)
    panel_label(axr, "(b)", S, dx=-0.33 if not talk else -0.35, dy=1.06)
    # --- (c): the zoom with every marked strength
    for key, tex, level in (("rA", r"$r_A$", 1), ("rF", r"$r_F$", 0), ("rN", r"$r_N$", 1), ("rJ", r"$r_J$", 0),
                            ("rS", r"$r_S$", 1)):
        mark_x(axb, BF[key], tex, S, level=level, lvl=0.085 if not talk else 0.095)
    panel_label(axb, "(c)", S, dx=-0.098 if not talk else -0.19, dy=1.17 if not talk else 1.06)
    # direct labels (zoom)
    if not talk:
        lab(axb, ZLO + 0.012, RHO - 0.024, r"N: quiet market", S, color=NAVY, va="top")
        axb.annotate(r"Q: mixed orders at the entry floor", xy=(1.857, RHO), xytext=(1.857, RHO - 0.05),
                     fontsize=S.fn, color="0.35", ha="center", va="top",
                     arrowprops=dict(arrowstyle="-", lw=S.lwt, color="0.5", shrinkA=0, shrinkB=3))
        axb.annotate(r"R: mixed" "\n" r"purchase" "\n" r"that recruits", xy=(1.428, float(ent_branch_R(PF, 1.428))),
                     xytext=(1.372, 0.492), fontsize=S.fn, color=BRICK, ha="right", va="center",
                     arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=1, shrinkB=2.5))
        axb.annotate(r"T: threshold pair", xy=(1.62, float(ent_threshold(PF, 1.62))),
                     xytext=(1.775, 0.385), fontsize=S.fn, color="k", ha="left", va="center",
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
        ls_ = [r"N quiet market", r"R mixed purchase that recruits", r"F full purchase",
               r"Q mixed orders at the entry floor", r"T threshold pair"]
        fig.legend(hs, ls_, loc="lower center", ncol=5, frameon=False, fontsize=S.fn - 1.0, handlelength=1.7,
                   columnspacing=1.1, handletextpad=0.5, bbox_to_anchor=(0.5, -0.015))
    return fig


# ============================================================ figure 3: research
def research_curves():
    """Recruiting research below the cap on [r_R, r_lambda-bar] and floor-entry research on [r_N, r_Q]."""
    rR, rRb, rN, rQ = BF["rR"], BF["rRbar"], BF["rN"], BF["rQ"]
    rb = np.linspace(rR, rRb, 300)
    lam_b = lamR(PF, rb)
    rq = np.linspace(rN, rQ, 300)
    lam_q = lamQ(PF, Delta(PF, rq))
    return rb, lam_b, entry_at(lam_b), rq, lam_q


def entry_at(lam):
    return RHO + (1 - RHO) * (PF.beta + (0.5 - PF.beta) * lam)


def fig_research(talk):
    S = Style(talk)
    S.apply()
    rR, rRb, rN, rQ, rC = (BF[k_] for k_ in ("rR", "rRbar", "rN", "rQ", "rC"))
    rb, lam_b, ent_b, rq, lam_q = research_curves()
    if talk:
        fig = plt.figure(figsize=(7.4, 3.1))
        gs = GridSpec(1, 2, left=0.085, right=0.985, bottom=0.205, top=0.80, wspace=0.30, figure=fig)
        al, bl = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
        xt = [1.2, 2.0, 2.8, 3.6]
    else:
        fig = plt.figure(figsize=(6.5, 5.5))
        gs = GridSpec(2, 1, left=0.105, right=0.975, bottom=0.095, top=0.91, hspace=0.30, figure=fig)
        al = fig.add_subplot(gs[0])
        bl = fig.add_subplot(gs[1], sharex=al)
        xt = [1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6]
    for ax_ in (al, bl):
        ax_.set_xlim(R0, R2)
        ax_.set_xticks(xt)
    lv = 0.085 if not talk else 0.1
    pdx = -0.075 if not talk else -0.20
    pdy = 1.10 if not talk else 1.12

    # ---------------- panel (a): research intensity
    al.set_ylim(-0.025, 0.40)
    al.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4])
    al.set_ylabel(r"research intensity, $\lambda$")
    al.plot([R0, rRb], [CAP, CAP], color="0.55", ls=(0, (1.2, 2.2)), lw=S.lwt, zorder=1)
    # zero research, closed at r_N
    al.plot([R0, rN], [0, 0], color=NAVY, lw=S.lw, solid_capstyle="butt", zorder=4, clip_on=False)
    dot(al, rN, 0.0, S, color=NAVY)
    # recruiting research: below the cap on [r_R, r_lambda-bar), at the cap on [r_lambda-bar, r_C]
    al.plot(rb, lam_b, color=BRICK, ls=DASH_R, lw=S.lw, zorder=4)
    dot(al, rR, float(lam_b[0]), S, color=BRICK)
    al.plot([rRb, rC], [CAP, CAP], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    dot(al, rRb, CAP, S, color=BRICK, size=S.ms * 0.8)
    # floor-entry research: (r_N, r_Q) below the cap, (r_C, r_2] at the cap
    al.plot(rq, lam_q, color=GREY, ls=DASH_Q, lw=S.lw, zorder=4)
    dot(al, rQ, float(lam_q[-1]), S, color=GREY, open_=True, z=7)
    al.plot([rC, R2], [CAP, CAP], color=GREY, ls=DASH_Q, lw=S.lw, zorder=5)
    dot(al, rC, CAP, S, color=BRICK, z=8)
    for x in NODES:
        dot(al, x, float(lamR(PF, x)), S)
        dot(al, x, 0.0, S)
    dot(al, R0, 0.0, S)
    dot(al, R1, CAP, S)
    dot(al, R2, CAP, S, size=S.ms * 0.8, z=9)
    marks = ((rR, r"$r_R$", 0), (rRb, r"$r_{\bar\lambda}$", 1 if talk else 0), (rN, r"$r_N$", 0 if talk else 1),
             (rQ, r"$r_Q$", 0), (rC, r"$r_C$", 0))
    for x, tex, level in marks:
        mark_x(al, x, tex, S, level=level, lvl=lv)
    for x, _, _ in marks:
        bl.axvline(x, color="0.3", ls=":", lw=S.lwd, zorder=1)
    if talk:
        lab(al, 1.24, 0.03, r"zero", S, color=NAVY, va="bottom")
        lab(al, 2.30, CAP + 0.026, r"recruiting", S, color=BRICK, ha="center", va="bottom")
        lab(al, 2.22, 0.20, r"floor-entry", S, color="0.3", ha="left", va="center")
    else:
        lab(al, 1.21, 0.018, r"zero research", S, color=NAVY, va="bottom")
        lab(al, (rN + rQ) / 2, CAP - 0.016, r"cap $\bar\lambda\approx %s$" % regd("res_cap", d6(CAP)), S, color="0.3",
            ha="center", va="top")
        al.annotate(r"recruiting" "\n" r"research", xy=(1.515, float(lamR(PF, 1.515))), xytext=(1.225, 0.235),
                    fontsize=S.fn, color=BRICK, ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", lw=S.lwt, color=BRICK, shrinkA=1, shrinkB=4))
        lab(al, 2.80, CAP + 0.018, r"recruiting research at the cap", S, color=BRICK, ha="center", va="bottom")
        x_ = 2.06
        al.annotate(r"floor-entry research", xy=(x_, float(lamQ(PF, Delta(PF, x_))) - 0.006), xytext=(2.30, 0.12),
                    fontsize=S.fn, color="0.3", ha="left", va="center",
                    arrowprops=dict(arrowstyle="-", lw=S.lwt, color="0.4", shrinkA=1, shrinkB=4))
    panel_label(al, "(a)", S, dx=pdx, dy=pdy)

    # ---------------- panel (b): entry
    bl.set_ylim(0.20, 0.58)
    bl.set_yticks([0.2, 0.3, 0.4, 0.5])
    bl.set_ylabel(r"entry, $\mathsf{E}$")
    # zero research, closed at r_N
    bl.plot([R0, rN], [RHO, RHO], color=NAVY, lw=S.lw, solid_capstyle="butt", zorder=4)
    # floor-entry research at the entry floor
    bl.plot([rN, rQ], [RHO, RHO], color=GREY, ls=DASH_Q, lw=S.lw, zorder=5)
    dot(bl, rN, RHO, S, color=NAVY, z=8)
    dot(bl, rQ, RHO, S, color=GREY, open_=True, z=7)
    bl.plot([rC, R2], [RHO, RHO], color=GREY, ls=DASH_Q, lw=S.lw, zorder=5)
    dot(bl, rC, RHO, S, color=GREY, open_=True, z=7)
    # recruiting research
    bl.plot(rb, ent_b, color=BRICK, ls=DASH_R, lw=S.lw, zorder=4)
    dot(bl, rR, float(ent_b[0]), S, color=BRICK)
    bl.plot([rRb, rC], [ENT1, ENT1], color=BRICK, lw=S.lw, solid_capstyle="butt", zorder=4)
    dot(bl, rRb, ENT1, S, color=BRICK, size=S.ms * 0.8)
    dot(bl, rC, ENT1, S, color=BRICK)
    for x in NODES:
        dot(bl, x, float(entry_at(lamR(PF, x))), S)
        dot(bl, x, RHO, S)
    dot(bl, R0, RHO, S)
    dot(bl, R1, ENT1, S)
    dot(bl, R2, RHO, S, size=S.ms * 0.8, z=9)
    if talk:
        lab(bl, 1.24, RHO - 0.016, r"zero", S, color=NAVY, va="top")
        lab(bl, 2.60, ENT1 + 0.02, r"recruiting", S, color=BRICK, ha="center", va="bottom")
        lab(bl, 2.22, RHO + 0.03, r"floor-entry", S, color="0.3", ha="left", va="bottom")
        for ax_ in (al, bl):
            ax_.set_xlabel(r"incumbent strength, $r$")
    else:
        lab(bl, 1.21, RHO - 0.014, r"zero research", S, color=NAVY, va="top")
        lab(bl, (rN + rQ) / 2, RHO - 0.014, r"floor-entry research", S, color="0.3", ha="center", va="top")
        lab(bl, 2.80, ENT1 + 0.016, r"recruiting research", S, color=BRICK, ha="center", va="bottom")
        ins = bl.inset_axes([0.43, 0.33, 0.33, 0.40])
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
        ins.text(1.495, 0.5248, r"entry along the recruiting branch", fontsize=S.fn - 0.5, color=BRICK, va="center",
                 ha="left")
        plt.setp(al.get_xticklabels(), visible=False)
        fig.text(0.5, 0.012, r"incumbent strength, $r$", ha="center", va="bottom", fontsize=S.fl)
    panel_label(bl, "(b)", S, dx=pdx, dy=1.04 if not talk else pdy)
    return fig


# ============================================================ build
def main(argv=None):
    global OUT, PNG, LOGFILE, MPL_CACHE, OUT_LABEL, ARCHIVO_OK
    ap = argparse.ArgumentParser(description="Figures of the order-slot manuscript.")
    ap.add_argument("--out", metavar="DIR", default=None,
                    help="write the six PDFs, the PNG previews and the run log to DIR instead of the manuscript folder")
    args = ap.parse_args(argv)
    if args.out is not None:
        OUT = PNG = pathlib.Path(args.out).expanduser().resolve()
        LOGFILE = OUT / "run_log.txt"
        MPL_CACHE = OUT / ".mpl"
        OUT_LABEL = str(OUT)
    ARCHIVO_OK = register_archivo()
    OUT.mkdir(parents=True, exist_ok=True)
    PNG.mkdir(parents=True, exist_ok=True)
    log("make_figures.py: figures of the order-slot manuscript")
    log(f"fonts: Archivo registered: {ARCHIVO_OK}; matplotlib {matplotlib.__version__}; mpmath dps {mp.dps}")
    log("")
    log("Primitives: h=10 ell=1 p=1/2 rho=1/4 c_H=6 k=1/50 pi=1/2; 1+u=e, beta=0.294655; research a=1/40, cap=lambda-bar(beta)")
    log(f"u={float(PM.u):.10f}  lambda-bar={float(PM.lam):.10f}  b={float(PM.b):.10f}  "
        f"M(1/2)={float(PM.M):.10f}  m(1/2)={float(PM.m):.10f}")
    log("")
    log("Boundaries used (40-digit values, 12 shown) beside the registry display value")
    log(f"{'name':<8}{'value':<22}{'computed':<12}{'registry key':<14}{'registry':<12}match")
    rows = [("r_A", "rA", "rA"), ("r_F", "rF", "rF_B"), ("r_N", "rN", "rN"), ("r_J", "rJ", "rJ"),
            ("r_S", "rS", "rS_B"), ("r_C", "rC", "rC_B"), ("r_C", "rC", "res_rC"), ("r_R", "rR", "res_rR"),
            ("r_lb", "rRbar", "res_rcap"), ("r_U", "rU", "res_rUR"), ("r_Q", "rQ", "res_rQ")]
    for name, key, rk in rows:
        v = BD[key]
        comp, reg = d6(v), REG.get(rk, "(no row)")
        log(f"{name:<8}{mp.nstr(v, 14):<22}{comp:<12}{rk:<14}{reg:<12}{'yes' if same(comp, reg) else 'DIFFERENT'}")
    log("")
    log("Other values used, computed beside the registry")
    P = PM
    checks = [
        ("M(1/2)", P.M, "M_half_B"), ("m(1/2)", P.m, "m_half_B"), ("lambda-bar (cap)", P.lam, "res_cap"),
        ("tau(r_0)", tau(P, mpf(6) / 5), "tau_r0"), ("tau(r_1)", tau(P, mpf(3)), "tau_r1"),
        ("tau(r_2)", tau(P, mpf(18) / 5), "tau_r2"),
        ("entry plateau, F", ent_plateau(P), "entry_r1_B"), ("entry at r_A, form R", ent_branch_R(P, BD["rA"]), "entry_rA_B"),
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
        # research intensity with the 40-digit root of Lambda_r by bisection
        D = Delta(P, r_)
        f = lambda z: 2 * P.a * (1 - 2 * P.beta) * z * z + (4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * D) * z + P.beta * (2 * P.k - D)
        lam_hp = bisect(f, mpf(0), mpf(1))
        ent_hp = P.rho + (1 - P.rho) * (P.beta + (mpf(1) / 2 - P.beta) * lam_hp)
        checks.append((f"research lambda_R at {float(r_):.2f}", lam_hp, f"res_lambda_r{tag}"))
        checks.append((f"entry, recruiting research at {float(r_):.2f}", ent_hp, f"res_entry_r{tag}"))
    lam_rR = bisect(lambda z: 2 * P.a * (1 - 2 * P.beta) * z * z + (4 * P.a * P.beta + P.k * (1 - 2 * P.beta) + P.beta * Delta(P, BD["rR"])) * z + P.beta * (2 * P.k - Delta(P, BD["rR"])), mpf(0), mpf(1))
    checks.append(("research at r_R", lam_rR, "res_lambda_rR"))
    checks.append(("research at r_R, recruitment intensity lambda_E(r_R)", lamE(P, BD["rR"]), "res_lambda_rR"))
    checks.append(("entry at r_R", P.rho + (1 - P.rho) * (P.beta + (mpf(1) / 2 - P.beta) * lam_rR), "res_entry_rR"))
    checks.append(("entry at the cap", ent_plateau(P), "res_entry_cap"))
    rQ = BD["rQ"]
    checks.append(("floor-entry research at r_Q, lambda_E(r_Q)", lamE(P, rQ), "res_lambda_floor_rQ"))
    checks.append(("floor-entry research at r_Q, lambda_Q(Delta(r_Q))", lamQ(P, Delta(P, rQ)), "res_lambda_floor_rQ"))
    checks.append(("floor-entry research at r_U, lambda_Q(Delta(r_U))", lamQ(P, Delta(P, BD["rU"])), "res_cap"))
    checks.append(("region: Delta(r_A) = k/(1 - tau(r_A))", Delta(P, BD["rA"]), "Delta_rA"))
    checks.append(("region: tau(r_A)", tau(P, BD["rA"]), "tau_rA"))
    checks.append(("region: Delta(r_0)", Delta(P, mpf(6) / 5), "Delta_r0"))
    checks.append(("region: tau(r_N) - 1/2", tau(P, BD["rN"]) - mpf(1) / 2, "margin_tau_rN_half_B"))
    log(f"{'quantity':<52}{'computed':<12}{'registry key':<20}{'registry':<12}match")
    for name, v, rk in checks:
        comp, reg = d6(v), REG.get(rk, "(no row)")
        log(f"{name:<52}{comp:<12}{rk:<20}{reg:<12}{'yes' if same(comp, reg) else 'DIFFERENT'}")
    log("")
    log("Values drawn without a registry row (40 digits, 12 shown)")
    log(f"  floor margin at r_N                          {mp.nstr(phi_rho(P, BD['rN']), 12)}  (negative)")
    log(f"  floor margin at r_U                          {mp.nstr(phi_rho(P, BD['rU']), 12)}  (positive)")
    log(f"  lambda_Q(Delta(r_N)) (rho Delta = 2k)       {mp.nstr(lamQ(P, Delta(P, BD['rN'])), 12)}")
    log(f"  region: Delta^F = k/(1 - M(1/2))             {mp.nstr(P.k / (1 - P.M), 12)}")
    log(f"  region: Delta^N = 2k/rho                     {mp.nstr(2 * P.k / P.rho, 12)}")
    log(f"  region: k/(1 - tau) at tau = 1/2             {mp.nstr(2 * P.k, 12)}")
    log(f"  region: tau(r_F), tau(r_N)                   {mp.nstr(tau(P, BD['rF']), 12)}, {mp.nstr(tau(P, BD['rN']), 12)}")
    log(f"  region: path leaves the window Delta = 1/5 at r = {mp.nstr(frak(P, mpf(1) / 5), 12)}")
    log("")
    log("Order of the marked strengths (coexistence figure): r_A < r_F < r_N < r_J < r_S < r_C: " +
        " < ".join(f"{BF[k_]:.6f}" for k_ in ("rA", "rF", "rN", "rJ", "rS", "rC")))
    log("Research figure: r_R < r_lambda-bar < r_N < r_Q < r_U < r_C: " +
        " < ".join(f"{BF[k_]:.6f}" for k_ in ("rR", "rRbar", "rN", "rQ", "rU", "rC")))
    log("Line breaks: no curve crosses an open interval. Coexistence: R ends at r_F where F starts at the same value;")
    log("  F ends at r_C (closed), the floor segment starts at r_C (open). Q is open at r_N and r_J.")
    log("  Region: 1/2 < tau <= M(1/2), k/(1 - tau) <= Delta <= 2k/rho; the edge tau = 1/2 is open (dotted), the")
    log("  other three are closed (solid). The path enters on the left edge at r_A and leaves on the right edge at r_N.")
    log("  Research: zero research closed at r_N. Recruiting research below the cap on [r_R, r_lambda-bar), at the cap on")
    log("  [r_lambda-bar, r_C], closed at r_C. Floor-entry research on (r_N, r_Q), open at both ends, entry rho; at the cap")
    log("  on (r_C, r_2], open at r_C. Nothing is drawn at rho on [r_Q, r_C], where recruiting research is unique.")
    log("  At (r_N, rho) the filled marker belongs to zero research; at (r_C, cap) it belongs to recruiting research.")
    log("  Markers: filled = the value is attained at that strength; open = approached, not attained.")
    log("  Nodes (black): r_0, 1.55, 1.60, 1.65, r_1 = 3, r_2 = 18/5.")
    log("Fonts: manuscript figures use STIXGeneral text and STIX math (TrueType, Type 42).")
    log("  Slide figures use Archivo (Regular, from slot/manuscript/fonts/) with STIX math; in-figure text and axes")
    log("  are ink (#1e2530) with tick labels in the muted grey (#5b6573). The Archivo files are TrueType, so the")
    log("  PDF embeds a TrueType font (Type 42) directly.")
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
        log(f"  {sha}  {OUT_LABEL}/{path.name}  ({path.stat().st_size} bytes)")
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
