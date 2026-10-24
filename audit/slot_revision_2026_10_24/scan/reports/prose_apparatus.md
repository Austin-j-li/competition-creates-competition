# L2 report: the "math paper" apparatus in the main text of the order-slot manuscript

Scope: `slot/manuscript/main.tex` (abstract) and `slot/manuscript/sections/01_introduction.tex` to `09_conclusion.tex`. Cross-references were collected from `sections/`, `appendix/`, `slides.tex` and `comparison.tex`. Reference draft: `laplace/manuscript/main.tex (branch laplace)`, main text lines 149 to 1503. Page numbers come from `build/main.aux`.

Rules kept: I did not edit a file in the repository and did not run `latexmk`. Symbol counts came from a short counting script in `/tmp/l2_scan_tools/`, outside the repository.

Register: my own analysis uses short, plain sentences. All proposed manuscript text (the replacement sentences and the draft proposition statements) uses the reference draft's register instead: longer sentences, "I", semicolons where the reference uses them, and no controlled-language limits. The brief gives the author's request priority over a general short-sentence style for this manuscript, and I followed that. Each proposed sentence keeps the facts and the `\reg{...}` macros of the text it replaces. It adds no fact, number, mechanism or citation.

---

## 0. Summary

- The main text has 15 numbered environments, not 16: 1 assumption, 1 definition, 4 propositions, 3 lemmas, 3 corollaries and 3 remarks. It also has four label systems that read like a math paper: (H1)–(H3), (E1)–(E7), the tie-rule names IM/I0/C1/CM, and the form letters N/R/F/Q/T. There are 10 status tags in environment titles, 2 status explanations and 8 inline status tags. The main text defines about 100 symbols (an approximate count).
- Recommendation: keep **four** numbered propositions in the main text, one for each claim in the abstract:
  1. Proposition 1, competition and the two returns to information (analytical);
  2. Proposition 2, competition creates competition (analytical);
  3. Proposition 3, coexistence on the benchmark path (computer-assisted);
  4. Proposition 4, competition creates research (a merge of the current Proposition 4 and Corollary 3).
- Assumption 1, Definition 1, Lemmas 1–3, Corollary 1 and Remark 3 become prose in the main text. Their formal statements go to Appendix A. Corollary 2 and Remarks 1–2 go to Appendix A.4 and A.5, and two sentences of prose stay in the main text. Most of the target text already exists in the appendix.
- This change keeps the Proposition A.1–A.14 numbering. The hard-typed numbers in `slides.tex` and `comparison.tex` then need only the changes listed in Section 6.
- Estimate: the main text goes from about 36.5 pages (38 with the title page) to about 29–30 pages. That is near the reference draft, which has no research section.

---

## 1. Inventory

### 1.1 Numbered environments and every place that cites them

Main-text page numbers are from the build. "App." means `appendix/`. Slides and the comparison note cite by hard-typed number, not by `\ref`.

| # | Environment, location, title as printed | Cited in sections | Cited in appendix | Cited in slides.tex / comparison.tex (hard-typed) |
|---|---|---|---|---|
| E-a | **Assumption 1**, `02_model.tex:67–73`, "[Class ranking]", no tag (p. 7) | `02:75`, `03:39`, `03:54`, `03:71`, `03:75`, `04:12`, `06:27` | `A1:106`, `A1:155` (paragraph title "Scope of Assumption~\ref{ass:classes}."), `A1:156`, `A3:7`, `A6:82`, `A6:95`, `A6:155`, `A6:163` | none |
| E-b | **Definition 1**, `02_model.tex:206–241`, "[Equilibrium]", with list (E1)–(E6) (p. 10) | `04:45`, `05:23` | `A1:4`, `A1:18`, `A2:11`, `A2:92` | comparison `:380`, `:654` ("Definition 1") |
| E-c | **Proposition 1**, `03_competition_information.tex:41–58`, "[Competition and the two returns to information; analytical]" (p. 13) | `02:76`, `03:38`; hand-typed "Proposition~1(c)" at `03:72` | `A1:20` (proof), `A2:22`, `A3:15`, `A3:18`, `A3:19`, `A3:114`, `A3:118`, `A6:22`, `A6:97`, `A6:334`; hand-typed `A1:113` (`named` env.) and `A1:120` | slides `:239`; comparison `:199`, `:480` ("Proposition 1(b)") |
| E-d | **Lemma 1**, `03:97–108`, "[Order probabilities and beliefs; analytical]" (p. 14) | `03:193`; also "Part~(c)" at `03:117` | `A2:28` (proof), `A2:72`, `A2:101`, `A2:150`, `A2:167`, `A3:53`, `A3:90`, `A3:122`, `A5:73`, `A6:38`, `A6:100`, `A6:400` | comparison `:138`, `:200`, `:658` |
| E-e | **Corollary 1**, `03:124–127`, "[High-cost preparation under every profile; analytical]" (p. 15) | `03:117`, `03:129`, `04:50` | `A2:70` (proof), `A2:164` | none (comparison `:66–67` lists only "Corollaries 2 and 3" in the main text) |
| E-f | **Lemma 2**, `03:139–150`, "[Entry and prices; analytical]" (p. 15) | `04:195` | `A2:79` (proof), `A2:129`, `A3:21`, `A3:54`, `A3:55`, `A4:7`, `A4:157`, `A4:179`, `A4:187`, `A4:212`, `A4:239`, `A4:240`, `A4:251`, `A5:75`, `A5:95`, `A8:226` | comparison `:141`, `:201` |
| E-g | **Lemma 3**, `03:168–188`, "[Informed trading; analytical]" (p. 16) | `03:160`, `04:47`, `04:277`, `06:13`, `07:11` | `A2:126` (proof), `A3:23`, `A3:49`, `A4:134`, `A4:176`, `A4:214`, `A4:240`, `A4:253`, `A5:9`, `A5:75`, `A6:79`, `A7:67`, `A7:175` | slides `:328` ("Lemma 3"); comparison `:144`, `:201` |
| E-h | **Proposition 2**, `04_equilibrium_results.tex:11–40`, "[Competition creates competition; analytical]" (p. 17) | `03:118`, `04:111`, `04:124`, `04:160`, `04:166`, `04:205`, `04:253`, `05:65`, `06:11`, `06:20`, `06:29`, `07:6`, `07:7`, `07:27`, `08:10` | `A2:166`, `A3:3`, `A3:11` (proof), `A3:170`, `A3:178`, `A3:201`, `A4:504`, `A5:187`, `A6:49`, `A6:56`, `A6:115`, `A6:126`, `A6:157`, `A6:158`, `A6:190`, `A6:237`, `A6:251` (twice), `A6:260`, `A7:8`, `A7:15`, `A7:26`, `A7:36`, `A9:91` | slides `:370`, `:372`, `:375`, `:652`, `:691`, `:702`, `:794`; comparison `:151`, `:167`, `:169`, `:202`, `:470`, `:572`, `:656`, `:667`, `:724` |
| E-i | **Proposition 3**, `04:296–322`, "[The equilibrium set on the benchmark path; computer-assisted]" (p. 23) | `03:118`, `04:339` (Figure 2 notes) | `A2:166`, `A3:131`, `A4:3`, `A4:287` (proof), `A8:147`, `A8:156`, `A8:240`, `A8:246`, `A9:110` | slides `:456`; comparison `:205`, `:232`, `:253`, `:267`, `:292` (slot column; `:246` and `:262` refer to the Laplace Proposition 3) |
| E-j | **Remark 1**, `04:362–372`, "[Other tie rules]" (p. 24) | `08:61` | none | comparison `:254`, `:294` |
| E-k | **Corollary 2**, `04:380–397`, "[Coexistence at every prior; computer-assisted]", label `prop:priors` (p. 24) | `03:118` | `A2:166`, `A4:3`, `A4:402` (proof), `A9:110` | comparison `:66–67`, `:206` |
| E-l | **Proposition 4**, `05_research.tex:56–69`, "[Research at the benchmark strengths; computer-assisted]" (p. 27) | `05:151` (Figure 3 notes), `05:167`, `05:178` | `A5:3`, `A5:208` (proof), `A5:293`, `A5:313`, `A5:361`, `A9:134` | slides `:476`, `:773`; comparison `:66–67`, `:207`, `:273` |
| E-m | **Corollary 3**, `05:113–121`, "[Research and entry rise together; analytical]", label `prop:researchbranch` (p. 28) | none | `A5:3`, `A5:241` (proof) | slides `:484`, `:776` ("Corollary 3"); comparison `:66–67`, `:207`, `:273` |
| E-n | **Remark 2**, `05:177–184`, "[Tie rules with research]" (p. 29) | none | `A5:4`, `A5:360` (proof) | none |
| E-o | **Remark 3**, `06_robustness.tex:90–97`, "[Continuous order sizes]", the only content of §6.4 `sec:sizes` (p. 33) | none | none | none (`sec:sizes` is cited nowhere either) |

Note on the count: the brief says 16 environments. The files contain 15 (`grep '\begin{(proposition|lemma|corollary|remark|definition|assumption)}'`). The two condition lists, (E1)–(E6) at `02:225` and (E7) at `05:26`, and the three in-text tabulars at `04:261`, `04:279` and `04:299` also act as formal statements. I treat them in Sections 1.2 and 2.

### 1.2 Label systems in the main text

| Label system | Where defined | Main-text uses | Other places that depend on it |
|---|---|---|---|
| (H1)–(H3), hypotheses of Proposition 2 | `04:15–19` | 22 tag occurrences (19 in §4, 3 in §6): e.g. `04:49–51`, `04:54`, `04:57`, `04:111`, `04:117`, `04:148` (Table 2 notes), `04:166`, `06:12`, `06:28` | `A3` (proof, "Each hypothesis is used once" at `A3:112`), `A6:157`, `A9` margins table `tab:margins`; slides `:347`, `:385–387` (named "High-cost window", "Trading-cost window", "Ceiling at r_2"), `:794`; comparison `:202` |
| (E1)–(E6), equilibrium conditions | `02:225–240` | 15: `02:248`, `02:250` (twice), `03:125`, `03:140`, `03:169`, and in Lemma texts; `05:23–24` | used throughout `A1`–`A8` |
| (E7), research optimality | `05:26–29` | 4 in §5 (`05:23`, `05:24`, `05:33`) | `A5:9` |
| Tie-rule names IM, I0, C1, CM | `02:257–265` | about 35: IM 7, I0 6, C1 9, CM 13; e.g. `03:155`, `04:42–43`, `04:124–125`, `04:339`, Remark 1, `05:95` (Table 4 row), `05:102`, `05:147`, Remark 2, `06:82–86`, `08:30–32`, `08:55`, `08:60–62` | `A4` "Other tie rules" and `tab:a4-ties`, `A3:170`, `A5:360`, `A8:246`; comparison `:167`, `:253`, `:667` |
| Form letters N, R, F, Q, T | `04:279–291` | §4.3 and Figure 2 notes; `08:54–62` uses the patterns in words | `A4:258–285`, `tab:a4-set`; comparison `:656` ("the five forms on the path in Section 4.3 and A.4") |

### 1.3 Status tags in the main text

- In environment titles (10): `03:41` analytical; `03:97` analytical; `03:124` analytical; `03:139` analytical; `03:168` analytical; `04:11` analytical; `04:296` computer-assisted; `04:380` computer-assisted; `05:56` computer-assisted; `05:113` analytical. Assumption 1, Definition 1 and the three remarks have no tag.
- Status explanations in the text (2): `04:324–325` "The status is computer-assisted because two monotonicity steps rest on exact Sturm counts: \(J\) and \(\DT(1-\tau)^2\) rise along the path. Every other step is analytical."; `05:71–72` "The equilibrium lists rest on analytical arguments; the strict signs at the benchmark use exact rational and interval arithmetic."
- Inline "(computer-assisted)" (8): `05:128`, `06:38`, `06:54`, `06:72`, `06:80`, `07:86` (Table 5 notes), `07:90`, `08:24`. Table 4 notes (`05:100–102`) give the method ("interval enclosures") instead of a tag.
- "Open" (5): `05:139` "On \((r_N,r_U)\), the equilibrium set with research is open."; `05:152` (Figure 3 notes) "strengths at which the equilibrium set is not characterized"; `07:51` "The trading and preparation equilibrium under the bargaining rule is open."; `07:101` "The seller's choice of a reserve with the whole continuation retained is open."; `08:61–62` "Which equilibrium a process selects is open."
- "Numerical diagnostic": no main-text occurrence. The appendix uses it at `A4:381`.

### 1.4 "Let / Fix / Suppose / Then / Write / Take" passages

| file:line | Exact text (opening) | Proposed fate |
|---|---|---|
| `02:64` | "Write \(G_j(p^-)\) for the probability that a class-\(j\) value falls below the reserve \(p\), and \(D(y)=G_L(y)-G_H(y)\)." | keep (Proposition 1 needs \(D\)) |
| `02:137` | "Write \(\eta(-1)=\eta(1)=\beta\) and \(\eta(0)=1-2\beta\) for the liquidity order distribution." | move to Appendix A (item 3 of the list at `02:130–131` already says it in words) |
| `02:189` | "For a known challenger value \(\theta\), write \(t(\theta)\) for expected target proceeds..." | keep (reference keeps it, ref. 502–505) |
| `02:202–204` | "When the incumbent's distribution matters, I write \(g_j(F)\), \(\DT(F)\), and \(B_F\). For the uniform incumbent on \([0,r]\), I write \(g_j(r)\), \(\DT(r)\), and \(B_r\)." | keep (reference 517–520 is identical) |
| `02:223–224` | "For each order \(x\), write \(f_j(x)=(1-\lambda)\eta(x)+\lambda\sigma_j(x)\) ... and \(e(x)=\rho+(1-\rho)\,\zeta(P(x))\) for entry after it." | \(f_j\) to Appendix A with Definition 1; keep \(e(x)\) as "entry after the order \(x\)" in words |
| `02:275` | "Write \(W_H(F)=\E_H\bigl[F(\theta)\1\{\theta\ge p\}\bigr]\) for the probability that a prepared challenger of class \(H\) wins..." | keep the symbol; it is needed for the ownership condition of Proposition 2 |
| `03:42`, `03:50` | "Let the incumbent's value have a continuous distribution \(F\)..."; "Let \(\tilde F\le F\) be a continuous first-order stochastic strengthening of \(F\)." | keep (inside Proposition 1; reference 584–596 is the same) |
| `03:90–91` | "Write \(\delta_q\) for the point mass at the order \(q\), and \(b_0=(1-\lambda)(1-2\beta)\) for the probability of a liquidity abstention." | move to Appendix A.2 |
| `03:98` | "Fix any order distributions \(\sigma_H\) and \(\sigma_L\)." | moves with Lemma 1 |
| `03:125` | "Let \(g_H\ge g_L\). If \(B(M(\pi))<c_H\), then no profile that satisfies (E1)--(E3)..." | moves with Corollary 1 |
| `03:132` | "When \(g_H>g_L\), write \(\tau=\dots\) for the preparation threshold." | keep \(\tau\); make the display inline |
| `03:140` | "Let \(\DT>0\) and \(g_H>g_L\). Fix a tuple that satisfies (E1)--(E4) and (E6)." | moves with Lemma 2 |
| `03:152` | "Suppose that two orders have one price." | keep as prose (it already reads as an argument) |
| `03:169` | "Let \(\DT\ge0\). Fix a tuple that satisfies (E1), (E4) and (E6), with entry \(e(x)\in[\rho,1]\) after every order." | moves with Lemma 3 |
| `03:177` | "Write \(K_H=e(1)\DT[1-\mu(1)]\) and \(K_L=e(-1)\DT\,\mu(-1)\) for the gross returns of the two correct orders." | keep in one display (Section 2, E-g) |
| `04:7–9` | "Write \(F_0\), \(F_1\) and \(F_2\) for the three incumbent distributions, \(B_i=B_{F_i}\), \(\Delta_i=\DT(F_i)\), \(M=M(\pi)\), \(m=m(\pi)\) and \(\kappa=\kappa(\pi)\)." | delete; write \(B_{F_0}\), \(\DT(F_0)\), \(M(\pi)\) in the statement, as in reference 795–803 |
| `04:12–14`, `04:20` | "Let the classes satisfy Assumption~\ref{ass:classes}. Let \(F_1\) be ... Fix \(0<\pi<1\) ... Suppose" ... "Then each economy has a unique equilibrium outcome." | keep the "Let ... suppose that" frame of a proposition (reference 786–793), remove "Then" |
| `04:255` | "Write \(M=(1+u)/(2+u)\) and \(m=1-M\)." | delete (redefines \(M\); use \(M(1/2)\)) |
| `04:257–260` | "Two functions organize the path. The first is \(J(r)=\dots\). The second is \(\fr(d)=\dots\)" | move to Appendix A.4 (it is already at `A4:11–17`) |
| `04:276` | "Write \(s_+=\lambda\sigma_H(1)\) for the probability of an informed purchase and \(s_-=\lambda\sigma_L(-1)\)..." | move to Appendix A.4 |
| `04:297–298` | "Take the benchmark auction, the prior \(1/2\) and any slot in the band of Proposition~\ref{prop:region}(a). Then \(r_0<r_A<\dots<r_2\)" | keep "Take"; move the threshold order to the appendix statement |
| `04:374–378` | "Coexistence also holds at other priors. For a prior \(\pi\), write \(r_N(\pi)=\dots\) ... let \(r_C(\pi)\) be the largest one ... let \(r_\pi\) solve ..." | move to Appendix A.4 (already at `A4:402–410`) |
| `04:381` | "Take the benchmark auction, any slot, and any prior \(\pi\in(0,1)\)." | moves with Corollary 2 |
| `05:27` | "Hold \(P\) and \(\zeta\) at their values in the tuple. Then \(\hat\lambda\) is the research choice of a best response..." | to prose plus Appendix A.5 |
| `05:30–31` | "Let \(V=\tfrac12\max_qU_H(q)+\tfrac12\max_qU_L(q)\) be the expected trading payoff after a success..." | to words |
| `05:36` | "At intensity \(\lambda\), write \(u_\lambda=\dots\), \(M_\lambda=\dots\) and \(m_\lambda=1-M_\lambda\)" | keep \(M_\lambda\) only, in words |
| `05:57`, `05:114` | "Take the benchmark \(B\) with the research cost..."; "Take the benchmark auction at the prior \(1/2\)..." | merge into one statement of Proposition 4 |
| `05:136–137` | "Against strong incumbents, research sits at the cap. Write \(r_U=\fr\bigl((k+a\lb)(1+\eu)/\rho\bigr)\approx\reg{res_rUR}\)." | keep \(r_U\approx\reg{res_rUR}\); move the formula to Appendix A.5 |
| `06:9` | "Let the cost mix a low component \(H^0\) on \([0,L]\), with weight \(\rho\), and a high component \(H^1\) on \([c_-,c_+]\)." | to words (Section 3.4) |
| `06:26`, `06:93` | "Take classes that satisfy Assumption~\ref{ass:classes}..."; "Take Laplace noise of scale \(s\)..." | keep the first (reword the reference); the second moves with Remark 3 |
| `07:5` | "Hold the incumbent at \(F_1\)." | keep (reference 1308 has "Hold the incumbent at \(r_1\)") |
| `07:23` | "Suppose that one order unit is \(z\) shares per share of float." | keep; rename \(z\) (collision, Section 3.2) |

### 1.5 Paragraphs that start with notation

- `02:62–65`: classes, prior, \(G_j\), \(G_j(p^-)\), \(D(y)\), then "Two restrictions rank the classes." Acceptable; the reference does the same (ref. 313–318).
- `02:154–161`: "Two numbers summarize the slot." \(b\), \(u\), \(1+u\), then the display `eq:bounds`. Keep; it is short and the bounds carry the paper.
- `02:189–204`: §2.4 opens with \(t(\theta)\), \(g(\theta)\), \(t_j\), \(g_j\), \(\DT\), \(B(\mu)\), \(g_j(F)\), \(B_F\), \(g_j(r)\), \(B_r\) before it says what an equilibrium is. The reference opens §2.4 with the equilibrium concept in words (ref. 490–500) and puts the payoff notation second. Recommend that order.
- `03:89–95`: §3.2 opens with \(\delta_q\), \(b_0\) and the odds-form display `eq:odds`.
- `03:132–137`: "When \(g_H>g_L\), write \(\tau=\dots\)".
- `04:5–9`: §4.1 ends its first paragraph with nine symbols (`04:7–9`).
- `04:255–274`: §4.3 has "Write \(M\) ... Two functions organize the path ... Six strengths mark the changes", then a definitions table.
- `04:276–294`: "Write \(s_+\) ... Five forms of the high-class order appear on the path", then a second table.
- `04:374–378`: four new objects for the prior extension.
- `05:35–42`: "Two functions of the intensity describe the branch...", with \(u_\lambda\), \(M_\lambda\), \(m_\lambda\) and \(\lambda_E(r)\) in display.
- `06:9–12`: \(H^0\), \(L\), \(H^1\), \(c_-\), \(c_+\).

### 1.6 Main-text pointers to appendix propositions

There are 21 pointers: 8 in §4 (`prop:region` four times, `prop:control` three times), 1 in §5, 4 in §6, 3 in §7 and 5 in §8. The reference uses the same device ("Proposition A.3", "A.5", "A.9"), so this register matches. No change is needed, apart from one pointer for each paragraph at most.

---

## 2. Decision for each environment

### 2.1 The four numbered propositions, and why

Test: each numbered proposition in the main text must carry one claim of the abstract (`main.tex:85–97`). Every other formal statement supports a proof and goes to Appendix A.

| Keep as | Abstract claim it carries | Why it is numbered |
|---|---|---|
| **Proposition 1** (competition and the two returns to information; analytical) | "A stronger incumbent lowers the buyer's acquisition profit at every belief ... It also makes target proceeds more sensitive to that quality" (`main.tex:86–88`) | It is the mechanism. The reference keeps it as Proposition 1 (ref. 582–604). The hand-typed "Proposition~1(c)" at `03:72`, `A1:113` and `A1:120` needs it to stay number 1. |
| **Proposition 2** (competition creates competition; analytical) | "On an open set of parameters, a stronger incumbent turns an uninformative price into an informative one, with unique trading and preparation outcomes. Challenger entry rises..." (`main.tex:91–93`) | It is the main result (reference Proposition 2, ref. 785–827). |
| **Proposition 3** (coexistence on the benchmark path; computer-assisted) | "informative and uninformative equilibria coexist, and entry rises weakly with incumbent strength along the informative branch" (`main.tex:93–95`) | The reference has the same slot (Proposition 3, ref. 1004–1021). The slot draft makes it stronger: it gives the whole set, not three points. |
| **Proposition 4** (competition creates research; part (a) analytical, part (b) computer-assisted) | "When the investor pays for research, research and entry rise together over a range of strengths" (`main.tex:95–96`) | §5 has no counterpart in the reference, and this is its only result. The merge costs little: `prop:researchbranch` has no `\ref` outside `A5:3` and `A5:241`. |

The abstract claim on price access (`main.tex:96–97`) stays as prose plus Proposition A.8. The reference does the same (prose plus its Proposition A.9, ref. 1307–1353).

Fallback for three propositions: move Proposition 4 to Appendix A.5 as Proposition A.15, and let §5 state the comovement in prose with a pointer. §5 then reads like the robustness sections of the reference. I recommend four.

amsthm detail: the `plain` theorem style at `main.tex:34–35` prints "**Proposition 1** (title; status)." followed by an italic statement. That already looks like the reference's inline bold paragraphs. The four kept propositions can stay as `proposition` environments.

### 2.2 Decision table

Codes: (a) keep as a numbered proposition; (b) fold into prose; (c) move to Appendix A. All proposed manuscript sentences below use the reference register.

#### E-a. Assumption 1 (`02:67–73`): (b) fold into prose

The template is reference lines 318–330. Replace `02:65–76` with:

> Two restrictions rank the classes. The high class, or high-value class, dominates the low class in the sense of first-order stochastic dominance, and both class supports lie above the reserve, so that every value meets it:
> \[ G_H(y)\le G_L(y)\quad\text{for every }y,\qquad G_H(p^-)=G_L(p^-)=0. \tag{\ref{eq:classes}} \]
> Under these restrictions competition widens the class difference in target proceeds under every incumbent distribution (Proposition~\ref{prop:returns}).

- Give the display a number (`\label{eq:classes}`).
- Each of the 15 citing sites changes "Assumption~\ref{ass:classes}" to "the class ranking~\eqref{eq:classes}" or, as in the reference, "the restrictions of Section~\ref{sec:values}". The sites are `02:75`, `03:39`, `03:54`, `03:71`, `03:75`, `04:12`, `06:27`, `A1:106`, `A1:155`, `A1:156`, `A3:7`, `A6:82`, `A6:95`, `A6:155` and `A6:163`.
- `A1:155` is a paragraph title, "Scope of Assumption~\ref{ass:classes}.". Rename it "Scope of the class ranking."

#### E-b. Definition 1 (`02:206–241`): (b) prose in the main text, and (c) the formal tuple to the opening of Appendix A

The template is reference lines 490–500. Replace `02:206–246` with:

> An equilibrium specifies, for each class, a distribution over the three orders, the market makers' posterior and price after each order, the challenger's belief at each price, its preparation choice at each price and cost, and truthful bids. The investor can mix, and wrong-signed orders are allowed. Every order has positive probability in both classes, because a liquidity trader can place it, so Bayes' rule defines the posterior after every order and no off-path belief enters. Prices are competitive, a high-cost challenger prepares when gross profit at its belief exceeds \(c_H\), and a zero-cost challenger, whose gross profit is an expected auction rent and never negative, prepares after every price. The investor's order maximizes
> \[ U_j(q)=q\,\bigl[t_0+e(q)(t_j-t_0)-P(q)\bigr]-k|q| \]
> at the candidate's prices and entry, where \(e(q)\) is entry after the order \(q\). Appendix~\ref{app:proofs} states the six conditions in full.

- Keep `eq:price` (`02:251–253`). Keep the "Two comparisons recur" paragraph (`02:267–271`); the reference keeps it (ref. 493–500).
- Tie rules, `02:257–265`: reduce them to one sentence in the reference register: "An indifferent investor may mix over its best orders, the standard best-response condition, and an indifferent high-cost challenger prepares." Move the alternatives I0 and CM, and the sentence "A remark states each place where I0 or CM changes a conclusion", to Appendix A.4, beside `tab:a4-ties`.
- Destination: the unnumbered opening of Appendix A, after `\section{Proofs}` (`main.tex:139`) and before `\subsection{Acquisition payoffs}`. The text that opens `A1_payoffs.tex:1–4` already sits there. Do not create a new numbered subsection: that would renumber A.1–A.9 and break the hard-typed "Appendix A.1 to A.9" at comparison `:66` and "(A.5)" at slides `:794`.
- The location must come before A.1, because `A1:4` and `A1:18` cite Definition 1 and check (E6).
- Counter: `main.tex:124–138` gives proposition, lemma, corollary, table and figure the prefix A, but not definition. Add `\renewcommand{\thedefinition}{A.\arabic{definition}}` (and `\theHdefinition`), or the definition prints as "Definition 1" in the appendix.
- Refs to carry: `04:45`, `05:23`, `A1:4`, `A1:18`, `A2:11`, `A2:92`; comparison `:380` and `:654` ("Definition 1" becomes "Definition A.1" if the counter changes).

#### E-c. Proposition 1 (`03:41–58`): (a) keep

- Title: "Competition and the two returns to information; analytical". This is the reference title (ref. 582–583).
- Change only "Under Assumption~\ref{ass:classes}" at `03:54` (see E-a).
- The intuition paragraph is already in place (`03:60–73`, "The proof works one incumbent value at a time...") and matches reference 606–622.

#### E-d, E-e, E-f, E-g. Lemmas 1–3 and Corollary 1 (`03:89–206`): (b) prose with two displays, and (c) the formal statements to Appendix A.2

The template is reference §3.2–3.3 (ref. 658–771). That text closes with "Propositions A.1 and A.2 give the formal statements." Appendix A.2 already proves all four results (`A2:28`, `A2:70`, `A2:79`, `A2:126`), so only the statements move.

Proposed §3.2 (replaces `03:89–161`):

> A liquidity order in the same direction is always possible, and this bounds what any order can reveal. Each class reaches a given nonzero order through a liquidity trader with probability \(b\), and the informed investor adds at most \(\lambda\), so the likelihood ratio of the order lies between \(1/(1+u)\) and \(1+u\). By Bayes' rule, the posterior after every order lies in the interval \([m(\pi),M(\pi)]\) of \eqref{eq:bounds}, under every investor strategy, mixed or pure; when the high class buys and the low class sells, the posteriors after a sale, no order and a purchase are \(m(\pi)\), \(\pi\) and \(M(\pi)\). The challenger's belief at a price is an average of the posteriors of the orders with that price, so it obeys the same bounds. A preparation decision that needs a belief above \(M(\pi)\) therefore follows no price: once gross profit at the top posterior falls below \(c_H\), no order recruits a high-cost challenger, in or out of equilibrium. This is the ceiling of the model.
>
> Gross profit covers the high cost exactly when the belief reaches the preparation threshold \(\tau=(c_H-g_L)/(g_H-g_L)\). A zero-cost challenger prepares after every price, so entry after every order is at least \(\rho\), and competitive pricing gives \eqref{eq:price}. When the classes differ in target proceeds, the price then rises strictly with the posterior, so two orders with one price have one posterior, and the challenger reads the market makers' posterior from the price. High-cost preparation follows exactly the orders whose posterior reaches \(\tau\). Appendix~\ref{app:beliefs} gives the formal statements.

Proposed §3.3 (replaces `03:165–188`; keep `03:190–206` almost as it is):

> Rational pricing removes the anticipated increase in proceeds from the investor's advantage. What remains is the gross return of a purchase in class \(H\) and of a sale in class \(L\),
> \[ K_H=e(1)\,\DT\,[1-\mu(1)],\qquad K_L=e(-1)\,\DT\,\mu(-1),\qquad \rho\,\kappa(\pi)\,\DT\le K_H,\,K_L\le\DT, \]
> with \(\kappa(\pi)=\min\{m(\pi),1-M(\pi)\}\). A wrong-signed order earns at most \(-k\), so it never pays. Class \(H\) buys when \(K_H\) exceeds \(k\) and abstains when it falls short, and class \(L\) compares \(K_L\) with \(k\) in the same way.

- Reword `03:190–206`, which then has no lemma parts to cite: "The lower bound in part~(c)" (`03:192`) becomes "The lower bound"; "the posterior bounds of Lemma~\ref{lem:beliefs}" (`03:193`) becomes "the posterior bounds"; "Part~(d) splits the investor's problem" (`03:204`) becomes "Each return depends only on the posterior and entry after its own order, which splits the investor's problem."
- Move to A.2 with the lemmas: `03:113–119` (\(\beta\le1/3\) and the "parts (a), (b) and (d) only" sentence) and `03:155–156` (the rule-CM clause of Lemma 2(d)). `A2:163–167`, "Where \(\beta\le1/3\) enters.", already says the same, so the main-text copy is a duplicate.
- Environments: move the lemmas as `lemma` and the corollary as `corollary`. Then they become Lemma A.1–A.3 and Corollary A.1, and the Proposition A.1–A.14 numbering does not change. No file hard-types "Lemma A." or "Corollary A.", so the shift of the A.4–A.5 lemmas (A.1–A.10 become A.4–A.13) and of `cor:purchasesonly` (A.1 becomes A.3, after Corollary 1 in A.2 and Corollary 2 in A.4) breaks nothing.
- Refs to carry: every row of E-d to E-g in Section 1.1. The main-text uses become prose or section pointers: `03:160` and `04:47` become "the trading bound of Section~\ref{sec:informed}"; `04:50` becomes "the ceiling of Section~\ref{sec:inference}"; `04:195`, `04:277`, `06:13` and `07:11` become `\ref` to Lemma A.x, or prose.
- Slides `:328` ("Lemma 3") and comparison `:138`, `:141`, `:144`, `:200`, `:201` and `:658` change number.

#### E-h. Proposition 2 (`04:11–40`): (a) keep, with a tighter statement

- Title: "Competition creates competition; analytical".
- Keep the tags (H1)–(H3) on displayed conditions, as the reference tags (A1) and (A2) (ref. 795–803). They are cited 22 times in the main text and also in `A3`, `A6:157` and `tab:margins`, slides `:347`, `:385–387` and `:794`, and comparison `:202`.
- Give the conditions economic names in the intuition paragraph, and use the names that the slides already use: the high-cost window (H1), the trading-cost window (H2), the ceiling (H3).

Proposed statement (reference register; every fact of `04:11–40` is kept):

> Let the classes satisfy the ranking~\eqref{eq:classes}, let \(F_1\) be a continuous first-order stochastic strengthening of the continuous incumbent distribution \(F_0\), and let \(F_2\) strengthen \(F_1\) in the same sense. Fix \(0<\pi<1\), \(0<\rho<1\), \(k>0\) and a slot \((\lambda,\beta)\), and suppose that
> \[ B_{F_0}(\pi)<c_H<B_{F_1}(M(\pi)), \tag{H1}\]
> \[ \DT(F_0)<k<\rho\,\kappa(\pi)\,\DT(F_1), \tag{H2}\]
> \[ B_{F_2}(M(\pi))<c_H. \tag{H3}\]
> Each economy then has a unique equilibrium outcome. (i) With the weak incumbent \(F_0\), the investor does not trade, every posterior equals \(\pi\), every order has the price \(t_0+\rho\,[t_L-t_0+\DT(F_0)\pi]\), the price carries no information, and entry equals \(\rho\). (ii) With the strong incumbent \(F_1\), the investor buys after good news and sells after bad news; the posteriors after a sale, no order and a purchase are \(m(\pi)\), \(\pi\) and \(M(\pi)\), the three prices are strictly ordered, and only a purchase recruits the high-cost challenger, so entry is \(\rho+(1-\rho)(b+\pi\lambda)>\rho\). High-class ownership rises from \(\pi\rho W_H(F_0)\) to \(\pi[\rho+(1-\rho)(b+\lambda)]W_H(F_1)\), where the bracket is entry given class \(H\), if and only if \([\rho+(1-\rho)(b+\lambda)]\,W_H(F_1)>\rho\,W_H(F_0)\). (iii) With the very strong incumbent \(F_2\), the investor again buys and sells, with the same posteriors, so the three prices differ and the price stays informative, but entry returns to \(\rho\).

What this removes: \(\delta_0\), \(\delta_{\pm1}\), \(e_H\), \(\Ent_1\), \(B_i\), \(\Delta_i\), the shorthand \(M\), \(m\), \(\kappa\) without \(\pi\), and the opening "Write" paragraph (`04:7–9`).

Intuition paragraph: put `04:47–50` ("The hypotheses fix trading before any order profile is known...") first. Then put the window `04:54–58`, ownership `04:60–64` and part (iii) `04:66–68`.

- Shorten `04:42–45` to one bold sentence: "Every comparison in the proof is strict, so the outcome does not depend on how ties are broken; Appendix~\ref{app:prop2} states the three equilibrium tuples." This keeps the fact "same unique outcome under all four pairs of tie rules" without the rule names.
- `04:51–52` ("the proof uses each hypothesis once and ... (H1) cannot be weakened") is already at `A3:112`. It can leave the main text.

#### E-i. Proposition 3 (`04:296–322`): (a) keep, with a short statement in the main text and the full statement in Appendix A.4

- Title: "Coexistence on the benchmark path; computer-assisted". It is close to the reference's "coexisting informative equilibria" (ref. 1005).
- Before the statement, define the strengths in words. This replaces the definitions table at `04:261–274`. All five stay in the main text, because the intuition paragraphs (`04:329–330`, `04:359–360`) and the Figure 2 notes (`04:341–342`) use \(r_J\) and \(r_S\):

> Five strengths organize the path. At \(r_A\), a purchase that just reaches the threshold and recruits earns exactly the trading cost; at \(r_F\), a full purchase that recruits earns it; at \(r_N\), a unit order against an uninformative price earns it, so no trade stops being an equilibrium above \(r_N\); at \(r_J\), a purchase that just reaches the threshold without recruitment earns it; and at \(r_S\), a full sale earns it.

Proposed statement:

> Take the benchmark auction, the prior \(1/2\) and any slot in the band of Proposition~\ref{prop:region}(a). An equilibrium exists at every strength on the path from \(r_0\) to \(r_2\), and Appendix~\ref{app:coexistence} lists the whole equilibrium set. (a) No informed trade and an informative equilibrium coexist exactly on \([r_A,r_N]\). (b) On the informative branch that coexists with no trade, entry is \(\rho+(1-\rho)\min\{b\DT(r)/(2k),\,b+\lambda/2\}\); it is continuous, rises strictly on \([r_A,r_F]\) and is constant on \([r_F,r_N]\), and it keeps this value along full purchases up to \(r_C\) and equals \(\rho\) above \(r_C\).

- The full statement goes to A.4 in a `named` environment, "Proposition 3 (full statement)", the same device as "Proposition 1(c)" at `A1:113`. It holds the threshold order \(r_0<r_A<r_F<r_N<r_J<r_S<r_1<r_C<r_2\), the strength-by-form table of `04:299–312`, and the entry formulas for N, Q, R and F (`04:313–314`).
- The forms table `04:279–291` and the definitions table `04:261–274` duplicate `A4:258–285` and `tab:a4-thresholds` (`A4:116`). `tab:a4-set` (`A4:385`) gives the same set in numbers. Moving them deletes duplicates; only the symbolic set table is new to A.4.
- `04:324–325`: rewrite it as a proof idea, which is the reference's form after its Proposition 3 (ref. 1023–1031): "Two monotonicity steps of the proof rest on exact Sturm counts; every other step is analytical (Appendix~\ref{app:coexistence})."
- Keep the threshold values and the entry values at `04:326–330`, including `\reg{rJ}` and `\reg{rS_B}`.
- Keep the intuition paragraphs `04:347–360`.
- Refs to carry: the row E-i in Section 1.1. Comparison `:656` ("the five forms on the path in Section 4.3 and A.4") becomes "A.4".

#### E-j. Remark 1 (`04:362–372`): (c) move to Appendix A.4, "Other tie rules" (`A4:477`)

- The content is already in `tab:a4-ties` and `A4:516–521`. The `\reg` values `entry_th_r155_B`, `entry_th_r160_B` and `entry_th_r165_B` are already at `A4:373–374`.
- Check whether A.4 states the clause "Its entry falls strictly from \(\Ent_R(r_A)\) at \(r_A\) to \(\rho\) at \(r_J\)" (`04:363–364`). If it does not, carry it.
- Main text: no sentence needed. Figure 2 notes (`04:339–340`) keep the dashed line in words: "The thin dashed line is the threshold pair, an equilibrium only if an indifferent high-cost challenger may prepare with any probability (Appendix~\ref{app:coexistence})."
- Refs: `08:61` changes to "Appendix~\ref{app:coexistence}". Comparison `:254` and `:294` ("Remark 1") change.
- Counter: `remark` has no A prefix (`main.tex:124–138`). Either extend the counter block, or put the content in the existing "Other tie rules" paragraph with no environment. I recommend the paragraph.

#### E-k. Corollary 2 (`04:374–406`): (c) move to Appendix A.4, plus two sentences in the main text

- The proof is already at `A4:402`. The definitions at `04:374–378` repeat `A4:403–410`.
- Proposed main-text text (replaces `04:374–406`):

> Coexistence also holds away from the even prior. At the benchmark slot, the informative branch starts at the same strength \(r_A\) for every prior between \(\approx\reg{piA_lo_B}\) and \(\approx\reg{piA_hi}\), and later, where the prior reaches the threshold, for priors up to \(\approx\reg{pimax}\); below the first prior even the top posterior cannot reach the threshold once a purchase can pay for itself, and from the last prior on the uninformative equilibrium fails before the prior falls below the threshold. Corollary~\ref{prop:priors} in Appendix~\ref{app:coexistence} gives the coexistence set at every prior.

- The rule-CM sentence `04:404–406` is already in `A4:477–490`.
- `\reg` path: `piA_lo_B`, `piA_hi` and `pimax` stay in the main-text sentence and are also in A.4.
- Refs: `03:118` and `A2:166` change to Corollary A.x by `\ref`. Comparison `:66–67` and `:206` change.

#### E-l and E-m. Proposition 4 and Corollary 3 (`05:56–69`, `05:113–121`): (a) merge into one Proposition 4

Proposed statement:

> **Proposition 4** (Competition creates research; part (b) computer-assisted). Take the benchmark auction at the prior \(1/2\), with \(0<\beta\le1/3\) and \(a>0\). (a) On the strengths with \(\DT(r)>2k\), research \(\lambda_R(r)\) is continuously differentiable and rises strictly in \(r\); wherever the research branch is an equilibrium, entry \(\rho+(1-\rho)[\beta+(1/2-\beta)\lambda_R(r)]\) and high-class ownership \(\tfrac12[\rho+(1-\rho)(\beta+(1-\beta)\lambda_R(r))]\) rise strictly with \(r\). (b) At the benchmark, with the research cost \(a=\reg{res_a}\) and the cap \(\lb=\reg{res_cap}\), the weak incumbent \(r_0\) has a unique equilibrium, with no research and no trade, and entry \(\rho\). At each \(r\in\{\reg{str_r155},\reg{str_r160},\reg{str_r165}\}\) there are exactly two equilibria: one without research, with entry \(\rho\), and the research branch, with research \(\lambda_R(r)\) between \(\lambda_E(r)\) and the cap, in which class \(H\) buys after a success, class \(L\) abstains and only a purchase recruits. At \(r_1\) and \(r_2\) the unique equilibrium has research at the cap and trade in both directions, and it is the equilibrium of Proposition~\ref{prop:ccc} with \(\lambda=\lb\); entry is \(\reg{res_entry_r1}\) at \(r_1\) and \(\rho\) at \(r_2\).

- "The investor's tie rule plays no role at these six strengths" (`05:68`) moves to the intuition paragraph as "Every trade choice at the six strengths is strict."
- Intuition: keep `05:106–111` and `05:123–125`. Move `05:162–164` ahead of the region paragraph.
- `05:71–72`: rewrite as a proof idea: "The equilibrium lists follow from analytical arguments, and exact rational and interval arithmetic settles the strict signs at the benchmark."
- Appendix: `A5:241` "Proof of Corollary~\ref{prop:researchbranch}" becomes "Proof of Proposition~\ref{prop:research}(a)". `A5:208` becomes "...(b)". Retire the label `prop:researchbranch`, or keep it as a second label on part (a).
- Refs to carry: slides `:476`, `:484`, `:773`, `:776` (drop "Corollary 3"); comparison `:66–67`, `:207`, `:273`.

#### E-n. Remark 2 (`05:177–184`): (c) move to Appendix A.5, before its existing proof (`A5:360`)

- `\reg` path: `res_th_entry_r155/160/165` are already at `A5:363–364`. `\reg{res_rC}` appears only in Remark 2 (`05:182`), so carry it into the A.5 statement.
- Move Table 4's last row, "Entry in the threshold equilibrium (rule CM)" (`05:95`), and the note sentence "The last row exists only under the challenger rule CM." (`05:102`) to A.5 with it. The values are already at `A5:363–364`.
- Main text: the first clause of the remark, "Research never has a tie", becomes one sentence in §5. `05:162` already says it: "The quadratic cost gives a unique research response, so no equilibrium needs indifference over research."

#### E-o. Remark 3 (`06:90–97`): (b) fold into a footnote in §2.3, and delete §6.4

Nothing cites the remark or `sec:sizes`. Proposed footnote after `02:169`:

> The unit menu keeps every order on path, so no off-path belief enters the analysis; a menu of continuous sizes needs a convention for the sizes that no class uses in equilibrium, as in \citet{EdmansGoldsteinJiang2015}. Additive Laplace flow of scale \(s\) with full unit orders also keeps every size on path: the largest likelihood ratio of a favorable flow is \(\eu^{2/s}\), so the two set-ups share the posterior bounds when \(1+u=\eu^{2/s}\), and they differ in the probability with which each class reaches the top posterior.

#### Condition lists (E1)–(E7)

- (E1)–(E6) leave with Definition 1.
- Proposed text for (E7), replacing `05:21–33`:

> Market makers and the challenger do not observe the research choice and price at a conjectured intensity. The prior is \(1/2\) throughout this section. In an equilibrium with research, market makers and the challenger use the equilibrium intensity, and that intensity is the investor's best research choice when prices and the entry rule stay at their equilibrium values; the order after a success must also be optimal, including after a deviation from zero research. The best research choice is unique: it equals the expected trading payoff after a success divided by \(a\), capped at \(\lb\), so research never has a tie.

  The formal tuple \((\hat\lambda,\sigma_H,\sigma_L,\mu,P,\bar\mu,\zeta)\) and (E7) go to the opening of A.5. `A5:9` already restates them.
- `05:35–42`: keep only "the recruitment intensity \(\lambda_E(r)\), the research level at which a full purchase just reaches the threshold" and "\(M_\lambda\), the top posterior at intensity \(\lambda\)". The \(\lambda_E\) formula goes to A.5 (`A5:17` "Derived functions." already holds the derived functions).

### 2.3 Constraints for the rewrite

1. **Counters.** `main.tex:124–138` gives proposition, lemma, corollary, table and figure the prefix A in the appendix, but not definition, assumption or remark. Anything of these kinds that moves into the appendix prints as "Definition 1" or "Remark 1" unless the block is extended.
2. **Placement of Definition 1.** It must come before A.1, in the unnumbered opening of Appendix A. A new numbered subsection would shift A.1–A.9.
3. **Numbering.** Move lemmas as lemmas and corollaries as corollaries. Then the Proposition A.1–A.14 counter does not change. The hard-typed "Proposition A.3/A.8/A.11–A.14" (slides `:429`, `:517`, `:545`) and "Propositions A.1 to A.14" (comparison `:67`) stay correct.
4. **Proposition 1(c).** It is hard-typed at `03:72`, `A1:113` and `A1:120`, so Proposition 1 must keep number 1.
5. **Main-text numbering after the change.** Propositions 1–4 keep their numbers. There is no main-text lemma, corollary, remark, definition or assumption.

### 2.4 Where each `\reg` macro of a moved block goes

| Moved block | Macros inside | Destination | Already present there? |
|---|---|---|---|
| Remark 1 (`04:364–366`) | `entry_th_r155_B`, `entry_th_r160_B`, `entry_th_r165_B`, `str_r155/160/165` | A.4 "Calibration B." | yes, `A4:373–374` |
| Corollary 2 text (`04:399–406`) | `piA_lo_B`, `piA_hi`, `pimax` | stay in the main-text sentence; A.4 | yes, A.4 |
| §4.3 in-text tables (`04:261–274`, `04:279–291`, `04:299–312`) | none (symbolic only) | A.4 | — |
| Remark 2 (`05:182–183`) | `res_rC`, `res_entry_cap` | A.5 statement | `res_entry_cap` yes; **`res_rC` no**, so carry it |
| Table 4, CM row (`05:95`) | `res_th_entry_r155/160/165` | A.5 | yes, `A5:363–364` |
| `05:137` formula for \(r_U\) | `res_rUR` | stays in the main text as \(r_U\approx\reg{res_rUR}\) | — |
| Lemmas 1–3, Corollary 1, Definition 1, Remark 3 | none | — | — |

---

## 3. Notation load

### 3.1 Symbols used fewer than three times after the definition

The counts are main-text occurrences after the defining occurrence. The `u` and `b` patterns were noisy and are left out; both are clearly in heavy use.

| Symbol | Defined at | Uses after the definition | Proposal |
|---|---|---|---|
| \(\mathcal E\) (the tuple) | `02:209` | 1 (`02:238`) | to the appendix with Definition 1 |
| \(\Ent_1\) | `04:29` | 0 | delete; write the formula |
| \(e_H\) | `04:31` | 1 | delete; write \(\rho+(1-\rho)(b+\lambda)\) |
| \(\Ent_F\) | `04:314` | 1 | to the A.4 full statement |
| \(\Ent_R\) | `04:313`; again `05:118` with **another meaning** | 1 each | collision; use words in the main text |
| \(p_H\) | `07:100`, never defined | 0 | "a reserve of about \(\reg{p2_reserve_ph}\)" |
| \(r_*\) | `04:377` | 1 | to A.4 |
| \(S(B)\) | `06:69` | 1 | "the signal example" |
| \(\vartheta\) | `08:8` | 1 (`08:18`) | "the informed share", and write \(u/(2+u)\) once |
| \(u_\lambda\) | `05:36` | 2, both inside the next definitions | delete |
| \(m_\lambda\) | `05:37` | 2 | write \(1-M_\lambda\) |
| \(V\) (research value) | `05:31` | 2 | words (see (E7) above); also collides with \(V_T\) |
| \(H^0\), \(H^1\) | `06:9–10` | 2 | words (Section 3.4) |
| \(c_-\), \(c_+\) | `06:10` | 2 | words |
| \(v_*\) | `06:32` | 2 | "the lowest value at which the classes start to differ above the reserve" (`06:32` already says it) |
| \(\varepsilon\) (cost band) | `06:16` | 2 | "half-width" |
| \(\tilde F\) | `03:50` | 2, inside Proposition 1 | keep; the statement needs it |
| \(G_j(p^-)\) | `02:64` | 2 | keep in the ranking display |
| \(J(r)\) | `04:257` | 3, all in the tables that move | to A.4 (already at `A4:11–14`) |
| \(\fr(d)\) | `04:258` | 5, all in the threshold definitions and \(r_U\) | to A.4 and A.5 |
| \(b_0\) | `03:91` | 5, all in Lemma 1 and its discussion | to A.2 |
| \(\delta_q\) | `03:90` | 15, all as order-profile notation (Proposition 2, Table 3 rows `04:206`, `04:224`) | words ("no trade", "buy and sell"), as the reference writes \((q_H,q_L)=(1,-1)\) |
| \(s_+\), \(s_-\) | `04:276` | 6, in the forms table | to A.4 |
| \(\pi_A^{\mathrm{lo}}\), \(\pi_A^{\mathrm{hi}}\), \(\pi_{\max}\), \(r_\pi\), \(r_N(\pi)\), \(r_C(\pi)\), \(C(\pi)\) | `04:374–384` | Corollary 2 only | to A.4 |
| \(\zeta\), \(\bar\mu\), \(\bar P\), \(f_j\), \(\eta(\cdot)\), \(\hat\lambda\) | `02`, `05` | Definition 1, Lemma 1, (E7) only | to the appendix |
| \(B_i\), \(\Delta_i\) | `04:8` | 7 each, §4.1 only | use \(B_{F_i}\) and \(\DT(F_i)\), as in the reference |
| \(U_j(q)\) | `02:236` | 10, inside (E5), Lemma 3 and \(V\) | keep one display in the §2.4 prose; drop the rest |

### 3.2 Collisions and redefinitions

- **\(B\)**: gross profit \(B(\mu)\), \(B_r\), \(B_F\) and \(B_0\) to \(B_2\), but also "The benchmark, which I call \(B\)" (`04:72`), "benchmark \(B\)" (`04:338`, `05:57`, `05:147`, `06:77`, `06:82`) and "parameter vector \(S(B)\)" (`06:69`). In the main text, say "the benchmark". Keep "calibration B" in the appendix and the tables.
- **\(L\)**: the low class, and also the top of the low cost component, "\(H^0\) on \([0,L]\)" with "\(L<B_1(m)\)" (`06:9–12`).
- **\(d\)**: the argument of \(\fr(d)\) (`04:258`) and the challenger's signal accuracy \(d\) (`06:62`).
- **\(z\)**: research intensity "\(z\in[0,\lb]\) at the cost \((a/2)z^2\)" (`05:4`), which then turns into \(\lambda\), \(\hat\lambda\) and \(\lambda_R\) in the same section; also the order-unit scale "one order unit is \(z\) shares per share of float" (`07:23`). Use \(\lambda\) for research from `05:4` on.
- **\(\Ent_R\)**: entry on form R (`04:313`) and entry on the research branch (`05:118`). **\(r_R\)** (the start of the research branch) also sits close to form R.
- **\(M\)** has three meanings: "\(M=M(\pi)\)" (`04:9`), "\(M=(1+u)/(2+u)\)" (`04:255`, which is \(M(1/2)\)), and \(M_\lambda\) (`05:36`). Use \(M(\pi)\) and \(M(1/2)\) throughout, and keep \(M_\lambda\) only in §5.
- **\(V\)**: the research value (`05:31`) against the terminal payoff \(V_T\).
- **\(C\)**: the cost \(C\) (`02:98`) against the coexistence set \(C(\pi)\) (`04:381`).
- **\(H\)**: the high class against the cost components \(H^0\), \(H^1\) (`06:9–10`).
- **\(a\)**: the research cost \(a\) against the investor accuracy \(a_T\) (`06:62`). This is minor.
- **Euler's number.** `04:78–79` reads "\(\eu\) is Euler's number; I print it upright to separate it from entry \(e(x)\)." The notation defends itself here. Proposed: "The largest likelihood ratio of an order is Euler's number, \(1+u=\eu\)."

### 3.3 Displays that only define notation

| file:line | Display | Proposal |
|---|---|---|
| `02:207–210` | \(\mathcal{E}=(\sigma_H,\sigma_L,\mu,P,\bar\mu,\zeta)\) | to the appendix |
| `02:140–142`, `eq:profit` | \(q[V_T-P(q)]-k|q|\); not cited anywhere | inline |
| `02:192–194` | \(t_j=\E_j[t(\theta)]\), \(g_j=\E_j[g(\theta)]\) | inline, as in reference 508–511, or keep |
| `02:199–201` | \(B(\mu)=g_L+\mu(g_H-g_L)\) | inline (the reference has it inline, ref. 516) |
| `03:93–95`, `eq:odds` | Bayes' rule in odds form; cited at `03:112`, `A2:29`, `A2:44` | to A.2 |
| `03:133–135` | \(\tau=(c_H-g_L)/(g_H-g_L)\) | inline |
| `03:171–176` | the six payoffs \(U_H(\cdot)\), \(U_L(\cdot)\) | replace with the \(K_H\), \(K_L\) display (E-g) |
| `04:28–30`, `04:33–35` | \(\Ent_1\); the ownership inequality | inline in the statement (E-h) |
| `04:261–274`, `04:279–291` | the threshold definitions table; the forms table | to A.4 (duplicates) |
| `04:383–385` | \(C(\pi)=\{\dots\}\) | to A.4 |
| `05:26–29` | the (E7) list | prose |
| `05:39–41` | the formula for \(\lambda_E(r)\) | to A.5 |

Keep these displays. They carry economics, and the reference keeps their counterparts: `eq:order` (`02:88–90`), `eq:bounds` (`02:158–161`), `eq:price` (`02:251–253`), \(t+g=\theta\) (`03:12–14`), `eq:payoffs` and `eq:derivatives` (`03:20–35`), `eq:spread` (inside Proposition 1), the class-gap identity (`03:76–78`), the (H1)–(H3) displays, and `eq:research` (`05:47–49`).

### 3.4 Places where a sentence of economics replaces a formula

Proposed manuscript text uses the reference register.

- `02:137` (\(\eta\)). Delete. The list item at `02:130–131` already says "It sells, abstains, or buys one unit with probabilities \(\beta\), \(1-2\beta\), and \(\beta\)".
- `02:275–276` (\(W_H\)). Keep the symbol and lead with the words: "the probability \(W_H(F)\) that a prepared high-class challenger outbids an incumbent drawn from \(F\)".
- `03:197–199` (the \(\kappa\) algebra). Replace with: "The bound is largest at an even prior, where it equals \(1/(2+u)\); the class the prior favors binds, because the price already leans toward it." The reference uses the same idea (ref. 755–758).
- `04:257–274` (\(J\), \(\fr\), six thresholds). Replace with the five-strength sentence of E-i.
- `05:30–33` (\(V\), \(\min\{\lb,V/a\}\)). Replace with "the expected trading payoff after a success divided by \(a\), capped at \(\lb\)".
- `05:35–42` (\(u_\lambda\), \(M_\lambda\), \(m_\lambda\), \(\lambda_E\)). Replace with: "Research raises the top posterior \(M_\lambda\) that a purchase can reach. The recruitment intensity \(\lambda_E(r)\) is the research level at which a full purchase just reaches the threshold, so a full purchase recruits exactly when research is at least \(\lambda_E(r)\)."
- `05:136–137` (\(r_U\) through \(\fr\) and \(\eu\)). Replace with: "Above a strength \(r_U\approx\reg{res_rUR}\), a bound on every candidate profile forces full orders and research at the cap (Appendix~\ref{app:research})."
- `06:9–12` (the cost law). The template is reference lines 1161–1172:

> The two-point cost law of Section~\ref{sec:values} is not needed. Let the cost mix a low component, with weight \(\rho\), and a high component; either may be atomless or have atoms. If the low component lies below gross profit at the lowest posterior against the strong incumbent, and the high component lies between gross profit at the prior against the weak incumbent and gross profit at the top posterior against the strong one, Proposition~\ref{prop:atomless} keeps parts (i) and (ii) of Proposition~\ref{prop:ccc} under the trading-cost window (H2).

- `06:21–22` (full-order entry \(\rho+(1-\rho)(b+\pi\lambda)H^1(B_r(M))\)). Replace with: "An atomless high component turns the drop at the ceiling into a ramp: full-order entry is continuous and nonincreasing in strength." Move the formula to A.6 if it is not there.
- `07:100` (\(p_H\), \(h-c_H/M\)). Replace with "for reserves between about \(\reg{p2_reserve_ph}\) and \(\reg{p2_reserve_weak_top}\)".

### 3.5 The notation the main text needs

About 65 symbols, against about 100 now:

- **Primitives**: \(R\), \(F\) (and \(r\) for the uniform case), \(j\in\{H,L\}\), \(\pi\), \(\theta\), \(G_j\) and \(D\) (only in §2.2, Proposition 1 and §6.2), \(p\), \(h\), \(\ell\), \(C\), \(\rho\), \(c_H\), \(\lambda\), \(\beta\), \(k\).
- **Slot**: \(b\), \(u\), \(X\) and \(q\), \(P\), \(V_T\), \(\mu\), \(M(\pi)\), \(m(\pi)\).
- **Payoffs**: \(t_0\), \(t_H\), \(t_L\), \(\DT\), \(g_H\), \(g_L\), \(B(\mu)\) (with \(B_F\), \(B_r\)), \(\tau\).
- **Trading**: \(e(x)\), \(K_H\), \(K_L\), \(\kappa(\pi)\), \(U_j\) (one display).
- **Outcomes**: \(\Ent\), \(\Own_H\), \(W_H\).
- **Strengths**: \(r_0\), \(r_1\), \(r_2\), \(r_C\), and \(r_A\), \(r_F\), \(r_N\), \(r_J\), \(r_S\) (defined in words in §4.3; §8 uses \(r_S\) again at `08:6–7`).
- **Research**: \(\lb\), \(a\), \(\lambda_R\), \(\lambda_E\), \(M_\lambda\), \(r_R\), \(\bar r_R\), \(r_U\).
- **Comparisons and extensions**: \(F_0\), \(F_1\), \(F_2\), \(\tilde F\) (Propositions 1 and 2), \(t(\theta)\), \(g(\theta)\), \(a_T\) and \(d\) (§6.3 only), \(\omega\) (§7.2 only).

---

## 4. Status tags

The labels analytical, computer-assisted, numerical diagnostic and open must stay visible. Proposal:

1. **The four numbered propositions** carry the tag in the title parenthetical, as in the reference: "Proposition 1 (competition and the two returns to information; analytical)" (ref. 582–583) and "Proposition 3 (coexisting informative equilibria; computer-assisted)" (ref. 1004–1005). Proposition 4 has two parts, and its title reads "(Competition creates research; part (b) computer-assisted)", so the analytical comovement stays visible. After a computer-assisted proposition, at most one sentence names the method as a proof idea. The reference has such a paragraph (ref. 1023–1031). Rewrites of `04:324–325` and `05:71–72` are in E-i and E-l. They drop "The status is computer-assisted because", which reads as a justification.
2. **Prose results in §§5–8** drop the seven inline "(computer-assisted)" tags in running text (`05:128`, `06:38`, `06:54`, `06:72`, `06:80`, `07:90`, `08:24`). The status then lives once with each appendix statement. `A1:1–2` already says "Each statement carries its status once: analytical, computer-assisted, numerical diagnostic, or open." The appendix paragraphs already carry the tags: `A5:261`, `A6:242`, `A6:356`, `A6:476`, `A6:491`, `A7:194`. The numbers in tables keep one phrase in the table notes ("Values are computer-assisted", as Table 5 already says). §6 opens with "Appendix~\ref{app:robustness} states each result in full and proves it" (`06:4–5`). Extend that sentence to "...in full, with its status, and proves it."
3. **"Open"** stays in the main text as short statements of fact: `05:139`, `07:51`, `07:101`, `08:61–62`, and the gray band in the Figure 3 notes. The reference prints "is open" in the same way (ref. 1089, 1412, 1455). These sentences state the frontier; they are not caveats. The conclusion already frames the reserve choice as "the next theoretical step" (`09:21`).
4. **"Numerical diagnostic"** stays where it is now, in the appendix (`A4:381`). No main-text result needs it.
5. A separate status table is not needed. The appendix titles already carry every label, and a table would add apparatus.

---

## 5. Proposed main-text skeleton and page estimate

The current pages come from `main.aux`: §1 p. 2, §2 p. 5, §3 p. 12, §4 p. 17, §5 p. 26, §6 p. 31, §7 p. 33, §8 p. 35, §9 p. 37. The estimates are approximate. The reference's main-text word count (10,633 tex words, ref. lines 149–1503) includes `\citeproc` and `\hyperref` markup. After a 10–15% discount it is about 9,200 words, against 14,151 tex words in the slot sections.

| § | What the section does | Numbered results | Becomes prose or moves | Current pages | Proposed pages | Reference counterpart |
|---|---|---|---|---|---|---|
| 1 Introduction | Mechanism, main result, benchmark numbers, extensions, literature | none | no apparatus here | 3.0 | 3.0 | §1 (≈3) |
| 2 The model | Decision interval; values and the class ranking in prose; slot; equilibrium in one paragraph; two tie conventions in one sentence | none | Assumption 1 → prose; Definition 1 → prose and the Appendix A opening; IM/I0/C1/CM → A.4; Remark 3 → a footnote in §2.3; \(\eta\), \(f_j\), \(\mathcal E\) → appendix | 7.0 | 5.0 | §2 (2.1–2.4, no environments) |
| 3 Competition and information | Two returns; what the price can reveal; informed trading | **Proposition 1** | Lemmas 1–3 and Corollary 1 → prose with the `eq:bounds`, `eq:price` and \(K_H,K_L\) displays, statements → A.2; `eq:odds`, \(b_0\), \(\delta_q\) → A.2 | 5.0 | 3.5 | §3 (Prop. 1; 3.2–3.3 in prose, "Propositions A.1 and A.2 give the formal statements") |
| 4 Equilibrium results | 4.1 main result; 4.2 benchmark, region, controls (Tables 1–3, Figure 1); 4.3 coexistence (Figure 2) | **Proposition 2**, **Proposition 3** | the three in-text tables of §4.3 → A.4 (duplicates); Remark 1 → A.4; Corollary 2 → two sentences and A.4; B_i/Δ_i shorthand removed | 9.0 | 7.0 | §4 (Props. 2–3; 4.2 benchmark and controls) |
| 5 Competition creates research | Research as chosen presence; research optimality `eq:research`; the branch; region (Table 4, Figure 3) | **Proposition 4** (merged) | Corollary 3 merged; (E7) → prose and A.5; Remark 2 and the CM row of Table 4 → A.5; \(u_\lambda\), \(V\), the \(\lambda_E\) formula, the \(r_U\) formula → A.5 | 5.0 | 3.5 | none; reference §8 names research as a next step |
| 6 Robustness | Cost laws, classes and priors, signals | none | §6.4 deleted (Remark 3 is in §2.3); cost-law notation → words; inline status tags dropped | 2.5 | 2.0 | §5 |
| 7 Welfare and sale terms | Access, payment rule, reserves (Table 5) | none | \(p_H\) → words; the \(z\) clash fixed | 2.5 | 2.5 | §6 |
| 8 Empirical implications | Tests from the spread, the informed share, winners, announcements, clusters | none | tie-rule clauses `08:30–32` and `08:60–62` → A.8; \(\vartheta\) → words | 2.0 | 1.8 | §7 (shorter in the reference) |
| 9 Conclusion | Summary and next steps | none | none | 0.5 | 0.5 | §8 |
| **Total** | | **4** | | **≈36.5** (+ title page ≈ 38) | **≈29** (+ title page ≈ 30) | ≈26–27 estimated (≈9,200 words at ≈450 words a page, plus 5 tables and 4 figures) |

Comparison with the reference structure:

- Sections 1–4 then map one to one: Introduction, Model, Competition and information, Equilibrium results. Each has the same proposition count as the reference (0, 0, 1, 2). The equilibrium concept moves into prose, as in reference §2.4.
- Slot §5 (research) is the section the reference lacks. With one numbered proposition and about 3.5 pages, it costs about the extra length.
- Slot §§6–9 map to reference §§5–8 and have no environments, as in the reference.
- The main text then has four numbered results and no lemma, corollary, remark, definition or assumption. The reference has three numbered results and none of the other environments.

---

## 6. Checklist of references to carry

Edits in `sections/` and `appendix/`. They are listed per environment in Section 2.2:

- `ass:classes` (15 sites);
- `def:equilibrium` (6);
- `lem:beliefs`, `lem:prices`, `lem:trading`, `cor:exclusion` (all A.2–A.8 sites keep `\ref` and only change the printed number);
- `rem:ties` (`08:61`);
- `prop:priors` (`03:118`, `A2:166`, `A4:3`, `A4:402`, `A9:110`);
- `prop:researchbranch` (`A5:3`, `A5:241`);
- `rem:researchties` (`A5:4`, `A5:360`);
- the hand-typed "Proposition~1(c)" (unchanged if Proposition 1 keeps its number).

Hard-typed numbers in `slides.tex` that change:

- `:328` "Lemma 3", which becomes Lemma A.3 or a section pointer;
- `:484` and `:776` "Corollary 3", which become "Proposition 4(a)".

Unchanged in `slides.tex`: `:239`, `:370–387`, `:456`, `:476`, `:652`, `:691`, `:702`, `:773`, `:794` (Propositions 1–4 and (H1)–(H3) keep their numbers and tags), and `:429`, `:517`, `:545` (Proposition A.x numbering is unchanged).

Hard-typed numbers in `comparison.tex` that change:

- `:66–67` "Propositions 1 to 4 and Corollaries 2 and 3 in the main text" becomes "Propositions 1 to 4 in the main text";
- `:138`, `:141`, `:144`, `:200`, `:201`, `:658` (Lemmas 1–3);
- `:206` (Corollary 2);
- `:207`, `:273` (Corollary 3);
- `:254`, `:294` (Remark 1);
- `:380`, `:654` (Definition 1, if its counter changes);
- `:656` ("the five forms on the path in Section 4.3 and A.4");
- `:167` (the tie-rules row: "I0 and CM stated where they change a result" becomes "...in Appendix A.4").

Counter block in `main.tex:124–138`: add definition (and remark, if a remark environment survives in the appendix).
