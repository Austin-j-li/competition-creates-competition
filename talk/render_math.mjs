// Renders TeX to HTML with the repository's local KaTeX, for build.py.
// stdin:  {"katex": "<path to katex.min.js>", "items": [{"tex": "...", "display": false, "where": "..."}]}
// stdout: {"html": ["<span class=\"katex\">...", ...]}
// Any TeX error stops the build: the message names the file and the TeX.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';

const input = JSON.parse(readFileSync(0, 'utf8'));
const require = createRequire(import.meta.url);
const katex = require(input.katex);

const html = [];
for (const item of input.items) {
  try {
    html.push(katex.renderToString(item.tex, {
      displayMode: !!item.display,
      throwOnError: true,
      output: 'htmlAndMathml',
      strict: 'ignore',
      // \htmlClass lets a page tag a term of a formula; nothing else is trusted
      trust: (ctx) => ctx.command === '\\htmlClass',
    }));
  } catch (err) {
    process.stderr.write(`KaTeX error in ${item.where}: ${err.message}\n  TeX: ${item.tex}\n`);
    process.exit(1);
  }
}
process.stdout.write(JSON.stringify({ html, version: katex.version }));
