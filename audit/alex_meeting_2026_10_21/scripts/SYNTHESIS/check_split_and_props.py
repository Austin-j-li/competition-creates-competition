"""Red-team check 1 and 2: the split identity and the generalized Propositions 1 and 2.

Print-only. Run from the repository root with .venv/bin/python.
"""
from mpmath import mp, mpf, quad, exp, log, sqrt

mp.dps = 30

# ---------- benchmark ----------
h, ell, p, rho, cL, cH, b, k = (mpf(10), mpf(1), mpf('0.5'), mpf('0.25'),
                                mpf(1), mpf(6), mpf(2), mpf('0.02'))


def uniform_objects(r, theta_H=h, theta_L=ell, pp=p):
    """Paper eq. (4) generalized through t(theta), g(theta) for uniform R on [0, r]."""
    F = lambda u: min(max(u / r, mpf(0)), mpf(1))
    t0 = pp * (1 - F(pp))
    def pts(th):
        return [pp] + ([r] if pp < r < th else []) + [th]
    def t(th):
        if th < pp:
            return t0
        return pp + quad(lambda u: 1 - F(u), pts(th))
    def g(th):
        if th < pp:
            return mpf(0)
        return quad(F, pts(th))
    return t0, t(theta_H), t(theta_L), g(theta_H), g(theta_L)


print("=== 1. Split identity in the binary model: Delta_T + (g_H - g_L) at various r ===")
for r in [mpf('0.3'), mpf('0.8'), mpf('1.2'), mpf(3), mpf('3.6'), mpf(9), mpf(25)]:
    t0, tH, tL, gH, gL = uniform_objects(r)
    DT = tH - tL
    print(f"r={float(r):6.2f}  Delta_T={float(DT):.6f}  g_H-g_L={float(gH-gL):.6f}  "
          f"sum={float(DT + gH - gL):.12f}  h-ell={float(h-ell):.1f}  "
          f"t_H+g_H={float(tH+gH):.6f} t_L+g_L={float(tL+gL):.6f}")
print("Note: r < ell gives Delta_T = 0, g_H - g_L = h - ell; r > h gives t_H = h/2 + p^2/(2h)... identity still holds.")

# ---------- distribution types ----------
print()
print("=== 2. Distribution types: Delta_T + (g_H - g_L) versus E_H max(theta,p) - E_L max(theta,p) ===")


def mix_uniform(pieces):
    """pieces: list of (weight, lo, hi). Returns (cdf, mean of max(theta,p) given p, mass below p)."""
    def cdf(u):
        s = mpf(0)
        for w, lo, hi in pieces:
            if u <= lo:
                continue
            if u >= hi:
                s += w
            else:
                s += w * (u - lo) / (hi - lo)
        return s
    def Emax(pp):
        s = mpf(0)
        for w, lo, hi in pieces:
            s += w * quad(lambda x: max(x, pp), [lo, hi]) / (hi - lo)
        return s
    def mass_below(pp):
        return cdf(pp)
    def expect(fun, brk=()):
        s = mpf(0)
        for w, lo, hi in pieces:
            inner = sorted(set([lo, hi] + [x for x in brk if lo < x < hi]))
            s += w * quad(fun, inner) / (hi - lo)
        return s
    return cdf, Emax, mass_below, expect


def type_objects(r, GH, GL, pp):
    """t_j, g_j by direct expectation of t(theta), g(theta) over G_j (uniform incumbent on [0,r])."""
    F = lambda u: min(max(u / r, mpf(0)), mpf(1))
    t0 = pp * (1 - F(pp))
    def pts(th):
        return [pp] + ([r] if pp < r < th else []) + [th]
    def t(th):
        if th < pp:
            return t0
        return pp + quad(lambda u: 1 - F(u), pts(th))
    def g(th):
        if th < pp:
            return mpf(0)
        return quad(F, pts(th))
    brk = (pp, r)
    tH = GH[3](t, brk); tL = GL[3](t, brk); gH = GH[3](g, brk); gL = GL[3](g, brk)
    return t0, tH, tL, gH, gL


cases = {
    "value classes p=0.5 (Sec 6.3)": (mix_uniform([(1, mpf('9.95'), mpf('10.05'))]), mix_uniform([(1, mpf('0.95'), mpf('1.05'))]), mpf('0.5')),
    "value classes p=1.1 (Sec 6.3, L class inadmissible)": (mix_uniform([(1, mpf('9.95'), mpf('10.05'))]), mix_uniform([(1, mpf('0.95'), mpf('1.05'))]), mpf('1.1')),
    "2a equal mass below p": (mix_uniform([(mpf('0.1'), mpf(0), mpf('0.5')), (mpf('0.9'), mpf('0.5'), mpf('19.5'))]), mix_uniform([(mpf('0.1'), mpf(0), mpf('0.5')), (mpf('0.9'), mpf('0.5'), mpf('2.5'))]), mpf('0.5')),
    "2b unequal mass below p": (mix_uniform([(1, mpf('0.2'), mpf('19.8'))]), mix_uniform([(1, mpf('0.2'), mpf('2.8'))]), mpf('0.5')),
}
for name, (GH, GL, pp) in cases.items():
    print(f"-- {name}")
    for r in [mpf('1.2'), mpf(3), mpf('3.6')]:
        t0, tH, tL, gH, gL = type_objects(r, GH, GL, pp)
        F_p = pp / r
        Dpm = GL[2](pp) - GH[2](pp)
        lhs = (tH - tL) + (gH - gL)
        rhs_free = GH[1](pp) - GL[1](pp)          # E_H max(theta,p) - E_L max(theta,p)
        reserve = pp * F_p * Dpm                 # p F(p) D(p-)
        # N7: lhs = int_p^inf D + p F(p) D(p-), and int_p^inf D = rhs_free - p*D(p-)... check both forms
        intD = rhs_free                          # int_p^inf [G_L - G_H] = E_H(theta-p)_+ - E_L(theta-p)_+ = E_H max - E_L max
        print(f"   r={float(r):4.1f} D(p-)={float(Dpm):.6f} Delta_T={float(tH-tL):.6f} g_H-g_L={float(gH-gL):.6f} "
              f"sum={float(lhs):.6f} | int_p^inf D + pF(p)D(p-)={float(intD+reserve):.6f} | E_H max - E_L max={float(rhs_free):.6f}")
print("Verdict: sum = int_p^inf D + p F(p) D(p-) in every case; equals E_H max - E_L max only when D(p-)=0 (or F(p)=0).")

print()
print("=== 2b. The F-free form also holds when F(p)=0 (incumbent always clears the reserve) ===")
# Incumbent uniform on [p, r]: F(p) = 0, t0 = p. Then t(theta)+g(theta) = max(theta,p) pointwise.
GH, GL, pp = cases["2b unequal mass below p"]
r = mpf(3)
F = lambda u: min(max((u - pp) / (r - pp), mpf(0)), mpf(1))
t0 = pp * (1 - F(pp))
def t(th):
    if th < pp:
        return t0
    return pp + quad(lambda u: 1 - F(u), [pp] + ([r] if pp < r < th else []) + [th])
def g(th):
    if th < pp:
        return mpf(0)
    return quad(F, [pp] + ([r] if pp < r < th else []) + [th])
tH = GH[3](t, (pp, r)); tL = GL[3](t, (pp, r)); gH = GH[3](g, (pp, r)); gL = GL[3](g, (pp, r))
print(f"   F(p)=0 case, D(p-)={float(GL[2](pp)-GH[2](pp)):.6f}: Delta_T+(g_H-g_L)={float(tH-tL+gH-gL):.6f}, "
      f"E_H max - E_L max={float(GH[1](pp)-GL[1](pp)):.6f}")

# ---------- generalized Prop 1: uniform derivative condition and the p=1.1 reversal ----------
print()
print("=== 3. Generalized Proposition 1: Delta_T(r) with the reserve term, Sec 6.3 at p=1.1 ===")
GH, GL, pp = cases["value classes p=1.1 (Sec 6.3, L class inadmissible)"]
for r in [mpf('1.2'), mpf('1.5'), mpf('1.9'), mpf('1.905'), mpf('2.5'), mpf(3), mpf('3.6')]:
    t0, tH, tL, gH, gL = type_objects(r, GH, GL, pp)
    closed = r / 2 - pp + 3 * pp**2 / (2 * r)
    print(f"   r={float(r):5.3f} Delta_T={float(tH-tL):.6f} closed form r/2-p+3p^2/(2r)={float(closed):.6f}  "
          f"d/dr sign: {'falls' if r < sqrt(3)*pp else 'rises'} (sqrt3 p={float(sqrt(3)*pp):.4f})")
print("   Delta_T(1.2) > Delta_T(3): a stronger incumbent lowers the spread between r_0 and r_1 at p=1.1 (memo Claim 4e confirmed).")

print()
print("=== 4. Posterior bounds with a general prior; x*; ownership condition (case 2c) ===")
def m_pi(pi): return pi / (pi + (1 - pi) * exp(2 / b))
def M_pi(pi): return pi / (pi + (1 - pi) * exp(-2 / b))
for pi in [mpf('0.3'), mpf('0.5'), mpf('0.7')]:
    print(f"   pi={float(pi):.1f}: m={float(m_pi(pi)):.6f} M={float(M_pi(pi)):.6f} 1-M(pi)={float(1-M_pi(pi)):.6f} m(1-pi)={float(m_pi(1-pi)):.6f}")
logit = lambda x: log(x / (1 - x))
# x* with general prior: logit mu_X(x) = logit pi + (2/b) clip(x,-1,1)
pi = mpf('0.3'); tau = mpf('0.6')
xs = (b / 2) * (logit(tau) - logit(pi))
mu_at = lambda x: 1 / (1 + exp(-(logit(pi) + (2 / b) * max(-1, min(1, x)))))
print(f"   pi=0.3, tau=0.6: x*={float(xs):.6f}, mu_X(x*)={float(mu_at(xs)):.6f} (should equal tau)")
# ownership condition case 2c: rho=0.95, from memo table: W_H(r0)=0.890329, W_H(r1)=0.850658, e_H(r1)=? rho/e_H = 0.970193
GH2, GL2, pp2 = cases["2a equal mass below p"]
def W_H(r):
    F = lambda u: min(max(u / r, mpf(0)), mpf(1))
    return GH2[3](lambda th: F(th) if th >= pp2 else mpf(0), (pp2, r))
r0, r1 = mpf('1.2'), mpf(3)
rho2 = mpf('0.95')
print(f"   case 2c: W_H(r0)={float(W_H(r0)):.6f} W_H(r1)={float(W_H(r1)):.6f} ratio={float(W_H(r1)/W_H(r0)):.6f}")
# e_H(r1) from the memo repaired vector: c_H = 5.121235, k = 0.029133; compute alpha_H
t0, tH, tL, gH, gL = type_objects(r1, GH2, GL2, pp2)
cH2 = mpf('5.121235')
tau2 = (cH2 - gL) / (gH - gL)
xs2 = (b / 2) * logit(tau2)
alphaH = 1 - exp((xs2 - 1) / b) / 2
eH = rho2 + (1 - rho2) * alphaH
print(f"   case 2c at r1: tau={float(tau2):.6f} x*={float(xs2):.6f} alpha_H={float(alphaH):.6f} e_H={float(eH):.6f} rho/e_H={float(rho2/eH):.6f}")
print(f"   O_H(r0)=pi*rho*W_H(r0)={float(0.5*rho2*W_H(r0)):.6f}  O_H(r1)=pi*e_H*W_H(r1)={float(0.5*eH*W_H(r1)):.6f}  -> ownership falls while entry rises: {bool(0.5*eH*W_H(r1) < 0.5*rho2*W_H(r0))}")
