# Numerical contract changes: 21 October 2026

New symbols: `Pi_acc`, `Pi_hid`, `Delta R_T`, `Omega_U`, and `Omega_0` follow the requested memo definitions.
For the additional noise law, `nu` denotes degrees of freedom and `s` denotes its scale.

The reference is commit `1eb6d2cfd70fdfca98bbf4557d666bd04417e1df`.
The author sets the low preparation cost to zero.
No numerical tolerance changes.
No unresolved result receives a replacement value.

1. The benchmark, moderate, and complementary-signal vectors now declare zero low cost.
   The three input rows in the quantity manifest use the same declaration.
   The legacy CSV column `c_L` remains for compatibility.
2. The atomless low-cost component is uniform on `[0, 0.2]`.
   Its width remains `2 epsilon_C = 0.2`; its mean is `0.1`.
   The high-cost component remains uniform on `[5.9, 6.1]`.
   All C.1 gross-profit floors exceed the low component's upper endpoint.
   The cost CDF, paid-cost integral, breakpoints, independent integral, and margins use the same support.
3. C.4's nonemptiness sequence also fixes zero low cost.
   The former positive-low-cost requirement disappears.
   The other choices, grid, and strict inequalities remain.
4. Exercise C.6b is retired, with its output, manifest, and seven quantity keys.
   The prior commit preserves them.
   The release stages and renderer no longer consume them.
   Minimal retirement notices replace their legacy manuscript source sections so substitution remains strict.
   The live manuscript clone receives no edit here.
5. The binary floor event is `p_L = h = 10`.
   For uniform value classes, zero gross profit first occurs at `h + epsilon_V = 10.05`.
   The class endpoint has zero mass; its sale probability and revenue are zero.
   The binary endpoint remains admissible under the existing bid tie rule.
   Exact floor events take precedence over coincident support labels.
6. The event grid retains all three offsets on each side of the floor endpoint.
   Upper offsets extend beyond the value support for this check alone.
   Above the support, gross profit and low cost both equal zero.
   Preparation remains `rho` under the existing tie rule; sale and revenue are zero.
   No negative-floor classification applies there.
7. The reserve solver no longer excludes full orders solely because challenger gross profit equals zero.
   Zero spread or impossible preparation still permits the constant-price shortcut.
   At a zero-spread constant-price node with identical state order laws, Bayes' rule gives the prior on the full preimage.
   A constant price map has no inverse.
8. The class-payoff integrals use factored polynomial differences near the support endpoint.
   This avoids cancellation of nearly equal squares without a tolerance change.
9. C.2 retains its domain, mesh, refinements, certificates, and four thresholds.
   `domain.json` records the old and new margins and threshold outputs.
10. Verification uses the producer commands and the two release gates directly.
    No test suite runs, and no test or assertion script is written.
    The historical release wrapper and independent seed do not define this revision's acceptance.
11. The first C.6 sweep stopped at the weak class node `p=0.9701`.
    Interior pure starts differed by about `4e-8` in orders and failed the stricter atom identity comparison.
    The bounded refinement now solves both held-schedule first-order equations, as C.2 already does.
    A proposal requires residual below `1e-10` and movement within the unchanged order identity tolerance.
    Every proposal faces the complete validation again.
    The raw prior candidates and all unconverged starts remain in the ledger.
    An unresolved identity still stops the exercise.
12. C.9 adds eight quantities after the first release gates passed.
    Gross trade profit excludes the trade cost. The stake bounds are sufficient bounds.
    Additional noise laws keep the prescribed full orders and score bound `1/b`.
    The Student law has three degrees of freedom and scale `b*(nu+1)/(2*sqrt(nu))`.
    Its entry set has two finite endpoints. The hyperbolic secant set is a half-line.
    C.9 has its own producer, independent acceptance layer, manifest, and registry rows.
    The final gate now requires this stage. C.0 tolerances remain unchanged.

## Round 3: C.10

The new exercise uses the general class model and the revised Proposition 2.
Its (A1) replaces the old high-cost condition, and its (A2) replaces the old trade condition.
The entry floor follows from zero cost.
The benchmark declaration and all earlier exercises retain their values.

The symbols are the prior $\pi$, bounds $m(\pi),M(\pi)$, constant $\kappa(\pi)$, and win probability $W_H$.
The table uses $B_i(\mu)=B_{r_i}(\mu)$ and $\Delta_i=\Delta_T(r_i)$.
Its two short labels are $u_1=(1-1/b)\rho\kappa(\pi)\Delta_1$ and
$s_W=(1+\rho)W_H(r_1)-2\rho W_H(r_0)$.

1. C.10 declares three examples and a matched point-mass comparison.
   Every input enters as an exact decimal string.
   The class supports are part of each complete parameter declaration.
2. The producer computes class payoffs, posterior bounds, entry, ownership, and every required margin.
   It records separate labels for an analytical outcome and satisfaction of the complete proposition.
   The comparison retains its negative high-cost margin.
3. Independent realized-auction integrals, density roots, and full-line integrals validate the formulas.
   Held-schedule deviations use both order signs and the initial and refined grids.
   The analytic Laplace tails have zero truncation error.
   The established global bounds justify uniqueness beyond the diagnostic grids.
4. The prior interval for a nonempty trade-cost window differs from the interval at fixed benchmark costs.
   The fixed collapse strength imposes another upper endpoint.
   C.10 records all three intervals separately and treats each endpoint as open.
5. The registry adds the benchmark trade bounds, the spread ratio, and the four-law entry range.
   The two additional noise laws retain their diagnostic status at fixed full orders.
6. C.10 has its own manifest, source hashes, output hashes, and acceptance record.
   Its serializer uses a local fifty-digit context, independent of other release stages.
   The final gate repeats the calculation and compares every saved CSV row.
7. The renderer consumes only the validated CSV files.
   The legacy appendix records the exercise contract and includes its table.
   The revised manuscript clone remains read-only.
8. The reconciliation marks each new quantity and source row with the note “new, round 3”.
   All tolerances and prior search records stay unchanged.
   The producer uses one process and one native numerical thread.
