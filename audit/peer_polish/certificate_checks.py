#!/usr/bin/env python3
"""S1-D: interval-certificate port comparison (tests T16, T17).

1. Compares the fresh run of the byte-for-byte seed copy (reference_seed/results) with the
   preserved result file (verification/results/asymmetric_interval_certificates.json).
2. Runs the repository port numerics.certificates.certify at the declared precision/mesh,
   then the declared refinement (400 intervals); escalates 50/80/120 digits and 200/400/800
   meshes only if a predicate fails, retaining every attempt.
3. Verifies the eight S1-D items per node from the full endpoint objects (not printed digits),
   compares them with numerics/certificates.csv and the seed JSON, and adds an independent
   high-precision (non-interval) evaluation of Psi at the bracket endpoints, of the high-type
   derivative on the mesh at v in {v_-, mid, v_+}, and of the entry probability.
4. Checks the displayed intervals in paper/main_filled.md and numerics/quantity_registry.csv
   enclose the computed enclosures with outward rounding (lower down, upper up).

Outputs audit/peer_polish/certificate_comparison.json and audit/peer_polish/logs/s1_certificates.md.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, getcontext
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from numerics import certificates as C  # noqa: E402  (the port under test)
from numerics.params import BENCHMARK, CERTIFICATE_BRACKETS, CONTROLS  # noqa: E402

getcontext().prec = 120
SEED_DIR = ROOT / "audit/peer_polish/reference_seed"
OUT_JSON = ROOT / "audit/peer_polish/certificate_comparison.json"
OUT_MD = ROOT / "audit/peer_polish/logs/s1_certificates.md"

NODES = [("1.55", "0.46031618", "0.46031620"), ("1.60", "0.70747537", "0.70747539"), ("1.65", "0.90333198", "0.90333201")]
ESCALATION = [(50, 200), (80, 400), (120, 800)]


class CheckFailure(Exception):
    pass


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def iv_endpoints(x) -> tuple[str, str]:
    """Exact decimal strings (outward, 60 digits) of an mpmath interval's endpoints."""
    return C.endpoint_str(x, "lower"), C.endpoint_str(x, "upper")


def parse_iv_string(s: str) -> tuple[Decimal, Decimal]:
    m = re.match(r"\[\s*([-0-9.eE+]+)\s*,\s*([-0-9.eE+]+)\s*\]", s)
    if not m:
        raise CheckFailure(f"cannot parse interval string {s!r}")
    return Decimal(m.group(1)), Decimal(m.group(2))


# ---------------------------------------------------------------------------------------
# independent (non-interval) high-precision evaluation of the certified objects
# ---------------------------------------------------------------------------------------
def indep_objects(r_s: str, v_s: str, s_val, sgn: int, dps: int = 30):
    """Return (U'(s), F(s), E) for the profile (1, -v) by mpmath quadrature at `dps` digits.

    sgn = -1: low type, center -s; sgn = +1: high type, center +s. Exact formulas from OA.56-57."""
    with mp.workdps(dps):
        r, v, s = mp.mpf(r_s), mp.mpf(v_s), mp.mpf(s_val)
        p, ell, h = mp.mpf(BENCHMARK.p), mp.mpf(BENCHMARK.ell), mp.mpf(BENCHMARK.h)
        b, rho, k, cH = mp.mpf(BENCHMARK.b), mp.mpf(BENCHMARK.rho), mp.mpf(BENCHMARK.k), mp.mpf(BENCHMARK.c_H)
        tH = r / 2 + p * p / (2 * r)
        tL = ell - (ell * ell - p * p) / (2 * r)
        gH, gL = h - tH, (ell * ell - p * p) / (2 * r)
        Delta = tH - tL
        tau = (cH - gL) / (gH - gL)
        xs = (b * mp.log(tau / (1 - tau)) + 1 - v) / 2
        f = lambda z: mp.exp(-abs(z) / b) / (2 * b)
        fprime = lambda z: -mp.sign(z) * f(z) / b
        mu = lambda x: 1 / (1 + mp.exp(-(abs(x + v) - abs(x - 1)) / b))
        e = lambda x: rho if x < xs else mp.mpf(1)
        A = (lambda x: e(x) * Delta * (1 - mu(x))) if sgn == 1 else (lambda x: e(x) * Delta * mu(x))
        center = sgn * s
        cuts = sorted({-v, xs, mp.mpf(1), center})
        pts = [-mp.inf] + cuts + [mp.inf]
        F = mp.mpf(0)
        Fp = mp.mpf(0)
        for a, c in zip(pts[:-1], pts[1:]):
            F += mp.quad(lambda x: f(x - center) * A(x), [a, c])
            # F_eps'(s) = -eps int f'(x - eps s) A(x) dx
            Fp += -sgn * mp.quad(lambda x: fprime(x - center) * A(x), [a, c])
        Up = F + s * Fp - k
        alphaH = 1 - mp.exp((xs - 1) / b) / 2
        alphaL = mp.exp(-(xs + v) / b) / 2
        E = rho + (1 - rho) * (alphaH + alphaL) / 2
        return Up, F, E, {"tau": tau, "xs": xs, "Delta": Delta, "M_v": 1 / (1 + mp.exp(-(1 + v) / b))}


def main() -> int:
    t0 = time.time()
    report: dict = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "environment": {"python": sys.version.split()[0], "mpmath": mp.__version__},
                    "checks": [], "nodes": {}}
    checks = report["checks"]

    def add(name, ok, note="", **kw):
        checks.append({"check": name, "status": "pass" if ok else "FAIL", "note": note, **kw})
        return ok

    # --- 1. seed provenance and fresh seed run vs preserved file ---------------------------
    seed_src = ROOT / "verification/certify_asymmetric.py"
    seed_copy = SEED_DIR / "certify_asymmetric.py"
    add("seed copy byte-identical to verification/certify_asymmetric.py", sha(seed_src) == sha(seed_copy), sha(seed_copy))
    add("seed copy unchanged after run (sha256_after_run.txt)", (SEED_DIR / "sha256_after_run.txt").read_text().split()[0] == sha(seed_copy))
    stdout = (SEED_DIR / "seed_run_stdout.txt").read_text()
    add("seed run completed with assertions enabled", "seed completed: every assertion held" in stdout and "optimize flag: 0" in stdout)
    seed_new = json.loads((SEED_DIR / "results/asymmetric_interval_certificates.json").read_text())
    seed_old = json.loads((ROOT / "verification/results/asymmetric_interval_certificates.json").read_text())
    report["seed_versions"] = {"preserved": seed_old["mpmath"], "fresh": seed_new["mpmath"], "digits": (seed_old["interval_decimal_precision"], seed_new["interval_decimal_precision"])}
    iv_fields = ["FOC_at_left", "FOC_at_right", "high_global_derivative_lower", "derivative_Lipschitz_bound", "pooling_margin",
                 "low_cost_margin", "high_cost_prior_margin", "entry", "low_trader_payoff", "high_trader_payoff"]
    for o, n in zip(seed_old["results"], seed_new["results"]):
        for fld in iv_fields:
            same = o[fld]["interval"] == n[fld]["interval"]
            if not same:
                lo_o, hi_o = parse_iv_string(o[fld]["interval"])
                lo_n, hi_n = parse_iv_string(n[fld]["interval"])
                # different mpmath versions may round differently; the enclosures must still overlap and agree to ~1e-45
                note = f"preserved {o[fld]['interval']} vs fresh {n[fld]['interval']}"
                add(f"seed r={o['r']} {fld}: fresh run reproduces preserved enclosure", abs(lo_o - lo_n) < Decimal("1e-45") and abs(hi_o - hi_n) < Decimal("1e-45"), note)
            else:
                add(f"seed r={o['r']} {fld}: fresh run reproduces preserved enclosure (identical string)", True)
        add(f"seed r={o['r']} high_derivative_mesh_min_lower identical", o["high_derivative_mesh_min_lower"] == n["high_derivative_mesh_min_lower"])

    # --- 2. port runs with declared controls and escalation schedule ----------------------
    csv_rows = {row["r"]: row for row in csv.DictReader(open(ROOT / "numerics/certificates.csv", newline=""))}
    reg = {row["name"]: row for row in csv.DictReader(open(ROOT / "numerics/quantity_registry.csv", newline=""))}
    main_filled = (ROOT / "paper/main_filled.md").read_text()
    node_letters = {"1.55": "a", "1.60": "b", "1.65": "c"}
    port_E = {}
    for (r_s, vl_s, vr_s), seed_res in zip(NODES, seed_new["results"]):
        node = {"r": r_s, "bracket": [vl_s, vr_s], "attempts": []}
        report["nodes"][r_s] = node
        add(f"r={r_s}: declared bracket matches numerics.params and C.2", CERTIFICATE_BRACKETS[NODES.index((r_s, vl_s, vr_s))] == (r_s, vl_s, vr_s))
        accepted_rec = None
        # declared pass (50 digits, 200 intervals) and the declared refinement (400 intervals), then escalation if needed
        schedule = [(CONTROLS.interval_decimal_precision, CONTROLS.certificate_derivative_intervals),
                    (CONTROLS.interval_decimal_precision, CONTROLS.certificate_refined_intervals)]
        for dps, n in schedule + [x for x in ESCALATION if x not in schedule]:
            if accepted_rec is not None and (dps, n) not in schedule:
                break  # escalation only after a failure
            ctrl = CONTROLS.__class__(**{**CONTROLS.as_dict(), "interval_decimal_precision": dps})
            rec = C.certify(BENCHMARK, r_s, vl_s, vr_s, ctrl, n=n)
            att = {"digits": dps, "mesh_intervals": n, "predicates": rec.predicates, "failures": rec.failures, "accepted": rec.accepted,
                   "values": {k: list(iv_endpoints(v)) for k, v in rec.values.items() if hasattr(v, "a")}}
            att["values"]["mesh_intervals"] = rec.values.get("mesh_intervals")
            node["attempts"].append(att)
            if rec.accepted and accepted_rec is None:
                accepted_rec = (dps, n, rec)
        if accepted_rec is None:
            add(f"r={r_s}: certificate accepted within the escalation schedule", False, "OPEN: no attempt accepted; see attempts")
            continue
        dps, n, rec = accepted_rec
        add(f"r={r_s}: accepted at the declared precision/mesh (50 digits, 200 intervals)", (dps, n) == (50, 200), f"accepted at {dps} digits, {n} intervals")
        add(f"r={r_s}: declared refinement (400 intervals) also accepted", node["attempts"][1]["accepted"])
        V = rec.values
        # eight items ---------------------------------------------------------------------
        m_glob = 1 / (1 + mp.iv.exp(2 / mp.iv.mpf(BENCHMARK.b)))
        Pi = C.primitives_iv(BENCHMARK, mp.iv.mpf(r_s))
        add(f"r={r_s} [1] support p < ell < r < h", rec.predicates["support"])
        add(f"r={r_s} [1] prior high-cost exclusion c_H - B_r(1/2) > 0", rec.predicates["high_cost_prior_exclusion"], iv_endpoints(V["high_prior_margin"])[0])
        add(f"r={r_s} [1] low-cost participation B_r(m) - c_L > 0", rec.predicates["low_cost_floor"], iv_endpoints(V["low_cost_margin"])[0])
        # [2] threshold location over the whole bracket: 1/2 < tau < M_v for v in [v_-, v_+] (tightest at v_-)
        v_iv = mp.iv.mpf([vl_s, vr_s])
        tau_iv = (mp.iv.mpf(BENCHMARK.c_H) - Pi["gL"]) / (Pi["gH"] - Pi["gL"])
        Mv_iv = 1 / (1 + mp.iv.exp(-(1 + v_iv) / mp.iv.mpf(BENCHMARK.b)))
        xs_iv = (mp.iv.mpf(BENCHMARK.b) * mp.iv.log(tau_iv / (1 - tau_iv)) + 1 - v_iv) / 2
        thr_ok = C.lo(tau_iv) > 0.5 and C.hi(tau_iv) < C.lo(Mv_iv) and C.lo(xs_iv) > -C.lo(v_iv) and C.hi(xs_iv) < 1
        add(f"r={r_s} [2] threshold 1/2 < tau < M_v and -v < x* < 1 throughout the bracket", thr_ok and rec.predicates["threshold_ordering"],
            f"tau={iv_endpoints(tau_iv)}, M_v={iv_endpoints(Mv_iv)}, x*={iv_endpoints(xs_iv)}")
        # [3], [4]
        psi_l, psi_r = V["Psi_left"], V["Psi_right"]
        add(f"r={r_s} [3] Psi(r, v_-) outward enclosure strictly positive", rec.predicates["psi_left_positive"], str(iv_endpoints(psi_l)))
        add(f"r={r_s} [4] Psi(r, v_+) outward enclosure strictly negative", rec.predicates["psi_right_negative"], str(iv_endpoints(psi_r)))
        # [5]
        add(f"r={r_s} [5] low-type strict concavity (OA.60: b > 1/2; posterior nondecreasing since 1 > -v; e nondecreasing)",
            rec.predicates["low_type_concavity"] and float(mp.mpf(BENCHMARK.b)) > 0.5 and float(vl_s) > 0 and float(vr_s) < 1)
        # [6] high-type cover at every mesh point uniformly over the bracket
        src = Path(C.__file__).read_text()
        uses_interval_v = "v = iv.mpf([vl_s, vr_s])" in src and "objects(prim, r, v, s, 1)" in src
        add(f"r={r_s} [6] high-type derivative enclosed on every mesh point with v = [v_-, v_+] interval (source inspection) and Gamma_H > 0",
            uses_interval_v and rec.predicates["gamma_H_positive"], f"Gamma_H={iv_endpoints(V['Gamma_H'])}, mesh min lower={C.endpoint_str(V['mesh_min_lower'], 'lower') if hasattr(V['mesh_min_lower'], 'a') else str(V['mesh_min_lower'])}, n={V['mesh_intervals']}")
        lip_check = 2 * Pi["Delta"] / mp.iv.mpf(BENCHMARK.b) + Pi["Delta"] / mp.iv.mpf(BENCHMARK.b) ** 2
        add(f"r={r_s} [6] L_U = 2 Delta/b + Delta/b^2 reproduced", iv_endpoints(lip_check) == iv_endpoints(V["L_U"]))
        # [7]
        add(f"r={r_s} [7] pooling-existence margin k - rho Delta/2 > 0", rec.predicates["pooling_exists_margin"], iv_endpoints(V["pooling_margin"])[0])
        # [8] entry enclosure (ordering checked after the loop)
        port_E[r_s] = V["E"]
        E_lo, E_hi = iv_endpoints(V["E"])
        # --- compare full endpoint objects with numerics/certificates.csv ------------------
        row = csv_rows[r_s]
        cmp = {"Psi_left_lower": iv_endpoints(psi_l)[0], "Psi_left_upper": iv_endpoints(psi_l)[1], "Psi_right_lower": iv_endpoints(psi_r)[0],
               "Psi_right_upper": iv_endpoints(psi_r)[1], "Gamma_H_lower": iv_endpoints(V["Gamma_H"])[0], "L_U_upper": iv_endpoints(V["L_U"])[1],
               "E_lower": E_lo, "E_upper": E_hi, "pooling_margin_lower": iv_endpoints(V["pooling_margin"])[0],
               "threshold_margin_lower": iv_endpoints(V["low_cost_margin"])[0]}
        for k_, v_ in cmp.items():
            add(f"r={r_s} certificates.csv {k_} equals port endpoint string", row[k_] == v_, f"csv={row[k_]} port={v_}")
        add(f"r={r_s} certificates.csv mesh/digits/accepted", row["mesh_intervals"] == "200" and row["interval_digits"] == "50" and row["accepted"] == "true")
        # --- compare with the seed JSON (fresh run) ------------------------------------------
        def seed_lohi(fld):
            return parse_iv_string(seed_res[fld]["interval"])
        for fld, val in (("FOC_at_left", psi_l), ("FOC_at_right", psi_r), ("high_global_derivative_lower", V["Gamma_H"]), ("derivative_Lipschitz_bound", V["L_U"]),
                         ("pooling_margin", V["pooling_margin"]), ("low_cost_margin", V["low_cost_margin"]), ("high_cost_prior_margin", V["high_prior_margin"]),
                         ("entry", V["E"]), ("low_trader_payoff", V["U_low"]), ("high_trader_payoff", V["U_high"])):
            slo, shi = seed_lohi(fld)
            plo, phi = (Decimal(x) for x in iv_endpoints(val))
            same = abs(slo - plo) < Decimal("1e-45") and abs(shi - phi) < Decimal("1e-45")
            add(f"r={r_s} port vs seed {fld} (full endpoints, 1e-45)", same, f"seed=[{slo},{shi}] port=[{plo},{phi}]")
        # --- independent non-interval diagnostics ---------------------------------------------
        Up_l = indep_objects(r_s, vl_s, vl_s, -1)[0]
        Up_r = indep_objects(r_s, vr_s, vr_s, -1)[0]
        def near(val, ivl, tol=Decimal("1e-22")):
            lo_, hi_ = (Decimal(x) for x in iv_endpoints(ivl))
            d = Decimal(mp.nstr(val, 40))
            return max(lo_ - d, d - hi_, Decimal(0)) <= tol, max(lo_ - d, d - hi_, Decimal(0))
        ok_l, d_l = near(Up_l, psi_l)
        ok_r, d_r = near(Up_r, psi_r)
        add(f"r={r_s} independent 30-digit quadrature: Psi(v_-) > 0 and within 1e-22 of the port enclosure", Up_l > 0 and ok_l,
            f"Psi(v_-)={mp.nstr(Up_l, 20)}, distance to enclosure {d_l:.1e}")
        add(f"r={r_s} independent 30-digit quadrature: Psi(v_+) < 0 and within 1e-22 of the port enclosure", Up_r < 0 and ok_r,
            f"Psi(v_+)={mp.nstr(Up_r, 20)}, distance to enclosure {d_r:.1e}")
        # high-type derivative on the declared mesh at v_-, mid, v_+
        vmid = str((Decimal(vl_s) + Decimal(vr_s)) / 2)
        mesh_min = mp.mpf(1)
        argmin = None
        for v_s in (vl_s, vmid, vr_s):
            for j in range(0, n + 1):
                s_val = mp.mpf(j) / n
                up = indep_objects(r_s, v_s, s_val, 1, dps=20)[0]
                if up < mesh_min:
                    mesh_min, argmin = up, (v_s, j)
        mesh_min_lower = Decimal(C.endpoint_str(V["mesh_min_lower"], "lower")) if hasattr(V["mesh_min_lower"], "a") else Decimal(str(V["mesh_min_lower"]))
        add(f"r={r_s} independent quadrature: min_j U_H'(s_j) over v in {{v_-, mid, v_+}} >= port mesh minimum lower endpoint",
            Decimal(mp.nstr(mesh_min, 25)) >= mesh_min_lower - Decimal("1e-15"), f"independent min {mp.nstr(mesh_min, 15)} at (v, j)={argmin}; port lower {mesh_min_lower}")
        add(f"r={r_s} independent quadrature: min_j U_H'(s_j) - L_U/(2n) > 0",
            mesh_min - mp.mpf(iv_endpoints(V["L_U"])[1]) / (2 * n) > 0)
        # entry at v_-, mid, v_+ inside the port enclosure
        E_vals = [indep_objects(r_s, v_s, v_s, -1)[2] for v_s in (vl_s, vmid, vr_s)]
        add(f"r={r_s} independent entry E(v) at v_-, mid, v_+ inside the port enclosure",
            all(Decimal(E_lo) <= Decimal(mp.nstr(Ev, 40)) <= Decimal(E_hi) for Ev in E_vals), f"E={[mp.nstr(Ev, 15) for Ev in E_vals]}; enclosure [{E_lo}, {E_hi}]")
        # --- T17 display rounding ---------------------------------------------------------------
        letter = node_letters[r_s]
        disp = reg[f"cert_{letter}_entry_interval"]["display"]
        dlo, dhi = parse_iv_string(disp.replace("\\,", ""))
        add(f"T17 r={r_s} registry entry display lower is floor(E_lower, 10 dp)", dlo == Decimal(E_lo).quantize(Decimal("1e-10"), rounding=ROUND_FLOOR) and dlo <= Decimal(E_lo), f"{dlo} vs {E_lo}")
        add(f"T17 r={r_s} registry entry display upper is ceil(E_upper, 10 dp)", dhi == Decimal(E_hi).quantize(Decimal("1e-10"), rounding=ROUND_CEILING) and dhi >= Decimal(E_hi), f"{dhi} vs {E_hi}")
        add(f"T17 r={r_s} registry entry lower/upper columns equal port endpoints", reg[f"cert_{letter}_entry_interval"]["lower"] == E_lo and reg[f"cert_{letter}_entry_interval"]["upper"] == E_hi)
        vdisp = reg[f"cert_{letter}_v_interval"]["display"].replace("\\,", "")
        add(f"T17 r={r_s} registry v display equals the exact declared bracket", parse_iv_string(vdisp) == (Decimal(vl_s), Decimal(vr_s)), vdisp)
        gdisp = Decimal(reg[f"cert_{letter}_high_derivative_lower"]["display"])
        glo = Decimal(iv_endpoints(V["Gamma_H"])[0])
        add(f"T17 r={r_s} registry Gamma_H display is floor(lower, 10 dp)", gdisp == glo.quantize(Decimal("1e-10"), rounding=ROUND_FLOOR) and gdisp <= glo, f"{gdisp} vs {glo}")
        pl = Decimal(reg[f"cert_{letter}_psi_left_lower"]["display"])
        pr = Decimal(reg[f"cert_{letter}_psi_right_upper"]["display"])
        add(f"T17 r={r_s} registry Psi_left display rounds the lower endpoint down (12 dp) and stays positive",
            pl == Decimal(iv_endpoints(psi_l)[0]).quantize(Decimal("1e-12"), rounding=ROUND_FLOOR) and pl > 0, f"{pl}")
        add(f"T17 r={r_s} registry Psi_right display rounds the upper endpoint up (12 dp) and stays negative",
            pr == Decimal(iv_endpoints(psi_r)[1]).quantize(Decimal("1e-12"), rounding=ROUND_CEILING) and pr < 0, f"{pr}")
        # manuscript text
        line = f"{r_s}&[{vl_s},\\,{vr_s}]&[{dlo},\\,{dhi}]"
        add(f"T17 r={r_s} main_filled.md table row shows the exact bracket and the outward entry display", line in main_filled, line)
        add(f"T17 r={r_s} main_filled.md shows the Gamma_H display", str(gdisp) in main_filled)
        add(f"T17 r={r_s} main_filled.md shows the Psi displays", format(pl, "f") in main_filled and format(pr, "f") in main_filled, f"{format(pl,'f')} / {format(pr,'f')}")
    # [8] ordering of entry enclosures across nodes
    if len(port_E) == 3:
        Es = [iv_endpoints(port_E[r]) for r in ("1.55", "1.60", "1.65")]
        ordered = Decimal(Es[0][1]) < Decimal(Es[1][0]) and Decimal(Es[1][1]) < Decimal(Es[2][0])
        add("[8] entry enclosures strictly ordered and non-overlapping across the three nodes", ordered, str(Es))
        # displayed intervals also ordered
        disp = [parse_iv_string(reg[f"cert_{l}_entry_interval"]["display"].replace("\\,", "")) for l in "abc"]
        add("[8] displayed entry intervals strictly ordered and non-overlapping", disp[0][1] < disp[1][0] and disp[1][1] < disp[2][0], str(disp))
        add("[8] port entry enclosures reproduce the seed's ordering assertion", all(seed_new["results"][i]["entry"]["upper_display"] < seed_new["results"][i + 1]["entry"]["lower_display"] for i in range(2)))
    report["elapsed_seconds"] = time.time() - t0
    nfail = sum(c["status"] == "FAIL" for c in checks)
    report["summary"] = {"checks": len(checks), "fail": nfail}
    OUT_JSON.write_text(json.dumps(report, indent=1, default=str))
    # markdown
    lines = ["# S1-D interval certificates (T16, T17)", "", f"Generated {report['generated']}; Python {report['environment']['python']}, mpmath {mp.__version__} "
             f"(preserved seed result: mpmath {report['seed_versions']['preserved']}, {report['seed_versions']['digits'][0]} digits).", "",
             f"Seed copy sha256 {sha(seed_copy)} (identical before and after the run; run under `run_seed.sh`, which refuses PYTHONOPTIMIZE and -O).", "",
             f"{len(checks)} checks, {nfail} failures.", ""]
    for r_s, node in report["nodes"].items():
        lines.append(f"## r = {r_s}, v in [{node['bracket'][0]}, {node['bracket'][1]}]")
        lines.append("")
        lines.append("| attempt | digits | mesh | accepted | failures |")
        lines.append("|---|---:|---:|---|---|")
        for i, a in enumerate(node["attempts"]):
            lines.append(f"| {i+1} | {a['digits']} | {a['mesh_intervals']} | {a['accepted']} | {'; '.join(a['failures']) or '-'} |")
        acc = next((a for a in node["attempts"] if a["accepted"]), None)
        if acc:
            v = acc["values"]
            lines += ["", f"- Psi(v_-) in [{v['Psi_left'][0][:30]}..., {v['Psi_left'][1][:30]}...]",
                      f"- Psi(v_+) in [{v['Psi_right'][0][:30]}..., {v['Psi_right'][1][:30]}...]",
                      f"- Gamma_H lower {v['Gamma_H'][0][:25]}...; L_U upper {v['L_U'][1][:20]}...",
                      f"- E in [{v['E'][0][:22]}..., {v['E'][1][:22]}...]", f"- pooling margin lower {v['pooling_margin'][0][:20]}..."]
        lines.append("")
    lines += ["## Checks", "", "| status | check | note |", "|---|---|---|"]
    for c in checks:
        lines.append(f"| {c['status']} | {c['check']} | {str(c['note'])[:160].replace('|', '/')} |")
    OUT_MD.write_text("\n".join(lines) + "\n")
    print(json.dumps(report["summary"]), f"elapsed {report['elapsed_seconds']:.0f}s")
    for c in checks:
        if c["status"] == "FAIL":
            print("FAIL", c["check"], c["note"])
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
