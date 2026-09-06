"""Complete price information and identity regressions for the shared adapter."""
from dataclasses import replace

import numpy as np
from scipy.integrate import quad

from numerics.auction import payoffs_closed_form
from numerics.continuations import (INFO_FEEDBACK_STATE, continuation_from_schedule, continuation_identity,
                                    economically_equivalent, schedule_price_atoms)
from numerics.deviations import U
from numerics.exercises import c6b_price_pools as c6b
from numerics.information import OrderProfile, make_schedule
from numerics.params import BENCHMARK, CONTROLS, CostLaw, Noise
from numerics.validation import validate


def adapt(sched):
    val = validate(sched, replace(CONTROLS, initial_order_intervals=20, refined_order_intervals=40), price_pools=True)
    return continuation_from_schedule(sched, val, candidate_id="test", parameter_set="test", information=INFO_FEEDBACK_STATE,
                                     controls=CONTROLS, branch="test", result_status="numerical diagnostic", existence_scope="test",
                                     uniqueness_scope="none", search_coverage_scope="test", run_id="test")


def test_exact_zero_pool_and_positive_plateau():
    sched = make_schedule(BENCHMARK, payoffs_closed_form(BENCHMARK, 1.2, 7), OrderProfile.pure(1, -1))
    cont = adapt(sched)
    pool, plateau = cont.price_information.atoms
    assert abs(pool.preimage[0][1] + np.log(2)) < 1e-12
    assert pool.preimage[0][0] == -np.inf
    assert plateau.preimage == ((1.0, np.inf),)
    assert abs(pool.posterior - pool.mass_H / (pool.mass_H + pool.mass_L)) < 1e-14
    assert not any("price_atom" in breach for breach in cont.validation.breaches)


def test_both_plateaus_and_cost_actions_at_observed_prices():
    sched = make_schedule(BENCHMARK, payoffs_closed_form(BENCHMARK, 3, .5), OrderProfile.pure(1, -1))
    cont = adapt(sched)
    low, high = cont.price_information.atoms
    assert low.preimage == ((-np.inf, -1.0),) and high.preimage == ((1.0, np.inf),)
    assert abs(low.mass_H - .5 * np.exp(-1)) < 1e-14 and low.mass_L == .5
    assert high.mass_H == .5 and abs(high.mass_L - .5 * np.exp(-1)) < 1e-14
    prep = cont.preparation_rule
    assert not prep.prepares("price_atom[0]", "c_H")
    assert prep.prepares("price_atom[1]", "c_H")
    assert any("nonatom_price:B(mu_P)>=" in r and cost == "c_H" and action for r, cost, action in prep.actions)
    assert any("nonatom_price:B(mu_P)<" in r and cost == "c_H" and not action for r, cost, action in prep.actions)


def test_nonmonotone_mixed_profile_has_disconnected_price_preimage():
    # Both extreme tails have the same posterior; the interior differs.
    profile = OrderProfile((-1., 1.), (.5, .5), (0.,), (1.,))
    sched = make_schedule(BENCHMARK, payoffs_closed_form(BENCHMARK, 3, .5), profile)
    atoms, breaches, _ = schedule_price_atoms(sched, CONTROLS)
    assert not breaches
    assert len(atoms) == 1 and atoms[0].preimage == ((-np.inf, -1.), (1., np.inf))
    for state, mass in (("H", atoms[0].mass_H), ("L", atoms[0].mass_L)):
        direct = sum(quad(lambda x: float(profile.a(BENCHMARK.noise, BENCHMARK.fb, np.array([x]), state)[0]),
                          lo, hi, epsabs=1e-12)[0] for lo, hi in atoms[0].preimage)
        assert abs(direct - mass) < 1e-10


def test_identity_retains_mapping_preimages_beliefs_and_preparation():
    _, cont, _ = c6b.evaluate_member(*c6b.cutoff_family()[0])
    changed = [replace(cont, pricing_rule=replace(cont.pricing_rule, positive_entry_price_map="changed price map")),
               replace(cont, price_information=replace(cont.price_information, atoms=(replace(cont.price_information.atoms[0],
                       preimage=((-np.inf, -.4),)), *cont.price_information.atoms[1:]))),
               replace(cont, price_information=replace(cont.price_information, atoms=(replace(cont.price_information.atoms[0],
                       posterior=.1), *cont.price_information.atoms[1:]))),
               replace(cont, preparation_rule=replace(cont.preparation_rule, actions=(("zero_price", "c_L", True),)))]
    for other in changed:
        assert not economically_equivalent(cont, other, CONTROLS)
        identity = continuation_identity(other.parameter_set_id, other.institution_id, other.information_structure_id,
                                         other.tie_rule_id, other.investor_strategy, other.pricing_rule,
                                         other.preparation_rule, other.price_information, CONTROLS)
        assert identity != cont.continuation_id


def test_uniform_cost_rule_and_logistic_nonatomic_prices():
    prim = BENCHMARK.with_(cost_law=CostLaw.UNIFORM_MIXTURE, cost_halfwidth="0.05")
    cont = adapt(make_schedule(prim, payoffs_closed_form(prim, 3, .5), OrderProfile.pure(1, -1)))
    assert any(cost == "C in declared cost support" for _, cost, _ in cont.preparation_rule.actions)
    prim = BENCHMARK.with_(noise=Noise.LOGISTIC)
    atoms, breaches, _ = schedule_price_atoms(make_schedule(prim, payoffs_closed_form(prim, 3, .5), OrderProfile.pure(1, -1)), CONTROLS)
    assert not atoms and not breaches


def test_unilateral_orders_hold_complete_price_and_preparation_schedule_fixed():
    sched, pay = c6b.build(0., "0")
    # Outside [-100,100], the omitted payoff is below 2*7*exp(-99/2).
    points = [-100., *sched.breakpoints, 100.]
    for state, q in (("H", .3), ("H", -.3), ("L", -.7), ("L", .7)):
        def profit(x):
            xx = np.array([x])
            conditional_value = pay.t_0 + float(sched.entry(xx)[0]) * (pay.w_H if state == "H" else pay.w_L)
            held_price = float(sched.price(xx)[0])
            from numerics.noise import pdf
            return q * (conditional_value - held_price) * float(pdf(BENCHMARK.noise, xx - q, BENCHMARK.fb)[0])
        # Include the deviating density kink; the candidate thresholds stay fixed.
        edges = sorted(set(points + [q]))
        direct = sum(quad(profit, lo, hi, epsabs=1e-12)[0] for lo, hi in zip(edges[:-1], edges[1:])) - BENCHMARK.fk * abs(q)
        assert abs(U(sched, state, q).value - direct) < 1e-10
