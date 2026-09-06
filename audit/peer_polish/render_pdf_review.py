"""Render every PDF page and contact sheets; record text bounds for visual review."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw


def render(pdf: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "120", "-png", str(pdf), str(output / "page")], check=True)
    xml = subprocess.check_output(["pdftotext", "-bbox", str(pdf), "-"], text=True)
    document = ET.fromstring(xml)
    pages = [node for node in document.iter() if node.tag.endswith("}page")]
    info = subprocess.check_output(["pdfinfo", "-f", "1", "-l", str(len(pages)), str(pdf)], text=True)
    rotations = {int(page): int(angle) for page, angle in re.findall(r"Page\s+(\d+) rot:\s+(\d+)", info)}
    report = []
    for index, page in enumerate(pages, 1):
        width, height = float(page.attrib["width"]), float(page.attrib["height"])
        rotation = rotations.get(index, 0)
        if rotation % 180:
            width, height = height, width
        words = [node for node in page.iter() if node.tag.endswith("}word")]
        outside = [word.text for word in words if float(word.attrib["xMin"]) < 0 or float(word.attrib["yMin"]) < 0
                   or float(word.attrib["xMax"]) > width or float(word.attrib["yMax"]) > height]
        report.append({"page": index, "width": width, "height": height, "rotation": rotation, "word_count": len(words), "off_page_words": outside,
                       "opening": " ".join((w.text or "") for w in words[:18])})
    images = sorted(output.glob("page-*.png"))
    if len(images) != len(pages):
        raise ValueError("page render count mismatch")
    for start in range(0, len(images), 12):
        sheet = Image.new("RGB", (1440, 1590), "#cccccc")
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(images[start:start + 12]):
            with Image.open(path) as page:
                page.thumbnail((350, 495))
                x, y = (index % 4) * 360, (index // 4) * 530
                sheet.paste(page, (x + (350 - page.width) // 2, y + 25))
                draw.text((x + 10, y + 7), f"{pdf.stem}: page {start + index + 1}", fill="black")
        sheet.save(output / f"contact-{start + 1:03d}.png")
    (output / "page_bounds.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Rendered {len(images)} pages to {output}; {sum(bool(p['off_page_words']) for p in report)} pages have off-page text")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.pdf, args.output)
