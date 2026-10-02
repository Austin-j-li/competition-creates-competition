/* Deck engine for the mockups. Slides are <section class="slide"> elements in the page.
 * Fixed 1600 x 900 design surface scaled to the window. Reveals use [data-step].
 * Keys: Right/Space next, Left previous, Home/End, O overview, N notes, T theme, F fullscreen,
 * R reset, Esc back from a backup or close a panel. Exposes window.DECK for the checks.
 * ES2019, no modules, no network.
 */
(function () {
  'use strict';
  var CCC = (window.CCC = window.CCC || {});
  var errors = (window.__errors = window.__errors || []);
  window.addEventListener('error', function (e) { errors.push(String(e.message)); });
  window.addEventListener('unhandledrejection', function (e) { errors.push(String(e.reason)); });
  var doc = document.documentElement, D = window.CCC_DATA;
  var KEY = doc.dataset.dir || 'ccc';
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var motion = matchMedia('(prefers-reduced-motion: reduce)');

  var slides = $$('.slide');
  var ids = slides.map(function (s) { return s.id; });
  var index = 0, step = 0, returnTo = null;
  var steps = {};
  var widgets = {};
  var NOTES = window.CCC_NOTES || {};
  var FRAMES = (D && D.frames) || [];
  var PARTS = (D && D.parts) || [];

  /* ---------- theme and pairing ---------- */
  function setTheme(t) {
    doc.dataset.theme = t;
    $$('[data-theme-toggle]').forEach(function (b) { b.textContent = t === 'dark' ? 'Light' : 'Projector'; b.setAttribute('aria-pressed', String(t === 'dark')); });
    store.set(KEY + '-deck-theme', t);
    renderCurrent();
  }
  function setPairing(p) {
    doc.dataset.pairing = p;
    $$('[data-pairing-choice]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.pairingChoice === p)); });
    store.set(KEY + '-deck-pairing', p);
  }
  var q = new URLSearchParams(location.search);
  var pairings = $$('[data-pairing-choice]').map(function (b) { return b.dataset.pairingChoice; });
  var p0 = q.get('pairing') || store.get(KEY + '-deck-pairing') || doc.dataset.pairing || pairings[0];
  if (pairings.indexOf(p0) < 0) p0 = pairings[0];
  if (p0) setPairing(p0);

  /* ---------- stage ---------- */
  function scale() {
    var s = Math.max(0.05, Math.min(innerWidth / 1600, (innerHeight - 96) / 900));
    $('#stage').style.setProperty('--stage-scale', String(s));
    return s;
  }
  addEventListener('resize', scale); scale();

  /* ---------- math ---------- */
  function math(root) {
    $$('[data-tex]', root || document).forEach(function (el) {
      if (el.dataset.done) return;
      try { if (!window.katex) throw new Error('KaTeX unavailable'); katex.render(el.dataset.tex, el, { displayMode: el.dataset.display === 'true', throwOnError: true, trust: false }); el.dataset.done = '1'; }
      catch (e) { errors.push('math: ' + e.message); el.textContent = el.dataset.tex; el.classList.add('math-error'); }
    });
  }

  /* ---------- navigation ---------- */
  function maxStep(i) { var s = slides[i === undefined ? index : i]; return Math.max(0, Math.max.apply(null, [0].concat($$('[data-step]', s).map(function (e) { return Number(e.dataset.step); })))); }
  function updateReveals() {
    var s = slides[index];
    $$('[data-step]', s).forEach(function (el) { var on = Number(el.dataset.step) <= step; el.classList.toggle('shown', on); el.setAttribute('aria-hidden', String(!on)); });
    steps[index] = step;
    var w = widgets[s.id]; if (w && w.onStep) w.onStep(step);
    var num = s.dataset.num, backup = s.dataset.backup === 'true';
    /* The PDF counts 16 main frames: F0 and the F10b build carry noframenumbering. */
    s.style.setProperty('--progress', backup ? '100%' : (100 * Number(num) / 16).toFixed(1) + '%');
    $('#counter').textContent = backup ? num : num + ' / 16';
    $('#progress-label').textContent = maxStep() ? 'step ' + (step + 1) + ' of ' + (maxStep() + 1) : (backup ? 'backup' : (s.dataset.minutes || '') + ' min');
    $('#previous').disabled = index === 0 && step === 0;
    $('#next').disabled = index === slides.length - 1 && step === maxStep();
    $('#return').hidden = !backup;
    $$('#rail li').forEach(function (li) {
      var part = li.dataset.part, cur = s.dataset.part;
      li.classList.toggle('current', !backup && part === cur);
      li.classList.toggle('done', !backup && Number(part) < Number(cur));
      li.classList.toggle('backup-current', backup && part === 'B');
    });
  }
  function go(id, opts) {
    opts = opts || {};
    var i = typeof id === 'number' ? id : ids.indexOf(id);
    if (i < 0) return;
    var prev = index;
    if (slides[i].dataset.backup === 'true' && slides[prev].dataset.backup !== 'true' && !opts.history) returnTo = { index: prev, step: step };
    index = i;
    step = Math.max(0, Math.min(maxStep(i), opts.step !== undefined ? opts.step : (steps[i] || 0)));
    slides.forEach(function (s, j) { var on = j === i; s.classList.toggle('active', on); s.setAttribute('aria-hidden', String(!on)); s.inert = !on; });
    updateReveals();
    renderCurrent();
    if (!opts.history) history.replaceState(null, '', '#' + slides[i].id);
    $('#announcer').textContent = (slides[i].dataset.title || '') + ', slide ' + slides[i].dataset.num;
    $('#stage').focus({ preventScroll: true });
  }
  function next() { if (step < maxStep()) { step++; updateReveals(); return; } if (index < slides.length - 1 && slides[index + 1].dataset.backup !== 'true') go(index + 1, { step: 0 }); }
  function previous() { if (step > 0) { step--; updateReveals(); return; } if (index > 0 && slides[index].dataset.backup !== 'true') go(index - 1, { step: maxStep(index - 1) }); }
  function back() { if (returnTo) { var t = returnTo; returnTo = null; go(t.index, { step: t.step }); } else { var o = slides[index].dataset.origin; if (o) go(o); } }
  function renderCurrent() { var w = widgets[slides[index].id]; if (w && w.render) { try { w.render(); } catch (e) { errors.push(slides[index].id + ': ' + e.message); } } }
  function reset() { step = 0; var w = widgets[slides[index].id]; if (w && w.reset) w.reset(); updateReveals(); }

  /* ---------- panels ---------- */
  function panel(title, html) { $('#panel-title').textContent = title; $('#panel-body').innerHTML = html; $('#panel').showModal(); }
  function overview() {
    var built = {}; slides.forEach(function (s) { built[s.id] = true; });
    var html = '<p class="muted small">All 47 frames of the Beamer deck in their order. Built in this mockup: ' + slides.length + '. Others are listed to show the organisation.</p><div class="overview">';
    FRAMES.forEach(function (f) {
      var on = built[f.id];
      html += '<button class="ov' + (on ? '' : ' off') + (f.backup ? ' backup' : '') + '" data-goto="' + esc(f.id) + '" ' + (on ? '' : 'disabled') + '><small>' + esc(f.num) + (f.part && !f.backup ? ' · ' + esc(partName(f.part)) : '') + (f.backup ? ' · from ' + esc(f.origin) : '') + '</small>' + esc(f.title) + '</button>';
    });
    panel('The talk', html + '</div>');
  }
  function partName(p) { var x = PARTS.filter(function (q) { return String(q.n) === String(p); })[0]; return x ? x.name : ''; }
  function notes() {
    var s = slides[index], n = NOTES[s.id] || {};
    panel('Speaker notes', '<p class="muted small">' + esc(n.timing || (s.dataset.backup === 'true' ? 'if asked' : (s.dataset.minutes || '') + ' min')) + '</p><h3>' + esc(s.dataset.title || '') + '</h3><div class="notes">' + (n.html || '<p>No block in script.tex; see structure-plan §9.</p>') + '</div><p class="muted small">Source: ' + esc(n.source || 'script.tex') + '</p>');
  }
  function help() { panel('Controls', '<div class="help"><kbd>→ / Space</kbd><span>next step, then next slide</span><kbd>←</kbd><span>previous</span><kbd>O</kbd><span>overview</span><kbd>N</kbd><span>speaker notes</span><kbd>T</kbd><span>theme</span><kbd>F</kbd><span>fullscreen</span><kbd>R</kbd><span>reset the slide</span><kbd>Esc</kbd><span>back from a backup, or close</span><kbd>Home / End</kbd><span>title / last</span></div>'); }
  function fullscreen() { try { if (document.fullscreenElement) document.exitFullscreen(); else doc.requestFullscreen(); } catch (e) { panel('Fullscreen', '<p>Use the browser control.</p>'); } }
  $('#close-panel').onclick = function () { $('#panel').close(); };
  $('#panel').addEventListener('click', function (e) { if (e.target === $('#panel')) $('#panel').close(); });
  document.addEventListener('click', function (e) {
    var g = e.target.closest && e.target.closest('[data-goto]'); if (g && !g.disabled) { if ($('#panel').open) $('#panel').close(); go(g.dataset.goto); }
    var b = e.target.closest && e.target.closest('[data-back]'); if (b) back();
    var t = e.target.closest && e.target.closest('[data-theme-toggle]'); if (t) setTheme(doc.dataset.theme === 'dark' ? 'light' : 'dark');
    var p = e.target.closest && e.target.closest('[data-pairing-choice]'); if (p) setPairing(p.dataset.pairingChoice);
    if (e.target.closest && e.target.closest('#overview')) overview();
    if (e.target.closest && e.target.closest('#notes')) notes();
    if (e.target.closest && e.target.closest('#help')) help();
    if (e.target.closest && e.target.closest('#fullscreen')) fullscreen();
    if (e.target.closest && e.target.closest('#previous')) previous();
    if (e.target.closest && e.target.closest('#next')) next();
    if (e.target.closest && e.target.closest('#return')) back();
  });
  document.addEventListener('keydown', function (e) {
    if ($('#panel').open) return;
    if (e.target.matches && e.target.matches('input, select, textarea, button, a')) { if (e.key === ' ' || e.key === 'Enter' || e.key === 'ArrowLeft' || e.key === 'ArrowRight') return; }
    var map = { ArrowRight: next, PageDown: next, ' ': next, ArrowLeft: previous, PageUp: previous, Home: function () { go(0, { step: 0 }); }, End: function () { go(ids.indexOf($$('.slide:not([data-backup=true])').slice(-1)[0].id), { step: 0 }); }, o: overview, n: notes, t: function () { setTheme(doc.dataset.theme === 'dark' ? 'light' : 'dark'); }, f: fullscreen, r: reset, Escape: function () { if (slides[index].dataset.backup === 'true') back(); }, '?': help };
    if (map[e.key]) { e.preventDefault(); map[e.key](); }
  });

  /* ---------- widgets ---------- */
  var P = CCC.closed.inputs();
  widgets.f6 = {
    chart: null,
    render: function () { var host = $('#x1'); if (!host) return; this.chart = CCC.charts.twoReturns(host, { mode: 'deck', width: 560, height: 330, start: host.dataset.cursor ? Number(host.dataset.cursor) : P.r_weak }); },
    reset: function () { var host = $('#x1'); if (host) delete host.dataset.cursor; this.render(); }
  };
  widgets.f8 = {
    chart: null, r: P.r_strong,
    render: function () {
      var host = $('#x2'); if (!host) return;
      this.chart = CCC.charts.thresholds(host, { width: 640, height: 330 });
      var slider = $('#x2-r'); if (slider) { slider.min = '1.05'; slider.max = '3.8'; slider.step = '0.01'; slider.value = String(this.r); }
      this.update(this.r);
    },
    update: function (r) {
      this.r = r; var c = this.chart.update(r);
      $('#x2-r-value').textContent = r.toFixed(2);
      var f = function (x) { return x.toFixed(3); };
      var chip = function (ch) { return '<span class="chip ' + (ch.ok ? 'ok' : 'no') + '">' + esc(ch.label) + ' ' + (ch.ok ? 'holds' : 'fails') + ' (' + (ch.margin >= 0 ? '+' : '') + ch.margin.toFixed(3) + ')</span>'; };
      $('#x2-readout').innerHTML = '<p>At r = <b>' + r.toFixed(2) + '</b>: B<sub>r</sub>(M) = <b>' + f(c.B_M) + '</b>, B<sub>r</sub>(½) = <b>' + f(c.B_prior) + '</b>, B<sub>r</sub>(m) = <b>' + f(c.B_m) + '</b></p>' +
        '<p class="chips">' + chip(c.chips.A1) + chip(c.chips.A2a) + chip(c.chips.A2b) + '</p>' +
        '<p class="muted small">Fixed-order calculation of the closed forms with only r moving; not an equilibrium solver. Registry values at r₀ and r₁ are on the slide text.</p>';
    },
    reset: function () { this.r = P.r_strong; this.render(); }
  };
  document.addEventListener('input', function (e) { if (e.target.id === 'x2-r') widgets.f8.update(Number(e.target.value)); });
  widgets.f10 = {
    onStep: function (s) { var t = $('#t3'); if (t) t.classList.toggle('with-r2', s >= 1); $('#f10 .takeaway-a').hidden = s >= 1; $('#f10 .takeaway-b').hidden = s < 1; var nav = $('#f10 .nav'); if (nav) nav.hidden = s < 1; }
  };

  /* ---------- rail ---------- */
  $('#rail').innerHTML = PARTS.map(function (p) { return '<li data-part="' + esc(p.n) + '"><span>' + esc(p.name) + '</span></li>'; }).join('');

  /* ---------- boot ---------- */
  math();
  setTheme(q.get('theme') || store.get(KEY + '-deck-theme') || doc.dataset.theme || 'light');
  var opening = location.hash.slice(1);
  go(ids.indexOf(opening) >= 0 ? opening : 0, { history: true, step: 0 });
  var ft = CCC.closed.selfTest(); if (!ft.ok) errors.push('closed-form self-test failed');
  window.DECK = {
    go: go, next: next, previous: previous, back: back, reset: reset, setTheme: setTheme, setPairing: setPairing,
    selfCheck: function () {
      return { errors: errors.slice(), mathErrors: $$('.math-error, .katex-error').length, katex: $$('.katex').length, active: slides[index].id, step: step, slides: slides.length, theme: doc.dataset.theme, pairing: doc.dataset.pairing, selfTest: ft.ok, scale: scale(),
        fonts: Array.prototype.slice.call(document.fonts).filter(function (f) { return f.status === 'loaded'; }).map(function (f) { return f.family + ' ' + f.weight + ' ' + f.style; }) };
    }
  };
  window.DECK.ready = document.fonts.ready.then(function () { return window.DECK.selfCheck(); });
})();
