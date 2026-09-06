"""C.2 regressions for node identity, status and mixed-support records."""
from decimal import Decimal

import numpy as np

from numerics.auction import payoffs_closed_form
from numerics.deviations import Convolution
from numerics.exercises import c2_correspondence as c2
from numerics.information import OrderProfile, make_schedule
from numerics.mixed_search import mixed_search_node
from numerics.params import BENCHMARK, CONTROLS
from numerics.status_rules import classify_tangency, pooling_existence_label
from numerics.validation import validate
from numerics.error_budget import error_budget


def test_grid_has_one_exact_node_per_strength():
    grid = c2.strength_grid()
    assert len(grid) == len({Decimal(r) for r in grid})
    assert c2.canonical_r('1.60') == '1.6'
    assert grid.count('1.6') == 1


def test_status_distinguishes_nonroot_open_and_rejection():
    conv = Convolution(0, 1e-13, 0)
    assert classify_tangency(1e-10, conv).status == 'open'
    assert classify_tangency(1e-4, conv).status == 'no candidate'
    assert pooling_existence_label(-1e-3, True, False)[0] == 'rejected'
    assert pooling_existence_label(-1e-3, True, True)[0] == 'open'


def test_budget_rejects_nonfinite_error():
    sched = make_schedule(BENCHMARK, payoffs_closed_form(BENCHMARK, 1.2), OrderProfile.pure(0, 0))
    val = validate(sched, CONTROLS)
    assert error_budget(val, sched, CONTROLS, analytical_cover=True).within_targets
    val.quadrature_error = float('nan')
    assert not error_budget(val, sched, CONTROLS).within_targets


def test_mixed_search_records_both_states_and_requires_monotonicity(monkeypatch):
    import numerics.mixed_search as ms
    pay = payoffs_closed_form(BENCHMARK, 1.2)
    monkeypatch.setattr(ms, 'residual_monotone', lambda sched: False)
    attempts = mixed_search_node(BENCHMARK, pay, CONTROLS, '1.2', meshes=(0.5,), max_iter=1)
    assert len(attempts) == 3
    for at in attempts:
        assert abs(sum(at.support_w) - 1) < 1e-12
        assert at.outcome == 'unresolved'
        assert at.residual_monotone is False
        assert np.isfinite(at.low_support_payoff)
        assert np.isfinite(at.low_gap_to_best_tested)


def test_deduplication_keeps_one_certified_asymmetric_root():
    brackets = {c2.canonical_r(r): (lo, hi) for r, lo, hi in c2.CERTIFICATE_BRACKETS}
    rows, _, _, _ = c2.solve_node('1.60', brackets, do_pure=False, do_mixed=False)
    acc = [r for r in rows if r['accepted'] and not r['duplicate_of']]
    assert len([r for r in acc if r['branch'] == 'asymmetric']) == 1
    assert next(r for r in acc if r['branch'] == 'asymmetric')['result_status'] == 'computer-assisted'
    assert all(r['n_distinct_accepted'] == len(acc) for r in rows)


def test_near_pooling_solver_endpoint_is_revalidated_and_deduplicated():
    rows, _, _, _ = c2.solve_node('1.2', {}, do_pure=True, do_mixed=False)
    accepted = [r for r in rows if r['accepted'] and not r['duplicate_of']]
    assert len(accepted) == 1
    assert accepted[0]['branch'] == 'pooling'
    assert all(r['n_distinct_accepted'] == 1 for r in rows)


def test_near_asymmetric_root_is_polished_before_atom_identity():
    rows, _, _, _ = c2.solve_node('1.51', {}, do_pure=True, do_mixed=False)
    accepted = [r for r in rows if r['accepted'] and not r['duplicate_of']]
    assert len(accepted) == 2
    assert {r['branch'] for r in accepted} == {'pooling', 'asymmetric'}


def test_interior_root_polish_prevents_false_multiplicity():
    rows, _, _, _ = c2.solve_node('1.79', {}, do_pure=True, do_mixed=True)
    accepted = [r for r in rows if r['accepted'] and not r['duplicate_of']]
    assert len(accepted) == 2
    assert {r['branch'] for r in accepted} == {'full_orders', 'symmetric_interior'}
