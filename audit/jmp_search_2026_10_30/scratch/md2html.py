"""Convert the memo's Markdown subset (headings, paragraphs, lists, tables, bold, code) to one HTML page."""
import html, re, sys

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t

def convert(md):
    out, lines, i = [], md.split('\n'), 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1; continue
        m = re.match(r'(#{1,4}) (.*)', ln)
        if m:
            n = len(m.group(1)); out.append(f'<h{n}>{inline(m.group(2))}</h{n}>'); i += 1; continue
        if ln.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            head, body = rows[0], [r for r in rows[2:]]
            out.append('<table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in head) + '</tr></thead><tbody>')
            for r in body:
                out.append('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>')
            out.append('</tbody></table>'); continue
        if re.match(r'(\s*)(- |\d+\. )', ln):
            stack = []
            while i < len(lines) and re.match(r'(\s*)(- |\d+\. )', lines[i]):
                m = re.match(r'(\s*)(- |\d+\. )(.*)', lines[i]); depth = len(m.group(1)) // 2
                tag = 'ol' if m.group(2)[0].isdigit() else 'ul'
                while len(stack) > depth + 1:
                    out.append(f'</li></{stack.pop()}>')
                if len(stack) < depth + 1:
                    out.append(f'<{tag}>'); stack.append(tag)
                else:
                    out.append('</li>')
                out.append(f'<li>{inline(m.group(3))}'); i += 1
            while stack:
                out.append(f'</li></{stack.pop()}>')
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r'(#{1,4} |\||\s*- |\s*\d+\. )', lines[i]):
            para.append(lines[i].strip()); i += 1
        out.append(f'<p>{inline(" ".join(para))}</p>')
    return '\n'.join(out)

CSS = """
body{font-family:"STIX Two Text","Libertinus Serif",Georgia,serif;color:#1a1a1a;background:#fff;max-width:56rem;margin:3rem auto;padding:0 1.5rem;line-height:1.55;font-size:17px}
h1{font-size:1.9rem;font-weight:600;border-bottom:2px solid #1a1a1a;padding-bottom:.4rem;margin-bottom:1rem}
h2{font-size:1.35rem;font-weight:600;border-top:1px solid #1a1a1a;padding-top:.8rem;margin-top:2.4rem}
h3{font-size:1.12rem;font-weight:600;margin-top:2rem}
p,li{margin:.45rem 0}
ul,ol{padding-left:1.4rem}
table{border-collapse:collapse;width:100%;margin:1rem 0;font-size:.86rem;line-height:1.35}
th{text-align:left;border-top:1.5px solid #1a1a1a;border-bottom:1px solid #1a1a1a;padding:.35rem .4rem;font-weight:600}
td{border-bottom:1px solid #d6d6d6;padding:.32rem .4rem;vertical-align:top}
tbody tr:last-child td{border-bottom:1.5px solid #1a1a1a}
code{font-family:"JetBrains Mono",Menlo,monospace;font-size:.82em}
strong{font-weight:600}
"""

src, dst = sys.argv[1], sys.argv[2]
md = open(src, encoding='utf-8').read()
title = re.search(r'^# (.*)$', md, re.M).group(1)
page = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head><body>\n{convert(md)}\n</body></html>\n'
open(dst, 'w', encoding='utf-8').write(page)
print('wrote', dst, len(page), 'bytes')
