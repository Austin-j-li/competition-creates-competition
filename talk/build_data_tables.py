#!/usr/bin/env python3
"""Bind B10/B11 master cells to semantic registry rows; print the full display ledger.

Run: python3 build_data_tables.py
Sources: master dumps slide40–46 (B10 and B11 by show position in the 20-page master; number ids keep the older names b39 to b45), presentation/content.js frames b10, b11, b11s,
b11f, b11b, b11c, b11d; handout/slot_data.py declarations. No equilibrium search.
"""
from pathlib import Path
from fractions import Fraction
import csv
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REGISTRY = ROOT / 'audit/slot_manuscript_2026_10_23/registry/registry.csv'
DUMPS = HERE / "master_dump"
# One spec per printed value; locations retain cell meaning even when values coincide.
SPECS = [{'id': 'tables.b45.t46.r0.c2.n1', 'key': 'prim_r1', 'digits': 0, 'where': '46.t46.r0.c2'},
{'id': 'tables.b44.t45.r0.c2.n1', 'key': 'prim_r1', 'digits': 0, 'where': '45.t45.r0.c2'},
{'id': 'tables.b40.t41.r0.c2.n1', 'key': 'prim_r1', 'digits': 0, 'where': '41.t41.r0.c2'},
{'id': 'tables.b39.t40.r1.c1.n1', 'key': 'prim_h', 'digits': 0, 'where': '40.t40.r1.c1'},
 {'id': 'tables.b39.t40.r1.c1.n2', 'key': 'prim_ell', 'digits': 0, 'where': '40.t40.r1.c1'},
 {'id': 'tables.b39.t40.r4.c1.n1', 'key': 'prim_cH', 'digits': 0, 'where': '40.t40.r4.c1'},
 {'id': 'tables.b39.t40.r5.c1.n1', 'key': 'beta_B', 'digits': 6, 'where': '40.t40.r5.c1'},
 {'id': 'tables.b39.t40.r5.c1.n2', 'key': 'lambda_B', 'digits': 6, 'where': '40.t40.r5.c1'},
 {'id': 'tables.b39.t40.r6.c1.n1', 'key': 'u_B', 'digits': 6, 'where': '40.t40.r6.c1'},
 {'id': 'tables.b39.t40.r6.c1.n2', 'key': 'b_B', 'digits': 6, 'where': '40.t40.r6.c1'},
 {'id': 'tables.b39.t40.r7.c1.n1', 'key': 'prim_r1', 'digits': 0, 'where': '40.t40.r7.c1'},
 {'id': 'tables.b39.t79.r1.c1.n1', 'key': 'u_lo', 'digits': 6, 'where': '40.t79.r1.c1'},
 {'id': 'tables.b39.t79.r1.c1.n2', 'key': 'u_hi', 'digits': 6, 'where': '40.t79.r1.c1'},
 {'id': 'tables.b39.t79.r1.c2.n1', 'key': 'u_B', 'digits': 6, 'where': '40.t79.r1.c2'},
 {'id': 'tables.b39.t79.r2.c1.n1', 'key': 'M_lo', 'digits': 6, 'where': '40.t79.r2.c1'},
 {'id': 'tables.b39.t79.r2.c1.n2', 'key': 'M_hi', 'digits': 6, 'where': '40.t79.r2.c1'},
 {'id': 'tables.b39.t79.r2.c2.n1', 'key': 'M_half_B', 'digits': 6, 'where': '40.t79.r2.c2'},
 {'id': 'tables.b39.t79.r3.c2.n1', 'key': 'beta_B', 'digits': 6, 'where': '40.t79.r3.c2'},
 {'id': 'tables.b39.t79.r4.c2.n1', 'key': 'lambda_B', 'digits': 6, 'where': '40.t79.r4.c2'},
 {'id': 'tables.b39.t79.r5.c1.n1', 'key': 'prior_lo_B', 'digits': 6, 'where': '40.t79.r5.c1'},
 {'id': 'tables.b39.t79.r5.c1.n2', 'key': 'prior_hi_B', 'digits': 6, 'where': '40.t79.r5.c1'},
 {'id': 'tables.b39.t79.r6.c1.n1', 'key': 'res_a_lo', 'digits': 6, 'where': '40.t79.r6.c1'},
 {'id': 'tables.b39.t79.r6.c1.n2', 'key': 'res_a_up', 'digits': 6, 'where': '40.t79.r6.c1'},
 {'id': 'tables.b39.t79.r7.c1.n1', 'key': 'res_cap_lo', 'digits': 6, 'where': '40.t79.r7.c1'},
 {'id': 'tables.b39.t79.r7.c1.n2', 'key': 'res_cap_hi', 'digits': 6, 'where': '40.t79.r7.c1'},
 {'id': 'tables.b39.t79.r7.c2.n1', 'key': 'res_cap', 'digits': 6, 'where': '40.t79.r7.c2'},
 {'id': 'tables.b40.t41.r1.c1.n1', 'key': 'Bprior_r0', 'digits': 6, 'where': '41.t41.r1.c1'},
 {'id': 'tables.b40.t41.r1.c2.n1', 'key': 'Bprior_r1_B', 'digits': 6, 'where': '41.t41.r1.c2'},
 {'id': 'tables.b40.t41.r1.c3.n1', 'key': 'Bprior_r2', 'digits': 6, 'where': '41.t41.r1.c3'},
 {'id': 'tables.b40.t41.r2.c1.n1', 'key': 'Delta_r0', 'digits': 6, 'where': '41.t41.r2.c1'},
 {'id': 'tables.b40.t41.r2.c2.n1', 'key': 'Delta_r1', 'digits': 6, 'where': '41.t41.r2.c2'},
 {'id': 'tables.b40.t41.r2.c3.n1', 'key': 'Delta_r2', 'digits': 6, 'where': '41.t41.r2.c3'},
 {'id': 'tables.b40.t41.r5.c1.n1', 'key': 'entry_r0', 'digits': 6, 'where': '41.t41.r5.c1'},
 {'id': 'tables.b40.t41.r5.c2.n1', 'key': 'entry_r1_B', 'digits': 6, 'where': '41.t41.r5.c2'},
 {'id': 'tables.b40.t41.r5.c3.n1', 'key': 'entry_r2', 'digits': 6, 'where': '41.t41.r5.c3'},
 {'id': 'tables.b40.t41.r6.c1.n1', 'key': 'own_r0', 'digits': 6, 'where': '41.t41.r6.c1'},
 {'id': 'tables.b40.t41.r6.c2.n1', 'key': 'own_r1_B', 'digits': 6, 'where': '41.t41.r6.c2'},
 {'id': 'tables.b40.t41.r6.c3.n1', 'key': 'own_r2_B', 'digits': 6, 'where': '41.t41.r6.c3'},
 {'id': 'tables.b41.t42.r1.c1.n1', 'key': 'entry_r0', 'digits': 6, 'where': '42.t42.r1.c1'},
 {'id': 'tables.b41.t42.r1.c2.n1', 'key': 'entry_r1_B', 'digits': 6, 'where': '42.t42.r1.c2'},
 {'id': 'tables.b41.t42.r2.c1.n1', 'key': 'p4_frozen_r0_entry', 'digits': 6, 'where': '42.t42.r2.c1'},
 {'id': 'tables.b41.t42.r2.c2.n1', 'key': 'p4_frozen_r1_entry', 'digits': 6, 'where': '42.t42.r2.c2'},
 {'id': 'tables.b41.t42.r3.c1.n1', 'key': 'p4_hidden_r0_entry', 'digits': 6, 'where': '42.t42.r3.c1'},
 {'id': 'tables.b41.t42.r3.c2.n1', 'key': 'p4_hidden_r1_entry', 'digits': 6, 'where': '42.t42.r3.c2'},
 {'id': 'tables.b43.s23.n1', 'key': 'share_H_r0', 'digits': 6, 'where': '44.s23'},
 {'id': 'tables.b43.s23.n2', 'key': 'share_H_r1_B', 'digits': 6, 'where': '44.s23'},
 {'id': 'tables.b44.t45.r1.c1.n1', 'key': 'p2_base_r0_t0', 'digits': 6, 'where': '45.t45.r1.c1'},
 {'id': 'tables.b44.t45.r1.c2.n1', 'key': 'p2_base_r1_t0', 'digits': 6, 'where': '45.t45.r1.c2'},
 {'id': 'tables.b44.t45.r1.c3.n1', 'key': 'p2_base_r2_t0', 'digits': 6, 'where': '45.t45.r1.c3'},
 {'id': 'tables.b44.t45.r2.c1.n1', 'key': 'p2_base_r0_th', 'digits': 6, 'where': '45.t45.r2.c1'},
 {'id': 'tables.b44.t45.r2.c2.n1', 'key': 'p2_base_r1_th', 'digits': 6, 'where': '45.t45.r2.c2'},
 {'id': 'tables.b44.t45.r2.c3.n1', 'key': 'p2_base_r2_th', 'digits': 6, 'where': '45.t45.r2.c3'},
 {'id': 'tables.b44.t45.r3.c1.n1', 'key': 'p2_base_r0_tl', 'digits': 6, 'where': '45.t45.r3.c1'},
 {'id': 'tables.b44.t45.r3.c2.n1', 'key': 'p2_base_r1_tl', 'digits': 6, 'where': '45.t45.r3.c2'},
 {'id': 'tables.b44.t45.r3.c3.n1', 'key': 'p2_base_r2_tl', 'digits': 6, 'where': '45.t45.r3.c3'},
 {'id': 'tables.b44.t45.r4.c1.n1', 'key': 'Delta_r0', 'digits': 6, 'where': '45.t45.r4.c1'},
 {'id': 'tables.b44.t45.r4.c2.n1', 'key': 'Delta_r1', 'digits': 6, 'where': '45.t45.r4.c2'},
 {'id': 'tables.b44.t45.r4.c3.n1', 'key': 'Delta_r2', 'digits': 6, 'where': '45.t45.r4.c3'},
 {'id': 'tables.b44.t45.r5.c1.n1', 'key': 'p2_base_r0_gh', 'digits': 6, 'where': '45.t45.r5.c1'},
 {'id': 'tables.b44.t45.r5.c2.n1', 'key': 'p2_base_r1_gh', 'digits': 6, 'where': '45.t45.r5.c2'},
 {'id': 'tables.b44.t45.r5.c3.n1', 'key': 'p2_base_r2_gh', 'digits': 6, 'where': '45.t45.r5.c3'},
 {'id': 'tables.b44.t45.r6.c1.n1', 'key': 'p2_base_r0_gl', 'digits': 6, 'where': '45.t45.r6.c1'},
 {'id': 'tables.b44.t45.r6.c2.n1', 'key': 'p2_base_r1_gl', 'digits': 6, 'where': '45.t45.r6.c2'},
 {'id': 'tables.b44.t45.r6.c3.n1', 'key': 'p2_base_r2_gl', 'digits': 6, 'where': '45.t45.r6.c3'},
 {'id': 'tables.b44.t45.r7.c1.n1', 'key': 'Bprior_r0', 'digits': 6, 'where': '45.t45.r7.c1'},
 {'id': 'tables.b44.t45.r7.c2.n1', 'key': 'Bprior_r1_B', 'digits': 6, 'where': '45.t45.r7.c2'},
 {'id': 'tables.b44.t45.r7.c3.n1', 'key': 'Bprior_r2', 'digits': 6, 'where': '45.t45.r7.c3'},
 {'id': 'tables.b44.t45.r8.c1.n1', 'key': 'tau_r0', 'digits': 6, 'where': '45.t45.r8.c1'},
 {'id': 'tables.b44.t45.r8.c2.n1', 'key': 'tau_r1', 'digits': 6, 'where': '45.t45.r8.c2'},
 {'id': 'tables.b44.t45.r8.c3.n1', 'key': 'tau_r2', 'digits': 6, 'where': '45.t45.r8.c3'},
 {'id': 'tables.b44.s7.l1.n1', 'key': 'entry_r1_B', 'digits': 6, 'where': '45.s7.l1'},
 {'id': 'tables.b44.s7.l1.n2', 'key': 'own_r1_B', 'digits': 6, 'where': '45.s7.l1'},
 {'id': 'tables.b44.s7.l2.n1', 'key': 'entry_r0', 'digits': 6, 'where': '45.s7.l2'},
 {'id': 'tables.b44.s7.l2.n2', 'key': 'own_r0', 'digits': 6, 'where': '45.s7.l2'},
 {'id': 'tables.b44.s7.l3.n1', 'key': 'entry_r2', 'digits': 6, 'where': '45.s7.l3'},
 {'id': 'tables.b44.s7.l3.n2', 'key': 'own_r2_B', 'digits': 6, 'where': '45.s7.l3'},
 {'id': 'tables.b44.s7.l4.n1', 'key': 'Bprior_r0', 'digits': 6, 'where': '45.s7.l4'},
 {'id': 'tables.b44.s7.l4.n2', 'key': 'Bprior_r1_B', 'digits': 6, 'where': '45.s7.l4'},
 {'id': 'tables.b44.s7.l4.n3', 'key': 'Bprior_r2', 'digits': 6, 'where': '45.s7.l4'},
 {'id': 'tables.b45.t46.r3.c1.n1', 'key': 'p2_base_r0_mu_minus', 'digits': 6, 'where': '46.t46.r3.c1'},
 {'id': 'tables.b45.t46.r3.c2.n1', 'key': 'p2_base_r1_mu_minus', 'digits': 6, 'where': '46.t46.r3.c2'},
 {'id': 'tables.b45.t46.r3.c3.n1', 'key': 'p2_base_r2_mu_minus', 'digits': 6, 'where': '46.t46.r3.c3'},
 {'id': 'tables.b45.t46.r4.c1.n1', 'key': 'p2_base_r0_mu_zero', 'digits': 6, 'where': '46.t46.r4.c1'},
 {'id': 'tables.b45.t46.r4.c2.n1', 'key': 'p2_base_r1_mu_zero', 'digits': 6, 'where': '46.t46.r4.c2'},
 {'id': 'tables.b45.t46.r4.c3.n1', 'key': 'p2_base_r2_mu_zero', 'digits': 6, 'where': '46.t46.r4.c3'},
 {'id': 'tables.b45.t46.r5.c1.n1', 'key': 'p2_base_r0_mu_plus', 'digits': 6, 'where': '46.t46.r5.c1'},
 {'id': 'tables.b45.t46.r5.c2.n1', 'key': 'p2_base_r1_mu_plus', 'digits': 6, 'where': '46.t46.r5.c2'},
 {'id': 'tables.b45.t46.r5.c3.n1', 'key': 'p2_base_r2_mu_plus', 'digits': 6, 'where': '46.t46.r5.c3'},
 {'id': 'tables.b45.t46.r7.c1.n1', 'key': 'price_r0', 'digits': 6, 'where': '46.t46.r7.c1'},
 {'id': 'tables.b45.t46.r7.c2.n1', 'key': 'price_r1_m1_B', 'digits': 6, 'where': '46.t46.r7.c2'},
 {'id': 'tables.b45.t46.r7.c3.n1', 'key': 'price_r2_m1_B', 'digits': 6, 'where': '46.t46.r7.c3'},
 {'id': 'tables.b45.t46.r8.c1.n1', 'key': 'price_r0', 'digits': 6, 'where': '46.t46.r8.c1'},
 {'id': 'tables.b45.t46.r8.c2.n1', 'key': 'price_r1_0_B', 'digits': 6, 'where': '46.t46.r8.c2'},
 {'id': 'tables.b45.t46.r8.c3.n1', 'key': 'price_r2_0_B', 'digits': 6, 'where': '46.t46.r8.c3'},
 {'id': 'tables.b45.t46.r9.c1.n1', 'key': 'price_r0', 'digits': 6, 'where': '46.t46.r9.c1'},
 {'id': 'tables.b45.t46.r9.c2.n1', 'key': 'price_r1_p1_B', 'digits': 6, 'where': '46.t46.r9.c2'},
 {'id': 'tables.b45.t46.r9.c3.n1', 'key': 'price_r2_p1_B', 'digits': 6, 'where': '46.t46.r9.c3'},
 {'id': 'tables.b45.t46.r10.c1.n1', 'key': 'entry_r0', 'digits': 6, 'where': '46.t46.r10.c1'},
 {'id': 'tables.b45.t46.r10.c2.n1', 'key': 'entry_r1_B', 'digits': 6, 'where': '46.t46.r10.c2'},
 {'id': 'tables.b45.t46.r10.c3.n1', 'key': 'entry_r2', 'digits': 6, 'where': '46.t46.r10.c3'},
 {'id': 'tables.b45.t46.r11.c1.n1', 'key': 'own_r0', 'digits': 6, 'where': '46.t46.r11.c1'},
 {'id': 'tables.b45.t46.r11.c2.n1', 'key': 'own_r1_B', 'digits': 6, 'where': '46.t46.r11.c2'},
 {'id': 'tables.b45.t46.r11.c3.n1', 'key': 'own_r2_B', 'digits': 6, 'where': '46.t46.r11.c3'},
 {'id': 'tables.b45.t46.r12.c1.n1', 'key': 'p4_base_r0_proceeds', 'digits': 6, 'where': '46.t46.r12.c1'},
 {'id': 'tables.b45.t46.r12.c2.n1', 'key': 'p4_base_r1_proceeds', 'digits': 6, 'where': '46.t46.r12.c2'},
 {'id': 'tables.b45.t46.r12.c3.n1', 'key': 'p4_base_r2_proceeds', 'digits': 6, 'where': '46.t46.r12.c3'},
 {'id': 'tables.b45.t46.r14.c1.n1', 'key': 'p4_frozen_r0_entry', 'digits': 6, 'where': '46.t46.r14.c1'},
 {'id': 'tables.b45.t46.r14.c2.n1', 'key': 'p4_frozen_r1_entry', 'digits': 6, 'where': '46.t46.r14.c2'},
 {'id': 'tables.b45.t46.r15.c1.n1', 'key': 'p4_frozen_r0_own', 'digits': 6, 'where': '46.t46.r15.c1'},
 {'id': 'tables.b45.t46.r15.c2.n1', 'key': 'p4_frozen_r1_own', 'digits': 6, 'where': '46.t46.r15.c2'},
 {'id': 'tables.b45.t46.r16.c1.n1', 'key': 'p4_frozen_r0_proceeds', 'digits': 6, 'where': '46.t46.r16.c1'},
 {'id': 'tables.b45.t46.r16.c2.n1', 'key': 'p4_frozen_r1_proceeds', 'digits': 6, 'where': '46.t46.r16.c2'},
 {'id': 'tables.b45.t46.r19.c1.n1', 'key': 'p4_hidden_r0_entry', 'digits': 6, 'where': '46.t46.r19.c1'},
 {'id': 'tables.b45.t46.r19.c2.n1', 'key': 'p4_hidden_r1_entry', 'digits': 6, 'where': '46.t46.r19.c2'},
 {'id': 'tables.b45.t46.r20.c1.n1', 'key': 'p4_hidden_r0_own', 'digits': 6, 'where': '46.t46.r20.c1'},
 {'id': 'tables.b45.t46.r20.c2.n1', 'key': 'p4_hidden_r1_own', 'digits': 6, 'where': '46.t46.r20.c2'},
 {'id': 'tables.b45.t46.r21.c1.n1', 'key': 'p4_hidden_r0_proceeds', 'digits': 6, 'where': '46.t46.r21.c1'},
 {'id': 'tables.b45.t46.r21.c2.n1', 'key': 'p4_hidden_r1_proceeds', 'digits': 6, 'where': '46.t46.r21.c2'}]


def master_at(where: str, occurrence: int) -> str:
    page, obj, *rest = where.split('.')
    kind, ident = obj[0], int(obj[1:])
    current = False
    row = None
    lines = []
    for line in (DUMPS / f'slide{page}.txt').read_text().splitlines():
        start = re.match(r"(TABLE|SHAPE) id=(\d+)", line)
        if start:
            current = start[1] == ('TABLE' if kind == 't' else 'SHAPE') and int(start[2]) == ident
        elif current:
            if kind == 't':
                r = re.match(r'    ROW (\d+)', line)
                if r: row = int(r[1])
                c = re.match(r'      CELL c(\d+).*?: (.*)', line)
                if c and row == int(rest[0][1:]) and int(c[1]) == int(rest[1][1:]): lines.append(c[2])
            elif line.strip().startswith('|'): lines.append(line)
    if kind == 's' and rest: lines = [lines[int(rest[0][1:])]]
    raw = ' '.join(lines)
    # Extract visible text/math only: formatting sizes and colour codes are not content.
    visible = ''.join(m[2] if m[2] else m[1] for m in re.findall(r'\[([^\]]*)\]\{([^}]*)\}|\$([^$]*)\$', raw))
    pattern = r'\d+\.\d+'
    if where in {'40.t40.r1.c1', '40.t40.r4.c1', '40.t40.r7.c1'}:
        pattern = r'(?<![\d/])\b(?:10|1|6|3)\b(?![/\d])|\d+\.\d+'
    if where in {'41.t41.r0.c2', '45.t45.r0.c2', '46.t46.r0.c2'}:
        pattern = r'(?<==)3'
    return re.findall(pattern, visible)[occurrence]


def half_up(value: str, digits: int) -> str:
    x = Fraction(value)
    scaled = abs(x) * 10 ** digits + Fraction(1, 2)
    n = scaled.numerator // scaled.denominator
    s = str(n).rjust(digits + 1, '0')
    return ('-' if x < 0 else '') + (s[:-digits] + '.' + s[-digits:] if digits else s)


def main() -> None:
    with REGISTRY.open(newline='') as stream:
        registry = {r['key']: r for r in csv.DictReader(stream)}
    numbers = {}
    print('| id | key | digits | registry value | printed text | master | mismatch |')
    print('|---|---|---:|---|---|---|---|')
    for spec in SPECS:
        ident, key, digits = spec['id'], spec['key'], spec['digits']
        master = master_at(spec['where'], int(ident.rsplit('n', 1)[1]) - 1)
        row = registry.get(key)
        rounded = half_up(row['value'], digits) if row else None
        mismatch = rounded != master
        text = master if mismatch else rounded
        numbers[ident] = dict(key=key, digits=digits, value=row['value'] if row else None,
                              text=text, master=master, mismatch=mismatch, where=spec['where'])
        print(f"| {ident} | {key} | {digits} | {row['value'] if row else 'missing'} | {text} | {master} | {str(mismatch).lower()} |")
    payload = {'meta': {'built_by': 'build_data_tables.py',
               'registry': str(REGISTRY.relative_to(ROOT)),
               'registry_sha256': hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
               'rounding': 'half-up on the exact Fraction; no binary float',
               'mapping': 'presentation/content.js b10, b11, b11s, b11b, b11c, b11d; handout/slot_data.py'},
               'numbers': numbers}
    (HERE / 'src/data_tables.json').write_text(json.dumps(payload, indent=2) + '\n')


if __name__ == '__main__':
    main()
