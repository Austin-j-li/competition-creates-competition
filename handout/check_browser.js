// Run with the existing Playwright browser_run_code_unsafe tool's filename argument.
// Serve docs/ at http://127.0.0.1:8765 first. No added package is required.
async (page) => {
  const base = 'http://127.0.0.1:8765/';
  await page.emulateMedia({ reducedMotion: 'reduce' });
  function check(ok, message) { if (!ok) throw new Error(message); }
  const results = [];
  for (const width of [1440, 390, 320]) {
    await page.setViewportSize({ width, height: 950 });
    for (const theme of ['light', 'dark']) {
      await page.goto(base + '?theme=' + theme);
      await page.evaluate(() => CCC.ready);
      await page.locator('#model-detail > summary').click();
      await page.locator('#explorer-r').focus();
      const before = await page.locator('#explorer-r').inputValue();
      await page.keyboard.press('ArrowRight');
      check(await page.locator('#explorer-r').inputValue() !== before, 'Slider keyboard control');
      await page.getByRole('button', { name: 'Reset', exact: true }).click();
      check(await page.locator('#explorer-r').inputValue() === before, 'Slider reset');
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
      await page.waitForFunction(() => [...document.querySelectorAll('.chart-mount')].every(e => e._fullLayout));
      const state = await page.evaluate(() => ({
        plots: document.querySelectorAll('.js-plotly-plot').length,
        mathErrors: document.querySelectorAll('.katex-error').length,
        errors: CCC.errors,
        overflow: document.documentElement.scrollWidth > innerWidth,
        theme: document.documentElement.dataset.theme
      }));
      check(state.plots === 5 && !state.mathErrors && !state.errors.length && !state.overflow, JSON.stringify(state));
      check(state.theme === theme, 'Requested theme');
      await page.locator('#theme-toggle').click();
      check(await page.locator('html').getAttribute('data-theme') !== theme, 'Theme toggle');
      results.push({ width, theme, ...state });
    }
  }
  for (const anchor of ['sec-03-model', 'sec-06-robustness', 'sec-appendix']) {
    await page.goto(base + '#' + anchor);
    await page.evaluate(() => CCC.ready);
    await page.waitForFunction(id => {
      const e = document.getElementById(id);
      return e.closest('details').open && Math.abs(e.getBoundingClientRect().top) < 120;
    }, anchor);
  }
  await page.goto(base);
  await page.evaluate(() => CCC.ready);
  await page.locator('.step-btn').first().focus();
  await page.keyboard.press('ArrowRight');
  check((await page.locator('.stepper li[aria-current="step"]').innerText()).includes('Investors trade'), 'Timeline keyboard control');
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
  await page.emulateMedia({ reducedMotion: null });
  return { passed: true, layouts: results, anchors: 3, keyboard: true };
}
