import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";
import fs from "node:fs/promises";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "../../..");
const pagePath = path.join(
  repoRoot,
  "exercises",
  "fde-16week",
  "week-01",
  "day-14",
  "closed_loop_prototype.html",
);
const pageUrl = `file:///${pagePath.replaceAll("\\", "/")}`;

const outDir = __dirname;
await fs.mkdir(outDir, { recursive: true });

const sampleRecords = [
  {
    operation_id: "LOOP20260701001",
    operation_date: "2026-07-01",
    material_name: "稻花香A",
    sowing_batch: "第一播期",
    plot_id: "A-01",
    operation_type: "播种",
    operation_detail: "无人机飞播",
    growth_stage: "播种",
    operator: "张工",
    need_follow_up: "是",
    note: "播后观察出苗",
  },
  {
    operation_id: "LOOP20260701002",
    operation_date: "2026-07-01",
    material_name: "稻花香A",
    sowing_batch: "第一播期",
    plot_id: "A-02",
    operation_type: "播种",
    operation_detail: "无人机飞播",
    growth_stage: "播种",
    operator: "张工",
    need_follow_up: "是",
    note: "同批次小区",
  },
  {
    operation_id: "LOOP20260712001",
    operation_date: "2026-07-12",
    material_name: "稻花香A",
    sowing_batch: "第一播期",
    plot_id: "A-01",
    operation_type: "植保",
    operation_detail: "分蘖药；常规防治",
    growth_stage: "",
    operator: "李工",
    need_follow_up: "否",
    note: "不更新生育期",
  },
  {
    operation_id: "LOOP20260725001",
    operation_date: "2026-07-25",
    material_name: "稻花香A",
    sowing_batch: "第一播期",
    plot_id: "A-01",
    operation_type: "巡田",
    operation_detail: "分蘖观察；记录分蘖情况",
    growth_stage: "分蘖",
    operator: "王工",
    need_follow_up: "是",
    note: "三天后复查",
  },
  {
    operation_id: "LOOP20260726001",
    operation_date: "2026-07-26",
    material_name: "新品系-01",
    sowing_batch: "第二播期",
    plot_id: "B-03",
    operation_type: "灌溉",
    operation_detail: "上水",
    growth_stage: "",
    operator: "王工",
    need_follow_up: "否",
    note: "保持浅水层",
  },
];

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1080, height: 1440 },
  deviceScaleFactor: 1,
});
const page = await context.newPage();

async function openFresh() {
  await page.goto(pageUrl, { waitUntil: "networkidle" });
  await page.evaluate((records) => {
    localStorage.setItem("day14_closed_loop_records", JSON.stringify(records));
    localStorage.setItem("day14_closed_loop_defaults", JSON.stringify({
      date: "2026-07-26",
      material: "稻香A",
      customMaterial: "",
      batch: "第一播期",
      customBatch: "",
      type: "植保",
      subtype: "破口药",
      customSubtype: "",
      stage: "分蘖",
      operator: "张工",
      followUp: "是",
    }));
  }, sampleRecords);
  await page.reload({ waitUntil: "networkidle" });
}

async function screenshot(name, options = {}) {
  await page.screenshot({
    path: path.join(outDir, name),
    fullPage: options.fullPage ?? false,
  });
}

await openFresh();
await screenshot("01-cover-closed-loop.png");

await page.locator("#field-form").screenshot({
  path: path.join(outDir, "02-input-form.png"),
});

await page.evaluate(() => {
  document.querySelector('[data-value="植保"]').click();
  document.querySelector("#operation-subtype").value = "齐穗药";
  document.querySelector("#operation-detail").value = "示例：齐穗期防治记录";
});
await page.locator("#field-form").screenshot({
  path: path.join(outDir, "03-operation-type-plant-protection.png"),
});

await page.click('[data-view-target="log-view"]');
await page.waitForTimeout(250);
await screenshot("04-operation-log-summary.png", { fullPage: true });

await page.click('[data-view-target="board-view"]');
await page.waitForTimeout(250);
await screenshot("05-stage-board-and-plot-history.png", { fullPage: true });

await page.click("#open-guide");
await page.waitForTimeout(250);
await screenshot("06-user-guide-modal.png");

await browser.close();

console.log(`Generated screenshots in ${outDir}`);
