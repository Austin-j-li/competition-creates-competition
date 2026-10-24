/* Render the slide records of content.js to HTML at build time.
 *
 * Reads one JSON object on stdin: { data: CCC_DATA, tables: { "<file>.tex": text } }.
 * Writes { frames, notation, numbers } to stdout. Supplies the helpers of the content.js
 * contract: KaTeX renders the mathematics here, and every number passes a guard. A number
 * from the registry must round from the registry value at the precision it is shown; a number
 * from a paper table must round from the printed cell. Any failure stops the build.
 * Node standard library and the locked KaTeX copy only.
 */
import { createRequire } from 'node:module';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
const katex = require('../handout/vendor/katex.min.js');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const D = input.data;
const TABLES = input.tables;
global.window = {};
require('./content.js');

const VOCABULARY = ['analytical', 'computer-assisted', 'numerical diagnostic', 'open', 'input'];
const problems = [];
const numbers = [];
let current = '';
/* Helpers record here; endFrame (called by content.js after each frame) labels and moves it. */
let pending = { problems: [], numbers: [] };
const report = (msg) => pending.problems.push(msg);
const record = (n) => pending.numbers.push(n);
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

/* Number strings as talk.tex prints them: "0.250", "-0.460", "8.01\times10^{-4}". */
function parseShown(shown) {
  const s = String(shown).replace(/\\,/g, '').replace(/−/g, '-').trim();
  const sci = /^(-?\d+(?:\.\d+)?)\\times10\^\{(-?\d+)\}$/.exec(s);
  const mant = sci ? sci[1] : s;
  if (!/^-?\d+(\.\d+)?$/.test(mant)) return null;
  const decimals = (mant.split('.')[1] || '').length;
  const exp = sci ? Number(sci[2]) : 0;
  return { value: Number(mant) * Math.pow(10, exp), half: 0.5 * Math.pow(10, exp - decimals) };
}
const close = (target, shown) => {
  const p = parseShown(shown);
  return p !== null && Math.abs(target - p.value) <= p.half * (1 + 1e-9) + 1e-15;
};

/* One registry key, possibly negated or a sum. Returns { ok, status, title }. */
function guardKey(key, shown) {
  const negated = key.startsWith('-');
  const parts = (negated ? key.slice(1) : key).split('+');
  const rows = parts.map((k) => D.registry[k]);
  if (rows.some((r) => !r)) return { ok: false, why: `unknown registry key ${key}` };
  const status = [...new Set(rows.map((r) => r.status))].join('|');
  if (!rows.every((r) => VOCABULARY.includes(r.status))) return { ok: false, why: `status outside the vocabulary for ${key}` };
  const title = parts.map((k, i) => `${k} = ${rows[i].display.replace(/\\,/g, ' ')} · ${rows[i].status} · ${rows[i].source_file}`).join('; ');
  const interval = /^\[(-?[\d.]+),\\,(-?[\d.]+)\]$/.exec(String(shown));
  if (interval) {
    const disp = /^\[(-?[\d.]+),\\,(-?[\d.]+)\]$/.exec(rows[0].display);
    const ok = parts.length === 1 && disp && (negated
      ? interval[1] === '-' + disp[2] && interval[2] === '-' + disp[1]
      : interval[1] === disp[1] && interval[2] === disp[2]);
    return { ok: !!ok, status, title, why: `interval ${shown} differs from the registry display ${rows[0].display}` };
  }
  // talk.tex may print the registry display itself; that is exact by definition.
  if (parts.length === 1 && !negated && String(shown) === rows[0].display) return { ok: true, status, title };
  let value = rows.reduce((a, r) => a + Number(r.value), 0);
  if (negated) value = -value;
  if (!isFinite(value)) return { ok: false, why: `registry value of ${key} is not finite` };
  return { ok: close(value, shown), status, title, why: `${shown} does not round from the registry value ${value} of ${key}` };
}

function guard(keys, shown) {
  const out = keys.split(/\s+/).map((k) => [k, guardKey(k, shown)]);
  for (const [k, g] of out) if (!g.ok) report(`${g.why || 'guard failed for ' + k}`);
  record({ keys, shown });
  return { status: [...new Set(out.map(([, g]) => g.status))].join('|'), title: out.map(([, g]) => g.title).join('; ') };
}

const pretty = (s) => String(s).replace(/^-/, '−');

function q(keys, shown) {
  const g = guard(keys, shown);
  return `<span class="q" data-q="${esc(keys)}" data-shown="${esc(shown)}" data-status="${esc(g.status)}" title="${esc(g.title)}">${esc(pretty(shown))}</span>`;
}

function qm(latex, keys, shown) {
  const pairs = Array.isArray(keys) ? keys : [[keys, shown]];
  const gs = pairs.map(([k, s]) => {
    if (!latex.includes(s)) report(`the formula ${latex} does not print ${s}`);
    return guard(k, s);
  });
  return `<span class="q q-tex" data-q="${esc(pairs.map((p) => p[0]).join(' '))}" data-shown="${esc(pairs.map((p) => p[1]).join('|'))}" data-status="${esc(gs.map((g) => g.status).join('|'))}" title="${esc(gs.map((g) => g.title).join('; '))}">${tex(latex)}</span>`;
}

function qk(html, keys) {
  for (const k of keys.split(/\s+/)) if (!D.registry[k]) report(`unknown registry key ${k}`);
  return `<span class="qk" data-q="${esc(keys)}" title="${esc(keys.split(/\s+/).map((k) => `${k} = ${D.registry[k] ? D.registry[k].display : '?'}`).join('; '))}">${html}</span>`;
}

/* A number printed in a paper table file. */
function cellsOf(line) { return line.replace(/\\\\\s*$/, '').split('&').map((c) => c.trim()); }
function cellNumber(cell) {
  const s = cell.replace(/\$\^\{\*\}\$/g, '').replace(/[$]/g, '');
  const sci = /(-?\d+(?:\.\d+)?)\\times10\^\{(-?\d+)\}/.exec(s);
  if (sci) return Number(sci[1]) * Math.pow(10, Number(sci[2]));
  const m = /-?\d+(?:\.\d+)?/.exec(s);
  return m ? Number(m[0]) : NaN;
}
function tableRow(file, row) {
  const lines = (TABLES[file] || '').split('\n');
  if (!lines.length) return null;
  let start = 0, label = row;
  const panel = /^Panel ([AB]):(.*)$/.exec(row);
  if (panel) {
    start = lines.findIndex((l) => l.includes(`Panel ${panel[1]}.`));
    label = panel[2];
    if (start < 0) return null;
  }
  const hit = lines.slice(start).find((l) => l.trim().startsWith(label) && l.includes('&'));
  return hit || null;
}
function gridRows(file) {
  return (TABLES[file] || '').split('\n').filter((l) => /^0\.\d\d(\$\^\{\*\}\$)? & 0\.\d\d &/.test(l.trim())).map(cellsOf);
}
function tx(file, row, col, value, text, latex) {
  const where = `tables/${file}`;
  let target = NaN, status = 'analytical';
  const count = /^#count:(met|unchanged|falls)$/.exec(row);
  if (count) {
    const rows = gridRows(file);
    const pick = { met: (c) => c[9] === 'met', unchanged: (c) => c[9] !== 'met' && Number(c[1]) <= 0.75, falls: (c) => Number(c[1]) >= 0.76 }[count[1]];
    target = rows.filter(pick).length;
    status = count[1] === 'met' ? 'analytical' : 'numerical diagnostic';
    if (rows.length !== 25) report(`${where} has ${rows.length} grid rows, not 25`);
  } else {
    const line = tableRow(file, row);
    if (!line) { report(`no row "${row}" in ${where}`); }
    else {
      const cells = cellsOf(line);
      target = col === 0 ? (cells[0].includes(value) ? Number(value) : NaN) : cellNumber(cells[col] || '');
      if (line.includes('numerical diagnostic')) status = 'numerical diagnostic';
    }
  }
  if (!close(target, value)) report(`${value} does not round from ${where} "${row}" cell ${col} (${target})`);
  if (text !== undefined && text !== null && Math.abs(Number(text)) !== Math.abs(Number(value))) report(`${text} is not the magnitude of ${value}`);
  const shown = text !== undefined && text !== null ? text : value;
  record({ keys: where, shown, row, col });
  const inner = latex ? tex(latex) : esc(pretty(shown));
  return `<span class="q q-table" data-q="${esc(where)}" data-row="${esc(row)}" data-col="${col}" data-shown="${esc(shown)}" data-status="${status}" title="${esc(`${where} · ${row.replace(/^#count:/, 'count of rows: ')} · ${status}`)}">${inner}</span>`;
}

const H = {
  m: (l) => tex(l, false),
  d: (l) => `<div class="display-math">${tex(l, true)}</div>`,
  q, qm, qk, tx,
  go: (target, text) => `<button type="button" class="goto" data-target="${esc(target)}">${text}</button>`,
  back: (target) => `<button type="button" class="goto back" data-back="${esc(target)}">Back</button>`,
  status: (text) => {
    if (!VOCABULARY.some((w) => text.toLowerCase().includes(w))) report(`status "${text}" names no word of the paper's vocabulary`);
    return `<span class="status">${text}</span>`;
  }
};

/* Titles are talk.tex strings: $...$ is mathematics; titleQ marks registry numbers. */
function title(f) {
  let s = esc(f.title).replace(/\$([^$]+)\$/g, (_, l) => tex(l.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&')));
  for (const [num, key] of Object.entries(f.titleQ || {})) s = s.replace(num, q(key, num));
  return s;
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
const notation = deck ? deck.notation : [];
if (problems.length) {
  process.stderr.write(problems.join('\n') + '\n');
  process.exit(1);
}
process.stdout.write(JSON.stringify({ frames, notation, glossary: deck.glossary, numbers }));
