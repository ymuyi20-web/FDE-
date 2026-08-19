"""Day 08: generate a variety/material x sowing-batch stage board.

This script turns breeding-stage records into a matrix view:
rows are materials, columns are sowing batches, cells show the latest growth stage.
"""

from __future__ import annotations

import argparse
import csv
import html
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DATE_FORMAT = "%Y-%m-%d"
STAGE_ORDER = ["播种", "出苗", "分蘖", "拔节", "孕穗", "抽穗", "灌浆", "成熟", "收获"]


@dataclass(frozen=True)
class StageRecord:
    record_id: str
    material_name: str
    sowing_batch: str
    sowing_date: datetime
    plot_id: str
    event_date: datetime
    growth_stage: str
    farm_operation: str
    next_observation: str
    note: str


def format_date(value: datetime) -> str:
    return value.strftime(DATE_FORMAT)


def read_records(csv_path: Path) -> list[StageRecord]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return [row_to_record(row) for row in reader]


def row_to_record(row: dict[str, str]) -> StageRecord:
    return StageRecord(
        record_id=row["record_id"].strip(),
        material_name=row["material_name"].strip(),
        sowing_batch=row["sowing_batch"].strip(),
        sowing_date=datetime.strptime(row["sowing_date"].strip(), DATE_FORMAT),
        plot_id=row["plot_id"].strip(),
        event_date=datetime.strptime(row["event_date"].strip(), DATE_FORMAT),
        growth_stage=row["growth_stage"].strip(),
        farm_operation=row["farm_operation"].strip(),
        next_observation=row["next_observation"].strip(),
        note=row["note"].strip(),
    )


def latest_by_material_batch(records: list[StageRecord]) -> dict[tuple[str, str], StageRecord]:
    latest: dict[tuple[str, str], StageRecord] = {}
    for record in records:
        key = (record.material_name, record.sowing_batch)
        if key not in latest or record.event_date > latest[key].event_date:
            latest[key] = record
    return latest


def sorted_materials(records: list[StageRecord]) -> list[str]:
    return sorted({record.material_name for record in records})


def sorted_batches(records: list[StageRecord]) -> list[str]:
    def batch_key(batch: str) -> tuple[int, str]:
        order = {"第一播期": 1, "第二播期": 2, "第三播期": 3}
        return (order.get(batch, 99), batch)

    return sorted({record.sowing_batch for record in records}, key=batch_key)


def stage_badge(record: StageRecord | None) -> str:
    if record is None:
        return "未记录"
    return record.growth_stage


def build_markdown(records: list[StageRecord]) -> str:
    materials = sorted_materials(records)
    batches = sorted_batches(records)
    latest = latest_by_material_batch(records)

    lines = [
        "# Day 08 育种生育期进度看板",
        "",
        "这是一份“品种/材料 × 播期”的当前生育期进度表。",
        "",
        "## 1. 看板总览",
        "",
        f"- 材料数：{len(materials)}",
        f"- 播期数：{len(batches)}",
        f"- 记录数：{len(records)}",
        "",
        "## 2. 品种/材料 × 播期进度表",
        "",
    ]

    header = ["品种/材料", *batches]
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * len(header)) + " |")

    for material in materials:
        row = [material]
        for batch in batches:
            record = latest.get((material, batch))
            if record is None:
                row.append("未记录")
            else:
                row.append(
                    f"{record.growth_stage}<br>"
                    f"小区：{record.plot_id}<br>"
                    f"播种：{format_date(record.sowing_date)}<br>"
                    f"最近：{format_date(record.event_date)}"
                )
        lines.append("| " + " | ".join(row) + " |")

    lines.extend(["", "## 3. 下一步观察事项", ""])
    for material in materials:
        lines.append(f"### {material}")
        for batch in batches:
            record = latest.get((material, batch))
            if record is None:
                lines.append(f"- {batch}：未记录，需确认是否已播种或是否漏填。")
            else:
                lines.append(
                    f"- {batch}：当前 `{record.growth_stage}`，下一步：{record.next_observation or '待人工确认'}。"
                )
        lines.append("")

    lines.extend(
        [
            "## 4. 边界提醒",
            "",
            "本看板只展示已有记录和固定观察提醒，不判断材料优劣，不生成育种选择建议。",
            "",
        ]
    )
    return "\n".join(lines)


def stage_class(stage: str) -> str:
    if stage == "未记录":
        return "stage-missing"
    if stage in {"抽穗", "灌浆", "成熟", "收获"}:
        return "stage-late"
    if stage in {"拔节", "孕穗"}:
        return "stage-mid"
    return "stage-early"


def build_html(records: list[StageRecord]) -> str:
    materials = sorted_materials(records)
    batches = sorted_batches(records)
    latest = latest_by_material_batch(records)

    header_cells = "".join(f"<th>{html.escape(batch)}</th>" for batch in batches)
    body_rows: list[str] = []

    for material in materials:
        cells = [f"<th class='material'>{html.escape(material)}</th>"]
        for batch in batches:
            record = latest.get((material, batch))
            if record is None:
                cells.append(
                    "<td class='stage-missing'><strong>未记录</strong><span>需确认是否漏填</span></td>"
                )
            else:
                cells.append(
                    f"<td class='{stage_class(record.growth_stage)}'>"
                    f"<strong>{html.escape(record.growth_stage)}</strong>"
                    f"<span>小区：{html.escape(record.plot_id)}</span>"
                    f"<span>播种：{format_date(record.sowing_date)}</span>"
                    f"<span>最近：{format_date(record.event_date)}</span>"
                    f"<em>{html.escape(record.next_observation or '待人工确认')}</em>"
                    "</td>"
                )
        body_rows.append("<tr>" + "".join(cells) + "</tr>")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day 08 育种生育期进度看板</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      background: #f5f7ef;
      color: #16281a;
    }}
    main {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      padding: 36px 0 56px;
    }}
    .hero {{
      background: linear-gradient(135deg, #0e5f3b, #17341f);
      color: white;
      border-radius: 28px;
      padding: 32px;
      box-shadow: 0 18px 40px rgba(20, 50, 29, 0.18);
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 40px;
    }}
    .hero p {{
      margin: 0;
      color: #dcebd7;
      line-height: 1.8;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 14px;
      margin: 18px 0;
    }}
    .stat {{
      background: white;
      border-radius: 20px;
      padding: 18px;
      border: 1px solid #dfe8d8;
    }}
    .stat strong {{
      display: block;
      font-size: 32px;
      color: #0e6b43;
    }}
    .stat span {{
      color: #61705f;
    }}
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      background: white;
      border: 1px solid #dfe8d8;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 18px 40px rgba(20, 50, 29, 0.10);
    }}
    th, td {{
      border-bottom: 1px solid #dfe8d8;
      border-right: 1px solid #dfe8d8;
      padding: 18px;
      vertical-align: top;
    }}
    tr:last-child th, tr:last-child td {{
      border-bottom: 0;
    }}
    th:last-child, td:last-child {{
      border-right: 0;
    }}
    thead th {{
      background: #eef5e9;
      color: #435440;
      text-align: left;
    }}
    .material {{
      width: 150px;
      background: #f8fbf4;
      font-size: 18px;
    }}
    td strong {{
      display: inline-block;
      margin-bottom: 10px;
      font-size: 22px;
    }}
    td span, td em {{
      display: block;
      margin-top: 6px;
      color: #526350;
      font-style: normal;
      line-height: 1.5;
    }}
    td em {{
      margin-top: 12px;
      color: #0e6b43;
      font-weight: 700;
    }}
    .stage-early strong {{ color: #277a43; }}
    .stage-mid strong {{ color: #9a6400; }}
    .stage-late strong {{ color: #b54a2a; }}
    .stage-missing strong {{ color: #777; }}
    .stage-missing {{ background: #f3f3ef; }}
    .note {{
      margin-top: 20px;
      color: #61705f;
      line-height: 1.8;
    }}
    @media (max-width: 800px) {{
      .stats {{ grid-template-columns: 1fr; }}
      table {{ font-size: 14px; }}
      th, td {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>育种生育期进度看板</h1>
      <p>按“品种/材料 × 播期”展示当前生育期、播种日期、最近观察日期和下一步观察事项。</p>
    </section>
    <section class="stats">
      <div class="stat"><strong>{len(materials)}</strong><span>材料数</span></div>
      <div class="stat"><strong>{len(batches)}</strong><span>播期数</span></div>
      <div class="stat"><strong>{len(records)}</strong><span>记录数</span></div>
    </section>
    <table>
      <thead>
        <tr><th>品种/材料</th>{header_cells}</tr>
      </thead>
      <tbody>
        {''.join(body_rows)}
      </tbody>
    </table>
    <p class="note">边界：本看板只展示已有记录和固定观察提醒，不判断材料优劣，不生成育种选择建议。</p>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Day 08 breeding stage board.")
    parser.add_argument("--data", required=True, help="输入 CSV 文件")
    parser.add_argument("--md-out", required=True, help="输出 Markdown 文件")
    parser.add_argument("--html-out", required=True, help="输出 HTML 文件")
    args = parser.parse_args()

    records = read_records(Path(args.data))
    md_out = Path(args.md_out)
    html_out = Path(args.html_out)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.parent.mkdir(parents=True, exist_ok=True)

    md_out.write_text(build_markdown(records), encoding="utf-8")
    html_out.write_text(build_html(records), encoding="utf-8")

    print("Day 08 育种生育期进度看板生成")
    print("=" * 42)
    print(f"读取记录数：{len(records)}")
    print(f"Markdown 看板：{md_out}")
    print(f"HTML 看板：{html_out}")
    print()
    print("提示：本看板只展示记录进展，不判断材料优劣。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
