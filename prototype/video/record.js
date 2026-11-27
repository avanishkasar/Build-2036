// Scripted walkthrough of the live page, timed to the narration timeline.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");

const [, , url, outDir] = process.argv;
const timeline = JSON.parse(fs.readFileSync(path.join(outDir, "timeline.json"), "utf8"));
const W = 1440, H = 810, OUT_W = 1920, OUT_H = 1080;

(async () => {
  const browser = await chromium.launch();
  const tStart = Date.now();
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1, recordVideo: { dir: path.join(outDir, "raw"), size: { width: W, height: H } } });
  const page = await ctx.newPage();
  await page.addInitScript(() => { window.__recording = true; });
  await page.goto(url, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  // Soft cursor so viewers can follow clicks.
  await page.addStyleTag({ content: `#cur{position:fixed;z-index:9999;width:22px;height:22px;border-radius:50%;background:rgba(31,77,58,.25);border:2px solid #1F4D3A;pointer-events:none;transform:translate(-50%,-50%);transition:left .6s ease,top .6s ease}
    .spot{outline:3px solid #1F4D3A!important;outline-offset:6px;border-radius:18px;transition:outline-color .3s}` });
  await page.evaluate(() => { const c = document.createElement("div"); c.id = "cur"; c.style.left = "50%"; c.style.top = "60%"; document.body.appendChild(c); });

  const sleep = (ms) => page.waitForTimeout(Math.max(0, ms));
  // JS glide instead of native smooth scroll: native smooth scroll leaves stale tiles in the screencast.
  const glideY = (y) => page.evaluate((target) => new Promise((done) => {
    const from = window.scrollY, to = Math.max(0, Math.min(target, document.documentElement.scrollHeight - innerHeight));
    const t0 = performance.now(), D = 900, ease = (k) => (k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
    // After the glide, damage the whole viewport for two frames so the recorder never freezes a torn frame.
    const repaint = () => { let v = document.getElementById("__rp"); if (!v) { v = document.createElement("div"); v.id = "__rp"; v.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:9998;background:#000;opacity:0"; document.body.appendChild(v); }
      requestAnimationFrame(() => { v.style.opacity = "0.004"; requestAnimationFrame(() => { v.style.opacity = "0"; requestAnimationFrame(() => done()); }); }); };
    const step = (t) => { const k = Math.min(1, (t - t0) / D); window.scrollTo(0, from + (to - from) * ease(k)); k < 1 ? requestAnimationFrame(step) : repaint(); };
    requestAnimationFrame(step);
  }), y);
  const scrollTo = async (sel, block = "start") => {
    const y = await page.evaluate(([s, b]) => { const r = document.querySelector(s).getBoundingClientRect(); return window.scrollY + r.top - (b === "center" ? (innerHeight - r.height) / 2 : 24); }, [sel, block]);
    await glideY(y);
  };
  const cursorTo = async (sel) => { const bx = await page.locator(sel).boundingBox(); if (bx) await page.evaluate(([x, y]) => { const c = document.getElementById("cur"); c.style.left = x + "px"; c.style.top = y + "px"; }, [bx.x + bx.width / 2, bx.y + bx.height / 2]); await sleep(700); };
  const spot = (sel, on = true) => page.evaluate(([s, o]) => document.querySelectorAll(".spot").forEach((e) => e.classList.remove("spot")) || (o && document.querySelector(s)?.classList.add("spot")), [sel, on]);

  const actions = {
    hero: async (ms) => { await sleep(ms); },
    mandate: async (ms) => { await spot("#mandate .card"); await cursorTo("#mandate dl"); await sleep(ms - 700); await spot(null, false); },
    run: async (ms) => { await cursorTo("#run"); await page.click("#run"); await page.waitForSelector("#steps article"); await sleep(600); await scrollTo("#demo"); await sleep(ms - 2200); },
    step1: async (ms) => { await spot("#step-1"); await cursorTo("#step-1 h3"); await sleep(ms - 700); },
    step2: async (ms) => {
      await spot("#step-2"); await cursorTo("#step-2 h3"); await sleep(ms * 0.45);
      await cursorTo("#step-2 details summary"); await page.evaluate(() => { document.querySelector("#step-2 details").open = true; });
      await sleep(400); await scrollTo("#step-2 details", "center"); await sleep(ms * 0.55 - 1800);
    },
    step3: async (ms) => { await page.evaluate(() => { document.querySelector("#step-2 details").open = false; }); await scrollTo("#demo"); await sleep(500); await spot("#step-3"); await cursorTo("#step-3 h3"); await sleep(ms - 1200); },
    verify: async (ms) => {
      await spot(null, false); await cursorTo("#verify"); await page.click("#verify"); await sleep(ms * 0.4);
      await cursorTo("#tamper"); await page.click("#tamper"); await sleep(300); await spot("#chain"); await sleep(ms * 0.6 - 2400);
    },
    attacks: async (ms) => {
      await spot(null, false); await scrollTo("#hero"); await sleep(900); await cursorTo("#attacks"); await page.click("#attacks");
      await page.waitForSelector("#rows tr"); await sleep(300); await scrollTo("#attack"); await sleep(ms * 0.35);
      await glideY(await page.evaluate(() => window.scrollY + 420)); await sleep(ms * 0.65 - 3200);
    },
    how: async (ms) => { await scrollTo("#how", "center"); await spot("#how .bg-allow-soft"); await sleep(ms); await spot(null, false); },
    close: async (ms) => { await glideY(0); await sleep(ms + 600); },
  };

  fs.writeFileSync(path.join(outDir, "lead.txt"), String((Date.now() - tStart) / 1000));
  for (const seg of timeline) {
    const t0 = Date.now();
    await actions[seg.action](seg.dur * 1000);
    if (process.env.DBG) await page.screenshot({ path: path.join(outDir, `dbg_${seg.id}.png`) });
    const drift = seg.dur * 1000 - (Date.now() - t0);
    if (drift > 0) await sleep(drift);
  }
  await ctx.close();
  await browser.close();
})();
