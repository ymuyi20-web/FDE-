"""Day 09: generate observation tasks from breeding stage records.

Day 08 answers: what stage is each material x sowing batch in?
Day 09 answers: what should be checked first today?
"""

from __future__ import annotations

import argparse
import csv
import html
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


DATE_FORMAT = "%Y-%m-%d"

CHECK_INTERVAL_DAYS = {
    "播种": 7,
    "出苗": 10,
    "分蘖": 14,
    "拔节": 7,
    "孕穗": 5,
    "抽穗": 3,
    "灌浆": 7,
    "成熟": 5,
    "收获": 999,
}

STATUS_ORDER = {
    "逾期": 1,
    "今日到期": 2,
    "即将到期": 3,
    "正常跟踪": 4,
}


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


@dataclass(frozen=True)
class ObservationTask:
    material_name: str
    sowing_batch: str
    plot_id: str
    growth_stage: str
    last_event_date: datetime
    due_date: datetime
    status: str
    days_delta: int
    suggestion: str


def parse_date(value: str) -> datetime:
    return datetime.strptime(value.strip(), DATE_FORMAT)


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
        sowing_date=parse_date(row["sowing_date"]),
        plot_id=row["plot_id"].strip(),
        event_date=parse_date(row["event_date"]),
        growth_stage=row["growth_stage"].strip(),
        farm_operation=row["farm_operation"].strip(),
        next_observation=row["next_observation"].strip(),
        note=row["note"].strip(),
    )


def latest_by_material_batch(records: list[StageRecord]) -> list[StageRecord]:
    latest: dict[tuple[str, str], StageRecord] = {}
    for record in records:
        key = (record.material_name, record.sowing_batch)
        if key not in latest or record.event_date > latest[key].event_date:
            latest[key] = record
    return list(latest.values())


def task_status(today: datetime, due_date: datetime) -> tuple[str, int]:
    days_delta = (due_date - today).days
    if days_delta < 0:
        return "逾期", days_delta
    if days_delta == 0:
        return "今日到期", days_delta
    if days_delta <= 3:
        return "即将到期", days_delta
    return "正常跟踪", days_delta


def build_tasks(records: list[StageRecord], today: datetime) -> list[ObservationTask]:
    tasks: list[ObservationTask] = []
    for record in latest_by_material_batch(records):
        interval = CHECK_INTERVAL_DAYS.get(record.growth_stage)
        if interval is None:
            raise ValueError(f"未知生育期：{record.growth_stage}")

        due_date = record.event_date + timedelta(days=interval)
        status, days_delta = task_status(today, due_date)
        tasks.append(
            ObservationTask(
                material_name=record.material_name,
                sowing_batch=record.sowing_batch,
                plot_id=record.plot_id,
                growth_stage=record.growth_stage,
                last_event_date=record.event_date,
                due_date=due_date,
                status=status,
                days_delta=days_delta,
                suggestion=record.next_observation or "待人工确认",
            )
        )

    return sorted(
        tasks,
        key=lambda task: (
            STATUS_ORDER[task.status],
            task.due_date,
            task.material_name,
            task.sowing_batch,
        ),
    )


def status_text(task: ObservationTask) -> str:
    if task.status == "逾期":
        return f"已逾期 {abs(task.days_delta)} 天"
    if task.status == "今日到期":
        return "今天应观察"
    if task.status == "即将到期":
        return f"{task.days_delta} 天后应观察"
    return f"{task.days_delta} 天后跟踪"


def summarize(tasks: list[ObservationTask]) -> dict[str, int]:
    summary = {status: 0 for status in STATUS_ORDER}
    for task in tasks:
        summary[task.status] += 1
    return summary


def build_markdown(tasks: list[ObservationTask], today: datetime) -> str:
    summary = summarize(tasks)
    lines = [
        "# Day 09 育种观察待办",
        "",
        f"生成日期：{format_date(today)}",
        "",
        "## 1. 待办总览",
        "",
        f"- 逾期：{summary['逾期']} 项",
        f"- 今日到期：{summary['今日到期']} 项",
        f"- 即将到期：{summary['即将到期']} 项",
        f"- 正常跟踪：{summary['正常跟踪']} 项",
        "",
        "## 2. 观察任务清单",
        "",
        "| 状态 | 品种/材料 | 播期 | 小区 | 当前生育期 | 最近观察 | 应观察日期 | 提醒 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for task in tasks:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{task.status}（{status_text(task)}）",
                    task.material_name,
                    task.sowing_batch,
                    task.plot_id,
                    task.growth_stage,
                    format_date(task.last_event_date),
                    format_date(task.due_date),
                    task.suggestion,
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## 3. 边界提醒",
            "",
            "本清单只根据最近观察日期和固定复查间隔生成提醒，不判断材料优劣，不替代育种专家判断。",
            "",
        ]
    )
    return "\n".join(lines)


def status_class(status: str) -> str:
    return {
        "逾期": "overdue",
        "今日到期": "today",
        "即将到期": "soon",
        "正常跟踪": "normal",
    }[status]


def build_html(tasks: list[ObservationTask], today: datetime) -> str:
    summary = summarize(tasks)
    cards = "".join(
        f"<div class='stat {status_class(status)}'><strong>{count}</strong><span>{status}</span></div>"
        for status, count in summary.items()
    )
    rows = []
    for task in tasks:
        rows.append(
            f"<tr class='{status_class(task.status)}'>"
            f"<td><strong>{html.escape(task.status)}</strong><span>{html.escape(status_text(task))}</span></td>"
            f"<td>{html.escape(task.material_name)}</td>"
            f"<td>{html.escape(task.sowing_batch)}</td>"
            f"<td>{html.escape(task.plot_id)}</td>"
            f"<td>{html.escape(task.growth_stage)}</td>"
            f"<td>{format_date(task.last_event_date)}</td>"
            f"<td>{format_date(task.due_date)}</td>"
            f"<td>{html.escape(task.suggestion)}</td>"
            "</tr>"
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Day 09 育种观察待办</title>
  <style>
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
      background: #f7f4ee;
      color: #261d14;
    }}
    main {{
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      padding: 36px 0 56px;
    }}
    .hero {{
      border-radius: 28px;
      padding: 32px;
      color: white;
      background: linear-gradient(135deg, #7c3f19, #1f4d32);
      box-shadow: 0 20px 44px rgba(58, 37, 18, 0.18);
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 40px;
    }}
    .hero p {{
      margin: 0;
      color: #f3e7d7;
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
      border-radius: 20px;
      padding: 18px;
      border: 1px solid #e5ddcf;
    }}
    .stat strong {{
      display: block;
      font-size: 34px;
    }}
    .stat span {{
      color: #6c6155;
    }}
    .stat.overdue strong {{ color: #b42318; }}
    .stat.today strong {{ color: #b06a00; }}
    .stat.soon strong {{ color: #1d6f42; }}
    .stat.normal strong {{ color: #61705f; }}
    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      background: white;
      border: 1px solid #e5ddcf;
      border-radius: 24px;
      overflow: hidden;
      box-shadow: 0 18px 40px rgba(58, 37, 18, 0.10);
    }}
    th, td {{
      border-bottom: 1px solid #e5ddcf;
      padding: 16px;
      text-align: left;
      vertical-align: top;
    }}
    tr:last-child td {{ border-bottom: 0; }}
    thead th {{
      background: #f0e7da;
      color: #594737;
    }}
    td strong, td span {{
      display: block;
    }}
    td span {{
      margin-top: 5px;
      color: #6c6155;
      font-size: 13px;
    }}
    tr.overdue td:first-child strong {{ color: #b42318; }}
    tr.today td:first-child strong {{ color: #b06a00; }}
    tr.soon td:first-child strong {{ color: #1d6f42; }}
    tr.normal td:first-child strong {{ color: #61705f; }}
    .note {{
      margin-top: 20px;
      color: #6c6155;
      line-height: 1.8;
    }}
    @media (max-width: 900px) {{
      .stats {{ grid-template-columns: 1fr 1fr; }}
      table {{ font-size: 14px; }}
      th, td {{ padding: 12px; }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>育种观察待办</h1>
      <p>生成日期：{format_date(today)}。根据最近观察日期和生育期复查规则，列出今天应优先关注的材料、播期和小区。</p>
    </section>
    <section class="stats">{cards}</section>
    <table>
      <thead>
        <tr>
          <th>状态</th>
          <th>品种/材料</th>
          <th>播期</th>
          <th>小区</th>
          <th>当前生育期</th>
          <th>最近观察</th>
          <th>应观察日期</th>
          <th>提醒</th>
        </tr>
      </thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
    <p class="note">边界：本清单只生成观察提醒，不判断材料优劣，不替代育种专家判断。</p>
  </main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Day 09 breeding observation tasks.")
    parser.add_argument("--data", required=True, help="输入 CSV 文件")
    parser.add_argument("--today", required=True, help="今天日期，格式 YYYY-MM-DD")
    parser.add_argument("--md-out", required=True, help="输出 Markdown 文件")
    parser.add_argument("--html-out", required=True, help="输出 HTML 文件")
    args = parser.parse_args()

    today = parse_date(args.today)
    records = read_records(Path(args.data))
    tasks = build_tasks(records, today)

    md_out = Path(args.md_out)
    html_out = Path(args.html_out)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    html_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text(build_markdown(tasks, today), encoding="utf-8")
    html_out.write_text(build_html(tasks, today), encoding="utf-8")

    summary = summarize(tasks)
    print("Day 09 育种观察待办生成")
    print("=" * 38)
    print(f"读取记录数：{len(records)}")
    print(f"生成任务数：{len(tasks)}")
    print(f"逾期：{summary['逾期']} 项")
    print(f"今日到期：{summary['今日到期']} 项")
    print(f"即将到期：{summary['即将到期']} 项")
    print(f"正常跟踪：{summary['正常跟踪']} 项")
    print(f"Markdown 待办：{md_out}")
    print(f"HTML 待办：{html_out}")
    print()
    print("提示：本清单只生成观察提醒，不判断材料优劣。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

