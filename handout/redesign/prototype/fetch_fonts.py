"""Fetch candidate OFL web fonts from fontsource (jsdelivr) and check them.

Writes proposals/_fonts/<file>.woff2, LICENSE texts, and manifest.json with
package, version, license, sha256, font version (name table), and glyph checks.
Standard library plus fontTools (present on this machine) for the checks.
"""
import hashlib, io, json, sys, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_fonts"
OUT.mkdir(exist_ok=True)
VER = "5.3.0"
CDN = "https://cdn.jsdelivr.net/npm/"

# (package, variable?, subsets, [(weight, style)])
PLAN = [
    ("source-serif-4", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("source-sans-3", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("stix-two-text", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("ibm-plex-sans", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal")]),
    ("ibm-plex-mono", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("500", "normal")]),
    ("libertinus-serif", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("400", "italic"), ("600", "normal"), ("700", "normal")]),
    ("libertinus-sans", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("400", "italic"), ("700", "normal")]),
    ("inter", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("inter-tight", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("jetbrains-mono", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal"), ("wght", "italic")]),
    ("source-code-pro", True, ["latin", "latin-ext", "greek", "math", "symbols"], [("wght", "normal")]),
    ("fira-sans", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("400", "italic"), ("500", "normal"), ("600", "normal"), ("700", "normal")]),
    ("fira-mono", False, ["latin", "latin-ext", "greek", "math", "symbols"], [("400", "normal"), ("500", "normal"), ("700", "normal")]),
]

# Code points the handout tables and prose use as text (outside KaTeX).
TEST = {
    "theta": 0x03B8, "mu": 0x03BC, "Delta": 0x0394, "rho": 0x03C1, "tau": 0x03C4, "eta": 0x03B7, "alpha": 0x03B1,
    "ell": 0x2113, "arrow_right": 0x2192, "arrow_up": 0x2191, "arrow_down": 0x2193, "leq": 0x2264, "geq": 0x2265,
    "approx": 0x2248, "in": 0x2208, "infinity": 0x221E, "minus": 0x2212, "times": 0x00D7, "middot": 0x00B7,
    "endash": 0x2013, "half": 0x00BD, "degree_sign_sub2": 0x2082,
}


def fetch(url):
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def inspect(blob):
    from fontTools.ttLib import TTFont
    f = TTFont(io.BytesIO(blob))
    cmap = f.getBestCmap()
    name = f["name"]
    version = ""
    for rec in name.names:
        if rec.nameID == 5:
            version = rec.toUnicode()
            break
    feats = set()
    if "GSUB" in f and f["GSUB"].table.FeatureList:
        feats = {fr.FeatureTag for fr in f["GSUB"].table.FeatureList.FeatureRecord}
    axes = [a.axisTag for a in f["fvar"].axes] if "fvar" in f else []
    return {
        "version": version,
        "glyphs": {k: (cp in cmap) for k, cp in TEST.items()},
        "tnum": "tnum" in feats, "lnum": "lnum" in feats, "onum": "onum" in feats,
        "axes": axes, "num_glyphs": len(cmap),
    }


def main():
    manifest = {"fontsource_version": VER, "fetched": {}, "licenses": {}}
    for pkg, variable, subsets, faces in PLAN:
        scope = "@fontsource-variable/" if variable else "@fontsource/"
        base = f"{CDN}{scope}{pkg}@{VER}/"
        lic = fetch(base + "LICENSE")
        if lic:
            (OUT / f"{pkg}-LICENSE.txt").write_bytes(lic)
            manifest["licenses"][pkg] = f"{pkg}-LICENSE.txt"
        meta = fetch(base + "package.json")
        meta = json.loads(meta) if meta else {}
        for subset in subsets:
            for weight, style in faces:
                fname = f"{pkg}-{subset}-{weight}-{style}.woff2"
                target = OUT / fname
                if target.exists():
                    blob = target.read_bytes()
                else:
                    blob = fetch(base + "files/" + fname)
                    if blob is None:
                        continue
                    target.write_bytes(blob)
                info = inspect(blob)
                manifest["fetched"][fname] = {
                    "package": scope + pkg, "package_version": meta.get("version", VER),
                    "license": meta.get("license", "OFL-1.1"), "sha256": hashlib.sha256(blob).hexdigest(),
                    "bytes": len(blob), "subset": subset, "weight": weight, "style": style, **info,
                }
                print(fname, len(blob), info["version"][:40], "tnum" if info["tnum"] else "-", file=sys.stderr)
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1))
    # Family summary: union of glyph coverage over subsets, per family.
    fam = {}
    for fname, m in manifest["fetched"].items():
        key = m["package"].split("/")[-1]
        d = fam.setdefault(key, {"files": 0, "bytes": 0, "glyphs": {k: [] for k in TEST}, "tnum": False, "italic": False, "version": m["version"]})
        d["files"] += 1; d["bytes"] += m["bytes"]
        d["tnum"] = d["tnum"] or m["tnum"]
        d["italic"] = d["italic"] or m["style"] == "italic"
        for k, ok in m["glyphs"].items():
            if ok and m["subset"] not in d["glyphs"][k]:
                d["glyphs"][k].append(m["subset"])
    (OUT / "families.json").write_text(json.dumps(fam, indent=1))
    for k, d in fam.items():
        missing = [g for g, s in d["glyphs"].items() if not s]
        print(f"{k:18s} files={d['files']:2d} tnum={d['tnum']} italic={d['italic']} missing={missing}", file=sys.stderr)


if __name__ == "__main__":
    main()
