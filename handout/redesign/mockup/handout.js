/* Handout page script for the mockups: theme, font pairing, tabs, math, folds, figure, errors.
 * ES2019, no modules, no network. Exposes window.CCC.page for the checks.
 */
(function () {
  'use strict';
  var CCC = (window.CCC = window.CCC || {});
  var errors = (window.__errors = window.__errors || []);
  window.addEventListener('error', function (e) { errors.push(String(e.message)); });
  window.addEventListener('unhandledrejection', function (e) { errors.push(String(e.reason)); });
  var doc = document.documentElement;
  var KEY = doc.dataset.dir || 'ccc';
  var store = { get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }

  /* ---------- theme ---------- */
  function setTheme(t) {
    doc.dataset.theme = t;
    $$('[data-theme-toggle]').forEach(function (b) { b.textContent = t === 'dark' ? 'Light' : 'Dark'; b.setAttribute('aria-pressed', String(t === 'dark')); });
    store.set(KEY + '-theme', t);
    document.dispatchEvent(new CustomEvent('ccc:theme'));
  }
  var q = new URLSearchParams(location.search);
  setTheme(q.get('theme') || store.get(KEY + '-theme') || doc.dataset.theme || 'light');
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-theme-toggle]');
    if (b) setTheme(doc.dataset.theme === 'dark' ? 'light' : 'dark');
  });

  /* ---------- font pairing ---------- */
  function setPairing(p) {
    doc.dataset.pairing = p;
    $$('[data-pairing-choice]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.pairingChoice === p)); });
    var sel = $('select[data-pairing-select]'); if (sel) sel.value = p;
    var why = $('[data-pairing-why]'), btn = $('[data-pairing-choice="' + p + '"]');
    if (why && btn) why.textContent = btn.title;
    store.set(KEY + '-pairing', p);
  }
  var pairings = $$('[data-pairing-choice]').map(function (b) { return b.dataset.pairingChoice; });
  var first = (q.get('pairing') || store.get(KEY + '-pairing') || doc.dataset.pairing || pairings[0]);
  if (pairings.indexOf(first) < 0) first = pairings[0];
  if (first) setPairing(first);
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-pairing-choice]');
    if (b) setPairing(b.dataset.pairingChoice);
  });
  document.addEventListener('change', function (e) { if (e.target.matches && e.target.matches('select[data-pairing-select]')) setPairing(e.target.value); });

  /* ---------- tabs (brief / paper / talk) ---------- */
  function showTab(name, push) {
    $$('[role=tab]').forEach(function (t) {
      var on = t.dataset.tab === name;
      t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
    });
    $$('[role=tabpanel]').forEach(function (p) { p.hidden = p.dataset.tab !== name; });
    doc.dataset.tab = name;
    if (push) history.replaceState(null, '', '#' + (name === 'brief' ? '' : 'tab-' + name));
    var panel = $('[role=tabpanel][data-tab="' + name + '"]');
    if (panel && name === 'paper') mountViewer(panel);
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[role=tab]');
    if (t) { e.preventDefault(); showTab(t.dataset.tab, true); t.focus(); }
    var j = e.target.closest && e.target.closest('[data-open-tab]');
    if (j) { e.preventDefault(); showTab(j.dataset.openTab, true); var tt = $('[role=tab][data-tab="' + j.dataset.openTab + '"]'); if (tt) tt.focus(); }
  });
  document.addEventListener('keydown', function (e) {
    var t = e.target.closest && e.target.closest('[role=tab]');
    if (!t) return;
    var tabs = $$('[role=tab]'), i = tabs.indexOf(t);
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      e.preventDefault();
      var n = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      showTab(n.dataset.tab, true); n.focus();
    }
  });
  var mounted = false;
  function mountViewer(panel) {
    if (mounted) return; mounted = true;
    var host = $('[data-viewer]', panel);
    if (host && host.dataset.src) host.innerHTML = '<iframe title="Manuscript, inline viewer" src="' + host.dataset.src + '#view=FitH"></iframe>';
  }
  var hashTab = (location.hash.match(/^#tab-([a-z]+)$/) || [])[1];
  showTab(hashTab && $('[role=tab][data-tab="' + hashTab + '"]') ? hashTab : 'brief', false);

  /* ---------- math: minimal delimiter walker for \( \) and \[ \] ---------- */
  function renderMath(root) {
    if (!window.katex) { errors.push('KaTeX unavailable'); return; }
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p || /^(SCRIPT|STYLE|TEXTAREA|CODE|PRE)$/.test(p.nodeName) || p.closest('.katex')) return NodeFilter.FILTER_REJECT;
        return /\\[\(\[]/.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });
    var nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(function (n) {
      var text = n.nodeValue, frag = document.createDocumentFragment(), i = 0;
      var re = /\\\((.+?)\\\)|\\\[([\s\S]+?)\\\]/g, m;
      while ((m = re.exec(text))) {
        if (m.index > i) frag.appendChild(document.createTextNode(text.slice(i, m.index)));
        var span = document.createElement(m[2] !== undefined ? 'div' : 'span');
        span.className = m[2] !== undefined ? 'math-display' : 'math-inline';
        try { katex.render((m[1] !== undefined ? m[1] : m[2]).replace(/&amp;/g, '&'), span, { displayMode: m[2] !== undefined, throwOnError: true, trust: false }); }
        catch (e) { errors.push('math: ' + e.message); span.textContent = m[0]; span.classList.add('math-error'); }
        frag.appendChild(span);
        i = m.index + m[0].length;
      }
      if (i < text.length) frag.appendChild(document.createTextNode(text.slice(i)));
      n.parentNode.replaceChild(frag, n);
    });
  }

  /* ---------- figure 1 ---------- */
  function mountFigure() {
    var host = $('#chart-fig1'); if (!host) return;
    try { CCC.charts.twoReturns(host, { mode: 'handout', width: 520, height: 300 }); }
    catch (e) { errors.push('fig1: ' + e.message); }
  }
  document.addEventListener('ccc:theme', function () {});

  /* ---------- progress and section highlight ---------- */
  function progress() {
    var bar = $('[data-progress]'); if (!bar) return;
    var h = document.documentElement, p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    bar.style.transform = 'scaleX(' + p.toFixed(4) + ')';
  }
  addEventListener('scroll', progress, { passive: true }); progress();

  /* ---------- details folds: hash opens enclosing fold ---------- */
  function openForHash() {
    var id = location.hash.slice(1); if (!id) return;
    var el = document.getElementById(id); if (!el) return;
    var d = el.closest('details'); while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); }
  }
  addEventListener('hashchange', openForHash);

  /* ---------- boot ---------- */
  function boot() {
    renderMath(document.body);
    mountFigure();
    openForHash();
    var ft = CCC.closed && CCC.closed.selfTest ? CCC.closed.selfTest() : { ok: false };
    if (!ft.ok) errors.push('closed-form self-test failed');
    CCC.page = {
      selfCheck: function () {
        return {
          errors: errors.slice(), mathErrors: $$('.math-error, .katex-error').length, katex: $$('.katex').length,
          theme: doc.dataset.theme, pairing: doc.dataset.pairing, tab: doc.dataset.tab,
          placeholders: $$('.q').length, selfTest: ft.ok,
          fonts: Array.prototype.slice.call(document.fonts).filter(function (f) { return f.status === 'loaded'; }).map(function (f) { return f.family + ' ' + f.weight + ' ' + f.style; })
        };
      },
      showTab: showTab, setTheme: setTheme, setPairing: setPairing
    };
    CCC.ready = document.fonts.ready.then(function () { return CCC.page.selfCheck(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
