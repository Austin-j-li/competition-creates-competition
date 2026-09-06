"""Presentation boundaries: gaps, identities, endpoint semantics, and finite scalars."""
from decimal import Decimal
from unittest.mock import patch

import numpy as np

from numerics.continuations import parameter_set_id
from numerics.params import BENCHMARK
from numerics.render import figures, tables


def test_correspondence_gaps_ambiguity_and_complete_identity():
    rows = [{"r": r, "E": "0.3", "accepted": "true"} for r in ("1", "1.01")]
    x, y = figures._broken_series(rows, "r", "E", 0.005, nodes=list(map(Decimal, ("1", "1.005", "1.01"))))
    assert np.isnan(y[1]), "a missing searched node must break the line"
    rows.append({"r": "1.01", "E": "0.4", "accepted": "true"})
    x, y = figures._broken_series(rows, "r", "E", 0.005)
    assert np.isnan(y[-1]), "multiple family members must not become a vertical fitted segment"
    row = dict(rows[0], parameter_set_id=parameter_set_id(BENCHMARK, "1", BENCHMARK.p, "binary", "0"),
               candidate_id="candidate", continuation_id="complete strategy and pricing record", result_status="numerical diagnostic",
               n_distinct_accepted="1", multiplicity_found="false")
    assert figures._correspondence_rows([row]) == [row]
    for bad_rows in ([row, row], [dict(row, parameter_set_id="rounded-r-only")], [dict(row, n_distinct_accepted="2")]):
        try:
            figures._correspondence_rows(bad_rows)
        except ValueError:
            pass
        else:
            raise AssertionError("Figure 2 accepted invalid continuation identity or multiplicity")


def test_finite_table_boundaries():
    for value in ("nan", "inf", "-inf"):
        for formatter in (tables.d6, tables.sci, figures._f):
            try:
                formatter(value)
            except ValueError:
                pass
            else:
                raise AssertionError(f"{formatter.__name__} accepted {value}")
    assert tables.d6("n/a") == "n/a"
    assert tables.d6("0.1234567") == "0.123457"


def test_matched_panel_rejects_changed_investor_residuals():
    read = tables.read_csv
    def changed(path):
        rows = read(path)
        if path == "numerics/feedback_comparisons.csv":
            rows = [dict(row, residual_invariance_error="0.01") for row in rows]
        return rows
    with patch.object(tables, "read_csv", side_effect=changed):
        try:
            tables.matched_price_panel()
        except ValueError as error:
            assert "residual_invariance_error" in str(error)
        else:
            raise AssertionError("matched-price panel accepted changed investor residuals")


def test_reserve_coverage_uses_a_consistent_attempt_ledger():
    row = {key: "n/a" for key in tables.RANGE_COLUMNS}
    row.update(value_law="binary", r="1.2", p_exact="0.5", candidates_evaluated="5", candidates_accepted_raw="3",
               candidates_rejected="1", candidates_unresolved="1", duplicates_merged="1", accepted_continuations_found="2")
    with patch.object(tables, "read_csv", return_value=[row]):
        assert tables._read_ranges("probe.csv") == [row]
    for rows in ([row, row], [dict(row, candidates_evaluated="99")], [dict(row, accepted_continuations_found="3")]):
        with patch.object(tables, "read_csv", return_value=rows):
            try:
                tables._read_ranges("probe.csv")
            except ValueError:
                pass
            else:
                raise AssertionError("duplicated or inconsistent attempt ledger accepted")


def test_logistic_closed_endpoint_and_bargaining_log_domain():
    captured = []
    with patch("matplotlib.figure.Figure.savefig", lambda fig, *a, **kw: captured.append(fig)), patch.object(figures.plt, "close"):
        figures.figure3()
        figures.figure4()
    tails, bargaining = captured
    for ax, endpoint in zip(tails.axes, (0, float(BENCHMARK.rho))):
        points = [line for line in ax.lines if len(line.get_xdata()) == 1 and line.get_color() == figures.RUST]
        assert len(points) == 1 and float(points[0].get_ydata()[0]) == endpoint
        assert points[0].get_markerfacecolor() == figures.RUST, "logistic endpoint must be closed"
    for line in bargaining.axes[1].lines:
        if len(line.get_xdata()) > 2:
            assert max(line.get_xdata()) < 1
            assert np.all(np.asarray(line.get_ydata()) > 0)
    for fig in captured:
        figures.plt.close(fig)


def test_logistic_unattained_endpoint_is_not_a_finite_tail_proxy():
    original = figures.read_csv("figures_data/posterior_tails.csv")
    rows = [dict(row) for row in original]
    row = next(r for r in rows if r["noise"] == "logistic" and float(r["M_minus_tau"]) == 0)
    row.update(x_star="1000000", threshold_noise_sd="100000", posterior_upper_tail_mass="0.00000001")
    with patch.object(figures, "read_csv", return_value=rows):
        try:
            figures.figure3()
        except ValueError:
            pass
        else:
            raise AssertionError("finite proxy for logistic unattained threshold reached renderer")
