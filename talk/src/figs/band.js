/* Schematic coordinates follow the shape boxes of master_dump/slide14.txt, scaled by 5/3. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const EASE = 'cubic-bezier(.16,1,.3,1)';
  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    parent.append(el); return el;
  }
  TALK.figure('band', {
    mount(el, ctx) {
      this.el = el; this.ctx = ctx; this.anims = [];
      // The shared look wipes ordinary reveals. These two schematics own their geometry's
      // motion, so finish only the look's additional wipe on our figure groups.
      document.addEventListener('talk:state', event => {
        if (event.detail.page !== ctx.page) return;
        el.getAnimations({ subtree: true }).forEach(animation => {
          if (!this.anims.includes(animation) && animation.effect.getKeyframes().some(frame => 'clipPath' in frame)) animation.finish();
        });
      });
      const root = svg('svg', { viewBox: '0 0 1440 268', 'aria-hidden': 'true' }, el);
      svg('path', { class: 'blocks-line', d: 'M158 122H1282M158 122v9M1282 122v9' }, root);
      // the axis ends are tick numbers: Jost, on the baseline of the words under the axis
      this.label(el, 'center ax-label', 158, 153, '', 'zero', true);
      this.label(el, 'center ax-label', 1282, 153, '', 'one', true);
      const band = svg('g', { 'data-step': 1 }, root);
      this.left = svg('path', { class: 'blocks-line blocks-heavy', d: 'M720 122H462' }, band);
      this.right = svg('path', { class: 'blocks-line blocks-heavy', d: 'M720 122H978' }, band);
      this.caps = svg('path', { class: 'blocks-line', d: 'M462 105v34M978 105v34' }, band);
      svg('circle', { class: 'blocks-dot', cx: 720, cy: 122 }, band);
      this.labels = document.createElement('div'); this.labels.dataset.step = 1; el.append(this.labels);
      this.label(this.labels, 'center', 462, 65, '', 'lower');
      this.label(this.labels, 'center', 720, 65, '', 'prior');
      this.label(this.labels, 'center', 978, 65, '', 'upper');
      ['after a sale', 'after no order', 'after a purchase'].forEach((word, i) => this.label(this.labels, 'center', [462, 720, 978][i], 153, word));
      this.label(this.labels, 'center', 720, 187, 'when class H buys and class L sells');
      this.legend = svg('path', { class: 'blocks-line', d: 'M462 224V234H978V224' }, band);   // a bracket with its two ends, as the master draws it
      this.label(this.labels, '', 994, 219, 'beliefs after any order');
      const prep = svg('g', { 'data-step': 3 }, root);
      this.arrow = svg('path', { class: 'blocks-line preparation', d: 'M877 122V42H1282', pathLength: 1 }, prep);
      this.tip = svg('path', { class: 'blocks-line preparation', d: 'M1270 33l12 9-12 9' }, prep);
      this.prepLabels = document.createElement('div'); this.prepLabels.dataset.step = 3; el.append(this.prepLabels);
      this.label(this.prepLabels, 'center preparation', 877, 0, '', 'threshold');
      this.label(this.prepLabels, 'preparation word-strong', 924, 3, 'costly rival prepares');
    },
    label(parent, cls, x, y, word, key, plain) {
      const span = document.createElement('span'); span.className = 'fig-label ' + cls;
      span.style.left = x + 'px'; span.style.top = y + 'px';
      if (key) span.innerHTML = word + this.ctx.math['blocks.' + key]; else span.textContent = word;
      if (plain) span.textContent = (span.querySelector('.katex-html') || span).textContent;   // a number, set as text
      parent.append(span); return span;
    },
    animate(el, frames, timing) {
      const a = el.animate(frames, { easing: EASE, fill: 'both', ...timing }); this.anims.push(a); return a;
    },
    setStep(step, opts) {
      this.finish();
      if (!opts.animate || opts.dir !== 1 || opts.from.page !== opts.page) return;
      if (step === 1) {
        // Both halves start at the prior, so the band expands outwards rather than wiping across.
        [this.left, this.right].forEach(line => this.animate(line, [
          { transform: 'translateX(720px) scaleX(0) translateX(-720px)' },
          { transform: 'translateX(720px) scaleX(1) translateX(-720px)' },
        ], { duration: 350 }));
        [this.caps, this.legend].forEach(el => this.animate(el, [{ opacity: 0 }, { opacity: 1 }], { delay: 280, duration: 70 }));
        this.animate(this.labels, [{ opacity: 0 }, { opacity: 1 }], { delay: 150, duration: 200 });
      } else if (step === 3) {
        this.animate(this.arrow, [{ strokeDasharray: '1', strokeDashoffset: '1' }, { strokeDasharray: '1', strokeDashoffset: '0' }], { duration: 350 });
        this.animate(this.tip, [{ opacity: 0 }, { opacity: 1 }], { delay: 300, duration: 50 });
        this.animate(this.prepLabels, [{ opacity: 0 }, { opacity: 1 }], { duration: 240 });
      }
      if (!this.anims.length) return;
      this.release = TALK.motion({ finish: () => this.finish() });
      const batch = this.anims;
      Promise.all(batch.map(a => a.finished)).then(() => { if (batch === this.anims) this.finish(); }, () => {});
    },
    finish() {
      const batch = this.anims || []; this.anims = [];
      if (this.release) { this.release(); this.release = null; }
      batch.forEach(a => a.cancel());
    },
    isMoving() { return !!this.anims.length; },
  });
})();
