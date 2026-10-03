// Browser check of the handout and, when its address is given, the slides.
// Run with the existing Playwright browser tool's run-code function and this file as filename.
// Serve docs/ at http://127.0.0.1:8765 first. No added package is required.
// Optional arguments: base (the handout address) and deck (the slides address, for example
// 'http://127.0.0.1:8766/' with presentation/dist served there).
async (page, base = 'http://127.0.0.1:8765/', deck = '') => {
  // A hidden tab runs no animation frames, and clicks then wait forever.
  await page.bringToFront();
  await page.emulateMedia({ reducedMotion: 'reduce' });
  function check(ok, message) { if (!ok) throw new Error(message); }
  const results = [];
  for (const width of [1440, 390, 320]) {
    await page.setViewportSize({ width, height: 950 });
    for (const theme of ['light', 'dark']) {
      await page.goto(base + '?theme=' + theme);
      await page.evaluate(() => CCC.ready);
      const mathVisible = await page.evaluate(() =>
        ['model-brief', 'incentive-brief', 'equilibrium-brief', 'main-result'].every(id => {
          const e = document.getElementById(id);
          return e && !e.closest('details') && e.querySelectorAll('.katex-display').length >= 2;
        }));
      check(mathVisible, 'Model, incentives, equilibrium and theorem are visible without expansion');
      await page.locator('#model-detail > summary').click();
      await page.locator('#explorer-r').focus();
      const before = await page.locator('#explorer-r').inputValue();
      await page.keyboard.press('ArrowRight');
      check(await page.locator('#explorer-r').inputValue() !== before, 'Slider keyboard control');
      await page.getByRole('button', { name: 'Reset', exact: true }).click();
      check(await page.locator('#explorer-r').inputValue() === before, 'Slider reset');
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
      await page.waitForFunction(() => [...document.querySelectorAll('.chart-mount')].every(e => e.querySelector('svg.plot')));
      const state = await page.evaluate(() => ({
        plots: document.querySelectorAll('.chart-mount svg.plot').length,
        mathErrors: document.querySelectorAll('.katex-error').length,
        errors: CCC.errors,
        overflow: document.documentElement.scrollWidth > innerWidth,
        theme: document.documentElement.dataset.theme,
        fira: [...document.fonts].some(f => f.family.replace(/"/g, '') === 'Fira Sans' && f.status === 'loaded'),
        charts: Object.values(CCC.charts.status()).every(s => s.mounted)
      }));
      check(state.plots === 5 && state.charts && !state.mathErrors && !state.errors.length && !state.overflow, JSON.stringify(state));
      check(state.fira, 'Fira Sans is loaded');
      check(state.theme === theme, 'Requested theme');
      // hover readout on Figure 2
      await page.locator('#chart-fig2').scrollIntoViewIfNeeded();
      const box = await page.locator('#chart-fig2 svg.plot').boundingBox();
      await page.mouse.move(box.x + box.width * 0.6, box.y + box.height * 0.25);
      check(await page.locator('#chart-fig2 .chart-tip').isVisible(), 'Figure 2 hover readout');
      await page.locator('#theme-toggle').click();
      check(await page.evaluate(() => document.documentElement.dataset.theme) !== theme, 'Theme toggle');
      results.push({ width, theme, ...state });
    }
  }
  // tabs: the paper tab shows the two PDFs and the inline viewer; the talk tab links the slides
  await page.setViewportSize({ width: 1440, height: 950 });
  await page.goto(base);
  await page.evaluate(() => CCC.ready);
  await page.locator('#tablink-paper').click();
  check(await page.locator('#panel-paper').isVisible() && !(await page.locator('#panel-brief').isVisible()), 'Paper tab');
  check(await page.locator('#panel-paper a[href="main_filled.pdf"]').count() >= 2 && await page.locator('#panel-paper a[href="online_appendix_filled.pdf"]').count() >= 2, 'PDF links');
  check(/main_filled\.pdf/.test(await page.locator('[data-viewer] iframe').getAttribute('src')), 'Inline viewer');
  await page.locator('#tablink-paper').focus();
  await page.keyboard.press('ArrowRight');
  check(await page.locator('#panel-talk').isVisible() && await page.locator('#panel-talk a[href="talk/"]').count() === 1, 'Talk tab by keyboard');
  await page.goto(base + '#tab-paper');
  await page.evaluate(() => CCC.ready);
  check(await page.locator('#panel-paper').isVisible(), 'Paper tab from the address');
  for (const anchor of ['sec-03-model', 'sec-06-robustness', 'sec-appendix']) {
    await page.goto(base + '#' + anchor);
    await page.evaluate(() => CCC.ready);
    await page.waitForFunction(id => {
      const e = document.getElementById(id);
      return e.closest('details').open && !e.closest('[role=tabpanel]').hidden && Math.abs(e.getBoundingClientRect().top) < 120;
    }, anchor);
  }
  await page.goto(base);
  await page.evaluate(() => CCC.ready);
  await page.locator('.step-btn').first().focus();
  await page.keyboard.press('ArrowRight');
  check((await page.locator('.stepper li[aria-current="step"]').innerText()).includes('Investors trade'), 'Timeline keyboard control');
  await page.setViewportSize({ width: 390, height: 950 });
  await page.goto(base);
  await page.evaluate(() => CCC.ready);
  await page.locator('nav.toc summary').click();
  await page.locator('nav.toc a[href="#sec-evidence"]').click();
  check(!await page.locator('nav.toc details').evaluate(e => e.open), 'Mobile navigation closes');
  await page.goto(base);
  await page.keyboard.press('Tab');
  check(await page.locator('.skip-link').evaluate(e => e === document.activeElement), 'Skip link is first keyboard target');
  await page.keyboard.press('Enter');
  check(await page.locator('main').evaluate(e => e === document.activeElement), 'Skip link reaches main content');
  await page.goto(base + '#%');
  await page.evaluate(() => CCC.ready);
  check(!(await page.evaluate(() => CCC.errors)).length, 'Malformed fragment is harmless');
  let slides = null;
  if (deck) {
    await page.setViewportSize({ width: 1440, height: 900 });
    await page.goto(deck);
    await page.waitForFunction(() => window.DECK);
    const s = await page.evaluate(() => ({ check: DECK.selfCheck(), audit: DECK.audit() }));
    check(s.check.slides === 47 && !s.check.errors.length && !s.check.mathErrors && !s.audit.length, JSON.stringify(s));
    await page.evaluate(() => DECK.go('f10b', { step: 0 }));
    await page.locator('#f10b button[data-target="app:scale"]').click();
    check(await page.evaluate(() => DECK.selfCheck().active) === 'a19', 'Backup link');
    await page.keyboard.press('Escape');
    check(await page.evaluate(() => DECK.selfCheck().active) === 'f10b', 'Back from a backup');
    await page.keyboard.press('End');
    check(await page.evaluate(() => DECK.selfCheck().active) === 'f16', 'End key');
    slides = s.check;
  }
  await page.emulateMedia({ reducedMotion: null });
  return { passed: true, layouts: results, anchors: 3, keyboard: true, slides };
}
