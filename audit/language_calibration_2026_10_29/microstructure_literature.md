# Microstructure terms for the order-slot model

29 October 2026. Discussion note only. No manuscript or deck changes.

## Recommendation

Use **outside informed investor**, **liquidity trader**, and **competitive market makers** in both paper and deck. Define each role once. Use **informed trader** as an equivalent functional description, rather than a second character name.

Use **sector specialist** only as an interpretation of the investor's expertise. Avoid **specialist investor** as the principal model label. In classic microstructure, a specialist also names the intermediary on the other side of the trade.

These recommendations concern fit with this model. The sources establish usage; they do not establish a universal terminology standard or relative term frequencies.

## Current model and definitions

Sources read: `CLAUDE.md`; `overleaf/slot/main.tex`; `sections/01_introduction.tex`; `sections/02_model.tex`; `sections/05_research.tex`; relevant passages in `slides.tex`.

The investor knows the challenger's class, not its eventual value or all target proceeds. Its information comes from outside research. It has no initial net target position, no control rights, and no right to acquire the target. The first buyer's preparation and the investor's information are distinct attributes.

Suggested paper definition:

“An outside informed investor observes the challenger's synergy class. It has no initial net target position, no control rights, and cannot acquire the target.”

Suggested deck definition:

“The informed investor knows the second buyer's synergy class and trades target shares. Neither buyer trades target shares.”

Do not call either buyer the informed investor. The prepared buyer knows its acquisition value. The prospective buyer uses the price before it pays for preparation. Neither fact gives either buyer the investor's role.

## Informed trader and informed investor

Kyle (1985), p. 1315, abstract, uses “a single risk neutral insider” and “random noise traders”. The introduction calls the latter “uninformed noise traders”. These are exact short quotations from the article text indexed at the link below.

[Continuous Auctions and Insider Trading, article PDF](https://people.stern.nyu.edu/lpederse/courses/LAP/papers/Information%2CFundamental/Kyle85.pdf).

Kyle's insider observes liquidation value. This model's investor observes a class that affects a takeover outcome. Thus, Kyle supports the information-based distinction without supplying an exact economic identity.

Glosten and Milgrom (1985), p. 77, use both “informed investor” and “informed trader”. They allow information from “private information or superior analysis”. These short quotations show that investor and trader need not name different agents.

[Glosten–Milgrom article PDF, p. 77](https://www.edegan.com/pdfs/Glosten%20Milgrom%20%281985%29%20-%20Bid%20Ask%20and%20Transaction%20Prices%20in%20a%20Specialist%20Market%20with%20Heterogeneously%20Informed%20Trades.pdf).

The source is the original article, on a mirror. The NYU copy yielded indexed article text but failed on direct fetch. Do not infer a corporate insider or illegal information source from this literature's use of insider. For this paper, outside informed investor states the intended distinction more clearly.

## Noise trader, liquidity trader, and uninformed trader

Noise trader accurately describes the exogenous order distribution. It need not imply irrational conduct. Liquidity trader fits the manuscript's stated reasons apart from the sale. The manuscript assigns cash needs to sales and outside investors to purchases.

Uninformed trader states an information restriction. Alone, it does not state why this trader trades or why its order ignores price. A rational uninformed investor could condition its order on public information. Thus, these three terms are related but not interchangeable assumptions.

Suggested definition:

“A liquidity trader has no private information about the synergy class. Its order is exogenous and independent of that class.”

Then give the three order probabilities. Explain that liquidity motives are an interpretation; the model does not solve a consumption or portfolio problem.

Glosten–Milgrom, p. 77, model preference or endowment differences for uninformed participants. Their informed trader can also have a liquidity motive. Therefore, liquidity motive and private information are separate dimensions. This model assigns them to separate slot types as an assumption.

## Market maker and dealer

Kyle (1985), p. 1315, abstract, uses “competitive risk neutral market makers”. This directly supports the current label.

Use market makers for agents that observe the order, absorb it, and set the conditional expected target payoff. Dealer can describe an intermediary that trades for its own account. It adds no useful precision here. Neither label alone implies competition, risk neutrality, or conditional break-even prices; state those assumptions separately.

Do not describe this as the full Glosten–Milgrom quote mechanism. The present model has one order-contingent price, including a price after no order. It does not specify their full sequential bid–ask institution.

## Specialist investor

Glosten–Milgrom (1985), p. 71, introduction, describe specialists and floor traders as “middlemen”. Their abstract discusses a “specialist” that makes zero expected profits.

[Original article text, NYU copy](https://pages.stern.nyu.edu/~lpederse/courses/LAP/papers/Information%2CFundamental/GlostenMilgrom85.pdf); [author institution record and abstract](https://business.columbia.edu/faculty/research/bid-ask-and-transaction-prices-specialist-market-heterogeneously-informed-traders).

This creates a real historical collision with the paper's sector specialist. Sector specialist describes expertise, not a distinct equilibrium role. A sector-focused long-short fund is an example, not a necessary assumption. It does not imply a blockholding, activist mandate, dealer role, or takeover right.

## Takeovers and feedback: source boundaries

Kyle and Vila (1991), *Noise Trading and Takeovers*, pp. 54–71, is the relevant classic. The primary publisher issue record confirms its title and location.

[Publisher issue record](https://www.jstor.org/stable/i344676); [article](https://www.jstor.org/stable/2601007); [DOI](https://doi.org/10.2307/2601007).

The article fetch returned no substantive text. Its title verifies “Noise Trading”, but no internal role quotation is verified here. A secondary abstract mentions a large corporate outsider. I exclude that wording as primary evidence. Do not cite this check as proof that its outsider equals this paper's non-acquiring investor.

Edmans, Goldstein, and Jiang (2012), p. 933, abstract, call the price effect on takeover activity the “trigger effect”. They call price anticipation of takeovers the “anticipation effect”.

[Author-hosted published article](https://finance.wharton.upenn.edu/~itayg/Files/takeoverfeedback-published.pdf).

This is evidence for feedback and takeover vocabulary. It does not establish a standard label for this model's outside trader or prove its information channel empirically.

Luo (2005), abstract, writes: “Merging companies appear to extract information from the market reaction”.

[Publisher abstract, pp. 1951–1982](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2005.00784.x).

Luo studies decisions after an announcement. This paper places the price before the second buyer's preparation. Use Luo as related evidence for corporate use of market information, with that timing distinction.

Edmans–Goldstein–Jiang (2015), Section I.B, is a close theoretical comparator. Search exposed article excerpts with speculator terminology, but direct primary-text access failed. I do not treat the secondary transcription as verified quotation evidence.

[Author research page with theory link](https://alexedmans.com/research/research-financial-markets-and-the-real-economy/); [article DOI](https://doi.org/10.1257/aer.20140041).

The precise page and wording for its speculator labels remain a source-access gap in this note.

## Research, presence, and informed status

In the baseline, lambda is the probability that the informed investor occupies the slot. Conditional on that event, it knows the class perfectly. Lambda is not signal precision, the probability of a nonzero informed order, or a realized volume share.

In Section 5, the investor chooses research intensity before it knows the class. Research succeeds with probability lambda. A success reveals the class and gives the investor the slot. A failure gives the slot to a liquidity trader.

Use **research intensity** for the choice and **research success probability** for its probabilistic meaning. Use **informed presence probability** for the baseline slot probability. State their equality when the extension begins.

An investor can conduct research without success. An informed investor can abstain after success. An uninformed investor need not be a liquidity trader. These distinctions prevent presence, information, and observed trade from becoming accidental synonyms.

The extension also removes liquidity opportunities as research succeeds more often. It changes slot composition as well as information production. Do not describe it as a pure improvement in signal accuracy.

## Limits

The evidence supports several established labels, with definitions. It does not identify one mandatory disciplinary vocabulary. Kyle–Vila internal terms and EGJ 2015 exact wording need further primary-text access. No tests, external downloads, or canonical-source edits were made.
