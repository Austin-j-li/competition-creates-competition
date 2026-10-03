"""CSV slices to ``window.CCC_DATA`` (handout/README.md, section "CCC_DATA contract").

Every CSV token that reaches the page is copied verbatim: numeric tokens become JSON number
literals through :class:`Num`, everything else becomes a JSON string. Python never calls
``float()`` on a value that is emitted; ordering uses :class:`decimal.Decimal`. Stdlib only.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from decimal import Decimal
from pathlib import Path

NUMERIC = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")

REGISTRY_FIELDS = ("display", "value", "lower", "upper", "units", "status", "exercise",
                   "parameter_set", "branch", "source_file", "source_row", "definition")
INPUT_NAMES = {"h": "base_h", "ell": "base_ell", "p": "base_p", "rho": "base_rho", "c_L": "base_c_low",
               "c_H": "base_c_high", "b": "base_b", "k": "base_k", "r_weak": "base_r_weak",
               "r_strong": "base_r_strong", "r_collapse": "base_r_collapse"}
PLOTTED_BRANCHES = ("pooling", "full_orders", "asymmetric", "symmetric_interior", "mixed")
BRANCH_FIELDS = ("r", "E", "O_H", "q_H", "q_L", "v", "tau", "existence_status", "uniqueness_status", "multiplicity_found", "candidate_id", "result_status")
THRESHOLD_NAMES = ("pooling_unique_sufficient", "pooling_existence", "full_orders_unique_sufficient",
                   "high_cost_ceiling", "m", "M", "laplace_entry_left_limit")
SOURCES = ("numerics/quantity_registry.csv", "figures_data/two_returns.csv", "numerics/correspondence.csv",
           "numerics/certificates.csv", "numerics/thresholds.csv", "figures_data/posterior_tails.csv",
           "figures_data/bargaining.csv", "tables/auction_primitives.csv", "tables/equilibrium_controls.csv",
           "tables/extensions.csv", "numerics/moderate_values.csv", "tables/reserve_comparisons.csv",
           "numerics/feedback_comparisons.csv", "numerics/mixed_supports.csv", "numerics/two_signals.csv", "numerics/reserve_events.csv")


class DataError(ValueError):
    """A slice could not be built from the CSVs as declared."""


class Num:
    """A numeric CSV token emitted verbatim as a JSON number literal."""

    __slots__ = ("token",)

    def __init__(self, token: str) -> None:
        if not isinstance(token, str) or not NUMERIC.match(token):
            raise DataError(f"not a numeric token: {token!r}")
        self.token = token

    def __repr__(self) -> str:
        return f"Num({self.token})"


def read_csv(root: Path, rel: str) -> list[dict]:
    with open(root / rel, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sha256(root: Path, rel: str) -> str:
    return hashlib.sha256((root / rel).read_bytes()).hexdigest()


def num(token: str) -> Num:
    return Num(token)


def num_or_str(token: str):
    return Num(token) if NUMERIC.match(token) else token


# ----------------------------------------------------------------------------------------------
# Emitter


def _emit_str(s: str) -> str:
    out = json.dumps(s, ensure_ascii=False)
    return out.replace("</", "<\\/").replace("<!--", "<\\u0021--")


def emit_js(obj, _indent: int = 0) -> str:
    """Deterministic JSON text: sorted keys, verbatim numeric tokens, no bool/None."""
    if isinstance(obj, Num):
        return obj.token
    if isinstance(obj, str):
        return _emit_str(obj)
    if isinstance(obj, (bool, type(None), float, int)):
        raise DataError(f"value type not allowed in CCC_DATA: {type(obj).__name__} ({obj!r})")
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        parts = [f"{_emit_str(str(k))}:{emit_js(obj[k])}" for k in sorted(obj, key=str)]
        return "{" + ",".join(parts) + "}"
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(emit_js(x) for x in obj) + "]"
    raise DataError(f"unsupported type in CCC_DATA: {type(obj).__name__}")


# ----------------------------------------------------------------------------------------------
# Slices


def _registry(root: Path) -> tuple[dict, dict]:
    rows = read_csv(root, "numerics/quantity_registry.csv")
    reg = {}
    for r in rows:
        if r["name"] in reg:
            raise DataError(f"duplicate registry name {r['name']}")
        reg[r["name"]] = {k: r[k] for k in REGISTRY_FIELDS}
    inputs = {}
    for key, name in INPUT_NAMES.items():
        if name not in reg:
            raise DataError(f"registry input {name} missing")
        if reg[name]["status"] != "input":
            raise DataError(f"registry {name} is not an input row")
        inputs[key] = reg[name]["value"]
    return reg, inputs


def _fig1(root: Path) -> dict:
    rows = read_csv(root, "figures_data/two_returns.csv")
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r["mu"], []).append(r)
    mus = sorted(groups, key=Decimal)
    if len(mus) != 3:
        raise DataError(f"two_returns: expected 3 mu groups, found {len(mus)}")
    for mu in mus:
        groups[mu].sort(key=lambda x: Decimal(x["r"]))
    ref = groups[mus[0]]
    for col in ("r", "Delta_T", "d_Delta_T_dr"):
        for mu in mus[1:]:
            if [x[col] for x in groups[mu]] != [x[col] for x in ref]:
                raise DataError(f"two_returns: column {col} differs across mu groups")
    labels = {mus[0]: "m", mus[1]: "1/2", mus[2]: "M"}
    if mus[1] != "0.5":
        raise DataError(f"two_returns: middle mu is {mus[1]}, expected 0.5")
    return {
        "r": [num(x["r"]) for x in ref],
        "Delta_T": [num(x["Delta_T"]) for x in ref],
        "d_Delta_T_dr": [num(x["d_Delta_T_dr"]) for x in ref],
        "mu": list(mus),
        "mu_label": labels,
        "B": {mu: [num(x["B_r(mu)"]) for x in groups[mu]] for mu in mus},
        "dB": {mu: [num(x["d_B_r_mu_dr"]) for x in groups[mu]] for mu in mus},
    }


def _sig17(d: Decimal) -> str:
    return format(d, ".17g")


def _fig2(root: Path) -> dict:
    rows = read_csv(root, "numerics/correspondence.csv")
    corr = [r for r in rows if r["accepted"] == "true"]
    identities, counts = set(), {}
    for row in corr:
        for key in ("candidate_id", "continuation_id", "parameter_set_id", "result_status"):
            if row.get(key) in (None, "", "n/a"):
                raise DataError(f"correspondence: missing {key}")
        identity = row["parameter_set_id"], row["continuation_id"]
        if identity in identities or row.get("duplicate_of"):
            raise DataError("correspondence: duplicate accepted continuation")
        identities.add(identity)
        r = Decimal(row["r"])
        counts[r] = counts.get(r, 0) + 1
        if row["result_status"] not in ("analytical", "computer-assisted", "numerical diagnostic"):
            raise DataError("correspondence: unsupported evidence status")
        if not Decimal(row["E"]).is_finite() or not 0 <= Decimal(row["E"]) <= 1:
            raise DataError("correspondence: invalid preparation probability")
    for row in corr:
        count = counts[Decimal(row["r"])]
        if int(row["n_distinct_accepted"]) != count or (row["multiplicity_found"] == "true") != (count > 1):
            raise DataError("correspondence: multiplicity disagrees with distinct identities")
    if not {r["branch"] for r in corr} <= set(PLOTTED_BRANCHES):
        raise DataError("correspondence: accepted branch has no display style")
    branches = {}
    for branch in sorted({r["branch"] for r in corr}):
        sub = sorted((r for r in corr if r["branch"] == branch), key=lambda x: Decimal(x["r"]))
        branches[branch] = {f: [num_or_str(x[f]) for x in sub] for f in BRANCH_FIELDS}
    support_rows = read_csv(root, "numerics/mixed_supports.csv")
    supports = []
    for row in corr:
        if row["q_H"] != "mixed":
            continue
        matched = [r for r in support_rows if r["accepted"] == "true"
                   and r["candidate_id"] == row["candidate_id"] and r["continuation_id"] == row["continuation_id"]]
        if not matched or {r["state"] for r in matched} != {"H", "L"}:
            raise DataError("mixed continuation has no complete support records")
        supports.extend({k: num_or_str(r[k]) for k in ("r", "q", "weight", "state", "candidate_id")} for r in matched)
    certs = read_csv(root, "numerics/certificates.csv")
    if not certs or any(c["accepted"] != "true" for c in certs):
        raise DataError("certificates: missing or not all accepted")
    cert_out = []
    for c in sorted(certs, key=lambda x: Decimal(x["r"])):
        vl, vu, el, eu = (Decimal(c[k]) for k in ("v_lower", "v_upper", "E_lower", "E_upper"))
        if vl > vu or el > eu:
            raise DataError(f"certificate r={c['r']}: interval endpoints out of order")
        cert_out.append({
            "r": c["r"], "v_lower": c["v_lower"], "v_upper": c["v_upper"], "E_lower": c["E_lower"], "E_upper": c["E_upper"],
            "accepted": c["accepted"],
            "v_mid": num(_sig17((vl + vu) / 2)), "E_mid": num(_sig17((el + eu) / 2)),
            "v_halfwidth": format((vu - vl) / 2, ".2e"), "E_halfwidth": format((eu - el) / 2, ".2e"),
        })
    thr_rows = read_csv(root, "numerics/thresholds.csv")
    thr = {}
    for t in thr_rows:
        thr[t["boundary"]] = {"value": num(t["value"]), "value_str": t["value"], "lower": t["lower"],
                              "upper": t["upper"], "interpretation": t["interpretation"]}
    missing = [n for n in THRESHOLD_NAMES if n not in thr]
    if missing:
        raise DataError(f"thresholds: missing {missing}")
    multi = sorted({Decimal(r["r"]) for r in corr if r["multiplicity_found"] == "true"})
    if not multi:
        raise DataError("correspondence: no accepted row with multiplicity_found=true")
    return {
        "x_range": [num("1.0"), num("3.8")],
        "branches": branches,
        "nodes": [num(str(r)) for r in sorted({Decimal(row["r"]) for row in rows})],
        "multiplicity_nodes": [num(str(r)) for r in multi],
        "unresolved_nodes": [num(str(r)) for r in sorted({Decimal(row["r"]) for row in rows if row["result_status"] == "open"})],
        "mixed_supports": supports,
        "certificates": cert_out,
        "thresholds": thr,
        "regions": {
            "no_trade_unique": [num("1.0"), thr["pooling_unique_sufficient"]["value"]],
            "full_orders_unique": [thr["full_orders_unique_sufficient"]["value"], num("3.8")],
        },
    }


def _fig3(root: Path) -> dict:
    rows = [r for r in read_csv(root, "figures_data/posterior_tails.csv") if r["tau_label"] == "grid"]
    out = {}
    for noise in ("Laplace", "logistic"):
        sub = sorted((r for r in rows if r["noise"] == noise), key=lambda x: Decimal(x["M_minus_tau"]))
        if not sub:
            raise DataError(f"posterior_tails: no grid rows for {noise}")
        zero = [i for i, r in enumerate(sub) if Decimal(r["M_minus_tau"]) == 0]
        if zero != [0]:
            raise DataError(f"posterior_tails {noise}: zero-distance rows at indices {zero}, expected [0]")
        if noise == "logistic" and (sub[0]["x_star"] != "unattainable"
                or Decimal(sub[0]["posterior_upper_tail_mass"]) != 0):
            raise DataError("logistic endpoint must be unattainable with zero tail mass")
        out[noise] = {
            "M_minus_tau": [num(r["M_minus_tau"]) for r in sub],
            "posterior_upper_tail_mass": [num(r["posterior_upper_tail_mass"]) for r in sub],
            "E": [num(r["E"]) for r in sub],
            "x_star": [r["x_star"] for r in sub],
        }
    return out


def _fig4(root: Path) -> dict:
    rows = read_csv(root, "figures_data/bargaining.csv")
    out = {}
    for rs in sorted({r["r"] for r in rows}, key=Decimal):
        sub = sorted((r for r in rows if r["r"] == rs), key=lambda x: Decimal(x["eta"]))
        endpoint = [r for r in sub if Decimal(r["eta"]) == 1]
        if len(endpoint) != 1 or any(Decimal(endpoint[0][k]) != 0 for k in ("G_H_eta", "G_L_eta")):
            raise DataError("bargaining: missing zero-profit endpoint")
        out[rs] = {f: [num(r[f]) for r in sub] for f in ("eta", "Delta_eta", "G_H_eta", "G_L_eta")}
    if set(out) != {"1.2", "3"}:
        raise DataError(f"bargaining: strengths {sorted(out)}, expected 1.2 and 3")
    return out


def _tables(root: Path) -> dict:
    def all_rows(rel: str) -> list[dict]:
        return [dict(r) for r in read_csv(root, rel)]

    eq = [r for r in all_rows("tables/equilibrium_controls.csv")
          if r["noise"] == "Laplace" and r["cost_law"] == "atoms" and r["accepted"] == "true"]
    if not eq:
        raise DataError("equilibrium_controls: no accepted Laplace/atoms rows")
    return {
        "auction_primitives": all_rows("tables/auction_primitives.csv"),
        "equilibrium_controls": eq,
        "extensions": all_rows("tables/extensions.csv"),
        "moderate_values": all_rows("numerics/moderate_values.csv"),
        "reserve_comparisons": all_rows("tables/reserve_comparisons.csv"),
        "feedback_comparisons": all_rows("numerics/feedback_comparisons.csv"),
        "thresholds": all_rows("numerics/thresholds.csv"),
        "certificates": all_rows("numerics/certificates.csv"),
    }


def build_data(root: Path | str, vendor: dict | None = None) -> tuple[dict, dict]:
    """Return ``(CCC_DATA, source_hashes)``. ``vendor`` is the parsed vendor lock (optional)."""
    root = Path(root)
    if vendor is None:
        vendor = json.loads((root / "handout" / "vendor.lock.json").read_text(encoding="utf-8"))
    hashes = {rel: sha256(root, rel) for rel in SOURCES}
    # Bind the presentation to the audited output bytes; fail before rendering stale data.
    recorded = {}
    for path in sorted((root / "numerics/manifests").glob("*.json")):
        if path.stem == "handout":
            continue
        manifest = json.loads(path.read_text())
        if manifest.get("passed"):
            recorded.update(manifest.get("outputs", {}))
    for rel, digest in hashes.items():
        if recorded.get(rel) != digest:
            raise DataError(f"source differs from a passed numerical manifest: {rel}")
    registry, inputs = _registry(root)
    data = {
        "meta": {
            "katex": vendor["katex"]["version"],
            "registry_hash": hashes["numerics/quantity_registry.csv"],
            "sources": dict(hashes),
        },
        "inputs": inputs,
        "registry": registry,
        "fig1": _fig1(root),
        "fig2": _fig2(root),
        "fig3": _fig3(root),
        "fig4": _fig4(root),
        "tables": _tables(root),
    }
    return data, hashes


if __name__ == "__main__":
    d, h = build_data(Path(__file__).resolve().parents[1])
    text = emit_js(d)
    json.loads(text)
    print(f"CCC_DATA: {len(text.encode('utf-8'))} bytes, {len(h)} sources")
