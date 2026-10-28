/* Render the slide records of content.js to HTML at build time.
 *
 * Reads one JSON object on stdin: { registry: { "<key>": { value, display } } }, the slot registry.
 * Writes { frames, notation, glossary, numbers, used } to stdout. Supplies the helpers of the
 * content.js contract: KaTeX renders the mathematics here, and every number is the registry
 * display of its key, the string that \reg{key} prints in slot/manuscript/slides.tex. A key that the
 * registry does not hold stops the build. Node standard library and the locked KaTeX copy only.
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
const katex = require('../handout/vendor/katex.min.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const REG = input.registry;
global.window = {};
require('./content.js');

const problems = [];
const numbers = [];
const used = new Set();
/* Helpers record here; endFrame (called by content.js after each frame) labels and moves it. */
let pending = { problems: [], numbers: [] };
const report = (msg) => pending.problems.push(msg);
function flush(label) {
  for (const p of pending.problems) problems.push(`${label}: ${p}`);
  for (const n of pending.numbers) numbers.push({ ...n, frame: label });
  pending = { problems: [], numbers: [] };
}

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tex = (latex, display) => {
  try { return katex.renderToString(latex, { displayMode: !!display, throwOnError: true, strict: 'ignore', trust: false }); }
  catch (e) { report(`KaTeX cannot render ${latex}: ${e.message}`); return `<span class="math-error">${esc(latex)}</span>`; }
};

/* The registry display of a key. A display may hold LaTeX (a percent sign, \ensuremath). */
function row(key) {
  const r = REG[key];
  if (!r) { report(`unknown registry key ${key}`); return null; }
  used.add(key);
  pending.numbers.push({ key });
  return r;
}
const plain = (display) => display.replace(/\\ensuremath\{(.*)\}$/, '$1').replace(/\\%/g, '%');
const texOf = (display) => display.replace(/\\ensuremath\{(.*)\}$/, '$1').replace(/\\%/g, '\\%');
const needsMath = (display) => /\\/.test(plain(display));
const pretty = (s) => String(s).replace(/^-(?=\d)/, '−');

/* A registry value rounded to fewer decimals, as \regr{key}{digits} prints it in slides.tex (the talk
   prints some strengths with three decimals where the registry display has six). */
function rounded(r, digits) {
  const [a, b] = String(r.value).split('/');
  return (b === undefined ? Number(a) : Number(a) / Number(b)).toFixed(digits);
}

/* A registry number in running text; digits, when given, rounds it as \regr does. */
function q(key, digits) {
  const r = row(key);
  if (!r) return `<span class="math-error">??${esc(key)}</span>`;
  if (digits !== undefined) {
    return `<span class="q" data-q="${esc(key)}" data-round="${digits}" title="${esc(key + ' = ' + plain(r.display))}">${esc(rounded(r, digits))}</span>`;
  }
  const shown = needsMath(r.display) ? tex(texOf(r.display)) : esc(pretty(plain(r.display)));
  return `<span class="q" data-q="${esc(key)}" title="${esc(key + ' = ' + plain(r.display))}">${shown}</span>`;
}

/* Mathematics; {{key}} or \reg{key} inside the formula is replaced by the registry display before KaTeX
   runs. \reg{key} keeps a formula of a subtitle identical to its slides.tex text. */
function withKeys(latex, display) {
  const keys = [], rounds = [];
  const filled = latex.replace(/\{\{([A-Za-z0-9_]+)(?:\|(\d))?\}\}|\\reg\{([A-Za-z0-9_]+)\}/g, (_, k1, d, k2) => {
    const k = k1 || k2;
    const r = row(k);
    keys.push(k);
    if (d !== undefined) { rounds.push(`${k}:${d}`); return r ? rounded(r, Number(d)) : '??'; }
    return r ? texOf(r.display).replace(/^-(?=\d)/, '-') : '??';
  });
  const html = tex(filled, display);
  if (!keys.length) return html;
  const title = keys.map((k) => `${k} = ${REG[k] ? plain(REG[k].display) : '?'}`).join('; ');
  const round = rounds.length ? ` data-round="${esc(rounds.join(' '))}"` : '';
  return `<span class="q q-tex" data-q="${esc(keys.join(' '))}"${round} title="${esc(title)}">${html}</span>`;
}

/* The registry value as a number, for layout (the position of a mark on a scale). */
function value(key) {
  const r = row(key);
  if (!r) return NaN;
  const [a, b] = String(r.value).split('/');
  return b === undefined ? Number(a) : Number(a) / Number(b);
}

const H = {
  m: (l) => withKeys(l, false),
  d: (l) => `<div class="display-math">${withKeys(l, true)}</div>`,
  q,
  v: value,
  go: (target, text) => `<button type="button" class="goto" data-target="${esc(target)}">${text}</button>`,
  back: (target) => `<button type="button" class="goto back" data-back="${esc(target)}">Back</button>`
};

/* Titles are slides.tex strings: $...$ is mathematics. */
function title(f) {
  return esc(f.title).replace(/\$([^$]+)\$/g, (_, l) => tex(l.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')));
}

const frames = [];
H.endFrame = flush;
let deck = null;
try { deck = window.createDeck(H); }
catch (e) { problems.push(`content.js: ${e.stack || e.message}`); }
flush('content.js (outside a frame)');
if (deck) {
  for (const f of deck.frames) {
    const t = title(f);
    flush(f.label);
    frames.push({ ...f, titleHtml: t });
  }
}
if (problems.length) {
  process.stderr.write(problems.join('\n') + '\n');
  process.exit(1);
}
process.stdout.write(JSON.stringify({
  frames, notation: deck.notation, glossary: deck.glossary, numbers, used: [...used].sort()
}));
