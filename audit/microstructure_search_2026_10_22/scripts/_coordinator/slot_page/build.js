// Build the order-slot explainer page. TeX becomes static SVG at build time; no script loads at view time.
// Output 1 (argv[2]): a self-contained page; glyph paths sit in one hidden <defs> block (fontCache 'global').
// Output 2 (argv[3]): a compact page for the chat viewer; each formula is a local SVG file used as a CSS mask,
//   so the formula takes the text color of the theme. The viewer inlines the files.
const fs = require('fs');
const path = require('path');
const MJ = '/home/uctpiaj/work/.vscode-server/extensions/james-yu.latex-workshop-10.20.0/node_modules/mathjax-full/js/';
const {mathjax} = require(MJ + 'mathjax.js');
const {TeX} = require(MJ + 'input/tex.js');
const {SVG} = require(MJ + 'output/svg.js');
const {liteAdaptor} = require(MJ + 'adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require(MJ + 'handlers/html.js');
const {AllPackages} = require(MJ + 'input/tex/AllPackages.js');

const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
function makeDoc(cache) {
  const svg = new SVG({fontCache: cache});
  return {svg, doc: mathjax.document('', {InputJax: new TeX({packages: AllPackages}), OutputJax: svg})};
}
const G = makeDoc('global'), L = makeDoc('local');
let errors = 0;
function check(out, src) { if (out.includes('merror') || out.includes('data-mjx-error')) { errors++; console.error('TeX error in:', src); } }

const tpl = fs.readFileSync(path.join(__dirname, 'template.html'), 'utf8');
const chartJs = fs.readFileSync(path.join(__dirname, 'charts.js'), 'utf8');
const MATH = /\\\[([\s\S]+?)\\\]|\\\(([\s\S]+?)\\\)/g;

// ---- output 1: self-contained ----
let full = tpl.replace(MATH, (all, d, i) => {
  const src = (d || i).trim();
  const out = adaptor.outerHTML(G.doc.convert(src, {display: !!d, em: 16, ex: 8, containerWidth: 700}));
  check(out, src); return out;
});
const cache = `<svg id="MJX-SVG-global-cache" xmlns="http://www.w3.org/2000/svg" style="display:none">${adaptor.outerHTML(G.svg.fontCache.getCache())}</svg>`;
full = full.replace('<div class="page">', cache + '\n<div class="page">')
           .replace('/*CHARTS*/', chartJs)
           .replace(/ data-mml-node="[^"]*"/g, '').replace(/ data-c="[^"]*"/g, '');
fs.writeFileSync(process.argv[2], full);

// ---- output 2: compact page with mask images ----
const eqDir = path.join(__dirname, 'eq');
fs.mkdirSync(eqDir, {recursive: true});
for (const f of fs.readdirSync(eqDir)) fs.unlinkSync(path.join(eqDir, f));
const S = 1.12;                       // scale against the sans text
const seen = new Map(); const rules = [];
let compact = tpl.replace(MATH, (all, d, i) => {
  const src = (d || i).trim(); const display = !!d; const key = (display ? 'D:' : 'I:') + src;
  if (!seen.has(key)) {
    const node = L.doc.convert(src, {display, em: 16, ex: 8, containerWidth: 700});
    let s = adaptor.outerHTML(adaptor.firstChild(node)).replace(/ data-mml-node="[^"]*"/g, '').replace(/ data-c="[^"]*"/g, '');
    check(s, src);
    const vb = s.match(/viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"/);
    const va = s.match(/vertical-align: ([-\d.]+)ex/);
    const id = 'q' + seen.size;
    const file = path.join(eqDir, id + '.svg');
    fs.writeFileSync(file, s);
    rules.push(`.${id}{mask-image:url(${file})}`);
    seen.set(key, {id, w: +vb[3] / 1000 * S, h: +vb[4] / 1000 * S, v: (va ? +va[1] : 0) / 2 * S});
  }
  const q = seen.get(key);
  if (display) return `<span class="dm"><span class="mm ${q.id}" style="width:${q.w.toFixed(3)}em;aspect-ratio:${q.w.toFixed(3)}/${q.h.toFixed(3)}"></span></span>`;
  return `<span class="mm ${q.id}" style="width:${q.w.toFixed(3)}em;height:${q.h.toFixed(3)}em;vertical-align:${q.v.toFixed(3)}em"></span>`;
});
const maskCss = `.mm{display:inline-block;background:currentColor;mask-repeat:no-repeat;mask-position:center;mask-size:contain}
.dm{display:block;text-align:center;margin:14px 0}.dm .mm{max-width:100%;height:auto}
${rules.join('\n')}`;
compact = compact.replace(/mjx-container\[jax="SVG"\][^\n]*\n/g, '')
                 .replace('</style>', maskCss + '\n</style>').replace('/*CHARTS*/', chartJs);
fs.writeFileSync(process.argv[3], compact);
console.log(`unique formulas: ${seen.size}; TeX errors: ${errors}; full: ${Buffer.byteLength(full)} B; compact: ${Buffer.byteLength(compact)} B`);
