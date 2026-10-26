"""Build, check, and publish the website to Cloudflare.

The research brief of the order-slot version is served at the site root, its slides under /talk/,
and the earlier Laplace version under /laplace/ (front page and its two PDFs) and /laplace/talk/
(its slides).

    python3 handout/publish.py --stage-only DIR   # build, check and write the staged tree to DIR
    python3 handout/publish.py --dry-run          # the same, then a Wrangler dry run
    python3 handout/publish.py                    # the same, then deploy

The Laplace archive is built from a pinned commit, never from the working tree: the committed
handout build of that commit (docs/) and its slides, built by that commit's own
presentation/build.py in an extracted copy outside the repository. The extraction is cached by
commit in the system temporary directory.
"""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# The last commit of the Laplace website sources (handout/, presentation/, docs/ and the data they
# read); it is on the main and laplace branches.
LAPLACE_COMMIT = "312cf34091a75ed8c0f3dabe42bc0bad57d781f7"
LAPLACE_PATHS = ["handout", "presentation", "docs", "talk", "tables", "figures_data", "paper", "working_release"]
# The one line that names the archive as the earlier version, set in the site's ruled design: Archivo
# from the site root's locked fonts, ink on paper, a hairline below, in both themes. The archived page
# itself keeps its committed design.
ARCHIVE_NOTE = (
    '<style>'
    '@font-face { font-family: "Archivo"; font-style: normal; font-weight: 100 900; font-stretch: 62% 125%; '
    'font-display: swap; src: url("../fonts/archivo-latin-wdth-normal.woff2") format("woff2"); }'
    '.ccc-earlier { margin: 0; max-width: none; padding: 0.6rem 2rem; background: #fbfcfc; color: #1e2530; '
    'border-bottom: 1px solid #c7cdd5; font: 500 0.9rem/1.4 "Archivo", system-ui, Arial, sans-serif; text-align: left; }'
    '.ccc-earlier a { color: inherit; text-decoration: underline; text-decoration-thickness: 1px; '
    'text-underline-offset: 0.18em; text-decoration-color: #c7cdd5; }'
    '.ccc-earlier a:hover { text-decoration-color: currentColor; }'
    ':root[data-theme="dark"] .ccc-earlier { background: #1a1f26; color: #e8ecf1; border-bottom-color: #3d4652; }'
    ':root[data-theme="dark"] .ccc-earlier a { text-decoration-color: #3d4652; }'
    '</style>'
    '<p class="ccc-earlier">This is the earlier version of the paper, with Laplace order flow. '
    '<a href="../">The current version</a> uses one order slot.</p>')


def run(*cmd: str, cwd: Path = ROOT) -> None:
    subprocess.run(list(cmd), cwd=cwd, check=True)


# The ruled document (DESIGN.md) has no chrome colour; the purple palette of the earlier "UCL family"
# design must never be published again. Every staged HTML, CSS and JS file of the current site (the
# root and /talk/) is scanned. The archive under /laplace/ is the committed page of the pinned
# Laplace commit and keeps its own design, so it is outside the scan.
PURPLE = re.compile(r"#(?:361A54|993BFF|BA82FF)\b|--ucl-(?:dark|bright|mid)\b", re.I)


def check_palette(stage: Path) -> int:
    files = [p for p in stage.rglob("*") if p.is_file() and p.suffix in (".html", ".css", ".js", ".mjs")
             and not p.relative_to(stage).as_posix().startswith("laplace/")]
    hits = [f"{p.relative_to(stage)}: {m.group(0)}" for p in files for m in PURPLE.finditer(p.read_text(encoding="utf-8"))]
    if hits:
        raise SystemExit("The rejected purple palette appears in the staged site:\n  " + "\n  ".join(hits[:10]))
    return len(files)


def require_main_merged() -> None:
    """Publishing needs a checkout that contains origin/main: the author's local checkout can sit on an
    older branch whose committed site is the purple one."""
    fetched = subprocess.run(["git", "fetch", "--quiet", "origin", "main"], cwd=ROOT, capture_output=True, text=True)
    if fetched.returncode != 0:
        raise SystemExit("Could not fetch origin/main to confirm that this checkout is current:\n" + fetched.stderr.strip()
                         + "\nPublishing needs that confirmation; --stage-only and --dry-run do not.")
    merged = subprocess.run(["git", "merge-base", "--is-ancestor", "origin/main", "HEAD"], cwd=ROOT)
    if merged.returncode != 0:
        head = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        raise SystemExit(f"This checkout ({head}) does not contain origin/main, so its site may be out of date.\n"
                         "Update the checkout to main first (git checkout main && git pull, or merge main into this branch),\n"
                         "then publish again. --stage-only and --dry-run work from any branch.")


def laplace_archive() -> Path:
    """Extract the pinned commit once and build its slides there; return the extracted root."""
    root = Path(tempfile.gettempdir()) / f"ccc-laplace-archive-{LAPLACE_COMMIT[:12]}"
    if (root / "presentation/dist/index.html").is_file() and (root / ".complete").is_file():
        return root
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    listed = subprocess.run(["git", "ls-tree", "-r", "--name-only", LAPLACE_COMMIT, "numerics"], cwd=ROOT,
                            capture_output=True, text=True, check=True).stdout.split()
    numerics = [p for p in listed if p.startswith("numerics/manifests/") or (p.count("/") == 1 and p.endswith(".csv"))]
    archive = subprocess.run(["git", "archive", LAPLACE_COMMIT, *LAPLACE_PATHS, *numerics], cwd=ROOT,
                             capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=archive, check=True)
    run(sys.executable, "presentation/build.py", cwd=root)
    (root / ".complete").write_text(LAPLACE_COMMIT + "\n")
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="stage and run a Wrangler dry run without uploading")
    mode.add_argument("--stage-only", metavar="DIR", help="stage into DIR (replacing it) and stop")
    args = parser.parse_args()
    if not args.stage_only and not args.dry_run:
        require_main_merged()
    run(sys.executable, "handout/build.py", "--quiet")
    run(sys.executable, "handout/check_display.py")
    run(sys.executable, "presentation/build.py")
    run("node", "presentation/check_deck.mjs")
    lap = laplace_archive()

    # Stage an explicit file list so drafts, notes and stray files stay private.
    fonts = json.loads((ROOT / "handout/fonts.lock.json").read_text())
    vendor = json.loads((ROOT / "handout/vendor.lock.json").read_text())["katex"]["files"]
    locked = [f"fonts/{name}" for name in fonts] + [f"vendor/{name}" for name in vendor]
    plan: dict[str, Path] = {}
    # The site root: the research brief, the manuscript and the comparison note.
    for name in ["index.html", "paper.pdf", "comparison.pdf", *locked]:
        plan[name] = ROOT / "docs" / name
    # The talk: the built slides, the locked fonts and KaTeX files, the provenance record, and the
    # print export when it has been produced. Speaker notes in Markdown and QA output stay private.
    dist = ROOT / "presentation/dist"
    for name in ["index.html", "provenance.json", *locked] + (["presentation.pdf"] if (dist / "presentation.pdf").exists() else []):
        plan[f"talk/{name}"] = dist / name
    # The Laplace archive, from the pinned commit: its committed handout build and its slides.
    lap_fonts = json.loads((lap / "handout/fonts.lock.json").read_text())
    lap_vendor = json.loads((lap / "handout/vendor.lock.json").read_text())["katex"]["files"]
    lap_locked = [f"fonts/{name}" for name in lap_fonts] + [f"vendor/{name}" for name in lap_vendor]
    for name in ["index.html", "main_filled.pdf", "online_appendix_filled.pdf", *lap_locked]:
        plan[f"laplace/{name}"] = lap / "docs" / name
    for name in ["index.html", "main_filled.pdf", "online_appendix_filled.pdf", "provenance.json", *lap_locked]:
        plan[f"laplace/talk/{name}"] = lap / "presentation/dist" / name

    def stage_into(stage: Path) -> list[str]:
        for name, src in plan.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, target)
        # One line on the archived front page names it as the earlier version and links the current one.
        page = (stage / "laplace/index.html").read_text(encoding="utf-8")
        assert page.count("<body>") == 1
        (stage / "laplace/index.html").write_text(page.replace("<body>", "<body>\n" + ARCHIVE_NOTE, 1), encoding="utf-8")
        expected = sorted(plan)
        assert sorted(p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file()) == expected
        print(f"No purple palette in the {check_palette(stage)} HTML, CSS and JS files of the current site", flush=True)
        return expected

    def report(expected: list[str]) -> str:
        parts = {"talk/": 0, "laplace/talk/": 0, "laplace/": 0}
        for name in expected:
            for prefix in parts:
                if name.startswith(prefix):
                    parts[prefix] += 1
                    break
        return (f"{len(expected)} files: {len(expected) - sum(parts.values())} at the root, {parts['talk/']} under /talk/, "
                f"{parts['laplace/']} under /laplace/ and {parts['laplace/talk/']} under /laplace/talk/")

    if args.stage_only:
        stage = Path(args.stage_only).resolve()
        if stage == ROOT or ROOT in stage.parents:
            raise SystemExit("--stage-only needs a directory outside the repository")
        if stage.exists():
            shutil.rmtree(stage)
        stage.mkdir(parents=True)
        print(f"Staged {report(stage_into(stage))} in {stage}", flush=True)
        return
    with tempfile.TemporaryDirectory(prefix="ccc-publish-") as directory:
        stage = Path(directory)
        expected = stage_into(stage)
        print(f"Publishing {report(expected)} to competition.dealextract.org", flush=True)
        command = ["npx", "--yes", "wrangler@4.130.0", "deploy", "--config", "handout/wrangler.jsonc", "--assets", str(stage)]
        if args.dry_run:
            command.append("--dry-run")
        subprocess.run(command, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
