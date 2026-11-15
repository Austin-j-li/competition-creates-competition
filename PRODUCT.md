# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Static HTML, CSS and JavaScript with SVG figures, built by a script in the repository and served
as static files (Cloudflare Workers Static Assets). No framework. Fonts, KaTeX and data are local
files; the page makes no network request at run time.

## Users

The author, presenting a 30-minute theory seminar from this page: a lit seminar room, a
projector, a clicker or the arrow keys, an audience of finance and economics theorists and his
supervisor, who interrupt with questions and ask for backup material.

A second audience reads the page alone in a browser after the talk or instead of it.

## Product Purpose

The seminar talk for "Competition Creates Competition: Stock Prices and the Discovery of Takeover
Bidders" (Austin Li, Department of Economics, University College London), delivered as a web page
at https://competition.dealextract.org/talk/. The web page is the main form of the talk
(author's decision, 15 November 2026). It replaces the earlier web copy of the Beamer deck.

Success: the room follows the argument from the question to the result that entry can rise with
incumbent strength and then fall back, and a reader alone can follow the same pages without the
speaker.

## Positioning

A talk whose figures stay in place and change as the argument moves, which a slide file cannot
do: the same chart carries the main result, the fixed-news comparison and the coexistence region;
a comparison of two incumbents is shown as one picture shifting into the other.

## Operating Context

- Presented full screen, 16:9, driven by keys that a clicker sends. Questions cause jumps to a
  backup page and back.
- `presentation.pptx` is the fallback in the room and the source of the talk's words, numbers and
  page order: a title, 19 numbered main pages in six parts (Question, Model setup, Main results,
  Discussion, Extension, Conclusion) and 39 backup pages (B1 to B17). The author keeps and edits
  that file himself.
- The page sits beside the research brief and the paper on the same site.

## Capabilities and Constraints

- Words on the pages follow the PowerPoint. No new terminology: a figure is labelled with symbols
  the talk has already defined. Main pages do not say "slot", "round" or "recruit".
- Main pages 1 to 4 state effects in words only. Example numbers first appear on the example page
  (main page 14).
- Every printed number is the display of a row of the number registry
  (`audit/slot_manuscript_2026_10_23/registry/`). Figures may evaluate the paper's closed forms in
  the example; nothing on the page searches for an equilibrium.
- Motion may move marks between click steps and between pages (author's decision, 15 November
  2026). Each click step is a stored state: back, reload and the return from a backup land on it.
- A strength control on the entry chart, from main page 14 on, snaps to the strengths the paper
  marks and stays hidden on stage until called.
- Speaker notes are not published: the built talk carries none, and its build refuses to ship any.
- The look is the two-colour plate, chosen by the author on 15 November 2026 for the whole site: the front page and the talk. `DESIGN.md` records it.

## Brand Commitments

- Title, subtitle, author and affiliation as on the PowerPoint title page.
- Single author: "I", never "we".
- Things the author has rejected as machine-made: a pale tinted callout box with a heavy accent
  bar on its side or top; gradients, glows, pills, cards as page structure, small labels above
  headings, numbered section labels, reading-time badges. A plain box, a solid band and a plain
  tinted table column are acceptable where the statement warrants one. Rules in tables run
  continuous, one weight per role.
- The look of the site is its own; it does not follow the Beamer deck's or the PowerPoint's.
- One colour besides black: a green that means only that the price brings the costly rival in.

## Evidence on Hand

- `presentation.pptx` (repository root) and its page-by-page text dumps under
  `audit/beamer_stock_2026_11_15/`.
- The number registry and the closed forms of the example in `handout/figures.js`.
- No photographs, logos or testimonials exist; none are to be invented.

## Product Principles

1. The argument leads. Motion and interaction state a step of the argument or stay out.
2. A finished page equals the author's page: every build ends on the words and numbers he wrote.
3. What is on screen is true to the model: closed forms and registry values only.
4. The speaker never has to look at the laptop: forward and back are enough to give the talk.
5. The page reads without the speaker.

## Accessibility & Inclusion

Legible from the back of a lit room on a projector: no hairlines as data, no code carried by
colour alone, figures legible in greyscale. Reduced-motion preference replaces movement with cuts.
Keyboard reaches every control.
