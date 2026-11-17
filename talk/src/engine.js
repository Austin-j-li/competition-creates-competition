/* The talk's engine: state (page, step) in the hash, keys, steps, figures, carries, backups, overview, print,
   reading view. No framework. Public surface (window.TALK):

   TALK.figure(id, spec)    register a figure module; spec.mount(el, ctx), spec.setStep(step, opts).
                            Each mount gets its own instance (Object.create(spec)), so `this` holds
                            that mount's state; mount may also return an object with setStep.
                            ctx = { data, page, variant, math, steps, el }
                            opts = { animate, dir, el, page, from:{page, step} }
                            Optional: finish() (end own motion at once), isMoving(),
                            control = { open() -> false to refuse, close(), move(dir) } for key S.
   TALK.math[key]           KaTeX HTML of src/figs/labels.json
   TALK.data                src/data.json
   TALK.motion({finish})    register motion the engine cannot see; returns an unregister function
   TALK.state()             { page, step, moving }
   TALK.go(page, step)      jump (a cut)
   events on document:      'talk:state' { page, step, from, dir, animate, newEls, pageEl }
 */
(function () {
  'use strict';

  const TALK = (window.TALK = window.TALK || {});
  const doc = document;
  const root = doc.documentElement;
  const body = doc.body;
  const params = new URLSearchParams(location.search);

  function readJSON(id) {
    const el = doc.getElementById(id);
    if (!el) return null;
    try { return JSON.parse(el.textContent); } catch (err) { console.error('talk: cannot read #' + id, err); return null; }
  }

  TALK.math = readJSON('talk-math') || {};
  TALK.data = readJSON('talk-data') || {};
  const printMode = params.get('print');
  const printing = printMode === '1' || printMode === 'main';

  const STATIC = printing || params.get('static') === '1';
  const mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
  let reduced = STATIC || params.get('motion') === '0' || !!(mq && mq.matches);
  TALK.static = STATIC;
  TALK.reduced = () => reduced;

  const T_FADE = 200;          // the rest of a page on a forward page change
  const T_CARRY = 450;         // carry between adjacent pages
  const EASE_OUT = 'cubic-bezier(.16,1,.3,1)';
  const EASE_CARRY = 'cubic-bezier(.33,1,.68,1)';

  const specs = new Map();
  const motions = new Set();
  let pages = [];
  let cur = 0;
  let step = 0;
  let scale = 1;
  let started = false;
  let shown = false;
  let reading = false;
  let blank = false;
  let digits = '';
  let digitTimer = 0;
  let blankTimer = 0;
  let returnStack = [];
  let overviewOpen = false;
  let overviewBuilt = false;
  let overviewFocus = 0;
  let overviewOrigin = null;
  let thumbObserver = null;
  let readChoice = params.has('view');
  let control = null;          // the figure handler whose strength control is open
  let sheetOpen = '';            // '' or the name of the open sheet: 'notation' or 'keys'
  let sheetOrigin = null;
  let stage, deck, carryLayer, hud, keysEl;

  /* ------------------------------------------------------------ figure registry */

  TALK.figure = function (id, spec) {
    if (!spec || typeof spec.mount !== 'function') { console.error('talk: figure ' + id + ' has no mount()'); return; }
    specs.set(id, spec);
    if (started) { mountFigures(id); refreshFigures(); }
  };

  TALK.motion = function (handle) {
    motions.add(handle);
    return () => motions.delete(handle);
  };

  function call(handler, name, ...args) {
    if (!handler || typeof handler[name] !== 'function') return undefined;
    try { return handler[name](...args); } catch (err) { console.error('talk: figure ' + (handler.__id || '') + '.' + name + ' failed', err); return undefined; }
  }

  function mountFigures(onlyId) {
    pages.forEach((p) => {
      p.el.querySelectorAll('.fig[data-fig]').forEach((el) => {
        const id = el.dataset.fig;
        if ((onlyId && id !== onlyId) || el.__talkFig) return;
        const spec = specs.get(id);
        if (!spec) return;
        const inst = Object.create(spec);
        inst.__id = id;
        const ctx = { data: TALK.data, page: p.key, variant: el.dataset.variant || '', math: TALK.math, steps: p.steps, el };
        let handler = inst;
        try {
          const r = inst.mount(el, ctx);
          if (r && typeof r === 'object' && typeof r.setStep === 'function') { handler = r; handler.__id = id; }
        } catch (err) {
          console.error('talk: figure ' + id + '.mount failed on ' + p.key, err);
        }
        el.__talkFig = handler;
        p.figs.push({ id, el, h: handler });
      });
    });
  }

  function refreshFigures() {
    if (!shown) return;
    const P = pages[cur];
    P.figs.forEach((f) => call(f.h, 'setStep', step, figOpts(f, P, false, 0, { page: P.key, step })));
  }

  function figOpts(f, P, animate, dir, from) {
    return { animate: !!animate, dir, el: f.el, page: P.key, from };
  }

  /* ------------------------------------------------------------ geometry */

  function fit() {
    const W = root.clientWidth;
    const H = root.clientHeight;
    if (printing) return;
    if (reading) {
      stage.style.transform = '';
      stage.style.left = stage.style.top = '';
      root.style.setProperty('--read-zoom', String(W / 1600));
      scale = W / 1600;
      return;
    }
    // Outside full screen the control row is docked above the stage and the stage fits below it.
    const docked = !isFull();
    body.classList.toggle('is-full', !docked);
    const bar = docked && hud ? hud.offsetHeight : 0;
    scale = Math.min(W / 1600, (H - bar) / 900);
    stage.style.transform = 'scale(' + scale + ')';
    stage.style.left = (W - 1600 * scale) / 2 + 'px';
    stage.style.top = bar + (H - bar - 900 * scale) / 2 + 'px';
    const label = hud && hud.querySelector('.hud-full');
    if (label) label.textContent = docked ? 'Full screen' : 'Leave full screen';
  }

  // a screen rectangle in stage coordinates
  function toStage(r) {
    const s = stage.getBoundingClientRect();
    return { x: (r.left - s.left) / scale, y: (r.top - s.top) / scale, w: r.width / scale, h: r.height / scale };
  }

  function inkBox(el) {
    let r = null;
    if (!(el instanceof SVGElement)) {
      const range = doc.createRange();
      range.selectNodeContents(el);
      r = range.getBoundingClientRect();
      if (!r.width || !r.height) r = null;
    }
    return toStage(r || el.getBoundingClientRect());
  }

  /* ------------------------------------------------------------ steps and state */

  function pageSteps(el) {
    let max = 0;
    el.querySelectorAll('[data-step]').forEach((s) => { max = Math.max(max, +s.dataset.step || 0); });
    const declared = el.dataset.steps != null ? +el.dataset.steps : max;
    if (declared < max) console.warn('talk: ' + el.id + ' declares ' + declared + ' steps but has a step ' + max);
    return Math.max(declared, max);
  }

  function clearNew() {
    deck.querySelectorAll('.is-new').forEach((el) => el.classList.remove('is-new'));
  }

  function setState(i, s, o) {
    o = o || {};
    const P = pages[i];
    s = Math.max(0, Math.min(P.steps, s | 0));
    const from = { page: shown ? pages[cur].key : null, step: shown ? step : null };
    const pageChange = !shown || i !== cur;
    if (pageChange) {
      if (control) closeControl();
      pages.forEach((p, k) => {
        p.el.classList.toggle('is-current', k === i);
        p.el.setAttribute('aria-hidden', reading || k === i ? 'false' : 'true');
        p.el.inert = !reading && k !== i;
      });
    }
    clearNew();
    const newEls = [];
    const markNew = !!o.animate && !reduced && !pageChange && o.dir > 0;
    P.el.querySelectorAll('[data-step]').forEach((el) => {
      const n = +el.dataset.step;
      el.classList.toggle('is-on', n <= (reading ? P.steps : s));
      if (markNew && n === s) { el.classList.add('is-new'); newEls.push(el); }
    });
    cur = i;
    step = s;
    shown = true;
    const animate = !!o.animate && !reduced;
    P.figs.forEach((f) => call(f.h, 'setStep', reading ? P.steps : s, figOpts(f, P, animate && !reading, o.dir || 0, from)));
    writeHash(o.history || 'replace');
    updateHud();
    doc.dispatchEvent(new CustomEvent('talk:state', {
      detail: { page: P.key, step: s, from, dir: o.dir || 0, animate, newEls, pageEl: P.el },
    }));
  }

  function route() {
    const P = pages[cur];
    if (!P.backup) return pages.map((p, i) => !p.backup ? i : -1).filter((i) => i >= 0);
    let lo = cur, hi = cur;
    while (lo > 0 && pages[lo - 1].backup && pages[lo - 1].label === P.label) lo--;
    while (hi + 1 < pages.length && pages[hi + 1].backup && pages[hi + 1].label === P.label) hi++;
    return Array.from({ length: hi - lo + 1 }, (_, k) => lo + k);
  }

  function forward() {
    const P = pages[cur], group = route(), pos = group.indexOf(cur);
    if (step < P.steps) setState(cur, step + 1, { animate: true, dir: 1 });
    else if (pos < group.length - 1) {
      const next = group[pos + 1];
      if (!P.backup && +pages[next].key.slice(1) === +P.key.slice(1) + 1) turnForward(next);
      else setState(next, 0, { animate: false, dir: 1 });
    }
  }

  function back() {
    const group = route(), pos = group.indexOf(cur);
    if (step > 0) setState(cur, step - 1, { animate: false, dir: -1 });
    else if (pos > 0) setState(group[pos - 1], pages[group[pos - 1]].steps, { animate: false, dir: -1 });
  }

  function jump(i, s, remember = false, origin = null) {
    if (i < 0 || i >= pages.length) return;
    finishMotion();
    if (remember && (origin || i !== cur)) returnStack.push(origin || { page: pages[cur].key, step });
    setState(i, s || 0, { animate: false, dir: 0, history: 'push' });
    if (reading) pages[i].el.scrollIntoView({ block: 'start' });
  }

  function pageName(P) {
    return P.backup ? P.label : (P.num ? String(P.num) : 'the title');
  }

  // The control row names where you are, offers the way back from a backup and the strength control.
  function updateHud() {
    if (!hud || !shown) return;
    const P = pages[cur];
    const pos = hud.querySelector('.hud-pos');
    pos.textContent = (P.backup ? P.label : P.num ? 'Page ' + P.num + ' of ' + MAIN_COUNT() : 'Title') +
      (P.steps ? ' · click ' + step + ' of ' + P.steps : '');
    const ret = hud.querySelector('.hud-return');
    if (P.backup) {
      const saved = returnStack[returnStack.length - 1];
      const link = P.el.querySelector('.page-foot .back-link[data-go]') || P.el.querySelector('.back-link[data-go]');
      const target = saved ? pages.find((p) => p.key === saved.page) : link ? pages.find((p) => p.key === link.dataset.go) : linkingPage(P) || pages[0];
      ret.querySelector('.hud-return-label').textContent = 'Back to ' + (target ? pageName(target) : 'the title');
      ret.hidden = false;
    } else ret.hidden = true;
    const str = hud.querySelector('.hud-strength');
    const has = P.figs.some((f) => f.h && f.h.control && typeof f.h.control.open === 'function');
    str.hidden = !has || reading || P.backup;
    str.setAttribute('aria-pressed', control ? 'true' : 'false');
  }

  let mainCount = 0;
  function MAIN_COUNT() {
    if (!mainCount) mainCount = pages.filter((p) => !p.backup && p.num).length;
    return mainCount;
  }

  function flashNote(text) {
    keysEl.textContent = text;
    clearTimeout(digitTimer);
    digitTimer = setTimeout(() => { if (!digits) keysEl.textContent = ''; }, 2600);
  }

  // Without a remembered origin, a backup returns to its named page, else to the main page that links to it.
  function linkingPage(P) {
    const group = pages.filter((p) => p.backup && p.label === P.label).map((p) => p.key);
    return pages.find((p) => !p.backup && [...p.el.querySelectorAll('[data-go]')].some((a) => group.includes(a.dataset.go)));
  }

  function returnTo(link) {
    finishMotion();
    const saved = returnStack.pop();
    const linker = !saved && !(link && link.dataset.go) && pages[cur].backup ? linkingPage(pages[cur]) : null;
    const fallback = link && link.dataset.go || (linker && linker.key);
    const i = pages.findIndex((p) => p.key === (saved ? saved.page : fallback || 'p00'));
    jump(i >= 0 ? i : 0, saved ? saved.step : (fallback && i >= 0 ? pages[i].steps : 0));
  }

  function onDeckLink(e) {
    const a = e.target.closest('a.foot-link[data-go], a.back-link');
    if (!a || !deck.contains(a)) return;
    e.preventDefault();
    if (a.matches('.back-link')) {
      if (a.hasAttribute('data-back')) returnTo(a);
      else {
        // a named return ("◂ 13"): if that is the page the speaker came from, land on the exact
        // step left; otherwise on that page's finished state
        const i = pages.findIndex((p) => p.key === a.dataset.go);
        const saved = i >= 0 ? returnStack.pop() : null;
        jump(i, i >= 0 ? (saved && saved.page === a.dataset.go ? saved.step : pages[i].steps) : 0);
      }
    } else {
      const i = pages.findIndex((p) => p.key === a.dataset.go);
      const source = reading ? pages.find((p) => p.el === a.closest('.page')) : null;
      jump(i, i >= 0 && pages[i].backup ? pages[i].steps : 0, true,
        source ? { page: source.key, step: source.steps } : null);
    }
  }

  /* ------------------------------------------------------------ motion */

  function finiteRunning(a) {
    if (a.playState !== 'running') return false;
    try { return a.effect && isFinite(a.effect.getComputedTiming().endTime); } catch (err) { return false; }
  }

  function isMoving() {
    if (motions.size) return true;
    if (stage.getAnimations && stage.getAnimations({ subtree: true }).some(finiteRunning)) return true;
    return pages[cur].figs.some((f) => call(f.h, 'isMoving') === true);
  }

  function finishMotion() {
    [...motions].forEach((m) => {
      motions.delete(m);
      try { m.finish(); } catch (err) { console.error('talk: finish failed', err); }
    });
    if (stage.getAnimations) {
      stage.getAnimations({ subtree: true }).forEach((a) => {
        if (finiteRunning(a)) { try { a.finish(); } catch (err) { /* infinite or detached */ } }
      });
    }
    pages[cur].figs.forEach((f) => call(f.h, 'finish'));
  }

  // one motion made of web animations, settled synchronously when finished early
  function track(anims, cleanup) {
    let done = false;
    const handle = {
      finish() {
        if (done) return;
        done = true;
        anims.forEach((a) => { try { a.finish(); } catch (err) { /* ignore */ } });
        motions.delete(handle);
        cleanup();
      },
    };
    motions.add(handle);
    Promise.all(anims.map((a) => a.finished)).then(() => handle.finish(), () => handle.finish());
    return handle;
  }

  /* ------------------------------------------------------------ page turn and carries */

  function insideHiddenStep(el, pageEl) {
    const s = el.closest('[data-step]:not(.is-on)');
    return !!(s && pageEl.contains(s));
  }

  function present(el, pageEl) {
    if (insideHiddenStep(el, pageEl)) return false;
    if (getComputedStyle(el).visibility === 'hidden') return false;
    for (let n = el; n && n !== pageEl; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === 'none') return false;
      // an element fading in on arrival counts as present; one held at opacity 0 does not
      const fading = n.getAnimations && n.getAnimations().some((x) => x.playState === 'running');
      if (!fading && parseFloat(cs.opacity) < 0.01) return false;
    }
    const r = el.getBoundingClientRect();
    return r.width > 0 || r.height > 0;
  }

  function visibleText(el) {
    const c = el.cloneNode(true);
    if (c.querySelectorAll) c.querySelectorAll('.katex-mathml, title, desc').forEach((n) => n.remove());
    return (c.textContent || '').replace(/\s+/g, ' ').trim();
  }

  function carries(pageEl) {
    const out = new Map();
    pageEl.querySelectorAll('[data-carry]').forEach((el) => {
      const key = el.dataset.carry;
      if (out.has(key) || !present(el, pageEl)) return;
      out.set(key, { el, box: inkBox(el), text: visibleText(el) });
    });
    return out;
  }

  const TEXT_PROPS = ['color', 'font-family', 'font-size', 'font-weight', 'font-style', 'font-stretch',
    'font-variant-numeric', 'font-feature-settings', 'font-variation-settings', 'font-optical-sizing',
    'letter-spacing', 'word-spacing', 'line-height', 'text-transform', 'text-decoration-line'];
  const SVG_PROPS = ['fill', 'fill-opacity', 'stroke', 'stroke-width', 'stroke-opacity', 'stroke-dasharray',
    'stroke-dashoffset', 'stroke-linecap', 'stroke-linejoin', 'opacity', 'paint-order', 'font-family',
    'font-size', 'font-weight', 'font-style', 'font-stretch', 'letter-spacing', 'text-anchor', 'dominant-baseline'];

  function copyProps(from, to, props) {
    const cs = getComputedStyle(from);
    props.forEach((p) => to.style.setProperty(p, cs.getPropertyValue(p)));
  }

  function scrub(node) {
    const all = node.querySelectorAll ? [node, ...node.querySelectorAll('*')] : [node];
    all.forEach((n) => {
      if (!n.removeAttribute) return;
      n.removeAttribute('id');
      n.removeAttribute('data-step');
      n.removeAttribute('data-carry');
      if (n.classList) n.classList.remove('is-new', 'is-carrying');
    });
  }

  function htmlLayer(el, box) {
    const wrap = doc.createElement('div');
    copyProps(el, wrap, TEXT_PROPS);
    const cs = getComputedStyle(el);
    const lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.25;
    wrap.style.whiteSpace = box.h > lh * 1.5 ? 'normal' : 'nowrap';
    wrap.style.textAlign = 'left';
    el.childNodes.forEach((n) => wrap.appendChild(n.cloneNode(true)));
    const src = el.querySelectorAll('*');
    const dst = wrap.querySelectorAll('*');
    src.forEach((s, k) => {
      const d = dst[k];
      if (!d || !d.style) return;
      if (s.closest('.katex') && !s.classList.contains('katex')) return;
      if (s.classList.contains('katex')) { d.style.color = getComputedStyle(s).color; return; }
      copyProps(s, d, TEXT_PROPS);
    });
    scrub(wrap);
    return wrap;
  }

  function svgLayer(el, box) {
    const NS = 'http://www.w3.org/2000/svg';
    const svg = doc.createElementNS(NS, 'svg');
    let bb;
    try { bb = el.getBBox(); } catch (err) { bb = null; }
    if (!bb || !bb.width || !bb.height) bb = { x: 0, y: 0, width: Math.max(box.w, 1), height: Math.max(box.h, 1) };
    svg.setAttribute('viewBox', bb.x + ' ' + bb.y + ' ' + bb.width + ' ' + bb.height);
    svg.setAttribute('preserveAspectRatio', 'none');
    svg.style.overflow = 'visible';
    const c = el.cloneNode(true);
    c.removeAttribute('transform');
    const src = [el, ...el.querySelectorAll('*')];
    const dst = [c, ...c.querySelectorAll('*')];
    src.forEach((s, k) => { if (dst[k] && dst[k].style) copyProps(s, dst[k], SVG_PROPS); });
    scrub(c);
    svg.appendChild(c);
    return svg;
  }

  function layerOf(el, box) {
    const node = (el instanceof SVGElement && !(el instanceof SVGSVGElement)) ? svgLayer(el, box) : htmlLayer(el, box);
    node.classList.add('carry-layer');
    node.style.left = box.x + 'px';
    node.style.top = box.y + 'px';
    node.style.width = Math.ceil(box.w + 1) + 'px';
    node.style.height = box.h + 'px';
    return node;
  }

  function carry(src, tgt) {
    const a = src.box;
    const b = tgt.box;
    const same = src.text === tgt.text;
    const still = Math.abs(a.x - b.x) < 1.5 && Math.abs(a.y - b.y) < 1.5 && Math.abs(a.w - b.w) < 1.5 && Math.abs(a.h - b.h) < 1.5;
    if (still && same) return;                 // it sits at the same box: it simply stays
    const A = layerOf(src.el, a);
    const B = layerOf(tgt.el, b);
    carryLayer.append(A, B);
    src.el.classList.add('is-carrying');
    tgt.el.classList.add('is-carrying');
    const k = a.h > 0 && b.h > 0 ? b.h / a.h : 1;
    const dx = (b.x + b.w / 2) - (a.x + a.w / 2);
    const dy = (b.y + b.h / 2) - (a.y + a.h / 2);
    const f0 = same ? 0.55 : 0.3;             // where the content cross-fade starts and ends
    const f1 = same ? 0.9 : 0.65;
    const timing = { duration: T_CARRY, easing: EASE_CARRY, fill: 'both' };
    const animA = A.animate([
      { offset: 0, transform: 'none', opacity: 1 },
      { offset: f0, opacity: 1 },
      { offset: f1, opacity: 0 },
      { offset: 1, transform: 'translate(' + dx + 'px,' + dy + 'px) scale(' + k + ')', opacity: 0 },
    ], timing);
    const animB = B.animate([
      { offset: 0, transform: 'translate(' + -dx + 'px,' + -dy + 'px) scale(' + 1 / k + ')', opacity: 0 },
      { offset: f0, opacity: 0 },
      { offset: f1, opacity: 1 },
      { offset: 1, transform: 'none', opacity: 1 },
    ], timing);
    track([animA, animB], () => {
      A.remove();
      B.remove();
      src.el.classList.remove('is-carrying');
      tgt.el.classList.remove('is-carrying');
    });
  }

  function turnForward(i) {
    if (reduced) { setState(i, 0, { animate: false, dir: 1 }); return; }
    const oldP = pages[cur];
    const newP = pages[i];
    const sources = carries(oldP.el);
    oldP.el.classList.add('is-leaving');
    setState(i, 0, { animate: true, dir: 1 });
    const targets = carries(newP.el);
    sources.forEach((src, key) => { const tgt = targets.get(key); if (tgt) carry(src, tgt); });
    const fade = newP.el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: T_FADE, easing: EASE_OUT });
    track([fade], () => oldP.el.classList.remove('is-leaving'));
  }

  /* ------------------------------------------------------------ hash */

  function parseHash() {
    const m = /^#?([pb]?)(\d+)(?:\.(\d+))?$/.exec(location.hash || '');
    if (!m) return { i: 0, s: 0 };
    const key = (m[1] || 'p') + String(+m[2]).padStart(2, '0');
    const i = pages.findIndex((p) => p.key === key);
    return i < 0 ? { i: 0, s: 0 } : { i, s: m[3] ? +m[3] : 0 };
  }

  function writeHash(mode) {
    const h = '#' + pages[cur].key + '.' + step;
    try {
      history[mode === 'push' ? 'pushState' : 'replaceState'](
        { ...history.state, talkReturn: returnStack }, '', h);
    } catch (err) { /* file:// in some browsers */ }
  }

  function restoreStack() {
    returnStack = Array.isArray(history.state && history.state.talkReturn)
      ? history.state.talkReturn.filter((s) => pages.some((p) => p.key === s.page) && Number.isInteger(s.step)) : [];
  }

  function onHashChange() {
    if (!started) return;
    restoreStack();
    const st = parseHash();
    if (st.i === cur && st.s === step) return;
    finishMotion();
    setState(st.i, st.s, { animate: false, dir: 0 });
  }

  function setParam(name, value) {
    try {
      const u = new URL(location.href);
      if (value == null) u.searchParams.delete(name); else u.searchParams.set(name, value);
      history.replaceState(history.state, '', u.toString());
    } catch (err) { /* ignore */ }
  }

  /* ------------------------------------------------------------ blank, reading, control */

  // A phone, either way up, reads the pages as a column rather than presenting them.
  function small() { return root.clientWidth < 700 || root.clientHeight < 500; }

  function setBlank(on) {
    blank = on;
    body.classList.toggle('is-blank', on);
  }

  function setReading(on) {
    if (printing || on === reading) return;
    if (overviewOpen) closeOverview();
    finishMotion();
    if (control) closeControl();
    setBlank(false);
    reading = on;
    root.classList.toggle('is-reading', on);
    body.classList.toggle('is-reading', on);
    setParam('view', on ? 'read' : 'stage');
    fit();
    if (on) {
      clearNew();
      pages.forEach((p) => {
        p.el.setAttribute('aria-hidden', 'false');
        p.el.inert = false;
        p.el.querySelectorAll('[data-step]').forEach((el) => el.classList.add('is-on'));
        p.figs.forEach((f) => call(f.h, 'setStep', p.steps, figOpts(f, p, false, 0, { page: p.key, step: p.steps })));
      });
      const P = pages[cur];
      window.scrollTo(0, P.el.getBoundingClientRect().top + window.scrollY);
    } else {
      window.scrollTo(0, 0);
      pages.forEach((p, k) => {
        p.el.setAttribute('aria-hidden', k === cur ? 'false' : 'true');
        p.el.inert = k !== cur;
      });
      setState(cur, step, { animate: false, dir: 0 });
    }
  }

  function closeControl() {
    const c = control;
    control = null;
    if (c && c.control && typeof c.control.close === 'function') callControl(c, 'close');
    updateHud();
  }

  function callControl(h, name, ...args) {
    try { return h.control[name](...args); } catch (err) { console.error('talk: control.' + name + ' failed', err); return false; }
  }

  function toggleControl() {
    if (control) { closeControl(); return; }
    const f = pages[cur].figs.find((x) => x.h && x.h.control && typeof x.h.control.open === 'function');
    if (!f) return;
    finishMotion();
    if (callControl(f.h, 'open') === false) { flashNote('The strength control opens once the chart is complete'); return; }
    control = f.h;
    updateHud();
  }

  /* ------------------------------------------------------------ reading, print, overview */

  function prepareLinksAndReading() {
    let label = '';
    pages.forEach((p) => {
      p.el.querySelectorAll('a.foot-link[data-go], a.back-link').forEach((a) => {
        a.href = '#' + (a.dataset.go || 'p00') + '.0';
      });
      if (p.backup && p.label !== label) {
        const heading = doc.createElement('h2');
        heading.className = 'reading-label';
        heading.textContent = p.label;
        p.el.before(heading);
        label = p.label;
      }
    });
  }

  function preparePrint() {
    root.classList.add('is-print');
    if (printMode === 'main') root.classList.add('print-main');
    body.dataset.motion = 'off';
    pages.forEach((p) => {
      p.el.inert = false;
      p.el.setAttribute('aria-hidden', printMode === 'main' && p.backup ? 'true' : 'false');
      p.figs.forEach((f) => call(f.h, 'setStep', p.steps, figOpts(f, p, false, 0, { page: p.key, step: p.steps })));
      p.el.querySelectorAll('[data-step]').forEach((el) => el.classList.add('is-on'));
    });
  }

  function renderThumbnail(i) {
    const slot = doc.querySelector('[data-overview-page="' + i + '"] .overview-viewport');
    if (!slot || slot.firstElementChild) return;
    const P = pages[i];
    // Figures supply their own finished appearance, including comparison traces.
    P.figs.forEach((f) => call(f.h, 'setStep', P.steps, figOpts(f, P, false, 0, { page: P.key, step: P.steps })));
    slot.appendChild(clonePage(i, 'overview-' + i + '-'));
    const button = slot.parentElement;
    button.style.setProperty('--thumb-scale', String(slot.clientWidth / 1600));
    if (i === cur && !reading) {
      P.figs.forEach((f) => call(f.h, 'setStep', step, figOpts(f, P, false, 0, { page: P.key, step })));
    }
  }

  // A finished, inert copy of a page whose IDs (and the references to them) carry a prefix.
  function clonePage(i, prefix) {
    const P = pages[i];
    const clone = P.el.cloneNode(true);
    clone.dataset.thumbPage = P.key;
    clone.classList.remove('is-current', 'is-leaving');
    clone.removeAttribute('aria-hidden');
    clone.inert = true;
    clone.querySelectorAll('[data-step]').forEach((el) => {
      el.classList.add('is-on'); el.classList.remove('is-new', 'is-carrying');
    });
    const ids = new Map();
    [clone, ...clone.querySelectorAll('[id]')].forEach((el) => {
      if (!el.id) return;
      const id = el.id;
      el.id = prefix + id;
      ids.set(id, el.id);
    });
    // Local SVG patterns and HTML references must not share IDs with the stage.
    [clone, ...clone.querySelectorAll('*')].forEach((el) => {
      [...el.attributes].forEach((a) => {
        if (a.name === 'id') return;
        let value = a.value;
        ids.forEach((newId, oldId) => {
          value = value.replaceAll('url(#' + oldId + ')', 'url(#' + newId + ')');
          if (value === '#' + oldId) value = '#' + newId;
        });
        if (value !== a.value) el.setAttribute(a.name, value);
      });
    });
    return clone;
  }

  function buildOverview() {
    if (overviewBuilt) return;
    overviewBuilt = true;
    const overview = doc.getElementById('overview');
    const fragment = doc.createDocumentFragment();
    const roads = [...(doc.querySelector('.roadmap') || doc.createElement('nav')).querySelectorAll('.road')].map((r) => r.textContent.trim());
    let group = '', grid;
    pages.forEach((p, i) => {
      const key = p.backup ? p.label : 'part-' + (+p.el.dataset.part || 1);
      if (key !== group) {
        group = key;
        const section = doc.createElement('section');
        const heading = doc.createElement('h2');
        heading.textContent = p.backup
          ? p.label + '  ' + (p.el.querySelector('.page-title')?.textContent || '').trim()
          : roads[(+p.el.dataset.part || 1) - 1] || roads[0] || '';
        section.appendChild(heading);
        grid = doc.createElement('div');
        grid.className = 'overview-grid';
        section.appendChild(grid);
        fragment.appendChild(section);
      }
      const button = doc.createElement('button');
      button.type = 'button';
      button.className = 'overview-item';
      button.dataset.overviewPage = i;
      button.tabIndex = -1;
      button.setAttribute('aria-label', (p.backup ? p.label : String(p.num || 0)) + ' ' + (p.el.querySelector('.page-title, .cover-title')?.textContent || '').trim());
      const slot = doc.createElement('span');
      slot.className = 'overview-viewport';
      slot.setAttribute('aria-hidden', 'true');
      button.appendChild(slot);
      button.addEventListener('click', () => chooseOverview(i));
      button.addEventListener('focus', () => { overviewFocus = i; });
      grid.appendChild(button);
    });
    const head = doc.createElement('div');
    head.className = 'sheet-head overview-head';
    head.innerHTML = '<h2>Overview</h2><button type="button" class="sheet-close">Close <kbd>Esc</kbd></button>';
    head.querySelector('button').addEventListener('click', closeOverview);
    overview.appendChild(head);
    const list = doc.createElement('div');
    list.className = 'overview-list';
    list.appendChild(fragment);
    overview.appendChild(list);
    thumbObserver = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      renderThumbnail(+entry.target.dataset.overviewPage);
      thumbObserver.unobserve(entry.target);
    }), { root: overview, rootMargin: '200px' });
    overview.querySelectorAll('.overview-item').forEach((b) => thumbObserver.observe(b));
    const resizer = new ResizeObserver((entries) => entries.forEach(({ target }) => {
      target.style.setProperty('--thumb-scale', String(target.querySelector('.overview-viewport').clientWidth / 1600));
    }));
    overview.querySelectorAll('.overview-item').forEach((b) => resizer.observe(b));
  }

  function focusOverview(i) {
    overviewFocus = Math.max(0, Math.min(pages.length - 1, i));
    const overview = doc.getElementById('overview');
    overview.querySelectorAll('.overview-item').forEach((b) => { b.tabIndex = +b.dataset.overviewPage === overviewFocus ? 0 : -1; });
    const button = overview.querySelector('[data-overview-page="' + overviewFocus + '"]');
    renderThumbnail(overviewFocus);
    button.focus({ preventScroll: true });
    button.scrollIntoView({ block: 'nearest' });
  }

  function openOverview() {
    if (printing) return;
    finishMotion();
    if (control) closeControl();
    if (sheetOpen) closeSheet();
    overviewOrigin = doc.activeElement;
    overviewOpen = true;
    body.classList.add('is-overview');
    doc.getElementById('overview').hidden = false;
    doc.getElementById('viewport').inert = true;
    hud.inert = true;
    buildOverview();
    doc.querySelectorAll('.overview-item').forEach((b) => {
      const current = +b.dataset.overviewPage === cur;
      b.classList.toggle('is-current', current);
      if (current) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
    });
    focusOverview(cur);
  }

  function closeOverview() {
    if (!overviewOpen) return;
    overviewOpen = false;
    body.classList.remove('is-overview');
    doc.getElementById('overview').hidden = true;
    doc.getElementById('viewport').inert = false;
    hud.inert = false;
    if (overviewOrigin && overviewOrigin.isConnected) overviewOrigin.focus({ preventScroll: true });
  }

  /* ------------------------------------------------------------ sheets: notation and keys */

  const KEYS = [
    ['Next click', 'Right, Space, Page Down, Enter'],
    ['Previous click', 'Left, Page Up'],
    ['Go to main page 19', '1 9 Enter'],
    ['Go to backup B8', 'b 8 Enter'],
    ['Return from a backup', 'Backspace, or Back in the control row'],
    ['Restart this page', 'R'],
    ['First and last main page', 'Home, End'],
    ['Overview of all pages', 'O'],
    ['Notation', 'G'],
    ['Strength control (pages 19, 20, 22)', 'S'],
    ['Blank screen', 'B or . (a clicker’s blank key); click to return'],
    ['Reading view', 'V'],
    ['Full screen', 'F (or a clicker’s start key, F5)'],
    ['These keys', '?'],
    ['Close a panel, leave blank', 'Esc'],
  ];

  function openSheet(name) {
    if (printing) return;
    if (sheetOpen === name) { closeSheet(); return; }
    if (overviewOpen) closeOverview();
    finishMotion();
    if (control) closeControl();
    const sheet = doc.getElementById('sheet');
    const bodyEl = sheet.querySelector('.sheet-body');
    if (!sheetOpen) sheetOrigin = doc.activeElement;
    sheetOpen = name;
    bodyEl.textContent = '';
    sheet.dataset.sheet = name;
    if (name === 'notation') {
      doc.getElementById('sheet-title').textContent = 'Notation';
      pages.forEach((p, i) => {
        if (!p.backup || p.label !== 'B16') return;
        p.figs.forEach((f) => call(f.h, 'setStep', p.steps, figOpts(f, p, false, 0, { page: p.key, step: p.steps })));
        const frame = doc.createElement('div');
        frame.className = 'sheet-page';
        frame.appendChild(clonePage(i, 'sheet-' + i + '-'));
        bodyEl.appendChild(frame);
      });
    } else {
      doc.getElementById('sheet-title').textContent = 'Keys';
      const list = doc.createElement('dl');
      list.className = 'sheet-keys';
      KEYS.forEach(([what, how]) => {
        const dt = doc.createElement('dt'); dt.textContent = what;
        const dd = doc.createElement('dd'); dd.textContent = how;
        list.append(dt, dd);
      });
      bodyEl.appendChild(list);
      const note = doc.createElement('p');
      note.className = 'sheet-note';
      note.textContent = 'A press during a movement finishes it. Back, reload and the return from a backup land on the same click.';
      bodyEl.appendChild(note);
    }
    sheet.hidden = false;
    body.classList.add('is-sheet');
    doc.getElementById('viewport').inert = true;
    sizeSheet();
    sheet.querySelector('.sheet-close').focus({ preventScroll: true });
    sheet.scrollTop = 0;
  }

  function sizeSheet() {
    const sheet = doc.getElementById('sheet');
    sheet.querySelectorAll('.sheet-page').forEach((f) => f.style.setProperty('--sheet-scale', String(f.clientWidth / 1600)));
  }

  function closeSheet() {
    if (!sheetOpen) return;
    sheetOpen = '';
    const sheet = doc.getElementById('sheet');
    sheet.hidden = true;
    sheet.querySelector('.sheet-body').textContent = '';
    body.classList.remove('is-sheet');
    doc.getElementById('viewport').inert = false;
    if (sheetOrigin && sheetOrigin.isConnected) sheetOrigin.focus({ preventScroll: true });
  }

  function chooseOverview(i) {
    closeOverview();
    if (i === cur) return;                       // the current page resumes at its click
    jump(i, pages[i].backup ? pages[i].steps : 0, pages[i].backup);
  }

  function moveOverview(key) {
    if (key === 'Home') return focusOverview(0);
    if (key === 'End') return focusOverview(pages.length - 1);
    if (key === 'ArrowLeft' || key === 'ArrowRight') return focusOverview(overviewFocus + (key === 'ArrowLeft' ? -1 : 1));
    const buttons = [...doc.querySelectorAll('.overview-item')];
    const here = buttons[overviewFocus].getBoundingClientRect();
    const cx = here.left + here.width / 2;
    const down = key === 'ArrowDown';
    const candidates = buttons.map((b, i) => ({ i, r: b.getBoundingClientRect() }))
      .filter(({ r }) => down ? r.top > here.top + 4 : r.top < here.top - 4)
      .sort((a, b) => (Math.abs(a.r.top - here.top) - Math.abs(b.r.top - here.top)) ||
        Math.abs(a.r.left + a.r.width / 2 - cx) - Math.abs(b.r.left + b.r.width / 2 - cx));
    if (candidates.length) focusOverview(candidates[0].i);
  }

  /* ------------------------------------------------------------ input */

  const FORWARD = new Set(['ArrowRight', ' ', 'Spacebar', 'PageDown', 'Enter']);
  const BACK = new Set(['ArrowLeft', 'PageUp']);

  function showDigits() {
    keysEl.textContent = digits;
    clearTimeout(digitTimer);
    if (digits) digitTimer = setTimeout(() => { digits = ''; keysEl.textContent = ''; }, 2500);
  }

  function nav(fn) {
    if (isMoving()) { finishMotion(); return; }   // a press during motion only finishes it
    fn();
  }

  function onKey(e) {
    if (printing || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    const k = e.key, lower = k.length === 1 ? k.toLowerCase() : k;
    if (k === 'Escape') {
      e.preventDefault();
      if (sheetOpen) closeSheet();
      else if (overviewOpen) closeOverview();
      else if (control) closeControl();
      else if (blank) setBlank(false);
      else if (digits) { digits = ''; showDigits(); }
      return;
    }
    if (lower === 'b' || k === '.') {
      e.preventDefault();
      clearTimeout(blankTimer);
      if (blank || k === '.') { setBlank(!blank); digits = k === 'b' && blank ? 'b' : ''; showDigits(); return; }
      // b may start a backup number (b8 Enter): blank only if no digit follows at once.
      digits = 'b';
      showDigits();
      blankTimer = setTimeout(() => { if (digits === 'b') { setBlank(true); } }, 450);
      return;
    }
    // Lower-case b serves both the clicker's blank and a backup-number prefix.
    if (/^[0-9]$/.test(k) && (!blank || digits === 'b')) {
      e.preventDefault();
      clearTimeout(blankTimer);
      if (blank) setBlank(false);
      digits = (digits + k).slice(0, 4);
      showDigits();
      return;
    }
    if (blank) {
      if (FORWARD.has(k) || BACK.has(k) || k === 'Home' || k === 'End') {
        e.preventDefault(); setBlank(false); digits = ''; showDigits();
      }
      return;
    }
    if (lower === 'o') { e.preventDefault(); if (overviewOpen) closeOverview(); else openOverview(); return; }
    if (lower === 'g' || k === '?') { e.preventDefault(); openSheet(k === '?' ? 'keys' : 'notation'); return; }
    if (sheetOpen) {
      if (FORWARD.has(k) || BACK.has(k)) { e.preventDefault(); closeSheet(); }
      else if (lower === 'f') { e.preventDefault(); toggleFullscreen(); }
      return;
    }
    if (overviewOpen) {
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(k)) {
        e.preventDefault(); moveOverview(k); return;
      }
      if (k === 'Enter') { e.preventDefault(); chooseOverview(overviewFocus); return; }
      if (k === 'Tab') {
        e.preventDefault(); focusOverview((overviewFocus + (e.shiftKey ? -1 : 1) + pages.length) % pages.length);
      }
      return;
    }
    if (lower === 'v') { e.preventDefault(); readChoice = true; setReading(!reading); return; }
    if (lower === 'f' || k === 'F5') {
      e.preventDefault();
      if (k === 'F5' && doc.fullscreenElement) return;   // a clicker's start key: enter, never leave
      toggleFullscreen();
      return;
    }
    if (lower === 'r' && !reading) { e.preventDefault(); nav(() => { if (control) closeControl(); setState(cur, 0, { animate: false, dir: 0 }); }); return; }
    if (k === 'Backspace') {
      e.preventDefault();
      if (digits) { digits = digits.slice(0, -1); showDigits(); }
      else nav(() => returnTo(pages[cur].el.querySelector('.back-link[data-go]')));
      return;
    }
    if (k === 'Enter' && digits) {
      e.preventDefault();
      if (isMoving()) { finishMotion(); return; }
      const backup = digits[0] === 'b', n = +(backup ? digits.slice(1) : digits);
      digits = ''; showDigits();
      const i = pages.findIndex((p) => backup ? p.backup && p.label.toLowerCase() === 'b' + n : !p.backup && p.num === n);
      if (i >= 0) jump(i, backup ? pages[i].steps : 0, backup);
      return;
    }
    if (e.target.closest && e.target.closest('a, button') && (k === 'Enter' || k === ' ')) return;
    if (reading) return;
    if (control) {
      if (lower === 's') { e.preventDefault(); closeControl(); return; }
      if (FORWARD.has(k)) { e.preventDefault(); callControl(control, 'move', 1); return; }
      if (BACK.has(k)) { e.preventDefault(); callControl(control, 'move', -1); return; }
    }
    if (FORWARD.has(k)) { e.preventDefault(); digits = ''; showDigits(); clearNewOnInput(); nav(forward); return; }
    if (BACK.has(k)) { e.preventDefault(); digits = ''; showDigits(); clearNewOnInput(); nav(back); return; }
    if (k === 'Home') { e.preventDefault(); nav(() => jump(route()[0], 0)); return; }
    if (k === 'End') { e.preventDefault(); const r = route(); nav(() => jump(r[r.length - 1], 0)); return; }
    if (lower === 's') { e.preventDefault(); nav(toggleControl); }
  }

  // .is-new lasts until the next input: an input during motion finishes the motion first
  function clearNewOnInput() {
    if (!isMoving()) clearNew();
  }

  // Full screen by the button, the F key or the browser's own command (F11, Ctrl-Cmd-F).
  function isFull() {
    if (doc.fullscreenElement) return true;
    return window.innerWidth >= screen.width - 1 && window.innerHeight >= screen.height - 1;
  }

  function toggleFullscreen() {
    try {
      if (doc.fullscreenElement) doc.exitFullscreen();
      else if (root.requestFullscreen) root.requestFullscreen().catch(() => {});
    } catch (err) { /* not allowed here */ }
  }

  let awakeTimer = 0;
  function wake() {
    body.classList.add('is-awake');
    clearTimeout(awakeTimer);
    awakeTimer = setTimeout(function sleep() {
      if (hud.matches(':hover') || control) { awakeTimer = setTimeout(sleep, 800); return; }
      body.classList.remove('is-awake');
    }, 2200);
  }

  function onHud(e) {
    const b = e.target.closest('button[data-act]');
    if (!b) return;
    const act = b.dataset.act;
    if (act === 'prev') { if (blank) setBlank(false); else if (control) callControl(control, 'move', -1); else nav(back); }
    else if (act === 'next') { if (blank) setBlank(false); else if (control) callControl(control, 'move', 1); else { clearNewOnInput(); nav(forward); } }
    else if (act === 'return') nav(() => returnTo(pages[cur].el.querySelector('.back-link[data-go]')));
    else if (act === 'strength') nav(toggleControl);
    else if (act === 'overview') openOverview();
    else if (act === 'notation') openSheet('notation');
    else if (act === 'keys') openSheet('keys');
    else if (act === 'full') toggleFullscreen();
    else if (act === 'read') { readChoice = true; setReading(!reading); }
  }

  /* ------------------------------------------------------------ start */

  TALK.state = () => ({ page: pages[cur] && pages[cur].key, step, moving: started ? isMoving() : false, reading, look: body.dataset.look });
  TALK.go = (key, s) => { const i = pages.findIndex((p) => p.key === key); if (i >= 0) { finishMotion(); jump(i, s || 0); } };

  TALK.start = function () {
    if (started) return;
    stage = doc.getElementById('stage');
    deck = doc.getElementById('deck');
    carryLayer = doc.getElementById('carry');
    hud = doc.getElementById('hud');
    keysEl = doc.getElementById('keys');

    body.dataset.look = 'plate';
    body.dataset.motion = reduced ? 'off' : 'on';
    if (STATIC) body.classList.add('is-static');

    pages = [...deck.querySelectorAll(':scope > section.page')].map((el) => ({
      key: el.id, el, num: +el.dataset.page, steps: pageSteps(el), figs: [],
      backup: el.classList.contains('is-backup'), label: el.dataset.label || '',
    }));
    fit();
    void stage.offsetHeight;                     // lay the pages out so their fonts start loading

    let go = false;
    const begin = () => {
      if (go) return;
      go = true;
      started = true;
      mountFigures();
      restoreStack();
      prepareLinksAndReading();
      const st = parseHash();
      setState(st.i, st.s, { animate: false, dir: 0, history: 'replace' });
      if (printing) preparePrint();
      else if (params.get('view') === 'read' || (!params.has('view') && small())) setReading(true);
      root.classList.add('is-ready');

      window.addEventListener('keydown', onKey);
      window.addEventListener('resize', () => {
        if (!readChoice && !printing) setReading(small());
        fit();
      });
      doc.addEventListener('fullscreenchange', fit);
      window.addEventListener('hashchange', onHashChange);
      window.addEventListener('popstate', onHashChange);
      window.addEventListener('mousemove', wake, { passive: true });
      deck.addEventListener('click', onDeckLink);
      hud.addEventListener('mousedown', (e) => e.preventDefault());
      hud.addEventListener('click', onHud);
      doc.querySelector('#sheet .sheet-close').addEventListener('click', closeSheet);
      doc.getElementById('blank').addEventListener('click', (e) => { e.preventDefault(); setBlank(false); });
      doc.getElementById('sheet').addEventListener('click', (e) => { if (e.target.id === 'sheet') closeSheet(); });
      window.addEventListener('resize', sizeSheet);
      if (mq && !STATIC && params.get('motion') !== '0') {
        const onMq = () => { reduced = mq.matches; if (reduced) finishMotion(); body.dataset.motion = reduced ? 'off' : 'on'; };
        if (mq.addEventListener) mq.addEventListener('change', onMq); else if (mq.addListener) mq.addListener(onMq);
      }
    };
    // load every declared face (all are inline), so every page uses its declared face
    const faces = doc.fonts ? [...doc.fonts].map((f) => f.load().catch(() => null)) : [];
    Promise.all(faces).then(() => (doc.fonts ? doc.fonts.ready : null)).then(begin, begin);
    setTimeout(begin, 1500);
  };
})();
