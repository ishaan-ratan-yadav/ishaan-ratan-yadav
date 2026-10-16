const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
const fs = require('fs');
(async () => {
  const [out, list] = process.argv.slice(2); fs.mkdirSync(out, { recursive: true });
  const br = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await br.newPage({ viewport: { width: 960, height: 540 } });
  pg.on('pageerror', e => console.log('PAGE EXC', e.message)); pg.on('console', m => { if (m.type() === 'error') console.log('ERR', m.text()); });
  await pg.goto('http://127.0.0.1:8766/index.html');
  await pg.waitForFunction(() => window.__ready === true, null, { timeout: 120000 });
  const ts = list === 'all' ? Array.from({ length: 360 }, (_, i) => i / 24) : list.split(',').map(Number);
  for (let i = 0; i < ts.length; i++) { await pg.evaluate(t => window.__seek(t), ts[i]); await pg.locator('canvas').screenshot({ path: `${out}/f${String(i).padStart(4, '0')}.png` }); }
  await br.close();
})();
