/* Run through the Playwright browser tool with a preview server serving dist/.
   Checks real interactions, rendering and geometry without running research code. */
async (page) => {
  const base='http://127.0.0.1:8776/';
  const assert=(ok,message)=>{if(!ok)throw Error(message);};
  const results={layouts:[],interactions:[]};
  await page.goto(base);
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.evaluate(()=>DECK.ready);
  for(const size of [{width:1600,height:1000},{width:1366,height:768},{width:390,height:844}]){
    await page.setViewportSize(size);
    for(const theme of ['auto','light','dark']){
      await page.evaluate(t=>DECK.theme(t),theme);
      const overflow=await page.evaluate(()=>DECK.audit());
      assert(overflow.length===0,JSON.stringify({size,theme,overflow}));
      const width=await page.evaluate(()=>({scroll:document.documentElement.scrollWidth,client:document.documentElement.clientWidth}));
      assert(width.scroll<=width.client,'Horizontal overflow in presentation');
      results.layouts.push({size,theme,overflow:0});
    }
  }
  await page.setViewportSize({width:1366,height:768});
  await page.evaluate(()=>{DECK.theme('auto');DECK.go('s17',{step:0});});
  await page.keyboard.press('ArrowRight');
  assert((await page.evaluate(()=>DECK.selfCheck())).step===1,'Theorem advance must reveal A2');
  await page.keyboard.press('ArrowLeft');
  assert((await page.evaluate(()=>DECK.selfCheck())).step===0,'Previous must undo the reveal');
  await page.evaluate(()=>DECK.go('s11',{step:0}));
  await page.locator('[data-choice="quality"][data-value="L"]').click();
  await page.locator('#auction-r').fill('2');
  assert((await page.locator('#auction-readout').innerText()).includes('Incumbent wins'),'Auction winner must update');
  const before=await page.evaluate(()=>DECK.selfCheck().active);
  await page.locator('#auction-r').focus();await page.keyboard.press('ArrowRight');
  assert((await page.evaluate(()=>DECK.selfCheck().active))===before,'A focused slider must keep its arrows');
  await page.evaluate(()=>DECK.go('s16',{step:99}));
  await page.locator('[data-choice="dial-preset"][data-value="strong"]').click();
  assert(await page.evaluate(()=>DECK.state.dialR===3),'Strong preset');
  await page.evaluate(()=>DECK.go('s19',{step:0}));
  assert(await page.locator('#economies-view').innerText().then(t=>t.includes('25.0%')&&t.includes('52.3%')&&t.includes('32.4%')),'Bound benchmark comparison and ownership');
  await page.evaluate(()=>DECK.go('s20',{step:0}));
  await page.locator('[data-choice="experiment"][data-value="frozen"]').click();
  assert((await page.locator('#control-readout').innerText()).includes('falls'),'Frozen experiment must restore deterrence');
  assert((await page.locator('#control-plot').innerText()).includes('56.2%'),'Frozen weak result');
  await page.evaluate(()=>DECK.go('s21',{step:0}));
  await page.locator('#s21 .detail').click();
  assert((await page.evaluate(()=>DECK.selfCheck().active))==='b8','Technical link must target correspondence');
  await page.keyboard.press('Escape');
  assert((await page.evaluate(()=>DECK.selfCheck().active))==='s21','Escape must return to the originating slide');
  await page.keyboard.press('g');
  assert(await page.locator('#panel').evaluate(e=>e.open),'G must open the glossary');
  await page.keyboard.press('Escape');
  await page.keyboard.press('n');
  assert((await page.locator('#panel-body').innerText()).includes('If asked:'),'Speaker notes must be available');
  await page.keyboard.press('Escape');
  await page.locator('#reading').click();
  const reading=await page.evaluate(()=>({mode:document.body.dataset.reading,visible:[...document.querySelectorAll('.slide')].filter(e=>getComputedStyle(e).display!=='none').length}));
  assert(reading.mode==='true'&&reading.visible===39,'Reading view must expose every slide');
  await page.keyboard.press('Escape');
  assert((await page.evaluate(()=>document.body.dataset.reading))==='false','Escape must restore presenting');
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.evaluate(()=>DECK.go('s07',{step:0}));await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(600);
  const animated=await page.locator('#s07 [data-step="1"]').evaluate(e=>({opacity:getComputedStyle(e).opacity,visible:getComputedStyle(e).visibility}));
  assert(animated.opacity==='1'&&animated.visible==='visible','Normal-motion reveals must settle legibly');
  await page.evaluate(()=>DECK.go('s01',{step:0}));
  const check=await page.evaluate(()=>DECK.selfCheck());
  assert(check.formulaCheck.ok&&check.mathErrors===0&&check.errors.length===0&&!check.unresolved,'Runtime and bound formulas');
  results.interactions=['reveal forward/back','auction winner','slider keyboard focus','strength preset','benchmark and ownership','fixed-information comparison','technical return','glossary','notes','reading mode','normal-motion reveal'];
  results.check=check;
  return results;
}
