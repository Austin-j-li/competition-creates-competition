"""Build, check, and publish the supervisor handout and the talk to Cloudflare.

The handout is served at the site root; the interactive talk is served under /talk/.

    python3 handout/publish.py --dry-run
    python3 handout/publish.py
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="check without uploading")
    args = parser.parse_args()
    subprocess.run([sys.executable, "handout/build.py", "--quiet"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "handout/check_display.py"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, "presentation/build.py"], cwd=ROOT, check=True)
    subprocess.run(["node", "presentation/check_deck.mjs"], cwd=ROOT, check=True)

    # Stage an explicit file list so drafts and stray files in docs/ stay private.
    fonts = json.loads((ROOT / "handout/fonts.lock.json").read_text())
    vendor = json.loads((ROOT / "handout/vendor.lock.json").read_text())["katex"]["files"]
    files = ["index.html", "main_filled.pdf", "online_appendix_filled.pdf"]
    files += [f"fonts/{name}" for name in fonts]
    files += [f"vendor/{name}" for name in vendor]
    # The talk: the built slides, the same locked fonts and KaTeX files as the handout, the two
    # PDFs it links, its provenance record, and the print export when it has been produced.
    # Speaker notes in Markdown and QA output stay private.
    dist = ROOT / "presentation/dist"
    talk = ["index.html", "main_filled.pdf", "online_appendix_filled.pdf", "provenance.json"]
    talk += [f"fonts/{name}" for name in fonts]
    talk += [f"vendor/{name}" for name in vendor]
    if (dist / "presentation.pdf").exists():
        talk.append("presentation.pdf")
    with tempfile.TemporaryDirectory(prefix="ccc-publish-") as directory:
        stage = Path(directory)
        for name in files:
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "docs" / name, target)
        for name in talk:
            target = stage / "talk" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(dist / name, target)
        expected = sorted(files + [f"talk/{name}" for name in talk])
        assert sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file()) == expected
        print(f"Publishing {len(expected)} files to competition.dealextract.org ({len(talk)} under /talk/)", flush=True)
        command = ["npx", "--yes", "wrangler@4.130.0", "deploy", "--config",
                   "handout/wrangler.jsonc", "--assets", str(stage)]
        if args.dry_run:
            command.append("--dry-run")
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
