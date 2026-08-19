import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const coverPath = path.join(__dirname, "cover.html");
const coverUrl = `file:///${coverPath.replaceAll("\\", "/")}`;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({
  viewport: { width: 1080, height: 1440 },
  deviceScaleFactor: 1,
});

await page.goto(coverUrl, { waitUntil: "networkidle" });
await page.screenshot({
  path: path.join(__dirname, "育种基地田间记录闭环_宣传封面.png"),
  fullPage: false,
});

await browser.close();
console.log("Generated cover image.");
