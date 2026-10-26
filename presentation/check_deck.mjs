/* Offline check of the slides against slot/manuscript/slides.tex and the deck contract. Node standard library.
 *
 * Drift against slides.tex (the Beamer master): the same frames in the same order and labels; the
 * same titles and subtitles; the same \hypertarget names; the same link graph (\hyperlink buttons,
 * Back buttons and their order); and every registry key that slides.tex prints with \reg{key} on a
 * frame must be on the web frame as a number span with that key.
 * Contract: every number span names a key of the slot registry; no number sits in a slide headline;
 * every notation symbol is defined on its slide or an earlier one; the main frames follow the timing
 * plan; every frame has speaker notes.
 * Run after build.py (it reads dist/ for the notes); build.py runs it on every build.
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const require = createRequire(import.meta.url);
const problems = [];
const fail = (m) => problems.push(m);

/* ---------------------------------------------------------------- the registry */
function parseCsv(text) {
  const rows = []; let row = [], cell = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { row.push(cell); cell = ''; }
    else if (c === '\n') { row.push(cell); rows.push(row); row = []; cell = ''; }
    else if (c !== '\r') cell += c;
  }
  if (cell || row.length) { row.push(cell); rows.push(row); }
  const head = rows.shift();
  return rows.filter((r) => r.length === head.length).map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}
const REG = Object.fromEntries(parseCsv(fs.readFileSync(path.join(ROOT, 'audit/slot_manuscript_2026_10_23/registry/registry.csv'), 'utf8')).map((r) => [r.key, r]));

/* ---------------------------------------------------------------- slides.tex */
const TEX = fs.readFileSync(path.join(ROOT, 'slot/manuscript/slides.tex'), 'utf8');
function group(text, i) {
  let depth = 0;
  for (let j = i; j < text.length; j++) {
    const c = text[j];
    if (c === '\\') { j++; continue; }
    if (c === '{') depth++;
    else if (c === '}') { depth--; if (depth === 0) return [text.slice(i + 1, j), j + 1]; }
  }
  throw new Error('unbalanced braces at ' + i);
}
const stripComments = (s) => s.split('\n').map((l) => l.replace(/(^|[^\\])%.*$/, '$1')).join('\n');
const flat = (s) => stripComments(s).replace(/\\ /g, ' ').replace(/~/g, ' ').replace(/---/g, '—').replace(/--/g, '–').replace(/\s+/g, ' ').trim();

const talk = [];
{
  const re = /\\begin\{frame\}(\[[^\]]*\])?/g;
  let m;
  while ((m = re.exec(TEX))) {
    const opts = m[1] || '';
    const label = /label=([A-Za-z0-9]+)/.exec(opts)[1];
    let i = m.index + m[0].length, title = null;
    if (TEX[i] === '{') { const [t, j] = group(TEX, i); title = t; i = j; }
    const end = TEX.indexOf('\\end{frame}', i);
    const body = TEX.slice(i, end);
    let subtitle = '';
    const sm = /\\framesubtitle\{/.exec(body);
    if (sm) subtitle = flat(group(body, sm.index + sm[0].length - 1)[0]);
    const targets = [...body.matchAll(/\\hypertarget\{([^}]+)\}/g)].map((x) => x[1]);
    const links = [];
    const lre = /\\hyperlink\{([^}]+)\}\{\\beamer(goto|return)button\{([^}]*)\}\}|\\BackButton\{([^}]+)\}/g;
    let l;
    while ((l = lre.exec(body))) links.push(l[4] ? ['back', l[4]] : (l[2] === 'return' ? ['back', l[1]] : ['go', l[1], l[3]]));
    talk.push({ label, title, subtitle, targets, links, body });
  }
  const t = /\\title\[[^\]]*\]\{/.exec(TEX);
  const title = group(TEX, t.index + t[0].length - 1)[0].replace(/\\texorpdfstring\{[^}]*\}\{([^}]*)\}/, '$1').replace(/%\n/g, '');
  talk[0].title = title.replace(/\s+/g, ' ').trim();
}

/* The registry keys that slides.tex prints on a frame with \reg{key}. */
const regKeys = (f) => [...stripComments(f.body).matchAll(/\\reg\{([A-Za-z0-9_]+)\}/g)].map((x) => x[1]);

/* ---------------------------------------------------------------- content.js through stub helpers */
global.window = {};
require('./content.js');
const enc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
let LATEX = [];
/* {{key}} or \reg{key} prints a registry display inside a formula; for the symbol order check it stands for a digit. */
const withKeys = (l) => {
  LATEX.push(l.replace(/\{\{[A-Za-z0-9_]+\}\}|\\reg\{[A-Za-z0-9_]+\}/g, '0'));
  const keys = [...l.matchAll(/\{\{([A-Za-z0-9_]+)\}\}|\\reg\{([A-Za-z0-9_]+)\}/g)].map((x) => x[1] || x[2]);
  return keys.length ? `<span class="q q-tex" data-q="${enc(keys.join(' '))}">$${enc(l)}$</span>` : `<span class="m" data-latex="${enc(l)}">$${enc(l)}$</span>`;
};
const H = {
  m: withKeys,
  d: withKeys,
  q: (key) => `<span class="q" data-q="${enc(key)}">${enc(REG[key] ? REG[key].display : '?')}</span>`,
  v: (key) => { const [a, b] = String(REG[key] ? REG[key].value : 'NaN').split('/'); return b === undefined ? Number(a) : Number(a) / Number(b); },
  go: (target, text) => `<button data-target="${enc(target)}">${text}</button>`,
  back: (target) => `<button data-back="${enc(target)}">Back</button>`
};
const latexOf = {};
H.endFrame = (label) => { latexOf[label] = LATEX; LATEX = []; };
const deck = window.createDeck(H);
const frames = deck.frames;
const plain = (html) => html.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
const qkeys = (html) => [...html.matchAll(/data-q="([^"]*)"/g)].flatMap((m) => m[1].split(' '));

/* ---------------------------------------------------------------- drift */
if (frames.length !== talk.length) fail(`content.js has ${frames.length} frames; slides.tex has ${talk.length}`);
let numberPairs = 0;
talk.forEach((t, i) => {
  const f = frames[i];
  if (!f) return;
  const where = `${t.label}`;
  if (f.label !== t.label) fail(`frame ${i + 1}: content.js has ${f.label}, slides.tex has ${t.label}`);
  if ((f.title || '').trim() !== (t.title || '').trim()) fail(`${where}: title "${f.title}" differs from slides.tex "${t.title}"`);
  const sub = plain(f.subtitle || '');
  if (sub !== t.subtitle) fail(`${where}: subtitle differs\n   web:  ${sub}\n   tex:  ${t.subtitle}`);
  if (JSON.stringify(f.targets || []) !== JSON.stringify(t.targets)) fail(`${where}: hypertargets ${JSON.stringify(f.targets)} differ from ${JSON.stringify(t.targets)}`);
  const links = [...(f.body || '').matchAll(/<button data-(target|back)="([^"]*)">([^<]*)<\/button>/g)].map((m) => (m[1] === 'back' ? ['back', m[2]] : ['go', m[2], m[3]]));
  if (JSON.stringify(links) !== JSON.stringify(t.links)) fail(`${where}: links ${JSON.stringify(links)} differ from slides.tex ${JSON.stringify(t.links)}`);
  // numbers: every \reg{key} of the Beamer frame is on the web frame
  const have = new Set(qkeys((f.subtitle || '') + (f.body || '')));
  for (const k of regKeys(t)) {
    if (!REG[k]) { fail(`${where}: slides.tex prints \\reg{${k}}, which the registry does not hold`); continue; }
    numberPairs++;
    if (!have.has(k)) fail(`${where}: slides.tex prints \\reg{${k}}; the web frame does not carry it`);
  }
});

/* ---------------------------------------------------------------- contract */
const ids = new Set();
let mainMinutes = 0;
for (const f of frames) {
  if (ids.has(f.id)) fail(`duplicate id ${f.id}`);
  ids.add(f.id);
  const html = (f.subtitle || '') + (f.body || '');
  for (const k of qkeys(html)) if (!REG[k]) fail(`${f.label}: unknown registry key ${k}`);
  // no number in a headline
  const bare = (f.title || '').replace(/\$[^$]*\$/g, '');
  for (const n of bare.match(/\d+\.\d+/g) || []) fail(`${f.label}: number ${n} in the headline`);
  if (!f.backup) mainMinutes += f.minutes;
  if (f.backup) {
    if (!f.origin || !ids.has(f.origin) && !frames.some((g) => g.id === f.origin)) fail(`${f.label}: backup without a valid origin`);
    if (!/data-back=/.test(f.body)) fail(`${f.label}: backup without a Back button`);
  }
}
if (Math.abs(mainMinutes - 30.25) > 1e-9) fail(`main frames sum to ${mainMinutes} minutes, not the 30.25 of the timing plan`);

/* every symbol is defined on its slide or an earlier one, in deck order */
const keys = new Set(deck.glossary.map((g) => g.key));
const defined = new Set();
for (const f of frames) {
  for (const k of f.defines || []) { if (!keys.has(k)) fail(`${f.label}: defines unknown symbol ${k}`); defined.add(k); }
  const latex = (latexOf[f.label] || []).concat((f.title.match(/\$([^$]+)\$/g) || []).map((s) => s.slice(1, -1))).join('\n');
  for (const g of deck.glossary) {
    let re;
    try { re = new RegExp(g.pattern); } catch (e) { fail(`glossary ${g.key}: bad pattern`); continue; }
    if (re.test(latex) && !defined.has(g.key)) fail(`${f.label}: uses ${g.key} before the frame that defines it`);
  }
}
for (const k of keys) if (!frames.some((f) => (f.defines || []).includes(k))) fail(`symbol ${k} is never defined on a slide`);

/* speaker notes: every frame has a block */
const dist = path.join(HERE, 'dist');
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const page = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
  const nm = /window\.CCC_NOTES = (\{[\s\S]*?\});\s*<\/script>/.exec(page);
  const notes = nm ? JSON.parse(nm[1]) : {};
  for (const f of frames) if (!notes[f.label] || !notes[f.label].html) fail(`${f.label}: no speaker notes`);
  const sections = (page.match(/<section class="slide/g) || []).length;
  if (sections !== talk.length) fail(`dist/index.html has ${sections} slides, not ${talk.length}`);
} else fail('dist/index.html is missing; run python3 presentation/build.py');

/* ---------------------------------------------------------------- the design system */
/* The deck shares the ruled document of DESIGN.md (repository root) with the research brief. The
 * tokens that both stylesheets declare must agree, and the rejected purple palette of the earlier
 * "UCL family" design must not come back through any deck source or the built page. */
const PURPLE = /#(?:361A54|993BFF|BA82FF)\b|--ucl-(?:dark|bright|mid)\b/gi;
const deckFiles = ['deck.css', 'charts.js', 'deck.js', 'template.html', 'content.js'].map((n) => path.join(HERE, n));
if (fs.existsSync(path.join(dist, 'index.html'))) deckFiles.push(path.join(dist, 'index.html'));
for (const file of deckFiles) {
  const text = fs.readFileSync(file, 'utf8');
  const found = text.match(PURPLE);
  if (found) fail(`${path.relative(ROOT, file)}: the rejected purple palette appears (${[...new Set(found)].join(', ')})`);
}
function rootTokens(css, theme) {
  const re = theme === 'dark' ? /:root\[data-theme="dark"\]\s*\{([^}]*)\}/ : /:root(?:,\s*:root\[data-theme="light"\])?\s*\{([^}]*)\}/;
  const m = re.exec(css);
  if (!m) return null;
  const out = {};
  for (const decl of m[1].split(';')) {
    const i = decl.indexOf(':');
    if (i < 0) continue;
    const name = decl.slice(0, i).trim(), value = decl.slice(i + 1).trim().replace(/\s+/g, ' ');
    if (name.startsWith('--')) out[name] = value;
  }
  return out;
}
const deckCss = fs.readFileSync(path.join(HERE, 'deck.css'), 'utf8');
const briefCss = fs.readFileSync(path.join(ROOT, 'handout/style.css'), 'utf8');
let sharedTokens = 0;
for (const theme of ['light', 'dark']) {
  const a = rootTokens(deckCss, theme), b = rootTokens(briefCss, theme);
  if (!a || !b) { fail(`${theme} theme: a :root token block is missing in deck.css or handout/style.css`); continue; }
  for (const name of Object.keys(a)) {
    if (!(name in b)) continue;
    sharedTokens++;
    if (a[name] !== b[name]) fail(`${theme} theme: token ${name} is ${a[name]} in deck.css and ${b[name]} in handout/style.css`);
  }
}

const mains = frames.filter((f) => !f.backup).length;
console.log(`Compared ${frames.length} frames (${mains} main, ${frames.length - mains} backup) with slides.tex: order, titles, subtitles, targets and links; ` +
  `${numberPairs} printed registry keys found on the web frames; ${keys.size} notation symbols; ${mainMinutes} planned minutes before questions; ` +
  `${sharedTokens} design tokens shared with handout/style.css agree; no purple palette in ${deckFiles.length} deck files.`);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
console.log('Deck matches slides.tex and the deck contract.');
