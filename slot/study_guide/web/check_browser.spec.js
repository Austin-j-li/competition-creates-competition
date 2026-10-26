const { test, expect } = require('@playwright/test');

const base = process.env.CCC_GUIDE_URL || 'http://127.0.0.1:8765/';

for (const width of [1400, 390, 320]) {
  for (const theme of ['light', 'dark']) {
    test(`guide works at ${width}px in ${theme}`, async ({ page }) => {
      test.setTimeout(60000);
      await page.setViewportSize({ width, height: 900 });
      await page.goto(`${base}?theme=${theme}`);
      await page.evaluate(() => CCC.ready);
      const state = await page.evaluate(() => CCC.selfCheck());
      expect(state.chapters).toBe(17);
      expect(state.parts).toBe(4);
      expect(state.tables).toBe(34);
      expect(state.diagrams).toBe(4);
      expect(state.katexErrors).toBe(0);
      expect(state.consoleErrors).toEqual([]);
      expect(state.duplicateIds).toEqual([]);
      expect(state.brokenLinks).toEqual([]);
      expect(state.explorer.mounted).toBe(true);
      expect(Object.values(state.charts).every(chart => chart.mounted)).toBe(true);
      expect(state.theme).toBe(theme);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      expect(await page.locator('#part-argument .q').count()).toBe(0);
      expect(await page.locator('#part-numbers .q').count()).toBe(168);

      if (width < 1024) await page.locator('.toc-mobile > summary').click();
      await page.locator('#toc-search').fill('research');
      expect(await page.locator('.toc-part li[data-searchable]:visible').count()).toBe(1);
      await page.locator('#toc-search').fill('');
      await page.locator('#theme-toggle').click();
      expect(await page.evaluate(() => document.documentElement.dataset.theme)).not.toBe(theme);

      await page.locator('#explorer-r').focus();
      const before = await page.locator('#explorer-r').inputValue();
      await page.keyboard.press('ArrowRight');
      expect(await page.locator('#explorer-r').inputValue()).not.toBe(before);
      await page.locator('[data-eq="N"]').click();
      expect((await page.evaluate(() => CCC.explorer.status())).selected).toBe('N');

      await page.locator('#chart-payoffs').scrollIntoViewIfNeeded();
      const plot = await page.locator('#chart-payoffs svg.plot').boundingBox();
      await page.mouse.move(plot.x + plot.width * 0.35, plot.y + plot.height * 0.25);
      await expect(page.locator('#chart-payoffs .chart-tip')).toBeVisible();

      await page.goto(`${base}?theme=${theme}#eq:03-tau`);
      await page.evaluate(() => CCC.ready);
      expect(await page.locator('#eq\\:03-tau').count()).toBe(1);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    });
  }
}
