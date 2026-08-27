import fs from 'node:fs/promises';
import path from 'node:path';
import pkg from '/Users/israeljasma/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.59.1/node_modules/playwright/index.js';

const { chromium } = pkg;

const root = path.resolve('.');
const outDir = path.join(root, 'docs', 'manuales', 'capturas-sistema');
await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});

const page = await browser.newPage({
  viewport: { width: 1440, height: 960 },
  deviceScaleFactor: 1,
});

async function screenshot(name, route, selector = 'body') {
  await page.goto(`http://localhost:4200${route}`, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(1400);
  await page.locator(selector).screenshot({
    path: path.join(outDir, `${name}.png`),
  });
  console.log(`${name}: ${await page.title()} ${page.url()}`);
}

await page.goto('http://localhost:4200/admin/login', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(800);
const manualUserEmail = process.env.MANUAL_USER_EMAIL;
const manualUserPassword = process.env.MANUAL_USER_PASSWORD;
if (!manualUserEmail || !manualUserPassword) {
  throw new Error('Define MANUAL_USER_EMAIL y MANUAL_USER_PASSWORD para capturar pantallas.');
}
await page.locator('input').nth(0).fill(manualUserEmail);
await page.locator('input').nth(1).fill(manualUserPassword);
await page.getByRole('button', { name: /Entrar/i }).click();
await page.waitForTimeout(2500);

await screenshot('01-dashboard', '/admin/dashboard');
await screenshot('02-menu-y-buscador', '/admin/dashboard', 'app-dashboard-layout');
await screenshot('03-stock-inventario', '/admin/inventory');
await screenshot('04-recetas', '/admin/recipes');
await screenshot('05-produccion', '/admin/production');
await screenshot('06-pos-ordenes', '/admin/orders');
await screenshot('07-reporte-stock', '/admin/reports/inventory-stock');

await browser.close();
