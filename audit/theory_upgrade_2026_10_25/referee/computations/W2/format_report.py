from pathlib import Path
p=Path('audit/theory_upgrade_2026_10_25/referee/W2.md')
s=p.read_bytes().decode()
for c,v in [(8,r'\b'),(9,r'\t'),(11,r'\v'),(12,r'\f'),(13,r'\r')]:
    s=s.replace(chr(c),v)
s=s.replace('(ge)',r'(\ge)').replace('(gamma>0)',r'(\gamma>0)').replace('(psi)',r'(\psi)')
spans=[]
pos=0
display=False
for lineno,line in enumerate(s.splitlines(True),1):
    if line.strip()==r'\[':
        display=True
    elif line.strip()==r'\]':
        display=False
    elif not display:
        i=0
        while i<len(line):
            if line[i]=='(':
                if i and line[i-1]==']':
                    e=line.find(')',i+1)
                    i=(len(line) if e<0 else e+1)
                    continue
                depth=1
                j=i+1
                while j<len(line) and depth:
                    depth+=(line[j]=='(')-(line[j]==')')
                    j+=1
                if depth==0:
                    spans.append((pos+i,pos+j,lineno,line[i+1:j-1]))
                    i=j
                    continue
            i+=1
    pos+=len(line)
for _,_,lineno,v in spans:
    print(lineno,repr(v))
Path('audit/theory_upgrade_2026_10_25/referee/computations/W2/inline_spans.txt').write_text('\n'.join(f'{ln}: {v}' for _,_,ln,v in spans))
# All remaining parentheses outside displays and links are inline mathematics,
# except these two English labels.
exceptions={'the referee','file, name'}
for a,b,ln,v in reversed(spans):
    if v not in exceptions:
        s=s[:a]+'$'+v+'$'+s[b:]
p.write_text(s)
print('Inline expressions converted:',sum(v not in exceptions for _,_,_,v in spans))
