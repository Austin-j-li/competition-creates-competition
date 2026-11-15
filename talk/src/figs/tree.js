/* Page 8: the tree of what shareholders are paid after order x. Shapes from slide09's boxes.
   From "Order x" the branch "rival prepares", e(x), splits into class H, mu(x), ending at t_H,
   and class L, 1 - mu(x), ending at t_L; the branch "no prepared rival", 1 - e(x), ends at t_0.
   The tree is three root-to-leaf paths drawn on top of one another. On its click (step 2) each
   path is drawn from "Order x" at one common speed, so the drawing front moves outward through
   the first-level branches and then the class branches; every label arrives as the front passes
   it. When the formula's click is the newest step, the paths are set heavy and the leaves take a
   keyline (CSS, through .is-new on the formula's row). In the reading view only, pointing at a
   leaf marks its path and its leaf. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const W = 596, H = 452;
  const XS = 86, X1 = 104, X2 = 294, XE = 452, XL = 468;
  const YH = 128, YU = 194, YL = 260, YR = 298, YD = 402;
  const DRAW = 360;              // the longest path, drawn at constant speed
  const LABEL = 150;
  const PATHS = {
    t0: `M${XS} ${YR}H${X1}V${YD}H${XE}`,
    tH: `M${XS} ${YR}H${X1}V${YU}H${X2}V${YH}H${XE}`,
    tL: `M${XS} ${YR}H${X1}V${YU}H${X2}V${YL}H${XE}`,
  };
  // the terms of the formula's first line, if the page tags them (KaTeX \htmlClass with trust):
  // e(x) is shared by the two terms of the prepared rival
  const TERMS = { t0: ['.pf-t0'], tH: ['.pf-tH', '.pf-tE'], tL: ['.pf-tL', '.pf-tE'] };

  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    if (parent) parent.append(el);
    return el;
  }

  TALK.figure('tree', {
    mount(el, ctx) {
      this.el = el;
      this.ctx = ctx;
      this.anims = [];
      this.page = el.closest('.page');
      el.style.width = W + 'px';
      el.style.height = H + 'px';
      const box = this.box = document.createElement('div');
      box.className = 'tree-box';
      el.append(box);
      const root = svg('svg', { class: 'fig-svg', viewBox: `0 0 ${W} ${H}`, width: W, height: H, 'aria-hidden': 'true' }, box);
      this.paths = {};
      Object.entries(PATHS).forEach(([k, d]) => {
        const path = svg('path', { class: 'tree-path', 'data-leaf': k, d }, root);
        this.paths[k] = { el: path, len: path.getTotalLength() };
      });
      const sH = 20 + (YR - YU);                       // distance to the first fork's branches
      const sC = sH + (X2 - X1) + (YU - YH);           // to the class branches
      this.labels = [
        this.label('tree-root', XS - 10, YR, 'Order ', 'x', 'right-mid', 0),
        this.label('tree-branch', X1 + 10, YU - 4, 'rival prepares', null, 'above', sH),
        this.label('tree-prob', X1 + 10, YU + 6, null, 'ex', '', sH),
        this.label('tree-branch', X1 + 10, YD - 4, 'no prepared rival', null, 'above', sH),
        this.label('tree-prob', X1 + 10, YD + 6, null, 'onemex', '', sH),
        this.label('tree-branch', X2 + 10, YH - 4, 'class H', null, 'above', sC),
        this.label('tree-prob', X2 + 10, YH + 6, null, 'mux', '', sC),
        this.label('tree-branch', X2 + 10, YL - 4, 'class L', null, 'above', sC),
        this.label('tree-prob', X2 + 10, YL + 6, null, 'onemmu', '', sC),
        this.label('tree-head', XL, 6, 'shareholders are paid', null, '', 'end'),
      ];
      this.leaves = {};
      [['tH', YH], ['tL', YL], ['t0', YD]].forEach(([k, y]) => {
        const leaf = this.label('tree-leaf', XL, y, null, k, 'left-mid', 'end');
        leaf.dataset.leaf = k;
        this.leaves[k] = leaf;
        leaf.addEventListener('pointerenter', () => this.mark(k));
        leaf.addEventListener('pointerleave', () => this.mark(null));
      });
    },

    label(cls, x, y, word, key, align, at) {
      const span = document.createElement('span');
      span.className = 'fig-label ' + cls;
      span.style.left = x + 'px';
      span.style.top = y + 'px';
      if (align === 'right-mid') span.style.transform = 'translate(-100%, -50%)';
      else if (align === 'left-mid') span.style.transform = 'translateY(-50%)';
      else if (align === 'above') span.style.transform = 'translateY(-100%)';
      if (word) span.append(document.createTextNode(word));
      if (key) span.insertAdjacentHTML('beforeend', this.ctx.math['setupfigs.' + key]);
      span.__at = at;
      this.box.append(span);
      return span;
    },

    terms(k) {
      if (!k) return [];
      return TERMS[k].flatMap(sel => [...this.page.querySelectorAll(sel)]);
    },

    // reading view only: a leaf, its path and its term
    mark(k) {
      if (k && !document.body.classList.contains('is-reading')) return;
      Object.entries(this.paths).forEach(([key, p]) => p.el.classList.toggle('is-marked', key === k));
      Object.entries(this.leaves).forEach(([key, leaf]) => leaf.classList.toggle('is-marked', key === k));
      this.page.querySelectorAll('.pf-t0, .pf-tH, .pf-tL, .pf-tE').forEach(t => t.classList.remove('is-marked'));
      this.terms(k).forEach(t => t.classList.add('is-marked'));
      this.box.classList.toggle('is-pointing', !!k);
    },

    setStep(step, opts) {
      this.finish();
      this.mark(null);
      const on = step >= 2;
      this.box.classList.toggle('is-on', on);
      if (!on || !opts.animate || opts.dir !== 1 || opts.from.page !== opts.page || opts.from.step !== 1) return;
      const longest = Math.max(...Object.values(this.paths).map(p => p.len));
      const speed = longest / DRAW;
      Object.values(this.paths).forEach(({ el, len }) => {
        // pathLength 1 makes the dash pattern independent of the path's own length
        el.setAttribute('pathLength', '1');
        this.anims.push(el.animate([
          { strokeDasharray: '1 1', strokeDashoffset: 1 },
          { strokeDasharray: '1 1', strokeDashoffset: 0 },
        ], { duration: len / speed, easing: 'linear', fill: 'both' }));
      });
      this.labels.concat(Object.values(this.leaves)).forEach(span => {
        const at = span.__at === 'end' ? DRAW - 30 : span.__at / speed;
        this.anims.push(span.animate([{ opacity: 0 }, { opacity: 1 }],
          { duration: LABEL, delay: at, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'both' }));
      });
      this.moving = true;
      this.release = TALK.motion({ finish: () => this.finish() });
      const batch = this.anims;
      Promise.all(batch.map(a => a.finished)).then(() => { if (this.anims === batch) this.finish(); }, () => {});
    },

    finish() {
      const a = this.anims || [];
      this.anims = [];
      this.moving = false;
      if (this.paths) Object.values(this.paths).forEach(p => p.el.removeAttribute('pathLength'));
      if (this.release) { this.release(); this.release = null; }
      a.forEach(x => x.cancel());
    },
    isMoving() { return !!this.moving; },
  });
})();
