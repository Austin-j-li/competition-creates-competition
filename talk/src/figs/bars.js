/* Schematic split bars from slide11's shape boxes (960 × 540 pt).
   Every class has the same total against F and Ft; only the split moves. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const K = 5 / 3;
  const X = (143 - 48) * K;
  const TOTAL = [389.6 * K, 155.9 * K];
  const OLD = [124.7 * K, 116.9 * K];
  const NEW = [233.8 * K, 140.3 * K];
  const Y = [30.5 * K, 68.5 * K];
  const DY = 145 * K;
  const BY = 110.5 * K;
  const EASE = 'cubic-bezier(.16,1,.3,1)';
  // a spread narrower than two full caps is drawn with short caps and its label set further
  // out, so caps and bar never read as a letter H beside the label
  const CAP = (split) => (split[0] - split[1] < 24 ? 10 : 18);
  const LABEL_DX = (split) => (split[0] - split[1] < 24 ? 26 : 14);
  const capPath = (h) => `M0 ${BY - h / 2}v${h}`;

  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    if (parent) parent.append(el);
    return el;
  }

  TALK.figure('bars', {
    mount(el, ctx) {
      this.el = el;
      this.ctx = ctx;
      this.anims = [];
      const root = svg('svg', { class: 'fig-svg', viewBox: '0 0 808 452', 'aria-hidden': 'true' }, el);
      const defs = svg('defs', {}, root);
      const travelClip = svg('clipPath', { id: 'bars-travel-window', clipPathUnits: 'userSpaceOnUse' }, defs);
      svg('rect', { x: 0, y: 210, width: 808, height: 242 }, travelClip);
      this.screens = ['a', 'b'].map((letter, i) => {
        const p = svg('pattern', { id: `scr-${letter}-bars`, patternUnits: 'userSpaceOnUse', patternTransform: `rotate(${i ? 135 : 45})` }, defs);
        const path = svg('path', { class: 'screen-line' }, p);
        return { p, path };
      });
      this.pairs = [this.pair(root, 'F', 0, OLD, 1), this.pair(root, 'Ft', DY, NEW, 2)];
      this.note = el.closest('.page').querySelector('.bars-note');
      this.look();
    },

    label(parent, cls, x, y, word, key, attrs) {
      const span = document.createElement('span');
      span.className = 'fig-label ' + cls;
      span.style.left = x + 'px'; span.style.top = y + 'px';
      if (key) span.innerHTML = (word || '') + this.ctx.math['bars.' + key];
      else span.textContent = word;
      Object.entries(attrs || {}).forEach(([k, v]) => span.setAttribute(k, v));
      parent.append(span);
      return span;
    },

    pair(root, name, dy, split, step) {
      const window = svg('g', {}, root);
      const outer = svg('g', { class: 'pair', 'data-pair': name, 'data-step': step, transform: `translate(0 ${dy})` }, window);
      const drawing = svg('g', { class: 'pair-drawing' }, outer);
      // the rule between the pairs stays in place while the copy travels (outer is not moved)
      svg('path', { class: 'pair-rule', d: 'M0 0H808' }, name === 'F' ? drawing : outer);
      const labels = document.createElement('div');
      labels.className = 'pair pair-labels'; labels.dataset.pair = name; labels.dataset.step = step;
      labels.style.top = dy + 'px';
      const labelWindow = document.createElement('div');
      labelWindow.className = 'bars-label-window';
      labelWindow.append(labels); this.el.append(labelWindow);
      const title = this.label(labels, 'pair-label', 0, 10, name === 'F' ? 'Against ' : 'Against stronger ', name === 'F' ? 'againstF' : 'againstFt');
      const rows = split.map((t, i) => {
        const barT = svg('rect', { class: 'bar-t', x: X, y: Y[i], width: t, height: 50 }, drawing);
        const barG = svg('rect', { class: 'bar-g', x: X + t, y: Y[i], width: TOTAL[i] - t, height: 50 }, drawing);
        svg('rect', { class: 'bar-outline', x: X, y: Y[i], width: TOTAL[i], height: 50 }, drawing);
        const divider = svg('path', { class: 'bar-outline bar-divider', d: `M0 ${Y[i]}v50`, transform: `translate(${X + t} 0)` }, drawing);
        this.label(labels, 'row-label', 0, Y[i] + 8, i ? 'Class L rival' : 'Class H rival');
        this.label(labels, 'bar-label', X + 12, Y[i] + 8, null, i ? 'tL' : 'tH', { 'data-payoff': 't' });
        // The class-L bar's kept part is narrow in both pairs: its label sits just outside the
        // bar, clear of the dotted guide that runs down from the end of t_H.
        const gx = i === 1 ? (305.3 - 48) * K : X + t + 12;
        const gLabel = this.label(labels, 'bar-label', gx, Y[i] + 8, null, i ? 'gL' : 'gH', { 'data-payoff': 'g' });
        return { barT, barG, divider, gLabel, gx };
      });
      const guides = split.map((t, i) => svg('path', {
        class: 'spread-bracket spread-guide', d: `M0 ${Y[i] + 50}V${BY}`,
        transform: `translate(${X + t} 0)`,
      }, drawing));
      const bracket = svg('path', { class: 'spread-bracket', d: 'M0 0H1', transform: `translate(${X + split[1]} ${BY}) scale(${split[0] - split[1]} 1)` }, drawing);
      const caps = split.map(t => svg('path', { class: 'spread-bracket', d: capPath(CAP(split)), transform: `translate(${X + t} 0)` }, drawing));
      const spread = this.label(labels, 'spread-label', X + split[0] + LABEL_DX(split), BY - 15, null, 'spread');
      return { window, labelWindow, outer, drawing, labels, title, rows, guides, bracket, caps, spread, split };
    },

    look() {
      const pitch = parseFloat(getComputedStyle(this.el).getPropertyValue('--scr-pitch')) || 9;
      this.screens.forEach(({ p, path }) => {
        p.setAttribute('width', pitch); p.setAttribute('height', pitch);
        path.setAttribute('d', `M0 0V${pitch}`);
      });
    },

    animate(el, frames, timing) {
      const a = el.animate(frames, Object.assign({ easing: EASE, fill: 'both' }, timing));
      this.anims.push(a);
      return a;
    },

    setStep(step, opts) {
      this.finish();
      if (!opts.animate || opts.dir !== 1 || opts.from.page !== opts.page) return;
      if (step === 1) {
        const p = this.pairs[0];
        this.animate(p.drawing, [{ clipPath: 'inset(0 100% 0 0)' }, { clipPath: 'inset(0 0 0 0)' }], { duration: 350 });
        this.animate(p.labels, [{ opacity: 0 }, { opacity: 1 }], { duration: 240 });
      } else if (step === 2 && opts.from.step === 1) {
        const p = this.pairs[1];
        // The moving copy emerges from beneath the first pair, so it cannot cover
        // that pair's labels or bracket while it travels through their space.
        p.window.setAttribute('clip-path', 'url(#bars-travel-window)');
        p.labelWindow.style.clipPath = 'inset(210px 0 0 0)';
        const move = [
          { offset: 0, transform: `translateY(${-DY}px)` },
          { offset: 250 / 550, transform: 'translateY(0px)' },
          { offset: 1, transform: 'translateY(0px)' },
        ];
        this.animate(p.drawing, move, { duration: 550, easing: 'linear' });
        this.animate(p.labels, move, { duration: 550, easing: 'linear' });
        const morph = { delay: 250, duration: 300 };
        p.rows.forEach((row, i) => {
          this.animate(row.barT, [{ width: OLD[i] + 'px' }, { width: NEW[i] + 'px' }], morph);
          this.animate(row.barG, [
            { x: (X + OLD[i]) + 'px', width: (TOTAL[i] - OLD[i]) + 'px' },
            { x: (X + NEW[i]) + 'px', width: (TOTAL[i] - NEW[i]) + 'px' },
          ], morph);
          [row.divider, p.guides[i], p.caps[i]].forEach(mark => this.animate(mark, [
            { transform: `translateX(${X + OLD[i]}px)` },
            { transform: `translateX(${X + NEW[i]}px)` },
          ], morph));
          // the copy leaves with the first pair's short caps and grows them as the spread widens
          this.animate(p.caps[i], [{ d: `path("${capPath(CAP(OLD))}")` }, { d: `path("${capPath(CAP(NEW))}")` }], morph);
          // the class-L label sits outside its bar in both pairs, so only the class-H label moves
          if (i === 0) this.animate(row.gLabel, [
            { left: (X + OLD[i] + 12) + 'px' },
            { left: row.gx + 'px' },
          ], morph);
        });
        this.animate(p.bracket, [
          { transform: `translate(${X + OLD[1]}px, ${BY}px) scaleX(${OLD[0] - OLD[1]})` },
          { transform: `translate(${X + NEW[1]}px, ${BY}px) scaleX(${NEW[0] - NEW[1]})` },
        ], morph);
        this.animate(p.spread, [{ left: (X + OLD[0] + LABEL_DX(OLD)) + 'px' }, { left: (X + NEW[0] + LABEL_DX(NEW)) + 'px' }], morph);
        // the copy's spread label stays out of sight while it passes the first pair's own label
        this.animate(p.spread, [{ opacity: 0 }, { offset: 0.999, opacity: 0 }, { opacity: 1 }], { duration: 250, easing: 'linear', fill: 'none' });
        // the second pair's title stands in its own place from the start (it holds still against
        // the travelling labels: the inverse of their move) and is set once the copy's rows have
        // passed its line, as the copy lands, before the boundaries slide
        this.animate(p.title, [
          { offset: 0, transform: `translateY(${DY}px)`, opacity: 0 },
          { offset: 240 / 550, opacity: 0 },
          { offset: 250 / 550, transform: 'translateY(0px)' },
          { offset: 340 / 550, opacity: 1 },
          { offset: 1, transform: 'translateY(0px)', opacity: 1 },
        ], { duration: 550, easing: 'linear' });
        // the note arrives while the boundaries slide: the click ends at 550 ms
        this.animate(this.note, [{ opacity: 0 }, { opacity: 1 }], { delay: 300, duration: 240 });
      }
      if (!this.anims.length) return;
      this.moving = true;
      this.release = TALK.motion({ finish: () => this.finish() });
      const batch = this.anims;
      Promise.all(batch.map(a => a.finished)).then(() => {
        if (this.anims === batch) this.finish();
      }, () => {});
    },

    finish() {
      const a = this.anims || [];
      this.anims = [];
      this.moving = false;
      if (this.pairs) this.pairs.forEach(p => {
        p.window.removeAttribute('clip-path'); p.labelWindow.style.clipPath = '';
      });
      if (this.release) { this.release(); this.release = null; }
      a.forEach(animation => { animation.cancel(); });
    },
    isMoving() { return !!this.moving; },
  });
})();
