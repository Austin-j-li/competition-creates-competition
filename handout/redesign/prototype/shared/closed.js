/* Closed forms of the benchmark model at declared primitives with only r moving.
 * Same formula block as the handout explorer (handout/explorer.js, handout/crosscheck.py):
 *   t_0 = p (1 - p/r);  t_H = r/2 + p^2/(2r);  t_L = ell - (ell^2 - p^2)/(2r)
 *   g_H = h - r/2 - p^2/(2r);  g_L = (ell^2 - p^2)/(2r);  Delta_T = (r - ell)^2/(2r)
 *   m = 1/(1 + exp(2/b));  M = 1 - m;  B(mu) = g_L + mu (g_H - g_L)
 *   chips: A1 = B(m) - c_L; A2a = c_H - B(1/2); A2b = B(M) - c_H;
 *          A3_no_trade = k - Delta_T; A3_full = (1 - 1/b) rho m Delta_T - k
 * This is a fixed-order calculation. It never solves for an equilibrium.
 * ES2019, no modules. Exposes window.CCC.closed.
 */
(function () {
  'use strict';
  var CCC = (window.CCC = window.CCC || {});

  function inputs() {
    var src = (window.CCC_DATA && window.CCC_DATA.inputs) || {};
    var keys = ['h', 'ell', 'p', 'rho', 'c_L', 'c_H', 'b', 'k', 'r_weak', 'r_strong', 'r_collapse'];
    var P = {};
    keys.forEach(function (k) {
      P[k] = Number(src[k]);
      if (!isFinite(P[k])) throw new Error('closed forms: missing input ' + k);
    });
    return P;
  }

  function closedForms(P, r) {
    var h = P.h, ell = P.ell, p = P.p, rho = P.rho, c_L = P.c_L, c_H = P.c_H, b = P.b, k = P.k;
    var t_0 = p * (1 - p / r);
    var t_H = r / 2 + p * p / (2 * r);
    var t_L = ell - (ell * ell - p * p) / (2 * r);
    var g_H = h - r / 2 - p * p / (2 * r);
    var g_L = (ell * ell - p * p) / (2 * r);
    var Delta_T = (r - ell) * (r - ell) / (2 * r);
    var m = 1 / (1 + Math.exp(2 / b));
    var M = 1 - m;
    var B = function (mu) { return g_L + mu * (g_H - g_L); };
    var chips = {
      A1: { ok: c_L < B(m), margin: B(m) - c_L, label: 'low-cost floor' },
      A2a: { ok: B(0.5) < c_H, margin: c_H - B(0.5), label: 'high-cost window, prior' },
      A2b: { ok: c_H < B(M), margin: B(M) - c_H, label: 'high-cost window, best price' },
      A3_no_trade: { ok: Delta_T < k, margin: k - Delta_T, label: 'trading-cost window, weak' },
      A3_full: { ok: (1 - 1 / b) * rho * m * Delta_T > k, margin: (1 - 1 / b) * rho * m * Delta_T - k, label: 'trading-cost window, strong' }
    };
    return { r: r, inDomain: p < ell && ell < r && r < h, t_0: t_0, t_H: t_H, t_L: t_L, g_H: g_H, g_L: g_L,
      Delta_T: Delta_T, m: m, M: M, B_m: B(m), B_prior: B(0.5), B_M: B(M), chips: chips };
  }

  /* Self-test against the registry: the closed forms at r0 and r1 must reproduce
   * base_spread_* and base_profit_prior_* to 1e-9. */
  function selfTest() {
    var D = window.CCC_DATA, P = inputs(), out = { ok: true, checks: [] };
    var pairs = [['base_spread_weak', P.r_weak, 'Delta_T'], ['base_spread_strong', P.r_strong, 'Delta_T'],
      ['base_profit_prior_weak', P.r_weak, 'B_prior'], ['base_profit_prior_strong', P.r_strong, 'B_prior'],
      ['base_m', P.r_weak, 'm'], ['base_M', P.r_weak, 'M']];
    pairs.forEach(function (t) {
      var reg = D.registry[t[0]];
      var got = closedForms(P, t[1])[t[2]];
      var ok = !!reg && Math.abs(Number(reg.value) - got) < 1e-9;
      out.checks.push({ key: t[0], ok: ok, got: got, registry: reg && reg.value });
      if (!ok) out.ok = false;
    });
    return out;
  }

  CCC.closed = { inputs: inputs, closedForms: closedForms, selfTest: selfTest };
})();
