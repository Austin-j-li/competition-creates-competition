# S13: the website's research brief

Work of the prose writer (website) on branch `theory-upgrade`, 26 October 2026, for the coordinator. The six fragments `handout/sections/01-setting.html` to `06-tests.html` state the paper in `slot/manuscript/`: the abstract, the introduction, Propositions 1 to 4, Corollaries 1 to 3, Sections 6 to 8, and the vocabulary of `plan/NOTATION.md`. Structure, classes, IDs, figure and table mounts and the explorer mount are unchanged; every number prints through a `[[key]]` registry row that exists.

## Per fragment

**01-setting.html.** The incumbent is a continuous distribution \(F\) whose first-order shift strengthens it; the uniform law moves to the example. The fold defines a path and names the default tie rules (an indifferent investor may mix over its best orders; an indifferent high-cost challenger prepares) and the other two. The heading "The benchmark" reads "The example", and that paragraph introduces the example by its primitives. In the record table, "the further buyer" becomes "the challenger"; the literature paragraph follows the introduction ("a challenger that decides whether to prepare", "under rational pricing", learning from the target's price).

**02-mechanism.html.** Proposition 1 is stated for every pair of classes (profits) and under the class ranking (spread), with the class-gap identity read in words. The paragraph on the top posterior introduces the exclusion bound by name and places the entry ceiling in the example. The preparation threshold gets its name and the default challenger tie rule; "trade cost" becomes "trading cost", and the lower bound is named the trading bound. An added paragraph states Section 3.4: orders, posteriors and entry depend on the auction only through the spread and the threshold, and a stronger incumbent never narrows the first and never lowers the second while \(g_L\le c_H\). Figure 1's caption and the fold refer to the example and the strengths \(r_0,r_1,r_2\); the fold adds \(\tau(r)\).

**03-result.html.** The Proposition 2 box follows the paper: \(0<\beta<1/2\), the names of (H1) to (H3) (high-cost window, trading-cost window, exclusion condition), uniqueness under all four tie rules, and the ownership condition \(e_HW_H(F_1)>\rho W_H(F_0)\). The fold adds the sufficient ownership condition, the takeover-share result when class \(H\) outbids, the decisive advantage (`cH_DA_floor_B`) and the open parameter set. "The benchmark" section is "The example" with Corollary 1 (the band for \(M\) and \(u\), entry and ownership formulas) and the takeover share (`share_H_r0`, `share_H_r1_B`). The control paragraph states the full fixed-information experiment; table header, captions and the fold summary name the example; the strip label says "above the entry ceiling".

**04-path.html.** The h2 is "Between the three economies"; the first h3 is "Quiet and informative markets". The Proposition 3 box is the general result in the spread and the threshold: the coexistence region \(\pi<\tau\le M(\pi)\), \(k/(1-\tau)\le\Delta_T\le k/(\rho\max\{\pi,1-\pi\})\), the unique informative market and its entry, the interval of sure-purchase strengths, and the product condition. The example is Corollary 2 in prose (\([r_A,r_N]\), entry formula at the prior one half, \(r_F\), ceiling). The fold's table is "Marked strengths of the example's path", with the letters N, R, F, Q, T explained in the caption; other priors and the other tie rules follow Appendix A4's table. The research subsection states Proposition 4 in words at the even prior, with the research condition including the low class's sale term, and then Corollary 3: zero research on \([r_0,r_N]\), recruiting research on \([r_R,r_C]\) (below the cap up to \(r_{\bar\lambda}\), at the cap up to the entry ceiling), floor-entry research on \((r_N,r_Q)\) and \((r_C,r_2]\), and the unique outcome at \(r_0,r_1,r_2\). "Research branch" and \(r_U\) are gone. The fold adds the research parameter region (`res_cap_lo`, `res_cap_hi`, `res_a_lo`, `res_a_up`, `res_beta_lo`, `res_beta_upper`).

**05-robustness.html.** Cost laws, classes, many classes and signals follow Section 6, with \(\alpha_I,\alpha_C\) and `p4_comp_b_no_y_r1_entry`. Price access follows Section 7.1, with the proceeds gain `p2_access_proceeds_gain`, the same gains at the research cap, and the deterrence case as a result. The payment rule has \(\omega\in[0,1)\) and the case \(\omega=1/2\); the closer "This result concerns auction payoffs" is gone. Reserves add the strict-deterrence range (`p2_reserve_ph` to `p2_reserve_weak_top`), the flat case on \((\ell,r_0]\) and `rsv_bands_excl`. Every "benchmark" becomes "the example".

**06-tests.html.** The opening follows Section 8 (conditions named per prediction; informed share \(u/(2+u)\); \(r_S\) as the strength at which a full sale earns the trading cost). "Further buyer" becomes "challenger". The impact test uses frequency-weighted impacts and the price gap \(P(1)-P(-1)\) with its class and entry components; the fold adds the condition \(3p^2<\min\{\underline\theta,\underline r\}^2\). Identification uses the mean order \(\lambda(2\pi-1)\) and the sale impact. Winners carry the condition on where the incumbent's value falls and the gap formula; announcements read "exactly when preparation was still uncertain after some order"; the two clusters sit strictly between \(r_F\) and \(r_N\). The takeaway says "trading cost".

## Build, checks, staging

`python3 handout/build.py`: exit 0, 225 PASS, 0 FAIL, "registry keys used: 183", "HANDOUT BUILD PASSED".

`python3 handout/check_display.py`: exit 0.

```
PASS the paper tab states 150 and 7 pages, both hashes and the text date 26 October 2026
PASS 177 number spans and 49 numbers in formulas print their slot registry display; no decimal is typed into the prose
PASS only Fira Sans, Fira Mono and the symbol fallback; no network request
```

`python3 handout/publish.py --stage-only ../ccc-tu-scratch/site-stage`: exit 1. The handout build and display checks inside it pass (228 PASS); the talk build then stops, because the web slides (`presentation/content.js`) no longer match `slot/manuscript/slides.tex`. The first lines:

```
content.js has 33 frames; slides.tex has 34
F3: subtitle differs
   web:  Who wins and who pays at incumbent value $R$; benchmark order $p<\ell<r<h$
   tex:  Who wins and who pays at incumbent value $R$; in the example $p<\ell<r<h$
F6: title "Benchmark: only incumbent strength changes" differs from slides.tex "The example: only incumbent strength changes"
...
dist/index.html has 33 slides, not 34
The deck differs from slides.tex or breaks the deck contract.
subprocess.CalledProcessError: Command '[..., 'presentation/build.py']' returned non-zero exit status 1.
```

There are 157 mismatch lines in all; the web slides need the same update as `slides.tex`, which lies outside this task. The talk build wrote no tracked file; it rewrote the ignored `presentation/dist/` before its check failed. So that the brief could still be reviewed, the site root was built into the staging folder with `python3 handout/build.py --quiet --out ../ccc-tu-scratch/site-stage` (exit 0; `check_display.py --out` on it: the same three PASS lines), and `docs/` was then rebuilt so that the manifest refers to it. The staged `index.html` is byte-identical to `docs/index.html`. The staging folder holds `index.html`, `paper.pdf`, `comparison.pdf`, `fonts/` and `vendor/`; it has no `talk/` or `laplace/`.

A headless browser render of the staged page shows every formula typeset (no KaTeX error), the three charts and the explorer drawn, and every number span in place.

## Language

The print-only language scan on the six fragments lists 11 hits after the fixes. Three are the IDs `sec-setting-benchmark`, `sec-result-benchmark` and `benchmark-detail`, which are kept as navigation hooks and do not print. Two are "may mix" and "may place a wrong-signed order", which describe the model. "Illustrative" labels the opening scenario, and "check the contracts" is a diligence task. "Interval of strengths" restates Proposition 4(d). "No longer" ("Above the entry ceiling, orders no longer predict entry") compares strengths. "Could not attract" is the takeaway's counterfactual. Three hits were fixed: "unresolved", "run from about" and "no informed trade" as a name.

## Retired words that remain on the page, from files outside the fragments

Visible text with retired vocabulary, all from files this task does not touch:

- `handout/explorer.js:18`, the button "No informed trade"; `:97`, the legend "N: no informed trade"; the T legend "T: threshold branch"; `:176`, the title "Explore the benchmark path"; `:225`, the aria-label "...every equilibrium of the benchmark path"; `:227`, the Figure 3 caption ("Entry along the benchmark path", "N has no informed trade", "the thin dashed T branch").
- `handout/figures.js:250–260`, the Figure 4 legend and hover "research branch"; `:170` and `:205`, the trace names "benchmark spread" and "benchmark thresholds" (hover only).
- `handout/template.html:131`, the colophon "at the benchmark declarations".
- `handout/README.md` still describes "the benchmark path (coexistence and research)", "the three propositions of the main text" and "the research branch (Section 5)".

**Figure 4 and Corollary 3.** `figures.js` draws recruiting research only up to \(r_N\), labels the cap strength \(\bar r_R\) (the frozen symbol is \(r_{\bar\lambda}\)), and does not draw floor-entry research or the cap segment from \(r_N\) to \(r_C\). The caption says what the figure draws and states in words what holds above \(r_N\). The production assistant can bring the figure in line with Corollary 3 and the paper's Figure (research.pdf).

## Files changed

The six fragments; `docs/index.html`, `docs/paper.pdf`, `docs/comparison.pdf` (new, untracked) and `numerics/manifests/handout.json`, all written by `build.py`. The build also deletes the tracked `docs/main_filled.pdf` and `docs/online_appendix_filled.pdf` (`build.py:479–480`; those PDFs are served under `/laplace/`). Nothing is committed.
