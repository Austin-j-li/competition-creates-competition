"""Build, check, and publish only the supervisor handout to Cloudflare.

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

    # Stage an explicit file list so drafts and stray files in docs/ stay private.
    fonts = json.loads((ROOT / "handout/fonts.lock.json").read_text())
    files = ["index.html", "main_filled.pdf", "online_appendix_filled.pdf"]
    files += [f"fonts/{name}" for name in fonts]
    with tempfile.TemporaryDirectory(prefix="ccc-publish-") as directory:
        stage = Path(directory)
        for name in files:
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "docs" / name, target)
        assert sorted(str(p.relative_to(stage)) for p in stage.rglob("*") if p.is_file()) == sorted(files)
        print(f"Publishing {len(files)} files to competition.dealextract.org", flush=True)
        command = ["npx", "--yes", "wrangler@4.130.0", "deploy", "--config",
                   "handout/wrangler.jsonc", "--assets", str(stage)]
        if args.dry_run:
            command.append("--dry-run")
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
