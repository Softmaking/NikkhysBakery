import fs from 'node:fs/promises';
import path from 'node:path';
import pkg from '/Users/israeljasma/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright@1.59.1/node_modules/playwright/index.js';

const { chromium } = pkg;

const root = path.resolve('.');
const outDir = path.join(root, 'docs', 'manuales', 'capturas-manual-final');
await fs.mkdir(outDir, { recursive: true });

const email = process.env.MANUAL_USER_EMAIL;
const password = process.env.MANUAL_USER_PASSWORD;
if (!email || !password) {
  throw new Error('Define MANUAL_USER_EMAIL y MANUAL_USER_PASSWORD.');
}

const browser = await chromium.launch({
  headless: true,
  executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
});
const page = await browser.newPage({
  viewport: { width: 1440, height: 960 },
  deviceScaleFactor: 1,
});

async function safeClickByText(text) {
  const locator = page.getByText(text, { exact: true }).first();
  if (await locator.count()) {
    await locator.click();
    await page.waitForTimeout(900);
    return true;
  }
  return false;
}

async function capture(name, route = null) {
  if (route) {
    await page.goto(`http://localhost:4200${route}`, { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1400);
  }
  await page.screenshot({ path: path.join(outDir, `${name}.png`), fullPage: false });
  console.log(`${name}: ${page.url()}`);
}

await page.goto('http://localhost:4200/admin/login', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(700);
await page.locator('input').nth(0).fill(email);
await page.locator('input').nth(1).fill(password);
await page.getByRole('button', { name: /Entrar/i }).click();
await page.waitForTimeout(2400);

await capture('01-login-contexto', '/admin/dashboard');
await capture('02-dashboard-menu', '/admin/dashboard');

await capture('03-inventario-stock', '/admin/inventory');
await safeClickByText('Ingresos');
await capture('04-inventario-ingresos');
await safeClickByText('Ajustes');
await capture('05-inventario-ajustes');
await safeClickByText('Mermas');
await capture('06-inventario-mermas');
await safeClickByText('Kardex');
await capture('07-inventario-kardex');
await safeClickByText('Reposición');
await capture('08-inventario-reposicion');

await capture('09-recetas-listado-crear', '/admin/recipes');
await page.getByText('Pan amasado', { exact: true }).first().click().catch(() => {});
await page.waitForTimeout(1000);
await capture('10-recetas-pan-amasado');

await capture('11-produccion-general', '/admin/production');
await safeClickByText('Calcular requerimientos');
await capture('12-produccion-planificar');

await capture('13-pos-general', '/admin/orders');
await page.getByText('Americano simple', { exact: true }).first().click().catch(() => {});
await page.waitForTimeout(1000);
await capture('14-pos-producto-agregado');

await capture('15-reporte-stock', '/admin/reports/inventory-stock');
await capture('16-reporte-movimientos', '/admin/reports/inventory-movements');
await capture('17-reporte-produccion', '/admin/reports/production-summary');

await browser.close();
