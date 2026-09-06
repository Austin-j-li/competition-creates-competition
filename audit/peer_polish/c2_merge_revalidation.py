"""Replay the bounded C.2 interior-root revalidation against the preserved full run.

Run after the full producer and the 23-node command recorded in logs/s3_c2_revision.md.
The script refuses changed input hashes or a newly required refinement node.
"""
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from numerics.exercises.c2_correspondence import OUTPUT_NAMES, strength_grid
from numerics.io import sha256, write_csv

BASE = ROOT / 'audit/peer_polish/c2_full_before_interior_polish'
PATCH = ROOT / 'audit/peer_polish/c2_interior_polish'


def read(path):
    with path.open() as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def main():
    base = json.loads((BASE / 'c2_correspondence.json').read_text())
    patch = json.loads((PATCH / 'c2_correspondence.json').read_text())
    if not base['passed'] or not patch['passed']:
        raise ValueError('Both runs must pass before merging')
    for directory, manifest in ((BASE, base), (PATCH, patch)):
        for name, digest in manifest['outputs'].items():
            if sha256(directory / Path(name).name) != digest:
                raise ValueError(f'Changed input: {directory / Path(name).name}')
    changed = set(patch['inputs']['nodes'])
    merged = {}
    for name in OUTPUT_NAMES.values():
        columns, old = read(BASE / name)
        new_columns, new = read(PATCH / name)
        if columns != new_columns:
            raise ValueError(f'Schema changed: {name}')
        if 'r' in columns and name != 'certificates.csv':
            rows = [r for r in old if r['r'] not in changed] + new
            if name == 'mixed_supports.csv':
                key = lambda r: (Decimal(r['r']), r['branch'], r['init_id'], r['state'], int(r['support_index']))
            elif name == 'mixed_search_attempts.csv':
                key = lambda r: (Decimal(r['r']), float(r['mesh']), r['start_id'])
            else:
                key = lambda r: (Decimal(r['r']), r['branch'], r['candidate_id'])
            rows.sort(key=key)
        else:
            if old != new:
                raise ValueError(f'Unchanged core output differs: {name}')
            rows = old
        merged[name] = columns, rows
    attempts = merged['correspondence_attempts.csv'][1]
    distinct = merged['correspondence.csv'][1]
    mixed = merged['mixed_search_attempts.csv'][1]
    grid = strength_grid()
    accepted = lambda rs: {r['branch'] for r in distinct if r['r'] == rs and r['accepted'] == 'true'}
    pairs = [(a, b) for a, b in zip(grid[:-1], grid[1:]) if accepted(a) != accepted(b) and Decimal(b) - Decimal(a) > Decimal('.001')]
    expected = set(grid)
    for a, b in pairs:
        x = Decimal(a) + Decimal('.001')
        while x < Decimal(b):
            expected.add(str(x.normalize()))
            x += Decimal('.001')
    nodes = {r['r'] for r in distinct}
    if nodes != expected:
        raise ValueError(f'Refinement changed: missing={expected - nodes}, surplus={nodes - expected}')
    for rs in nodes:
        rows = [r for r in distinct if r['r'] == rs]
        n = sum(r['accepted'] == 'true' for r in rows)
        if any(int(r['n_distinct_accepted']) != n or (r['multiplicity_found'] == 'true') != (n >= 2) for r in rows):
            raise ValueError(f'Wrong multiplicity at {rs}')
    budget_fail = [r for r in attempts if r['error_budget_breaches'] not in ('', 'n/a')]
    if any(r['accepted'] == 'true' for r in budget_fail):
        raise ValueError('Accepted row breached its error budget')
    c = base['checks']['correspondence']
    c.update(nodes=len(nodes), refined_nodes=len(nodes - set(grid)), refinement_pairs=pairs,
             attempt_rows=len(attempts), distinct_rows=len(distinct), duplicate_attempts=len(attempts) - len(distinct),
             open_rows=sum(r['result_status'] == 'open' for r in distinct),
             open_rows_by_branch={b: sum(r['branch'] == b and r['result_status'] == 'open' for r in distinct) for b in sorted({r['branch'] for r in distinct})},
             no_candidate_rows=sum(r['result_status'] == 'no candidate' for r in distinct),
             rejected_rows=sum(r['result_status'] == 'rejected' for r in distinct),
             nodes_with_multiplicity=len({r['r'] for r in distinct if r['multiplicity_found'] == 'true'}),
             asymmetric_accepted_nodes=sorted({r['r'] for r in distinct if r['branch'] == 'asymmetric' and r['accepted'] == 'true'}, key=Decimal),
             accepted_branch_labels=sorted({r['branch'] for r in distinct if r['accepted'] == 'true'}),
             error_budget_breached_rows=len(budget_fail),
             mixed_attempt_outcomes={k: sum(r['outcome'] == k for r in mixed) for k in ('converged-candidate', 'converged-pure', 'unresolved')},
             mixed_nodes_unresolved=sorted({r['r'] for r in mixed if r['outcome'] == 'unresolved'}, key=Decimal),
             mixed_candidates_accepted=sum(r['branch'] == 'mixed' and r['accepted'] == 'true' for r in distinct))
    base['checks']['error_budget']['breached_candidates'] = [r['candidate_id'] for r in budget_fail]
    base['validation_replay'] = {'method': 'Full producer plus all 23 interior-pure nodes rerun after direct FOC polishing; unaffected node records retained byte-for-byte.',
                                 'nodes': sorted(changed, key=Decimal), 'baseline_manifest': str(BASE.relative_to(ROOT) / 'c2_correspondence.json'),
                                 'patch_manifest': str(PATCH.relative_to(ROOT) / 'c2_correspondence.json'),
                                 'baseline_hash': sha256(BASE / 'c2_correspondence.json'), 'patch_hash': sha256(PATCH / 'c2_correspondence.json'),
                                 'script': str(Path(__file__).resolve().relative_to(ROOT)),
                                 'additional_runtime_seconds': patch['inputs']['runtime_seconds']}
    base['notes'].append('Interior pure fixed points are polished by the two held-schedule first-order conditions, then revalidated. A bounded 23-node replay removed a numerical duplicate at r=1.79; no identity or acceptance tolerance changed.')
    for name, (columns, rows) in merged.items():
        write_csv(ROOT / 'numerics' / name, columns, rows)
    base['outputs'] = {f'numerics/{name}': sha256(ROOT / 'numerics' / name) for name in OUTPUT_NAMES.values()}
    base['timestamp_utc'] = patch['timestamp_utc']
    source_paths = json.loads((ROOT / 'audit/peer_polish/c2_full_source_snapshot.json').read_text())['sources']
    base['validated_source_hashes'] = {p: sha256(p) for p in source_paths}
    (ROOT / 'numerics/manifests/c2_correspondence.json').write_text(json.dumps(base, indent=1) + '\n')
    print('C.2 merged replay passed:', c)


if __name__ == '__main__':
    main()
