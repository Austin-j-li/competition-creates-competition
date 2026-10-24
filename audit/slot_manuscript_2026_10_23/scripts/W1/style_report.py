"""Print sentences over a word limit, paragraphs over 6 sentences, and -ing words in LaTeX prose.

Usage: python style_report.py FILE [FILE ...]
Math, comments and commands are removed first, so the counts are approximate.
"""
import re
import sys

LIMIT = 25
ING_OK = {"during", "nothing", "something", "thing", "things", "string", "king", "bring", "ring",
          "anything", "everything", "sing", "spring", "wing"}


def strip(text: str) -> str:
    text = re.sub(r"(?m)(?<!\\)%.*$", "", text)
    text = re.sub(r"\\\[.*?\\\]", " MATH. ", text, flags=re.S)
    text = re.sub(r"\\begin\{(equation|align|gather)\*?\}.*?\\end\{\1\*?\}", " MATH. ", text, flags=re.S)
    text = re.sub(r"\\\(.*?\\\)", " X ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " X ", text)
    text = re.sub(r"\\(cite[a-z]*|ref|eqref|label|reg|citetext)(\[[^\]]*\])*\{[^}]*\}", " X ", text)
    text = re.sub(r"\\(begin|end)\{[^}]*\}(\[[^\]]*\])?", "\n\n", text)
    text = re.sub(r"\\item(\[[^\]]*\])?", "\n\n", text)
    text = re.sub(r"\\(sub)*section\*?\{[^}]*\}", "\n\n", text)
    text = re.sub(r"\\paragraph\{([^}]*)\}", r"\n\n\1.", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = text.replace("~", " ").replace("{", "").replace("}", "")
    return text


def main() -> None:
    for path in sys.argv[1:]:
        raw = open(path, encoding="utf-8").read()
        prose = strip(raw)
        paras = [p for p in re.split(r"\n\s*\n", prose) if p.strip()]
        for para in paras:
            flat = " ".join(para.split())
            sents = [s for s in re.split(r"(?<=[.?!])\s+(?=[A-Z(])", flat) if s.strip()]
            if len(sents) > 6:
                print(f"{path}: PARAGRAPH {len(sents)} sentences: {flat[:90]}...")
            for s in sents:
                words = [w for w in s.split() if re.search(r"[A-Za-z]", w)]
                if len(words) > LIMIT:
                    print(f"{path}: SENTENCE {len(words)} words: {s}")
        ing = sorted({w.lower() for w in re.findall(r"\b[A-Za-z-]+ing\b", prose)} - ING_OK)
        print(f"{path}: -ing words: {', '.join(ing)}")


if __name__ == "__main__":
    main()
