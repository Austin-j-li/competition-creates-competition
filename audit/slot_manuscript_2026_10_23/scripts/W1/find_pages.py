"""Print the PDF page of each phrase. Usage: python find_pages.py PDF "phrase" ["phrase" ...]"""
import subprocess
import sys

pdf = sys.argv[1]
text = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
pages = [" ".join(p.split()) for p in text.split("\f")]
for phrase in sys.argv[2:]:
    hits = [i + 1 for i, p in enumerate(pages) if phrase in p]
    print(f"{hits}  {phrase}")
