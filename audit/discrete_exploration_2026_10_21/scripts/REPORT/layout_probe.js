// Print-only probe: run the report's chart script against a minimal DOM stub at two widths,
// then print text boxes (estimated) that leave the viewBox or overlap another text box or a mark.
const fs = require('fs');
const src = fs.readFileSync(process.argv[2], 'utf8');
function run(width) {
  const nodes = {};
  function mk(tag) {
    return { tag, attrs: {}, children: [], textContent: '', parentNode: null,
      setAttribute(k, v) { this.attrs[k] = String(v); },
      appendChild(c) { c.parentNode = this; this.children.push(c); return c; },
      removeChild(c) { this.children = this.children.filter(x => x !== c); },
      get firstChild() { return this.children[0]; },
      classList: { set: new Set(), toggle(c, on) { on ? this.set.add(c) : this.set.delete(c); } } };
  }
  for (const id of ['ch-post', 'ch-p2', 'ch-p3']) { const s = mk('svg'); s.parentNode = { clientWidth: width }; nodes[id] = s; }
  global.document = { createElementNS: (ns, t) => mk(t), getElementById: id => nodes[id] || null };
  global.window = { addEventListener() {} };
  eval(src);
  return nodes;
}
function textOf(t) { return t.children.map(c => c.textContent).join(''); }
function analyse(nodes, width) {
  for (const id in nodes) {
    const svg = nodes[id];
    const vb = svg.attrs.viewBox.split(' ').map(Number), W = vb[2], H = vb[3];
    const fs = svg.classList.set.has('narrow') ? 16 : 12;
    const boxes = [], marks = [];
    for (const e of svg.children) {
      if (e.tag === 'text') {
        const s = textOf(e), x = +e.attrs.x, y = +e.attrs.y;
        const w = s.length * fs * (/\bb\b/.test(e.attrs.class || '') ? 0.62 : 0.55), anc = e.attrs['text-anchor'] || 'start';
        const x0 = anc === 'end' ? x - w : anc === 'middle' ? x - w / 2 : x;
        boxes.push({ s, x0, x1: x0 + w, y0: y - fs * 0.78, y1: y + fs * 0.22 });
      } else if (e.tag === 'circle') {
        const r = +e.attrs.r; marks.push({ s: 'circle', x0: +e.attrs.cx - r, x1: +e.attrs.cx + r, y0: +e.attrs.cy - r, y1: +e.attrs.cy + r });
      } else if (e.tag === 'rect' && !(e.attrs['fill-opacity'] && +e.attrs['fill-opacity'] < 0.2)) {
        marks.push({ s: 'rect', x0: +e.attrs.x, x1: +e.attrs.x + +e.attrs.width, y0: +e.attrs.y, y1: +e.attrs.y + +e.attrs.height });
      } else if (e.tag === 'line') {
        const x1 = +e.attrs.x1, x2 = +e.attrs.x2, y1 = +e.attrs.y1, y2 = +e.attrs.y2;
        marks.push({ s: 'line ' + (e.attrs.class || ''), x0: Math.min(x1, x2) - 1, x1: Math.max(x1, x2) + 1, y0: Math.min(y1, y2) - 1, y1: Math.max(y1, y2) + 1 });
      }
    }
    const ov = (a, b) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;
    console.log(`== ${id} at ${width}px: viewBox ${W}x${H}, ${boxes.length} labels, ${marks.length} marks`);
    for (const b of boxes) {
      if (b.x0 < 0 || b.x1 > W || b.y0 < 0 || b.y1 > H) console.log(`  EDGE  "${b.s}" x ${b.x0.toFixed(0)}..${b.x1.toFixed(0)} y ${b.y0.toFixed(0)}..${b.y1.toFixed(0)}`);
    }
    for (let i = 0; i < boxes.length; i++) for (let j = i + 1; j < boxes.length; j++)
      if (ov(boxes[i], boxes[j])) console.log(`  TEXT  "${boxes[i].s}" / "${boxes[j].s}"`);
    for (const b of boxes) for (const m of marks) if (ov(b, m)) console.log(`  MARK  "${b.s}" / ${m.s} x ${m.x0.toFixed(0)}..${m.x1.toFixed(0)} y ${m.y0.toFixed(0)}..${m.y1.toFixed(0)}`);
  }
}
for (const w of [713, 375]) analyse(run(w), w);
