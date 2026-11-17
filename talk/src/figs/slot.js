/* The order slot in full (backup B7), drawn in code from the shape boxes of slide33.txt
   (960 x 540 pt page; 1 pt = 5/3 px on the stage; x measured from the page margin at 48 pt,
   y from the top of the first row of boxes at 115 pt).
   The boxes are in the page file (div.slot-box[data-box]); this module places them, draws their
   outlines and the arrows between them. Who fills the slot is on the left, who sees what on the
   right. Nothing moves. */
(function () {
  'use strict';
  const NS = 'http://www.w3.org/2000/svg';
  const K = 5 / 3;
  const X = (x) => (x - 48) * K, Y = (y) => (y - 115) * K;
  const H = 100 * K;
  // the first line of every box sits about 30 px below its top edge: the arrows leave from there
  const LINE = 30;
  const BOX = {
    informed: { x: X(48), y: Y(115), w: 215 * K },
    liquidity: { x: X(48), y: Y(226), w: 215 * K, h: 190 },   // the master's box is 197.5 pt wide; drawn as wide as the one above
    slot: { x: X(311), y: Y(115), w: 160 * K, heavy: true },
    makers: { x: X(519), y: Y(115), w: 205 * K },
    rival: { x: X(772), y: Y(115), w: 128 * K },
  };

  function svg(tag, attrs, parent) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs || {}).forEach(([k, v]) => el.setAttribute(k, v));
    if (parent) parent.append(el);
    return el;
  }

  TALK.figure('slot', {
    mount(el) {
      const root = svg('svg', { class: 'fig-svg', viewBox: '0 0 1440 376', 'aria-hidden': 'true' }, el);
      el.prepend(root);
      Object.entries(BOX).forEach(([id, b]) => {
        svg('rect', { class: 'slot-outline' + (b.heavy ? ' is-heavy' : ''), x: b.x, y: b.y, width: b.w, height: b.h || H }, root);
        const text = el.querySelector(`.slot-box[data-box="${id}"]`);
        if (text) Object.assign(text.style, { left: b.x + 'px', top: b.y + 'px', width: b.w + 'px', height: (b.h || H) + 'px' });
      });
      const head = (x, y, dir) => {   // an arrowhead, tip at (x, y), pointing right (dir 0) or up (dir 1)
        const d = dir ? `M${x} ${y}l-8 14h16z` : `M${x} ${y}l-14 -8v16z`;
        svg('path', { class: 'slot-head', d }, root);
      };
      const arrow = (x0, x1, y) => {
        svg('path', { class: 'slot-arrow', d: `M${x0} ${y}H${x1 - 12}` }, root);
        head(x1, y, 0);
      };
      const y0 = LINE;
      arrow(X(270), X(304), y0);        // informed trader to the slot
      arrow(X(478), X(512), y0);        // slot to market makers
      arrow(X(731), X(765), y0);        // market makers to the rival
      // the liquidity trader joins the first arrow from below
      const yl = Y(226) + LINE;
      svg('path', { class: 'slot-arrow', d: `M${X(270)} ${yl}H${X(287)}V${y0 + 12}` }, root);
      head(X(287), y0, 1);
    },
    setStep() {},
  });
})();
