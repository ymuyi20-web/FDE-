"""Day 10: generate a breeding field operation log.

This script turns field operation records into:
- a date-ordered operation timeline;
- operation-type statistics;
- material x sowing-batch summaries.
"""

from __future__ import annotations

import argparse
import csv
import html
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DATE_FORMAT = "%Y-%m-%d"
ALLOWED_OPERATION_TYPES = {"播种", "施肥", "打药", "灌溉", "除草", "巡田", "拍照", "测量", "收获"}
ALLOWED_FOLLOW_UP_VALUES = {"是", "否"}


@dataclass(frozen=True)
class OperationRecord:
    operation_id: str
    operation_date: datetime
    material_name: str
    sowing_batch: str
    plot_id: str
    operation_type: str
    operation_detail: str
    operator: str
    need_follow_up: str
    note: str


def parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), DATE_FORMAT)


def format_date(value: datetime) -> str:
    return value.strftime(DATE_FORMAT)


def read_operations(csv_path: Path) -> list[OperationRecord]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        records = [row_to_record(row) for row in reader]
    validate_operations(records)
    return records


def row_to_record(row: dict[str, str]) -> OperationRecord:
    return OperationRecord(
        operation_id=row["operation_id"].strip(),
        operation_date=parse_date(row["operation_date"]),
        material_name=row["material_name"].strip(),
        sowing_batch=row["sowing_batch"].strip(),
        plot_id=row["plot_id"].strip(),
        operation_type=row["operation_type"].strip(),
        operation_detail=row["operation_detail"].strip(),
        operator=row["operator"].strip(),
        need_follow_up=row["need_follow_up"].strip(),
        note=row["note"].strip(),
    )


def validate_operations(records: list[OperationRecord]) -> None:
    seen_ids: set[str] = set()
    for record in records:
        if record.operation_id in seen_ids:
            raise ValueError(f"操作编号重复：{record.operation_id}")
        seen_ids.add(record.operation_id)

        if record.operation_type not in ALLOWED_OPERATION_TYPES:
            raise ValueError(f"{record.operation_id} 的操作类型不在允许范围：{record.operation_type}")

        if record.need_follow_up not in ALLOWED_FOLLOW_UP_VALUES:
            raise ValueError(f"{record.operation_id} 的 need_follow_up 必须是 是 或 否")

        required_values = [
            record.operation_id,
            record.material_name,
            record.sowing_batch,
            record.plot_id,
            record.operation_detail,
            record.operator,
        ]
        if any(not value for value in required_values):
            raise ValueError(f"{record.operation_id} 存在必填字段为空")


def sort_operations(records: list[OperationRecord]) -> list[OperationRecord]:
    return sorted(
        records,
        key=lambda record: (
            record.operation_date,
            record.material_name,
            record.sowing_batch,
            record.plot_id,
            record.operation_type,
        ),
    )


def operation_type_counts(records: list[OperationRecord]) -> Counter[str]:
    return Counter(record.operation_type for record in records)


def material_batch_summary(records: list[OperationRecord]) -> dict[tuple[str, str], list[OperationRecord]]:
    summary: dict[tuple[str, str], list[OperationRecord]] = defaultdict(list)
    for record in sort_operations(records):
        summary[(record.material_name, record.sowing_batch)].append(record)
    return dict(summary)


def build_markdown(records: list[OperationRecord]) -> str:
    sorted_records = sort_operations(records)
    counts = operation_type_counts(records)
    follow_up_count = sum(1 for record in records if record.need_follow_up == "是")
    summary = material_batch_summary(records)

    lines = [
        "# Day 10 农事操作日志",
        "",
        "这是一份按日期排序的育种基地农事操作记录。",
        "",
        "## 1. 日志总览",
        "",
        f"- 操作记录数：{len(records)}",
        f"- 需要复查：{follow_up_count} 项",
        f"- 材料/播期组合：{len(summary)} 个",
        "",
        "## 2. 操作类型统计",
        "",
    ]

    for operation_type, count in counts.most_common():
        lines.append(f"- {operation_type}：{count} 次")

    lines.extend(
        [
            "",
            "## 3. 按日期排序的操作时间线",
            "",
            "| 日期 | 品种/材料 | 播期 | 小区 | 操作类型 | 操作内容 | 负责人 | 复查 | 备注 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    for record in sorted_records:
        lines.append(
            "| "
            + " | ".join(
                [
                    format_date(record.operation_date),
                    record.material_name,
                    record.sowing_batch,
                    record.plot_id,
                    record.operation_type,
                    record.operation_detail,
                    record.operator,
                    record.need_follow_up,
                    record.note,
                ]
            )
            + " |"
        )

    lines.extend(["", "## 4. 按材料/播期回溯", ""])
    for (material_name, sowing_batch), group in summary.items():
        lines.append(f"### {material_name} / {sowing_batch}")
        for record in group:
            follow_up = "，需复查" if record.need_follow_up == "是" else ""
            lines.append(
                f"- {format_date(record.operation_date)}：{record.operation_type}，{record.operation_detail}"
                f"（小区：{record.plot_id}，负责人：{record.operator}{follow_up}）"
            )
        lines.append("")

    lines.extend(
        [
            "## 5. 边界提醒",
            "",
            "本日志记录已经发生的农事操作，不判断材料优劣，不替代育种结论。",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(records: list[OperationRecord]) -> str:
    sorted_records = sort_operations(records)
    counts = operation_type_counts(records)
    follow_up_count = sum(1 for record in records if record.need_follow_up == "是")
    summary = material_batch_summary(records)

    stat_cards = (
        f"<div class='stat'><strong>{len(records)}</strong><span>操作记录</span></div>"
        f"<div class='stat danger'><strong>{follow_up_count}</strong><span>需要复查</span></div>"
        f"<div class='stat'><strong>{len(summary)}</strong><span>材料/播期组合</span></div>"
        f"<div class='stat'><strong>{len(counts)}</strong><span>操作类型</span></div>"
    )

    type_tags = "".join(
        f"<span class='tag'>{html.escape(operation_type)}：{count}</span>"
        for operation_type, count in counts.most_common()
    )

    rows = []
    for record in sorted_records:
        follow_class = "need-follow" if record.need_follow_up == "是" else ""
        rows.append(
            f"<tr class='{follow_class}'>"
            f"<td>{format_date(record.operation_date)}</td>"
            f"<td>{html.escape(record.material_name)}</td>"
            f"<td>{html.escape(record.sowing_batch)}</td>"
            f"<td>{html.escape(record.plot_id)}</td>"
            f"<td><strong>{html.escape(record.operation_type)}</strong></td>"
            f"<td>{html.escape(record.operation_detail)}</td>"
            f"<td>{html.escape(record.operator)}</td>"
            f"<td>{html.escape(record.need_follow_up)}</td>"
            f"<td>{html.escape(record.note)}</td>"
            "</tr>"
        )

    group_cards = []
    for (material_name, sowing_batch), group in summary.items():
        items = "".join(
            f"<li><strong>{format_date(record.operation_date)} {html.escape(record.operation_type)}</strong>"
            f"<span>{html.escape(record.operation_detail)}｜小区：{html.escape(record.plot_id)}｜负责人：{html.escape(record.operator)}</span></li>"
            for record in group
        )
        group_cards.append(
            f"<section class='group'><h3>{html.escape(material_name)} / {html.escape(sowing_batch)}</h3><ul>{items}</ul></section>"
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day 10 农事操作日志</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      background: #f3f6f2;
      color: #1d251d;
    }}
    main {{
      width: min(1200px, calc(100% - 32px));
      margin: 0 auto;
      padding: 36px 0 64px;
    }}
    .hero {{
      padding: 34px;
      border-radius: 28px;
      color: white;
      background: linear-gradient(135deg, #123c28, #7b4a1e);
      box-shadow: 0 18px 42px rgba(34, 42, 26, .18);
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 40px;
    }}
    .hero p {{
      margin: 0;
      color: #e8efdf;
      line-height: 1.8;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
      margin: 18px 0;
    }}
    .stat {{
      background: white;
      border: 1px solid #dfe6da;
      border-radius: 20px;
      padding: 18px;
    }}
    .stat strong {{
      display: block;
      color: #136b42;
      font-size: 34px;
    }}
    .stat.danger strong {{
      color: #b84a2a;
    }}
    .stat span, .tag {{
      color: #647060;
    }}
    .tags {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin: 0 0 18px;
    }}
    .tag {{
      background: white;
      border: 1px solid #dfe6da;
      border-radius: 999px;
      padding: 9px 13px;
      font-weight: 700;
    }}
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      background: white;
      border: 1px solid #dfe6da;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 18px 42px rgba(34, 42, 26, .10);
    }}
    th, td {{
      border-bottom: 1px solid #dfe6da;
      padding: 14px;
      text-align: left;
      vertical-align: top;
    }}
    tr:last-child td {{
      border-bottom: 0;
    }}
    thead th {{
      background: #e8efe3;
      color: #485847;
    }}
    tr.need-follow {{
      background: #fff8f0;
    }}
    tr.need-follow td:nth-child(8) {{
      color: #b84a2a;
      font-weight: 800;
    }}
    h2 {{
      margin-top: 30px;
    }}
    .groups {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 16px;
    }}
    .group {{
      background: white;
      border: 1px solid #dfe6da;
      border-radius: 20px;
      padding: 18px;
    }}
    .group h3 {{
      margin: 0 0 10px;
    }}
    .group ul {{
      margin: 0;
      padding-left: 20px;
    }}
    .group li {{
      margin: 10px 0;
      line-height: 1.6;
    }}
    .group span {{
      display: block;
      color: #647060;
    }}
    .note {{
      margin-top: 20px;
      color: #647060;
      line-height: 1.8;
    }}
    @media (max-width: 900px) {{
      .stats, .groups {{ grid-template-columns: 1fr; }}
      table {{ font-size: 14px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>农事操作日志</h1>
      <p>按时间线记录育种基地已经发生的播种、施肥、打药、巡田、拍照和测量操作，帮助后续回溯。</p>
    </section>
    <section class="stats">{stat_cards}</section>
    <section class="tags">{type_tags}</section>
    <table>
      <thead>
        <tr>
          <th>日期</th>
          <th>品种/材料</th>
          <th>播期</th>
          <th>小区</th>
          <th>类型</th>
          <th>内容</th>
          <th>负责人</th>
          <th>复查</th>
          <th>备注</th>
        </tr>
      </thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <h2>按材料/播期回溯</h2>
    <section class="groups">{''.join(group_cards)}</section>
    <p class="note">边界：本日志记录已经发生的农事操作，不判断材料优劣，不替代育种结论。</p>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Day 10 breeding operation log.")
    parser.add_argument("--data", required=True, help="输入 CSV 文件")
    parser.add_argument("--md-out", required=True, help="输出 Markdown 文件")
    parser.add_argument("--html-out", required=True, help="输出 HTML 文件")
    args = parser.parse_args()

    records = read_operations(Path(args.data))
    md_out = Path(args.md_out)
    html_out = Path(args.html_out)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text(build_markdown(records), encoding="utf-8")
    html_out.write_text(build_html(records), encoding="utf-8")

    counts = operation_type_counts(records)
    follow_up_count = sum(1 for record in records if record.need_follow_up == "是")

    print("Day 10 农事操作日志生成")
    print("=" * 34)
    print(f"读取操作记录：{len(records)} 条")
    print(f"操作类型：{len(counts)} 类")
    print(f"需要复查：{follow_up_count} 项")
    print(f"Markdown 日志：{md_out}")
    print(f"HTML 日志：{html_out}")
    print()
    print("提示：本日志只记录已经发生的操作，不判断材料优劣。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

