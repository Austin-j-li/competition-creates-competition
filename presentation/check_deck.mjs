/* Offline check of the slides against slot/manuscript/slides.tex, its speaker script and the deck
 * contract. Node standard library.
 *
 * Drift against slides.tex (the Beamer master): the same frames in the same order and labels; the
 * same frame numbers (n of the main frames, the \BackupId of a backup page); the same titles and
 * subtitles; the same \hypertarget names; the same link graph in source order (\hyperlink buttons,
 * inline \hyperlink text links, return buttons and Back buttons, with their texts); the same registry
 * keys, each as often as slides.tex prints it with \reg{key}; the same rounded numbers, which TeX and
 * the web must print alike; and the same words in the same order outside mathematics and diagrams.
 * Words, titles and subtitles are compared after NFKC normalisation, so a unicode maths glyph and its
 * plain form agree.
 * Against slides_script.md: the timing line of every main frame, the planned total, and the frame
 * titles of the script headings.
 * Contract: every number span names a key of the slot registry; no number sits in a slide headline;
 * no example number before the first example frame that the slides.tex header names; every backup
 * page carries a Back or return button to a main frame; every link names a hypertarget; every main
 * frame has speaker notes; the journal palette only.
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
const nfkc = (s) => String(s).normalize('NFKC');

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
const RAW = fs.readFileSync(path.join(ROOT, 'slot/manuscript/slides.tex'), 'utf8');
const stripComments = (s) => s.split('\n').map((l) => l.replace(/(^|[^\\])%.*$/, '$1')).join('\n');
const TEX = stripComments(RAW);
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
const flat = (s) => s.replace(/\\ /g, ' ').replace(/~/g, ' ').replace(/---/g, '—').replace(/--/g, '–').replace(/\s+/g, ' ').trim();

/* Remove \name with its optional argument and n brace groups; keep the last group when keepLast. */
function dropMacro(s, name, nargs, keepLast) {
  const re = new RegExp('\\\\' + name + '(?![A-Za-z@])', 'g');
  let out = '', last = 0, m;
  while ((m = re.exec(s))) {
    let i = m.index + m[0].length;
    while (/\s/.test(s[i] || '')) i++;
    if (s[i] === '[') i = s.indexOf(']', i) + 1;
    let kept = '';
    for (let a = 0; a < nargs; a++) {
      while (/\s/.test(s[i] || '')) i++;
      if (s[i] !== '{') break;
      const [g, j] = group(s, i);
      if (keepLast && a === nargs - 1) kept = g;
      i = j;
    }
    out += s.slice(last, m.index) + ' ' + kept + ' ';
    last = i; re.lastIndex = i;
  }
  return out + s.slice(last);
}

/* The words a reader sees on a Beamer frame outside mathematics, figures and diagrams. */
function texWords(body) {
  let s = body.replace(/\\\\(\[[^\]]*\])?/g, ' ');
  s = dropMacro(s, 'framesubtitle', 1);
  s = s.replace(/\\ModelStrip\{[^}]*\}/g, ' Players Timing Information Actions Payoffs Equilibrium ');
  s = s.replace(/\\begin\{tikzpicture\}[\s\S]*?\\end\{tikzpicture\}/g, ' ');
  for (const [name, n] of [['SplitLine', 2], ['GapLine', 2], ['BeliefsFigB', 1], ['ResearchFig', 1], ['CoexRegion', 1], ['CoexPanelA', 1], ['CoexPanelC', 1]]) s = dropMacro(s, name, n);
  s = s.replace(/\\hyperlink\{[^}]*\}\{\\beamer(?:goto|return)button\{[^}]*\}\}/g, ' ');
  for (const [name, n] of [['BackButton', 1], ['hypertarget', 2], ['BackupId', 1]]) s = dropMacro(s, name, n);
  s = dropMacro(s, 'hyperlink', 2, true);
  s = s.replace(/\\\[[\s\S]*?\\\]/g, ' ').replace(/\$[^$]*\$/g, ' ');
  s = s.replace(/\\regr?\{[^}]*\}(\{\d\})?/g, ' ');
  s = s.replace(/\\'\{?e\}?/g, 'é');
  for (const [name, n, keep] of [['vspace\\*?', 1], ['hspace\\*?', 1], ['setlength', 2], ['renewcommand', 2], ['setbeamerfont', 2], ['column', 1],
    ['scalebox', 2, true], ['multicolumn', 3, true], ['textcolor', 2, true], ['color', 1], ['rule', 2], ['includegraphics', 1]]) s = dropMacro(s, name, n, keep);
  s = s.replace(/\\begin\{tabular\}/g, '\\tabularstart');
  s = dropMacro(s, 'tabularstart', 1);
  s = s.replace(/\\begin\{minipage\}(\[[^\]]*\])?\{[^}]*\}/g, ' ').replace(/\\begin\{(columns|DefList)\}(\[[^\]]*\])?/g, ' ');
  s = s.replace(/\\(begin|end)\{[A-Za-z*]+\}/g, ' ');
  s = s.replace(/\\[A-Za-z@]+\*?/g, ' ').replace(/\\./g, ' ');
  s = s.replace(/[{}&~]/g, ' ');
  return words(s);
}
const words = (s) => (nfkc(s).toLowerCase().match(/[\p{L}\p{N}]+/gu) || []);

const talk = [];
{
  const re = /\\begin\{frame\}(\[[^\]]*\])?/g;
  let m;
  while ((m = re.exec(TEX))) {
    const opts = m[1] || '';
    const lm = /label=([A-Za-z0-9]+)/.exec(opts);
    if (!lm) { fail(`slides.tex: a frame at offset ${m.index} has no label`); continue; }
    const label = lm[1];
    let i = m.index + m[0].length, title = null;
    if (TEX[i] === '{') { const [t, j] = group(TEX, i); title = t; i = j; }
    const end = TEX.indexOf('\\end{frame}', i);
    const body = TEX.slice(i, end);
    let subtitle = '';
    const sm = /\\framesubtitle\{/.exec(body);
    if (sm) subtitle = flat(group(body, sm.index + sm[0].length - 1)[0]);
    const targets = [...body.matchAll(/\\hypertarget\{([^}]+)\}/g)].map((x) => x[1]);
    const links = [];
    const lre = /\\hyperlink\{([^}]+)\}\{\\beamer(goto|return)button\{([^}]*)\}\}|\\BackButton\{([^}]+)\}|\\hyperlink\{([^}]+)\}\{([^\\}][^}]*)\}/g;
    let l;
    while ((l = lre.exec(body))) {
      if (l[4]) links.push(['back', l[4], 'Back']);
      else if (l[5]) links.push(['link', l[5], l[6]]);
      else links.push([l[2] === 'return' ? 'back' : 'go', l[1], l[3]]);
    }
    const bid = /\\BackupId\{([^}]+)\}/.exec(body);
    talk.push({ label, title, subtitle, targets, links, body, backupId: bid ? bid[1] : null });
  }
  const t = /\\title\[[^\]]*\]\{/.exec(TEX);
  const title = group(TEX, t.index + t[0].length - 1)[0].replace(/\\texorpdfstring\{[^}]*\}\{([^}]*)\}/, '$1');
  talk[0].title = title.replace(/\s+/g, ' ').trim();
}
const backupStart = talk.findIndex((t) => t.backupId);

/* The first frame that may print an example number, as the slides.tex header states it. */
const firstExample = /No registry number[\s%]*appears[\s%]*before[\s%]*frame[\s%]*(\d+)/.exec(RAW);
if (!firstExample) fail('slides.tex: the header no longer names the first frame with a registry number ("No registry number appears before frame N")');
const FIRST_EXAMPLE = firstExample ? Number(firstExample[1]) : 0;

/* The registry keys that slides.tex prints on a frame with \reg{key} or \regr{key}{digits}. */
const regKeys = (f) => [...f.body.matchAll(/\\regr?\{([A-Za-z0-9_]+)\}/g)].map((x) => x[1]);
const regRounds = (f) => [...f.body.matchAll(/\\regr\{([A-Za-z0-9_]+)\}\{(\d)\}/g)].map((x) => `${x[1]}:${x[2]}`);
/* \regr rounds the registry display in TeX; the web rounds the registry value. Both must print the same. */
const roundDisplay = (key, d) => Number(REG[key].display).toFixed(d);
const roundValue = (key, d) => { const [a, b] = String(REG[key].value).split('/'); return (b === undefined ? Number(a) : Number(a) / Number(b)).toFixed(d); };
const counts = (xs) => xs.reduce((o, x) => { o[x] = (o[x] || 0) + 1; return o; }, {});
const sameCounts = (a, b) => { const ca = counts(a), cb = counts(b); return Object.keys({ ...ca, ...cb }).every((k) => ca[k] === cb[k]); };

/* ---------------------------------------------------------------- the speaker script */
const SCRIPT = fs.readFileSync(path.join(ROOT, 'slot/manuscript/slides_script.md'), 'utf8');
const scriptTiming = {};
for (const m of SCRIPT.matchAll(/^## (Title|Frame (\d+)) — (.+)\n+\*([\d.]+) minutes? · ends at [\d:]+\*/gm)) {
  scriptTiming[m[2] ? 'S' + m[2] : 'S0'] = { minutes: Number(m[4]), title: m[3].trim() };
}
const planned = /Prepared speech: ([\d.]+) minutes/.exec(SCRIPT);

/* ---------------------------------------------------------------- content.js through stub helpers */
global.window = {};
require('./content.js');
const enc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
let VALUES = [];
const withKeys = (l) => {
  const found = [...l.matchAll(/\{\{([A-Za-z0-9_]+)(?:\|(\d))?\}\}|\\reg\{([A-Za-z0-9_]+)\}/g)];
  const keys = found.map((x) => x[1] || x[3]);
  const rounds = found.filter((x) => x[2] !== undefined).map((x) => `${x[1]}:${x[2]}`);
  return keys.length ? `<span class="q q-tex" data-q="${enc(keys.join(' '))}" data-round="${enc(rounds.join(' '))}">$${enc(l)}$</span>` : `<span class="m">$${enc(l)}$</span>`;
};
const H = {
  m: withKeys,
  d: withKeys,
  q: (key, digits) => `<span class="q" data-q="${enc(key)}" data-round="${digits === undefined ? '' : enc(key + ':' + digits)}">${enc(REG[key] ? REG[key].display : '?')}</span>`,
  v: (key) => { VALUES.push(key); const [a, b] = String(REG[key] ? REG[key].value : 'NaN').split('/'); return b === undefined ? Number(a) : Number(a) / Number(b); },
  go: (target, text) => `<button data-target="${enc(target)}">${text}</button>`,
  back: (target, text) => `<button data-back="${enc(target)}">${text === undefined ? 'Back' : text}</button>`,
  link: (target, text) => `<a data-link="${enc(target)}">${text}</a>`
};
const valuesOf = {};
H.endFrame = (label) => { valuesOf[label] = VALUES; VALUES = []; };
const deck = window.createDeck(H);
const frames = deck.frames;
const decode = (s) => s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');
const plain = (html) => decode(html.replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
const qkeys = (html) => [...html.matchAll(/data-q="([^"]*)"/g)].flatMap((m) => m[1].split(' '));
const qrounds = (html) => [...html.matchAll(/data-round="([^"]*)"/g)].flatMap((m) => m[1].split(' ')).filter(Boolean);
function webWords(html) {
  const s = html.replace(/<!--dg-->[\s\S]*?<!--\/dg-->/g, ' ')
    .replace(/<span class="(?:m|q[^"]*)"[^>]*>[^<]*<\/span>/g, ' ')
    .replace(/<button[^>]*>[^<]*<\/button>/g, ' ');
  return words(plain(s.replace(/<[^>]+>/g, ' ')));
}
function firstDiff(a, b) {
  let i = 0;
  while (i < a.length && i < b.length && a[i] === b[i]) i++;
  return i;
}

/* ---------------------------------------------------------------- drift */
if (frames.length !== talk.length) fail(`content.js has ${frames.length} frames; slides.tex has ${talk.length}`);
let numberPairs = 0, wordCount = 0, linkCount = 0;
talk.forEach((t, i) => {
  const f = frames[i];
  if (!f) return;
  const where = `${t.label}`;
  if (f.label !== t.label) fail(`frame ${i + 1}: content.js has ${f.label}, slides.tex has ${t.label}`);
  const isBackup = i >= backupStart && backupStart > 0;
  if (!!f.backup !== isBackup) fail(`${where}: backup flag ${!!f.backup} differs from slides.tex`);
  const num = isBackup ? t.backupId : String(i);
  if (String(f.num) !== num) fail(`${where}: frame number ${f.num} differs from slides.tex ${num}`);
  if (nfkc(f.title || '').trim() !== nfkc(t.title || '').trim()) fail(`${where}: title "${f.title}" differs from slides.tex "${t.title}"`);
  const sub = plain(f.subtitle || '');
  if (nfkc(sub) !== nfkc(t.subtitle)) fail(`${where}: subtitle differs\n   web:  ${sub}\n   tex:  ${t.subtitle}`);
  if (JSON.stringify(f.targets || []) !== JSON.stringify(t.targets)) fail(`${where}: hypertargets ${JSON.stringify(f.targets)} differ from ${JSON.stringify(t.targets)}`);
  const links = [...(f.body || '').matchAll(/<button data-(target|back)="([^"]*)">([^<]*)<\/button>|<a data-link="([^"]*)">([^<]*)<\/a>/g)]
    .map((m) => (m[4] !== undefined ? ['link', m[4], m[5]] : [m[1] === 'back' ? 'back' : 'go', m[2], m[3]]));
  linkCount += links.length;
  if (JSON.stringify(links) !== JSON.stringify(t.links)) fail(`${where}: links ${JSON.stringify(links)} differ from slides.tex ${JSON.stringify(t.links)}`);
  // numbers: the same registry keys, each as often as slides.tex prints it
  const html = (f.subtitle || '') + (f.body || '');
  const texKeys = regKeys(t);
  for (const k of texKeys) if (!REG[k]) fail(`${where}: slides.tex prints \\reg{${k}}, which the registry does not hold`);
  numberPairs += texKeys.length;
  if (!sameCounts(qkeys(html), texKeys)) {
    const cw = counts(qkeys(html)), ct = counts(texKeys);
    const diff = Object.keys({ ...cw, ...ct }).filter((k) => cw[k] !== ct[k]).map((k) => `${k} web ${cw[k] || 0} tex ${ct[k] || 0}`);
    fail(`${where}: registry keys differ from slides.tex (${diff.join('; ')})`);
  }
  // rounded numbers: the same keys at the same digits, and TeX and the web print the same string
  const webRounds = qrounds(html).sort(), texRounds = regRounds(t).sort();
  if (JSON.stringify(webRounds) !== JSON.stringify(texRounds)) fail(`${where}: rounded numbers ${JSON.stringify(webRounds)} differ from slides.tex ${JSON.stringify(texRounds)}`);
  for (const r of texRounds) {
    const [k, d] = r.split(':');
    if (REG[k] && roundDisplay(k, Number(d)) !== roundValue(k, Number(d))) fail(`${where}: ${k} rounds to ${roundDisplay(k, Number(d))} from its display and ${roundValue(k, Number(d))} from its value`);
  }
  // words outside mathematics and diagrams, in order (the title frame prints \titlepage)
  if (i === 0) return;
  const tw = texWords(t.body), ww = webWords(f.body || '');
  wordCount += tw.length;
  if (JSON.stringify(tw) !== JSON.stringify(ww)) {
    const k = firstDiff(tw, ww);
    fail(`${where}: words differ from slides.tex at word ${k + 1}\n   web:  …${ww.slice(Math.max(0, k - 6), k + 8).join(' ')}…\n   tex:  …${tw.slice(Math.max(0, k - 6), k + 8).join(' ')}…`);
  }
});

/* Script: the timing of each main frame, the planned total and the headings. */
let mainMinutes = 0;
for (const f of frames.filter((x) => !x.backup)) {
  const s = scriptTiming[f.label];
  if (!s) { fail(`${f.label}: slides_script.md has no timing line for this frame`); continue; }
  if (f.minutes !== s.minutes) fail(`${f.label}: ${f.minutes} minutes in content.js, ${s.minutes} in slides_script.md`);
  if (f.label !== 'S0' && nfkc(s.title) !== nfkc(f.title)) fail(`${f.label}: script heading "${s.title}" differs from the title "${f.title}"`);
  mainMinutes += f.minutes;
}
if (!planned) fail('slides_script.md: no "Prepared speech: N minutes" line');
else if (Math.abs(mainMinutes - Number(planned[1])) > 1e-9) fail(`main frames sum to ${mainMinutes} minutes; slides_script.md plans ${planned[1]}`);

/* No example number before the first example frame: no registry number on the slide face or in a
   subtitle, no decimal in the text, no registry value used for layout, and no \reg in the Beamer frame. */
let earlyFrames = 0;
talk.forEach((t, i) => {
  const f = frames[i];
  if (!f || f.backup || !(Number(f.num) < FIRST_EXAMPLE)) return;
  earlyFrames++;
  const html = (f.subtitle || '') + ' ' + (f.body || '');
  if (qkeys(html).length) fail(`${f.label}: example number before frame ${FIRST_EXAMPLE} (${qkeys(html).join(', ')})`);
  const dec = plain(html.replace(/data-[a-z]+="[^"]*"/g, '')).replace(/§\s*\d+(\.\d+)*/g, ' ').match(/\d+\.\d+/g);
  if (dec) fail(`${f.label}: decimal ${dec.join(', ')} before frame ${FIRST_EXAMPLE}`);
  if ((valuesOf[f.label] || []).length) fail(`${f.label}: registry value used for layout before frame ${FIRST_EXAMPLE} (${valuesOf[f.label].join(', ')})`);
  if (regKeys(t).length) fail(`${t.label}: slides.tex prints a registry number before frame ${FIRST_EXAMPLE}`);
});

/* ---------------------------------------------------------------- contract */
const ids = new Set(), allTargets = new Set(frames.flatMap((f) => f.targets || []));
const mainTargets = new Set(frames.filter((f) => !f.backup).flatMap((f) => f.targets || []));
const idOfTarget = Object.fromEntries(frames.flatMap((f) => (f.targets || []).map((t) => [t, f.id])));
for (const f of frames) {
  if (ids.has(f.id)) fail(`duplicate id ${f.id}`);
  ids.add(f.id);
  const html = (f.subtitle || '') + (f.body || '');
  for (const k of qkeys(html)) if (!REG[k]) fail(`${f.label}: unknown registry key ${k}`);
  const bare = (f.title || '').replace(/\$[^$]*\$/g, '');
  for (const n of bare.match(/\d+\.\d+/g) || []) fail(`${f.label}: number ${n} in the headline`);
  for (const m of (f.body || '').matchAll(/data-(?:target|link)="([^"]*)"/g)) if (!allTargets.has(m[1])) fail(`${f.label}: link to ${m[1]}, which no frame carries`);
  if (f.backup) {
    const backs = [...(f.body || '').matchAll(/data-back="([^"]*)"/g)].map((m) => m[1]);
    if (!backs.length) fail(`${f.label}: backup page without a Back or return button`);
    for (const b of backs) if (!mainTargets.has(b)) fail(`${f.label}: Back button to ${b}, which is not a main frame`);
    if (backs.length && f.origin !== idOfTarget[backs[0]]) fail(`${f.label}: origin ${f.origin} is not the frame of its first Back button (${idOfTarget[backs[0]]})`);
  } else if (/data-back=/.test(f.body || '')) fail(`${f.label}: a main frame carries a Back button`);
}

/* speaker notes: every main frame has its block from the script */
const dist = path.join(HERE, 'dist');
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const page = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
  const nm = /window\.CCC_NOTES = (\{[\s\S]*?\});\s*<\/script>/.exec(page);
  const notes = nm ? JSON.parse(nm[1]) : {};
  for (const f of frames) if (!f.backup && (!notes[f.label] || !notes[f.label].html)) fail(`${f.label}: no speaker notes`);
  const sections = (page.match(/<section class="slide/g) || []).length;
  if (sections !== talk.length) fail(`dist/index.html has ${sections} slides, not ${talk.length}`);
} else fail('dist/index.html is missing; run python3 presentation/build.py');

/* ---------------------------------------------------------------- the design system */
/* The deck shares the journal look of DESIGN.md (repository root) with the research brief: white
 * paper, ink, greys and one oxblood accent, with a composed dark theme. Every hex colour in the deck
 * styles, the renderer, the engine and the built page's styles must be in that palette; the tokens
 * that both stylesheets declare must agree; and the rejected purple palette of the earlier "UCL
 * family" design must not come back through any deck source or the built page. */
const PURPLE = /#(?:361A54|993BFF|BA82FF)\b|--ucl-(?:dark|bright|mid)\b/gi;
const deckFiles = ['deck.css', 'charts.js', 'deck.js', 'template.html', 'content.js'].map((n) => path.join(HERE, n));
if (fs.existsSync(path.join(dist, 'index.html'))) deckFiles.push(path.join(dist, 'index.html'));
for (const file of deckFiles) {
  const text = fs.readFileSync(file, 'utf8');
  const found = text.match(PURPLE);
  if (found) fail(`${path.relative(ROOT, file)}: the rejected purple palette appears (${[...new Set(found)].join(', ')})`);
}
const JOURNAL = new Set([
  '#ffffff', '#f2f2f2', '#ebebeb', '#e9e9e9', '#1c1c1c', '#666666', '#c9c9c9', '#e6e6e6', '#7a1f1f',
  '#171717', '#0d0d0d', '#242424', '#2a2a2a', '#a3a3a3', '#474747', '#2e2e2e', '#d4908f',
  '#000000']);
const HEX = /#[0-9a-f]{6}\b/gi;
const styledFiles = ['deck.css', 'charts.js', 'deck.js', 'template.html', 'content.js'].map((n) => path.join(HERE, n));
const styledTexts = styledFiles.map((f) => [path.relative(ROOT, f), fs.readFileSync(f, 'utf8')]);
if (fs.existsSync(path.join(dist, 'index.html'))) {
  const page = fs.readFileSync(path.join(dist, 'index.html'), 'utf8');
  styledTexts.push(['presentation/dist/index.html (styles)', [...page.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/g)].map((m) => m[1]).join('\n')]);
}
for (const [name, text] of styledTexts) {
  const stray = [...new Set((text.match(HEX) || []).map((h) => h.toLowerCase()).filter((h) => !JOURNAL.has(h)))];
  if (stray.length) fail(`${name}: colour outside the journal palette (${stray.join(', ')})`);
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
const lightTokens = rootTokens(deckCss, 'light') || {};
if ((lightTokens['--accent'] || '').toLowerCase() !== '#7a1f1f') fail(`deck.css: --accent is ${lightTokens['--accent']}, not the oxblood #7a1f1f`);
if ((lightTokens['--bg'] || '').toLowerCase() !== '#ffffff') fail(`deck.css: --bg is ${lightTokens['--bg']}, not white paper`);

const mains = frames.filter((f) => !f.backup).length;
console.log(`Compared ${frames.length} frames (${mains} main with the title, ${frames.length - mains} backup pages) with slides.tex: order, labels, numbers, titles, subtitles, targets, ` +
  `${linkCount} links, ${numberPairs} printed registry keys and ${wordCount} words; ${mainMinutes} planned minutes as in slides_script.md; ` +
  `${sharedTokens} design tokens shared with handout/style.css agree; only the journal palette in ${styledTexts.length} styled files and no purple palette in ${deckFiles.length} deck files; ` +
  `no example number on the ${earlyFrames} frames before frame ${FIRST_EXAMPLE}.`);
if (problems.length) { console.error(problems.join('\n')); process.exit(1); }
console.log('Deck matches slides.tex, slides_script.md and the deck contract.');
