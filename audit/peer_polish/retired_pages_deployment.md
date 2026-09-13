# Retired website publishing procedure

Historical record only. Do not use these commands for current publishing or rollback.
Current hosting and rollback instructions are in [handout/README.md](../../handout/README.md).
The old deployment branch is preserved on GitLab for provenance.

### Historical GitHub Pages deployment

GitHub Pages previously served the root of `gh-pages`. That site stopped serving because
the account plan did not support Pages from the private repository. The deployment branch
is retained as a historical copy. Its former publishing procedure was to build and check
the source branch, then
copy only `index.html`, `.nojekyll`, `main_filled.pdf`, `online_appendix_filled.pdf`, and the
`fonts/` directory from `docs/` into an isolated checkout of the current remote `gh-pages` commit.
Commit the generated files there and push normally, without force. Do not switch the source
checkout to the deployment branch or publish other files from `docs/`.

The deployment before this research-brief revision is
`07380e7fc95d9c385afdef69d932472d624d93b9`. To roll back, restore those four files from that
commit in a fresh deployment checkout and publish a new commit. This preserves history.
After publishing, check Pages build status and compare the live HTML and both PDF hashes
with the reviewed local artifacts.

The deployment immediately before the visible-mathematics revision is
`af99f89d28e4b8c106b00543fa733776d9624cf8`. Restore its `index.html` in a new deployment
commit to undo that content revision while retaining the redesigned typography and fonts.

The revision was checked at desktop and mobile sizes in both themes. The main reading path
contains approximately 1,700 words of prose plus four mathematical stops, excluding expanded details. Prose, the benchmark table and
PDF links also remain available with JavaScript disabled or the CDN blocked.

