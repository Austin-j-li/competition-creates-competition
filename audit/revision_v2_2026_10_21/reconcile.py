"""Compare the committed reference with the current numerical release outputs."""
from __future__ import annotations

import csv
from collections import Counter
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = json.loads((HERE / 'baseline.json').read_text())['commit']
FIELDS = ['name', 'file', 'row_selector', 'old_value', 'new_value', 'changed', 'note']


def prior_bytes(path: str) -> bytes | None:
    result = subprocess.run(['git', 'show', f'{BASE}:{path}'], cwd=ROOT, capture_output=True)
    return result.stdout if result.returncode == 0 else None


def csv_rows(data: bytes | None) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode()))) if data else []


def current_bytes(path: str) -> bytes | None:
    file = ROOT / path
    return file.read_bytes() if file.exists() else None


def scalar(text: str) -> Decimal | None:
    try:
        result = Decimal(text)
        return result if result.is_finite() else None
    except (InvalidOperation, TypeError):
        return None


def equal(left: str, right: str) -> bool:
    lnum, rnum = scalar(left), scalar(right)
    return lnum == rnum if lnum is not None and rnum is not None else left == right


def digest(data: bytes | None) -> str:
    return hashlib.sha256(data).hexdigest() if data is not None else 'retired'


def main() -> None:
    records: list[dict[str, str]] = []

    def add(name: str, file: str, selector: str, old: str, new: str, note: str = '') -> None:
        records.append(dict(zip(FIELDS, (name, file, selector, old, new, 'no' if equal(old, new) else 'yes', note))))

    old_registry = {r['name']: r for r in csv_rows(prior_bytes('numerics/quantity_registry.csv'))}
    new_registry = {r['name']: r for r in csv_rows(current_bytes('numerics/quantity_registry.csv'))}
    for name in dict.fromkeys([*old_registry, *new_registry]):
        old, new = old_registry.get(name), new_registry.get(name)
        row = new or old
        old_value = old['value'] or f"[{old['lower']}, {old['upper']}]" if old else ''
        new_value = new['value'] or f"[{new['lower']}, {new['upper']}]" if new else 'retired'
        note = 'new' if old is None else 'retired: C.6b has no premise at zero low cost' if new is None else 'registry quantity'
        if old is None and new['exercise'] == 'C.10':
            note = 'new, round 3'
        if old and new and old['display'] == new['display'] and not equal(old_value, new_value):
            note += '; serialized value differs; displayed value is unchanged'
        add(name, row['source_file'], row['source_row'], old_value, new_value, note)

    sources = {
        'tables/auction_primitives.csv': ['parameter_set', 'r', 'p'],
        'tables/equilibrium_controls.csv': ['parameter_set', 'noise', 'cost_law', 'r', 'experiment', 'q_H', 'q_L'],
        'tables/extensions.csv': ['noise', 'cost_law', 'r_weak', 'r_strong'],
        'tables/extensions_margins.csv': ['panel', 'parameter_set', 'noise', 'cost_law'],
        'tables/matched_price.csv': ['parameter_set', 'noise', 'cost_law', 'r', 'environment'],
        'tables/reserve_comparisons.csv': ['value_law', 'epsilon_V', 'r', 'p', 'branch'],
        'numerics/feedback_comparisons.csv': ['noise', 'cost_law', 'r'],
        'numerics/two_signals.csv': ['a', 'd', 'r', 'q_plus', 'q_minus'],
        'numerics/moderate_values.csv': ['r_weak', 'r_strong'],
        'numerics/certificates.csv': ['r'],
        'numerics/thresholds.csv': ['boundary'],
        'numerics/reserve_event_ranges.csv': ['value_law', 'r', 'event_id'],
    }
    class_keys = ['case', 'h', 'ell', 'p', 'rho', 'c_L', 'c_H', 'b', 'k', 'fundamental_prior_H',
                  'noise', 'cost_law', 'value_law', 'a_L', 'b_L', 'a_H', 'b_H', 'r_0', 'r_1', 'r_2']
    sources.update({
        'numerics/class_exhibit.csv': class_keys + ['node', 'r', 'branch'],
        'numerics/class_conditions.csv': class_keys + ['condition'],
        'numerics/class_bounds.csv': class_keys + ['quantity', 'branch'],
    })

    def index_rows(rows: list[dict[str, str]], keys: list[str], path: str) -> dict[tuple, dict]:
        indexed, counts = {}, Counter()
        for number, row in enumerate(rows, 2):
            if row.get('accepted', 'true') != 'true':
                continue
            if 'event_ranges' in path and (row['event_id'] == 'grid' or row['event_id'].startswith('offset')):
                continue
            identity = tuple(row.get(key, '') for key in keys)
            ordinal = counts[identity]
            counts[identity] += 1
            indexed[(*identity, ordinal)] = {**row, '_csv_line': str(number)}
        return indexed

    for path, keys in sources.items():
        before = index_rows(csv_rows(prior_bytes(path)), keys, path)
        after = index_rows(csv_rows(current_bytes(path)), keys, path)
        for identity in sorted(set(before) | set(after)):
            old, new = before.get(identity, {}), after.get(identity, {})
            selector = '; '.join(f'{k}={v}' for k, v in zip(keys, identity))
            selector += f"; occurrence={identity[-1]}; old_line={old.get('_csv_line','absent')}; new_line={new.get('_csv_line','absent')}"
            for column in dict.fromkeys([*old, *new]):
                if column.startswith('_'):
                    continue
                left, right = old.get(column, ''), new.get(column, '')
                if scalar(left) is None and scalar(right) is None:
                    continue
                name = f"cell.{Path(path).stem}.{'.'.join(identity[:-1])}.{identity[-1]}.{column}"
                note = 'table or certificate source; revisions align on the declared scenario'
                if not old:
                    note = 'new, round 3' if path.startswith('numerics/class_') else 'new source row'
                elif not new:
                    note = 'source row no longer belongs to the declared scenario'
                elif column in ('c_L', 'zeta_L', 'low_cost_margin', 'low_cost_floor_margin'):
                    note += '; zero-cost declaration or its margin'
                add(name, path, selector + '; column=' + column, left, right, note)

    # These aggregates are the exact operations used by the exploratory table renderer.
    path = 'numerics/reserve_ranges.csv'
    old_ranges, new_ranges = csv_rows(prior_bytes(path)), csv_rows(current_bytes(path))
    for law in ('binary', 'uniform_classes'):
        for strength in ('1.2', '3'):
            summaries = []
            selectors = []
            for data in (old_ranges, new_ranges):
                sub = [r for r in data if r['value_law'] == law and r['r'] == strength]
                found = [r for r in sub if int(r['accepted_continuations_found']) and r['R_T_max_found'] != 'n/a']
                best = min(found, key=lambda r: (-Decimal(r['R_T_max_found']), Decimal(r['p'])))
                summary = {f'best_{key}': best[key] for key in ('p','accepted_continuations_found','E_min_found','E_max_found','R_T_min_found','R_T_max_found')}
                summary.update(nodes=str(len(sub)), events=str(sum(r['event_id'] not in ('','grid') and not r['event_id'].startswith('offset') for r in sub)),
                    multiple=str(sum(int(r['accepted_continuations_found']) > 1 for r in sub)),
                    unresolved=str(sum(r['search_unresolved']=='true' for r in sub)),
                    none_found=str(sum(int(r['accepted_continuations_found'])==0 for r in sub)))
                summary.update({key:str(sum(int(r[key]) for r in sub)) for key in ('candidates_evaluated','candidates_rejected','candidates_unresolved','duplicates_merged')})
                summaries.append(summary)
                selectors.append(f"p={best['p']}; event_id={best['event_id']}")
            for field in summaries[0]:
                add(f'reserve_summary.{law}.r{strength}.{field}', path,
                    f'value_law={law}; r={strength}; old_best: {selectors[0]}; new_best: {selectors[1]}; statistic={field}',
                    summaries[0][field], summaries[1][field], 'highest revenue among continuations found; no global optimum claim')

    baseline = csv_rows((HERE/'baseline_outputs.csv').read_bytes())
    paths = {r['file'] for r in baseline}
    # Include every file named by a prior or current exercise manifest.
    for entry in baseline:
        if entry['file'].startswith('numerics/manifests/'):
            paths.update(json.loads(prior_bytes(entry['file']))['outputs'])
    for manifest in (ROOT/'numerics/manifests').glob('*.json'):
        paths.add(str(manifest.relative_to(ROOT)))
        paths.update(json.loads(manifest.read_text())['outputs'])
    figure_refs = {r['file']: r for r in json.loads((HERE/'baseline_figures.json').read_text())}
    output_diff = []
    for path in sorted(paths):
        if path in figure_refs:
            reference = ROOT/figure_refs[path]['local_reference']
            old = reference.read_bytes() if reference.exists() else None
        else:
            old = prior_bytes(path)
        new = current_bytes(path)
        old_hash, new_hash = digest(old), digest(new)
        if path in figure_refs and old is None:
            old_hash = figure_refs[path]['sha256']
        note = 'file SHA-256; a changed manifest includes new provenance'
        round3_file = path.startswith('numerics/class_') or path in ('numerics/manifests/c10_classes.json', 'tables/table_class_exhibit.tex')
        detail = {'file':path, 'old_sha256':old_hash, 'new_sha256':new_hash, 'changed':old_hash != new_hash}
        if path.endswith('.csv'):
            old_rows, new_rows = csv_rows(old), csv_rows(new)
            old_fields = set().union(*(set(r) for r in old_rows)) if old_rows else set()
            new_fields = set().union(*(set(r) for r in new_rows)) if new_rows else set()
            old_count = Counter(tuple(sorted(r.items())) for r in old_rows)
            new_count = Counter(tuple(sorted(r.items())) for r in new_rows)
            detail.update(old_rows=len(old_rows),new_rows=len(new_rows),removed_rows=sum((old_count-new_count).values()),added_rows=sum((new_count-old_count).values()),old_columns=sorted(old_fields),new_columns=sorted(new_fields))
            note = f"file SHA-256; rows {len(old_rows)} -> {len(new_rows)}; exact removed/added rows {detail['removed_rows']}/{detail['added_rows']}"
        if path in figure_refs and new is not None:
            raster_hashes = []
            for label, file in [('old',ROOT/figure_refs[path]['local_reference']),('new',ROOT/path)]:
                if label == 'old' and not file.exists():
                    raster_hashes.append(figure_refs[path]['raster_sha256_150dpi'])
                    continue
                prefix=HERE/'figure_comparison'/f'{Path(path).stem}_{label}'
                prefix.parent.mkdir(parents=True,exist_ok=True)
                subprocess.run(['pdftoppm','-singlefile','-r','150','-png',str(file),str(prefix)],check=True,capture_output=True)
                raster_hashes.append(digest(prefix.with_suffix('.png').read_bytes()))
            detail['raster_changed'] = raster_hashes[0] != raster_hashes[1]
            note += '; rendered content ' + ('changed' if detail['raster_changed'] else 'unchanged at 150 dpi; PDF metadata may differ')
            add(f'figure_content.{Path(path).stem}',path,'150 dpi rendered page',*raster_hashes,note)
        output_diff.append(detail)
        if round3_file:
            note = 'new, round 3; ' + note
        add('file.'+path.replace('/','.'),path,'whole file SHA-256',old_hash,new_hash,note)

    with (HERE/'reconciliation.csv').open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS);writer.writeheader();writer.writerows(records)
    (HERE/'output_diff.json').write_text(json.dumps(output_diff,indent=2)+'\n')
    original=[r for r in records if r['name'] in old_registry]
    scalar_rows = [r for r in records if not r['name'].startswith(('file.', 'figure_content.'))]
    summary={'reference_commit':BASE,'original_registry_quantities':len(original),
        'original_registry_changed':sum(r['changed']=='yes' for r in original),
        'registry_retired':len(set(old_registry)-set(new_registry)), 'registry_new':len(set(new_registry)-set(old_registry)),
        'original_registry_display_changes':sum(name not in new_registry or old_registry[name]['display'] != new_registry[name]['display'] for name in old_registry),
        'scalar_rows':len(scalar_rows),
        'existing_scalar_rows_changed':sum(r['changed']=='yes' and r['old_value'] != '' for r in scalar_rows),
        'new_scalar_rows':sum(r['old_value'] == '' for r in scalar_rows),
        'reconciliation_rows':len(records), 'changed_table_files':[d['file'] for d in output_diff if d['file'].startswith('tables/') and d['file'].endswith('.tex') and d['changed']],
        'changed_figure_content':[d['file'] for d in output_diff if d.get('raster_changed')],
        'outputs_compared':len(output_diff)}
    (HERE/'reconciliation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    main()
