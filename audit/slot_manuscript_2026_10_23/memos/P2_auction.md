# R6 and R9: proof summary

**Analytical:** The two-class comparison holds for general laws and priors. Every ranked pair with a positive gap admits an open region of strengths and costs.

**Computer-assisted:** Every source example retains its costs and strengths. The constructive sequences first work at n = 3. Control D keeps floor entry.

**Analytical:** Separation from every feasible posterior mean gives the many-class comparison. **Computer-assisted:** A strict three-class equilibrium gives two posteriors one price.

**Analytical:** Access raises proceeds and net surplus in the recruitment region. **Computer-assisted:** At B, the gains are 0.257948 and 0.081960; the liquidity transfer is 0.037665. The break-even scale is 6.848394.

**Analytical:** The payment rule gives a spread response with the sign of 1 − 2η.

**Computer-assisted:** Entry is flat at the exclusion reserves. Reserve 31/20 restores strict deterrence and higher proceeds. It excludes the low class and the weak incumbent.

## Strict margins at B

The columns are C0 = c_H − B0(π), C1 = B1(M) − c_H, T0 = k − Δ0, TH = ρ(1 − M)Δ1 − k, TL = ρmΔ1 − k, C2 = c_H − B2(M), and O = e_H W1 − ρW0. For D, O uses the hypothetical recruitment coefficient.

| Example | C0 | C1 | T0 | TH | TL | C2 | O |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 1.195833 | 0.217155 | 0.003333 | 0.024824 | 0.024824 | 0.002689 | 0.398803 |
| Moderate | 0.033452 | 0.030137 | 0.000810 | 0.003603 | 0.003603 | — | 0.398803 |
| Narrow | 1.195660 | 0.217192 | 0.002986 | 0.024833 | 0.024833 | 0.002658 | 0.398803 |
| A | 1.460455 | 0.109179 | 0.005455 | 0.066983 | 0.012698 | 0.058137 | 0.398803 |
| B | 0.562273 | 0.123413 | 0.005455 | 0.012698 | 0.066983 | 0.132569 | 0.398803 |
| C | 0.021000 | 0.058891 | 0.006667 | 0.023541 | 0.127671 | 0.314551 | 0.349742 |
| D | 0.025000 | -0.018122 | 0.020000 | 0.026343 | 0.137174 | 0.447727 | 0.398803 |

All successful rows have positive margins. Collapse preserves the trade bounds. D has a negative upper cost margin.

| Strict primitive or support restriction | Positive margin, in the same order |
|---|---|
| λ, 1−λ, β, 1/3−β | 0.336122, 0.663878, 0.294655, 0.038678 |
| π, 1−π, ρ, 1−ρ | 0.500000, 0.500000, 0.250000, 0.750000 |
| p, ℓ−p, r0−ℓ, r1−r0, r2−r1, h−r2 | 0.500000, 0.500000, 0.200000, 1.800000, 0.600000, 6.400000 |
| k, c_H, Γ, b+λ−1/2 | 0.020000, 6.000000, 9.000000, 0.031737 |

Reserve columns are T = ρκΔ − k, C = 6 − B(1/2), and J = B(M) − 6. Positive J recruits; negative J excludes.

| Values; reserve; strength | T | C | J |
|---|---:|---:|---:|
| Points; 101/100; 6/5 | 0.038167 | 1.512521 | 0.561220 |
| Points; 101/100; 3 | 0.047239 | 1.835008 | 0.089706 |
| Bands; 11/10; 6/5 | 0.048076 | 1.552083 | 0.503375 |
| Bands; 11/10; 3 | 0.047572 | 1.850833 | 0.066568 |
| Either; 31/20; 6/5 | 0.084215 | 1.775000 | 0.177445 |
| Either; 31/20; 3 | 0.057405 | 1.950208 | -0.078730 |

| Additional strict condition | Margin |
|---|---|
| Collision: β−1/4, w, 1−w, c_H−max g | 0.044655, 0.940709, 0.059291, 4.062500 |
| Collision: strict order gaps, classes 1–3 | 0.260795, 0.020627, 0.024768 |
| Groups: weak range, weak cost, return, profit gap, top profit | 0.003333, 1.195875, 0.024718, 8.332667, 0.216834 |
| Deterrence: p_H−r0, 31/20−p_H, 10−6/M−31/20 | 0.125270, 0.224730, 0.242723 |

The payment comparison has strength distance 13/20 and weight margin 1/2−η or η−1/2. B fixes no η. The proof and `margins.csv` give the boundary and candidate margins.

## Scope and verification

P1 fixes zero-cost preparation at every price. IM permits investor mixtures; C1/CM govern high-cost ties. The strict results and both upper endpoints survive both rules. Entry at p_H depends on C1/CM.

Full posterior recovery and strict deterrence at the source exclusion reserve fail. The brief already states both corrections. Generic recovery under mixed class profiles, the full game under the alternative payment rule, and a global optimal reserve stay open.

The CLI prints exact auction integrals, 60-digit intervals, and every deviation payoff. The article compiles with `latexmk`; the PDF page review found no layout defect. The equilibrium definition and notation match `P1_core.tex`.
