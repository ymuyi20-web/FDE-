import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const htmlPath = path.join(__dirname, "xhs_assets.html");

const slides = [
  "slide-01-cover",
  "slide-02-input",
  "slide-03-add",
  "slide-04-result",
  "slide-05-yield",
  "slide-06-share",
];

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 1080, height: 1440 },
  deviceScaleFactor: 1,
});

await page.goto(`file://${htmlPath.replaceAll("\\", "/")}`, { waitUntil: "networkidle" });

for (let index = 0; index < slides.length; index += 1) {
  const slideId = slides[index];
  const locator = page.locator(`#${slideId} .stage`);
  await locator.screenshot({
    path: path.join(__dirname, `${String(index + 1).padStart(2, "0")}-${slideId.replace("slide-", "")}.png`),
  });
}

await browser.close();
