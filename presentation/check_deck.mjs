/* Offline check of the slides against talk/talk.tex and the deck contract. Node standard library.
 *
 * Drift against talk.tex (the Beamer master): the 47 frames in the same order and labels; the
 * same titles and subtitles; the same \hypertarget names; the same link graph (\hyperlink
 * buttons, Back buttons and their order); and every number that talk.tex tags with a
 * "% source:" comment. A tagged number must be on the web slide as a span that carries the
 * same registry key and rounds from the registry value; a formula reference (no number of
 * its own, such as M = 1 - m) must carry its key on the slide; table numbers must appear.
 * Contract: status words come from the paper's vocabulary; every number span names a
 * registry key or a paper table; no registry number sits in a slide headline unless talk.tex
 * prints it there; every notation symbol is defined on its slide or an earlier one; the main
 * frames follow the timing plan; every frame has speaker notes.
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
const VOCABULARY = ['analytical', 'computer-assisted', 'numerical diagnostic', 'open', 'input'];

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
const REG = Object.fromEntries(parseCsv(fs.readFileSync(path.join(ROOT, 'numerics/quantity_registry.csv'), 'utf8')).map((r) => [r.name, r]));

function norm(s) {
  return String(s).replace(/\\,/g, '').replace(/−/g, '-').replace(/(\d+(?:\.\d+)?)\\times10\^\{(-?\d+)\}/g, '$1e$2').replace(/\s+/g, '');
}
function parseShown(s) {
  const t = norm(s), m = /^(-?\d+(?:\.\d+)?)(?:e(-?\d+))?$/.exec(t);
  if (!m) return null;
  const dec = (m[1].split('.')[1] || '').length, exp = m[2] ? Number(m[2]) : 0;
  // An integer token (0, 2, 7) is a declaration or a label: it must match exactly.
  return { value: Number(m[1]) * Math.pow(10, exp), half: dec === 0 && !m[2] ? 0 : 0.5 * Math.pow(10, exp - dec) };
}
/* Does the shown string round from the registry quantity named by key? */
function matches(key, shown) {
  const neg = key.startsWith('-'), parts = (neg ? key.slice(1) : key).split('+'), rows = parts.map((k) => REG[k]);
  if (rows.some((r) => !r)) return false;
  const iv = /^\[(-?[\d.]+),(-?[\d.]+)\]$/.exec(norm(shown));
  if (iv) {
    const d = /^\[(-?[\d.]+),\\,(-?[\d.]+)\]$/.exec(rows[0].display);
    return !!d && (neg ? iv[1] === '-' + d[2] && iv[2] === '-' + d[1] : iv[1] === d[1] && iv[2] === d[2]);
  }
  if (!neg && parts.length === 1 && norm(shown) === norm(rows[0].display)) return true;
  const p = parseShown(shown);
  if (!p) return false;
  let v = rows.reduce((a, r) => a + Number(r.value), 0);
  if (neg) v = -v;
  return Math.abs(v - p.value) <= p.half * (1 + 1e-9) + 1e-15;
}

/* ---------------------------------------------------------------- talk.tex */
const TEX = fs.readFileSync(path.join(ROOT, 'talk/talk.tex'), 'utf8');
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

/* Numbers that talk.tex tags with "% source:", line by line. */
function sourced(f) {
  const out = [];
  for (const line of f.body.split('\n')) {
    const at = line.search(/(^|[^\\])%/);
    if (at < 0) continue;
    const cut = line[at] === '%' ? at : at + 1;
    const code = line.slice(0, cut), comment = line.slice(cut + 1);
    if (!/^\s*source\s*:/.test(comment)) continue;
    let c = code.replace(/\\[vh]space\*?\{[^}]*\}/g, '').replace(/p\{[\d.]+cm\}/g, '').replace(/\\addlinespace\[[^\]]*\]/g, '')
      .replace(/(\d+(?:\.\d+)?)\\times10\^\{(-?\d+)\}/g, ' $1e$2 ')
      .replace(/\[(-?[\d.]+),\\,(-?[\d.]+)\]/g, ' [$1,$2] ')
      .replace(/\\,/g, ' ').replace(/_\{[^}]*\}|_\\?[A-Za-z0-9]/g, '').replace(/\^\{[^}]*\}|\^\*|\^\d/g, '')
      .replace(/A\.\d+|Prop\.[^&]*?(?=[);]|$)/g, '');
    const nums = (c.match(/\[-?[\d.]+,-?[\d.]+\]|-?\d+(?:\.\d+)?(?:e-?\d+)?/g) || []);
    if (!nums.length) continue;
    const text = comment.replace(/^\s*source\s*:/, '');
    const keys = [];
    const kre = /\b([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\b(\s*\(negated\))?|\+|(tables\/[a-z0-9_]+\.tex)/g;
    let k, plus = false;
    while ((k = kre.exec(text))) {
      if (k[0] === '+') { plus = true; continue; }
      if (k[3]) { keys.push({ table: k[3] }); continue; }
      if (!REG[k[1]]) continue;
      const name = (k[2] ? '-' : '') + k[1];
      if (plus && keys.length && !keys[keys.length - 1].table) keys[keys.length - 1].key += '+' + name;
      else keys.push({ key: name });
      plus = false;
    }
    out.push({ line: code.trim(), nums, keys });
  }
  return out;
}

/* ---------------------------------------------------------------- content.js through stub helpers */
global.window = {};
require('./content.js');
const enc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const statuses = [];
const normText = (s) => String(s).replace(/\\,/g, ' ').replace(/\u2212/g, '-').replace(/(\d+(?:\.\d+)?)\\times10\^\{(-?\d+)\}/g, '$1e$2').replace(/\s+/g, ' ');
let LATEX = [];
const mathSpan = (l) => { LATEX.push(l); return `<span class="m" data-latex="${enc(l)}">$${enc(l)}$</span>`; };
const H = {
  m: mathSpan,
  d: mathSpan,
  q: (key, shown) => `<span class="q" data-q="${enc(key)}" data-shown="${enc(shown)}">${enc(shown)}</span>`,
  qm: (latex, key, shown) => {
    const pairs = Array.isArray(key) ? key : [[key, shown]];
    LATEX.push(latex);
    return `<span class="q" data-q="${enc(pairs.map((p) => p[0]).join(' '))}" data-shown="${enc(pairs.map((p) => p[1]).join('|'))}">$${enc(latex)}$</span>`;
  },
  qk: (html, keys) => `<span class="qk" data-q="${enc(keys)}">${html}</span>`,
  tx: (file, row, col, value, text, latex) => {
    if (latex) LATEX.push(latex);
    return `<span class="q" data-q="tables/${enc(file)}" data-shown="${enc(text || value)}">${latex ? '$' + enc(latex) + '$' : enc(text || value)}</span>`;
  },
  go: (target, text) => `<button data-target="${enc(target)}">${text}</button>`,
  back: (target) => `<button data-back="${enc(target)}">Back</button>`,
  status: (text) => { statuses.push(text); return `<span class="status">${text}</span>`; }
};
const latexOf = {};
H.endFrame = (label) => { latexOf[label] = LATEX; LATEX = []; };
const deck = window.createDeck(H);
const frames = deck.frames;
const plain = (html) => html.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/\s+/g, ' ').trim();
const spans = (html) => [...html.matchAll(/<span class="q[^"]*" data-q="([^"]*)" data-shown="([^"]*)"/g)].map((m) => ({ q: m[1].replace(/&amp;/g, '&'), shown: m[2] }));
const qkeys = (html) => [...html.matchAll(/data-q="([^"]*)"/g)].flatMap((m) => m[1].split(' '));

/* ---------------------------------------------------------------- drift */
if (frames.length !== 47) fail(`content.js has ${frames.length} frames; talk.tex has 47`);
if (talk.length !== 47) fail(`talk.tex parsed into ${talk.length} frames, not 47`);
const asPrinted = [];
let numberPairs = 0;
talk.forEach((t, i) => {
  const f = frames[i];
  if (!f) return;
  const where = `${t.label}`;
  if (f.label !== t.label) fail(`frame ${i + 1}: content.js has ${f.label}, talk.tex has ${t.label}`);
  if ((f.title || '').trim() !== (t.title || '').trim()) fail(`${where}: title "${f.title}" differs from talk.tex "${t.title}"`);
  const sub = plain(f.subtitle || '');
  if (sub !== t.subtitle) fail(`${where}: subtitle differs\n   web:  ${sub}\n   tex:  ${t.subtitle}`);
  if (JSON.stringify(f.targets || []) !== JSON.stringify(t.targets)) fail(`${where}: hypertargets ${JSON.stringify(f.targets)} differ from ${JSON.stringify(t.targets)}`);
  const links = [...(f.body || '').matchAll(/<button data-(target|back)="([^"]*)">([^<]*)<\/button>/g)].map((m) => (m[1] === 'back' ? ['back', m[2]] : ['go', m[2], m[3]]));
  if (JSON.stringify(links) !== JSON.stringify(t.links)) fail(`${where}: links ${JSON.stringify(links)} differ from talk.tex ${JSON.stringify(t.links)}`);
  // numbers
  const html = (f.subtitle || '') + (f.body || '');
  const sp = spans(html), all = qkeys(html), text = normText(plain(html.replace(/<[^>]+>/g, ' ')).replace(/\$/g, ' '));
  for (const s of sourced(t)) {
    const used = new Set();
    for (const k of s.keys) {
      if (k.table) {
        if (!sp.some((x) => x.q === k.table)) fail(`${where}: no number on the slide carries ${k.table} (${s.line})`);
        continue;
      }
      // Of the numbers on the line that round from the key, take the most precise one.
      let j = -1;
      const disp = REG[k.key.replace(/^-/, '').split('+')[0]].display;
      s.nums.forEach((n, idx) => {
        if (used.has(idx) || !matches(k.key, n)) return;
        if (j >= 0 && norm(s.nums[j]) === norm(disp)) return;
        if (j < 0 || norm(n) === norm(disp) || parseShown(n) && parseShown(s.nums[j]) && parseShown(n).half < parseShown(s.nums[j]).half) j = idx;
      });
      if (j < 0) {
        if (!all.includes(k.key)) fail(`${where}: the slide does not carry ${k.key} (${s.line})`);
        continue;
      }
      used.add(j);
      numberPairs++;
      const n = s.nums[j];
      if (!sp.some((x) => x.q.split(' ').includes(k.key) && x.shown.split('|').some((v) => norm(v) === norm(n)))) fail(`${where}: talk.tex prints ${n} with ${k.key}; no slide span shows it with that key`);
    }
    for (const n of s.nums) {
      const pat = (x) => new RegExp('(^|[^0-9.])' + x.replace(/[.[\]]/g, (c) => '\\' + c).replace(/,/g, ', ?') + '(?![0-9])');
      const hit = pat(norm(n)).test(text) || (n.startsWith('-') && pat(norm(n).slice(1)).test(text));
      if (!hit) fail(`${where}: talk.tex prints ${n} on a sourced line; the slide does not (${s.line})`);
    }
  }
  // the title numbers of F10a and F10b
  const tm = /%\s*source \(title\):([^\n]*)/.exec(t.body);
  if (tm) {
    for (const pair of tm[1].matchAll(/([a-z][a-z0-9_]+) \(([\d.]+)\)/g)) {
      if (!f.titleQ || f.titleQ[pair[2]] !== pair[1]) fail(`${where}: the title number ${pair[2]} must carry ${pair[1]}`);
      else if (!matches(pair[1], pair[2])) fail(`${where}: the title number ${pair[2]} does not round from ${pair[1]}`);
    }
  }
  for (const x of sp) if (x.q.startsWith('tables/') && /#count/.test(html)) asPrinted.push(x);
});

/* ---------------------------------------------------------------- contract */
const ids = new Set();
let mainMinutes = 0;
for (const f of frames) {
  if (ids.has(f.id)) fail(`duplicate id ${f.id}`);
  ids.add(f.id);
  const html = (f.subtitle || '') + (f.body || '');
  for (const x of spans(html)) {
    for (const k of x.q.split(' ')) {
      const base = k.replace(/^-/, '').split('+');
      if (k.startsWith('tables/')) { if (!fs.existsSync(path.join(ROOT, k))) fail(`${f.label}: unknown table ${k}`); }
      else if (base.some((b) => !REG[b])) fail(`${f.label}: unknown registry key ${k}`);
      else if (base.some((b) => !VOCABULARY.includes(REG[b].status))) fail(`${f.label}: ${k} has a status outside the vocabulary`);
    }
  }
  // no registry number in a headline, unless talk.tex prints it there
  const bare = (f.title || '').replace(/\$[^$]*\$/g, '');
  for (const n of bare.match(/\d+\.\d+/g) || []) if (!f.titleQ || !f.titleQ[n]) fail(`${f.label}: number ${n} in the headline without a registry key`);
  if (!f.backup) mainMinutes += f.minutes;
  if (f.backup) {
    if (!f.origin || !ids.has(f.origin) && !frames.some((g) => g.id === f.origin)) fail(`${f.label}: backup without a valid origin`);
    if (!/data-back=/.test(f.body)) fail(`${f.label}: backup without a Back button`);
  }
}
for (const s of statuses) if (!VOCABULARY.some((w) => s.toLowerCase().includes(w))) fail(`status "${s}" names no word of the paper's vocabulary`);
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

/* speaker notes: every frame has a block; the four without a script block are the documented ones */
const dist = path.join(HERE, 'dist');
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const page = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
  const nm = /window\.CCC_NOTES = (\{[\s\S]*?\});\s*<\/script>/.exec(page);
  const notes = nm ? JSON.parse(nm[1]) : {};
  for (const f of frames) if (!notes[f.label] || !notes[f.label].html) fail(`${f.label}: no speaker notes`);
  const prov = JSON.parse(fs.readFileSync(path.join(dist, 'provenance.json'), 'utf8'));
  const fb = (prov.notes_from_structure_plan || []).join(',');
  if (fb !== 'A9,A12,A25,A29') fail(`notes fall back to the structure plan for ${fb}, expected A9,A12,A25,A29`);
  const sections = (page.match(/<section class="slide/g) || []).length;
  if (sections !== 47) fail(`dist/index.html has ${sections} slides, not 47`);
} else fail('dist/index.html is missing; run python3 presentation/build.py');

const mains = frames.filter((f) => !f.backup).length;
console.log(`Compared ${frames.length} frames (${mains} main, ${frames.length - mains} backup) with talk.tex: order, titles, subtitles, targets and links; ` +
  `${numberPairs} sourced numbers paired with registry keys; ${keys.size} notation symbols; ${mainMinutes} planned minutes before questions.`);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
console.log('Deck matches talk.tex and the deck contract.');
