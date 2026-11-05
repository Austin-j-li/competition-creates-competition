# Independent review of the web deck and website

Date: 29 October 2026.

The sampled slide faces match the Beamer deck in content and structure. The deck fails the blanket terminology rule through its Notes panels.

Counts: **1 must-fix, 1 should-fix, 4 optional**. Each row below counts as one item.

Do not accept the blanket terminology claim until item M1 is resolved. The sampled slide faces need no substantive correction.

## Findings

| Location | What is seen | Expected | Severity |
|---|---|---|---|
| **M1. Notes panels: S1, S7, B5.** Source: `slot/manuscript/slides_script.md:39,47,129,327`. | Four visible uses of **fund** remain. S1 twice says “sector fund”. S7 and B5 each say “sector-focused long-short fund”. These appear after the reader selects Notes. See [S1](review_shots/notes-S1.png), [S7](review_shots/notes-S7.png), and [B5](review_shots/notes-B5.png). | The request bans “fund” anywhere in the visible deck. Apply the approved “informed trader” name to these notes. Preserve the sector expertise explanation. Reconcile the master script before the web rebuild. This is inherited script text, rather than a slide-face transcription error. | **must-fix** |
| **S1. Website, Seminar talk tab.** Source: `handout/template.html:85–92`; compare `presentation/build.py:37–38`. | “Parts of the talk” lists seven parts: Question, Setting, Price, Mechanism, Result, Beyond, Close. The deck rail and overview use six main parts. See [the website tab](review_shots/talk-tab.png) and [the deck overview](review_shots/web-overview.png). | Use the current six parts: Question; Model; Mechanism and main result; Fixed-information control; Extensions and prediction; Conclusion. Keep Backups separate. The current website outline no longer describes the deck's section structure. | **should-fix** |
| **O1. General slide layout**, including S1, S10–S13 and S19. | The web adds upper and lower controls. Its title rule sits nearer the title. Statement blocks sit higher. Text and mathematics wrap differently. S19's headline occupies two lines on the web and one in the PDF. See [comparison 1](review_shots/compare-01.png), [comparison 2](review_shots/compare-02.png), and [comparison 3](review_shots/compare-03.png). | Treat this as structural and content parity, rather than identical page geometry. Preserve the current readable layout unless closer visual parity is required. No sampled text clips or overlaps. | optional |
| **O2. Diagram and figure colours**, especially S8, S10, S14, B3 and B12b. | The PDF retains orange and teal exhibits. The web uses oxblood, ink and greys. See [comparison 2](review_shots/compare-02.png), [comparison 3](review_shots/compare-03.png), and [comparison 5](review_shots/compare-05.png). | Retain the approved website palette. State that colour parity with the supplied PDF is incomplete. The new palette follows the shared website design. No actor label or sampled numerical value changes. | optional |
| **O3. B3b and B12b figure guides.** PDF pages 25 and 46. | The web uses lighter dotted vertical guides, fewer axis ticks, and heavier point markers. The PDF uses stronger dashed guides and different tick spacing. The web's research thresholds are harder to trace down to the strength axis. See [B3b web](review_shots/web-B3b.png), [PDF page 25](review_shots/pdf-25.png), [B12b web](review_shots/web-B12b.png), and [PDF page 46](review_shots/pdf-46.png). | Consider stronger threshold guides within the approved palette. Preserve the existing thresholds and branch values. This is a visual difference, not an observed numerical mismatch. | optional |
| **O4. Brief, “Between the three economies”.** Source: `handout/sections/04-path.html:6–12`, plus the explorer labels. | The brief calls the no-information equilibrium a “quiet market”. The deck calls it an “uninformative market”. See [the brief](review_shots/brief-mobile-sec-path-h2.png) and [deck B3](review_shots/web-B3.png). | Consider one name across both documents. This does **not** fail the brief's explicit banned-word rule, which excludes “quiet”. The economic explanation remains consistent. | optional |

## Scope and method

The reviewed worktree is `/home/uctpiaj/work/tmp/ccc-main-slidepack`, branch `main`.

Its HEAD is `a542c310c9e9afe5ecb34943cc5a566f32afbde2`. I read the log from `5607e31` and the requested new commits.

I read the language decisions and the implementer's comparison. I made fresh browser observations and fresh PDF renders independently.

The master source is `slot/manuscript/slides.tex`. A byte comparison with `overleaf/slot/slides.tex` found no difference.

The supplied PDF has 56 pages. Its SHA-256 is `d8ad4fb2dbd30e76ab03480c0de0a888a29c83bb4b1d44d56ad5c6e27501abf3`.

I reviewed the existing built HTML. I did not invoke either builder. The slide builder runs a checker, and the brief builder writes a repository manifest.

All 14 source hashes in `presentation/dist/provenance.json` match the current files. The brief HTML hash matches its existing manifest.

The brief HTML SHA-256 is `6990e9cd9eeccf5d2ba1e1ed3d86f47aa6a0e3a582bd18fe4b5c00cb89d42ecf`.

The brief manifest does not record every template and style hash. Its output hash alone does not establish complete source provenance.

I used the vendored Chrome executable under `~/work/.cache/ccc-browser`, in headless mode. Its temporary profile was under `/home/uctpiaj/work/tmp`.

The static server bound only to `127.0.0.1:8879`. I used the browser's DevTools interface for navigation, text inspection and screenshots.

Every web slide screenshot uses a 1440 × 900 viewport. Every PDF page was rendered with `pdftoppm -r 80 -png`.

I wrote no tests and ran no test suite. I did not call `DECK.audit()` or `DECK.selfCheck()`.

## Sample comparison: 19 frames

I inspected each pair below. Words, numerical statements, actor labels and mathematical conditions agree in this sample.

The differences below supplement the six findings. They do not count as additional findings.

| Web frame | PDF page | Independent visual comparison | Screenshots |
|---|---:|---|---|
| S0 | 1 | Title, author and affiliation agree. The title rule and vertical placement differ. The web adds its controls. | [Web](review_shots/web-S0.png), [PDF](review_shots/pdf-01.png) |
| S1 | 2 | Seller, Rival and Price remain three columns. Their words agree. The web places these columns higher. | [Web](review_shots/web-S1.png), [PDF](review_shots/pdf-02.png) |
| S5 | 6 | The five label rows, model strip, definition text and bottom independence statement agree. Both define incumbent bidder and potential rival bidder. | [Web](review_shots/web-S5.png), [PDF](review_shots/pdf-06.png) |
| S6 | 7 | The five timeline stages and four explanatory bullets agree. Only the prepared rival learns its value at the final stage. | [Web](review_shots/web-S6.png), [PDF](review_shots/pdf-07.png) |
| S7 | 8 | The information table has the same players, observations and choices. Both belief definitions remain below it. | [Web](review_shots/web-S7.png), [PDF](review_shots/pdf-08.png) |
| S8 | 9 | The number line keeps the reserve, incumbent value, rival value and surplus split. Equations and bullets agree. Colours differ. | [Web](review_shots/web-S8.png), [PDF](review_shots/pdf-09.png) |
| S10 | 11 | Proposition 1 keeps its two columns, inequalities and explanatory glosses. The split diagram and intuition remain below. Diagram colours differ. | [Web](review_shots/web-S10.png), [PDF](review_shots/pdf-11.png) |
| S11 | 12 | The belief statement, two columns, preparation rule, intuition and B2 button agree. KaTeX changes line wraps. | [Web](review_shots/web-S11.png), [PDF](review_shots/pdf-12.png) |
| S12 | 13 | The trade bounds, correct-order gains, tie discussion, intuition and B2 button agree. The web statement occupies less vertical space. | [Web](review_shots/web-S12.png), [PDF](review_shots/pdf-13.png) |
| S13 | 14 | H1–H3, their explanations, the three-economy table and total-entry formula agree. B1 and B2 controls remain in the footline. | [Web](review_shots/web-S13.png), [PDF](review_shots/pdf-14.png) |
| S14 | 15 | The belief figure stays left of Corollary 1. Threshold values, top belief, example inputs and B10 links agree. Plot colours and proportions differ. | [Web](review_shots/web-S14.png), [PDF](review_shots/pdf-15.png) |
| S19 | 20 | The headline, three result bullets and final research sentence agree. The headline wraps on the web. Both retain the conclusion structure. | [Web](review_shots/web-S19.png), [PDF](review_shots/pdf-20.png) |
| B2 | 22 | Lemmas A.1 and A.2 agree. Both provide distinct return buttons for 11, 12 and 13. | [Web](review_shots/web-B2.png), [PDF](review_shots/pdf-22.png) |
| B3 | 24 | The coexistence region stays left of the conditions and explanation. The scope line, takeaway and Back button agree. Plot colours and scale differ. | [Web](review_shots/web-B3.png), [PDF](review_shots/pdf-24.png) |
| B3b | 25 | Both panels show the entry branches and coexistence band. The caption, three numerical bullets, takeaway and Back button agree. Guides and ticks differ. | [Web](review_shots/web-B3b.png), [PDF](review_shots/pdf-25.png) |
| B6 | 30 | The four scope rows and their results agree. The bottom takeaway, pointer line and Back button remain in the same structural roles. | [Web](review_shots/web-B6.png), [PDF](review_shots/pdf-30.png) |
| B8 | 34 | The payoff identities, class means, spread, win chance and takeaway agree. The web redistributes vertical space. | [Web](review_shots/web-B8.png), [PDF](review_shots/pdf-34.png) |
| B12b | 46 | Both research panels, branch names, cap value and numerical bullets agree. Colours, markers and threshold guides differ. | [Web](review_shots/web-B12b.png), [PDF](review_shots/pdf-46.png) |
| B16 | 55 | All eleven notation rows keep their symbols, glosses and first-definition references. The Back button and B16 footline remain. Text wraps differ. | [Web](review_shots/web-B16.png), [PDF](review_shots/pdf-55.png) |

The statement blocks use rules and a tag in both versions. Tables keep their header and body structure. Footlines keep the title and frame identifier.

Main footlines display the total of 19. Backup footlines display their B identifier. The extra web controls sit outside the slide stage.

## Navigation and terminology observations

I activated every slide link and return button through the DOM. All **60** landed on the expected frames.

I independently read the PDF link annotations. Its 60 content links match the web in source page, named target and destination page.

The PDF also has 55 title-footline links. These are separate from the 60 content links above.

B2 and B2b each return correctly to S11, S12 or S13. The lower Back control also returned from B2 to its S11 origin.

Actual keyboard events moved S5 → S6 → S5. End reached S19. Right Arrow stayed at S19. Home reached the title.

The overview contains **56 selectable frames**: one title, 19 main frames and 36 backup pages. See [the overview](review_shots/web-overview.png).

I collected rendered DOM text after each of the 56 frames became active. No slide face contains “quiet”, “challenger”, “second buyer” or “fund”.

I also inspected the SVG axis, annotation and legend text on every figure frame. These use rival and informed-trade language where relevant.

The Notes data contains the four “fund” uses in M1. I opened all three affected panels and confirmed their rendered text.

The PDF text extraction retains “quiet” beneath a figure patch. The inspected PDF figure does not visibly show that old label.

## Website observations

The opening box names the incumbent bidder, potential rival bidder and informed trader. “Who knows what” explicitly defines incumbent and rival.

That section also defines the informed trader's sector expertise. The incumbent knows its value before trade. Preparation reveals the rival's value.

I opened the details sections for the term scan. The brief has no visible “challenger”, “investor” or “second buyer”.

The two retained acquisition uses are appropriate: “outreach to other buyers” and “a leveraged financial buyer”. The second occurs in the model-to-record table.

All six timeline controls expose the correct information sequence. The last stage states that the incumbent bids its value and the prepared rival learns its value.

I inspected all six section starts at desktop and 390 px widths. Paragraphs, headings and the sampled equations remain readable.

The phone viewport has a 380 px content area after its scrollbar. The document stays within that width, even with the details sections open.

One wide control table uses its own horizontal scroll area. I moved it through its full 46 px range and read the last column.

See the table [before](review_shots/brief-mobile-wide-table-left.png) and [after](review_shots/brief-mobile-wide-table-right.png) horizontal scroll.

The brief and slides share Libertinus faces, thin rules and one oxblood accent. The light accent computes to `#7a1f1f`.

Chrome reports an actual custom `LibertinusSerif-Bold` font for the brief title. The required loaded Libertinus and KaTeX faces report no font error.

Dark mode retains readable text, equations and controls. I inspected the brief in both widths and S14 in the deck.

Representative website screenshots:

- [Desktop brief](review_shots/brief-desktop-top.png).
- [Phone brief](review_shots/brief-mobile-top.png).
- [Phone definitions](review_shots/brief-mobile-information.png).
- [Phone mechanism](review_shots/brief-mobile-sec-mechanism-h2.png).
- [Phone main result](review_shots/brief-mobile-sec-result-h2.png).
- [Phone robustness](review_shots/brief-mobile-sec-robustness-h2.png).
- [Phone empirical implications](review_shots/brief-mobile-sec-tests-h2.png).
- [Desktop dark theme](review_shots/brief-desktop-dark.png).
- [Phone dark theme](review_shots/brief-mobile-dark.png).
- [Deck dark theme](review_shots/web-S14-dark.png).
- [Paper tab](review_shots/paper-tab.png).

## Errors, limits and cleanup

The observed page loads and interactions produced no console errors, JavaScript exceptions, failed network requests or HTTP responses of 400 or above.

All 56 deck faces and the brief have zero rendered KaTeX error nodes. No visible formula error appeared in the inspected screenshots.

Unused font declarations can remain unloaded. I found no font with an error status and no missing font request.

This review covers local artifacts. It does not certify the deployed website or its route setup. I did not run a numerical reconstruction of the figures.

The 19 paired visual inspections establish sample parity. The full deck checks cover frame count, rendered text, navigation and browser errors.

Sources and tracked outputs remain unchanged. The five pre-existing untracked presentation documents remain untouched. No commit was made.

The review browser and static server were stopped after inspection. Only this report, its screenshots and the temporary browser profile were written.
