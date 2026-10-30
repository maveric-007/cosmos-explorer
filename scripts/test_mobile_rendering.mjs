#!/usr/bin/env node
/**
 * Browser-level mobile layout regression for Cosmos Explorer.
 * Emulates iPhone-sized touch viewports in Chromium; this does NOT replace
 * verification on physical iPhone Safari.
 */
import { chromium, devices } from 'playwright-core';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';

const url = process.env.COSMOS_TEST_URL || 'http://127.0.0.1:8765/';
const chromePath = process.env.CHROME_PATH || '/usr/bin/google-chrome';
const browser = await chromium.launch({ executablePath: chromePath, headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader'] });
await fs.mkdir('artifacts/mobile-smoke', { recursive: true });
const sizes = [
  { width: 320, height: 568 },
  { width: 375, height: 667 },
  { width: 390, height: 844 },
  { width: 430, height: 932 },
  { width: 844, height: 390, landscape: true },
  { width: 932, height: 430, landscape: true },
  { width: 768, height: 1024 },
];
try {
  for (const { width, height, landscape = false } of sizes) {
    const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, userAgent: devices['iPhone 13'].userAgent });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    // Prefer the checked-in copy for deterministic catalog coverage;
    // it avoids a current upstream change during this layout smoke test.
    await page.route('https://raw.githubusercontent.com/maveric-007/cosmos-explorer/main/data/**', route => route.abort());
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForFunction(() => document.querySelector('#sceneStatus')?.textContent?.startsWith('Renderer ready'), { timeout: 60000 });
    await page.locator('#quickMode').selectOption('system');
    await page.waitForFunction(() => document.querySelector('#selectedName')?.textContent === 'TRAPPIST-1', { timeout: 30000 });
    await page.waitForFunction(() => document.querySelector('#systemEmptyHint')?.hidden === true, { timeout: 30000 });
    const data = await page.evaluate(() => {
      const box = id => document.getElementById(id).getBoundingClientRect();
      const header = box('quickMode'), search = box('hostSearch'), stage = box('stage'), nav = box('scaleSlider'), canvas = box('scene');
      return {
        htmlWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth,
        headerBottom: header.bottom, searchBottom: search.bottom, stageTop: stage.top, stageBottom: stage.bottom, navTop: nav.top,
        stageWidth: stage.width, stageHeight: stage.height, canvasWidth: canvas.width, canvasHeight: canvas.height,
        systemSelected: document.getElementById('selectedName').textContent,
        hintHidden: document.getElementById('systemEmptyHint').hidden,
        hostCount: document.getElementById('hostMatches').options.length,
        fieldVisible: getComputedStyle(document.getElementById('hostSearch')).display !== 'none'
      };
    });
    assert.ok(data.htmlWidth <= data.clientWidth + 2, `${width}px: horizontal overflow (${data.htmlWidth}/${data.clientWidth})`);
    assert.ok(data.stageHeight >= (width <= 760 || landscape ? 90 : 230), `${width}px: stage collapsed`);
    assert.ok(Math.abs(data.stageWidth - data.canvasWidth) <= 2, `${width}px: canvas width mismatch`);
    assert.ok(Math.abs(data.stageHeight - data.canvasHeight) <= 2, `${width}px: canvas height mismatch`);
    assert.ok(data.hostCount > 0 && data.fieldVisible, `${width}px: system search unusable`);
    if (width <= 760 || landscape) {
      assert.ok(data.headerBottom < data.searchBottom && data.searchBottom <= data.stageTop + 4, `${width}px: search not above scene`);
      assert.ok(data.stageBottom < data.navTop + 4, `${width}px: navigation overlaps scene`);
    }

    // A control that is below the page fold is not usable as a first-screen
    // control, even if document.scrollWidth reports no horizontal overflow.
    const cockpit = await page.evaluate(() => {
      const bounds = id => {
        const r=document.getElementById(id).getBoundingClientRect();
        return { left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width };
      };
      const viewportWidth = document.documentElement.clientWidth;
      const viewportHeight = window.visualViewport?.height || window.innerHeight;
      const interactive = [...document.querySelectorAll('.frame button,.frame input,.frame select,.frame summary')]
        .filter(el=>el.getClientRects().length && getComputedStyle(el).visibility!=='hidden' && getComputedStyle(el).display!=='none')
        .map(el=>({id:el.id||el.textContent.trim().slice(0,36),left:el.getBoundingClientRect().left,right:el.getBoundingClientRect().right}));
      return { viewportWidth,viewportHeight,play:bounds('playPause'),scale:bounds('scaleSlider'),time:bounds('dateSlider'),
        search:bounds('hostSearch'),stage:bounds('stage'),interactive,
        mobile:matchMedia('(max-width:760px), (max-width:1100px) and (max-height:550px) and (pointer:coarse)').matches };
    });
    for (const control of cockpit.interactive)
      assert.ok(control.left >= -3 && control.right <= cockpit.viewportWidth + 3,
        `${width}x${height}: ${control.id} is outside the horizontal viewport [${control.left},${control.right}]`);
    if (cockpit.mobile) {
      assert.ok(cockpit.scale.top >= -2 && cockpit.time.bottom <= cockpit.viewportHeight + 12,
        `${width}x${height}: scale/time slider pushed outside initial visible screen`);
      assert.ok(cockpit.play.bottom <= cockpit.viewportHeight + 12,
        `${width}x${height}: playback controls below initial visible screen (${cockpit.play.bottom}/${cockpit.viewportHeight})`);
      assert.ok(cockpit.stage.height >= 90,`${width}x${height}: scene too small`);
      assert.ok(cockpit.search.top < cockpit.stage.top,`${width}x${height}: system search must precede scene`);
    }
    assert.deepEqual(errors, [], `${width}px: runtime exceptions`);
    await page.screenshot({ path: `artifacts/mobile-smoke/planetary-${width}.png`, fullPage: true });
    await page.locator('#quickMode').selectOption('local');
    await page.waitForFunction(() => document.querySelector('#selectedName')?.textContent === 'Proxima Centauri');
    const local = await page.evaluate(() => ({width:document.documentElement.scrollWidth,client:document.documentElement.clientWidth}));
    assert.ok(local.width <= local.client + 2, `${width}px: nearby-star overflow`);

    if (width <= 760 || landscape) {
      // The ordinary nearby-star view must also keep the main controls above
      // the fold, and the hidden system search must not steal their space.
      await page.waitForTimeout(80);
      const ordinary = await page.evaluate(() => {
        const r=id=>document.getElementById(id).getBoundingClientRect();
        return {bottom:r('playPause').bottom, scale:r('scaleSlider').top,
          top:r('stage').top, height:r('stage').height,
          viewport:window.visualViewport?.height||window.innerHeight};
      });
      assert.ok(ordinary.bottom <= ordinary.viewport + 12,
        `${width}x${height}: nearby-star playback below visible phone screen (${ordinary.bottom}/${ordinary.viewport})`);
      assert.ok(ordinary.scale >= ordinary.top,
        `${width}x${height}: nearby-star slider before canvas unexpectedly`);
    }

    console.log(JSON.stringify({ viewport: width, status: 'PASS', planetaryHost: data.systemSelected, systemSearchBeforeScene: width <= 760 || landscape, stageHeight: data.stageHeight }));
    await context.close();
  }
} finally { await browser.close(); }
