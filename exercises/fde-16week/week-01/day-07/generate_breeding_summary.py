"""Day 07: generate a business-readable summary from breeding records.

Day 06 checked whether the data shape is valid.
Day 07 turns valid rows into a small Markdown report that a field user can read.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


DATE_FORMAT = "%Y-%m-%d"


@dataclass(frozen=True)
class BreedingRecord:
    record_id: str
    variety_name: str
    sowing_batch: str
    plot_id: str
    plot_area_mu: float
    event_date: datetime
    growth_stage: str
    farm_operation: str
    operator: str
    note: str


def read_records(csv_path: Path) -> list[BreedingRecord]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        return [row_to_record(row) for row in reader]


def row_to_record(row: dict[str, str]) -> BreedingRecord:
    return BreedingRecord(
        record_id=row["record_id"].strip(),
        variety_name=row["variety_name"].strip(),
        sowing_batch=row["sowing_batch"].strip(),
        plot_id=row["plot_id"].strip(),
        plot_area_mu=float(row["plot_area_mu"]),
        event_date=datetime.strptime(row["event_date"].strip(), DATE_FORMAT),
        growth_stage=row["growth_stage"].strip(),
        farm_operation=row["farm_operation"].strip(),
        operator=row["operator"].strip(),
        note=row["note"].strip(),
    )


def format_date(value: datetime) -> str:
    return value.strftime(DATE_FORMAT)


def unique_sorted(values: list[str]) -> list[str]:
    return sorted(set(values))


def latest_record(records: list[BreedingRecord]) -> BreedingRecord:
    return max(records, key=lambda record: record.event_date)


def stage_path(records: list[BreedingRecord]) -> str:
    ordered = sorted(records, key=lambda record: record.event_date)
    stages: list[str] = []
    for record in ordered:
        if record.growth_stage not in stages:
            stages.append(record.growth_stage)
    return " → ".join(stages)


def build_overview(records: list[BreedingRecord]) -> list[str]:
    varieties = unique_sorted([record.variety_name for record in records])
    sowing_batches = unique_sorted([record.sowing_batch for record in records])
    plots = unique_sorted([record.plot_id for record in records])
    dates = [record.event_date for record in records]

    return [
        "## 1. 数据总览",
        "",
        f"- 记录数：{len(records)}",
        f"- 品种数：{len(varieties)}",
        f"- 播期数：{len(sowing_batches)}",
        f"- 小区数：{len(plots)}",
        f"- 日期范围：{format_date(min(dates))} 至 {format_date(max(dates))}",
        "",
    ]


def build_variety_summary(records: list[BreedingRecord]) -> list[str]:
    groups: dict[str, list[BreedingRecord]] = defaultdict(list)
    for record in records:
        groups[record.variety_name].append(record)

    lines = ["## 2. 按品种汇总", ""]
    for variety_name in sorted(groups):
        group_records = groups[variety_name]
        latest = latest_record(group_records)
        sowing_batches = "、".join(unique_sorted([r.sowing_batch for r in group_records]))
        plots = "、".join(unique_sorted([r.plot_id for r in group_records]))

        lines.extend(
            [
                f"### {variety_name}",
                "",
                f"- 记录数：{len(group_records)}",
                f"- 涉及播期：{sowing_batches}",
                f"- 涉及小区：{plots}",
                f"- 最近记录：{format_date(latest.event_date)}，{latest.growth_stage}，{latest.plot_id}",
                "",
            ]
        )

    return lines


def build_variety_batch_summary(records: list[BreedingRecord]) -> list[str]:
    groups: dict[tuple[str, str], list[BreedingRecord]] = defaultdict(list)
    for record in records:
        groups[(record.variety_name, record.sowing_batch)].append(record)

    lines = ["## 3. 按品种 + 播期汇总", ""]
    for variety_name, sowing_batch in sorted(groups):
        group_records = groups[(variety_name, sowing_batch)]
        latest = latest_record(group_records)
        plots = "、".join(unique_sorted([r.plot_id for r in group_records]))
        stages = stage_path(group_records)

        lines.extend(
            [
                f"### {variety_name} / {sowing_batch}",
                "",
                f"- 小区：{plots}",
                f"- 记录数：{len(group_records)}",
                f"- 生育期进展：{stages}",
                f"- 最近记录：{format_date(latest.event_date)}，{latest.growth_stage}",
                "",
            ]
        )

    return lines


def build_recent_records(records: list[BreedingRecord], limit: int = 5) -> list[str]:
    lines = ["## 4. 最近观察记录", ""]
    ordered = sorted(records, key=lambda record: record.event_date, reverse=True)
    for record in ordered[:limit]:
        lines.append(
            f"- {format_date(record.event_date)}｜{record.variety_name}｜{record.sowing_batch}｜"
            f"{record.plot_id}｜{record.growth_stage}｜{record.farm_operation or '未记录操作'}"
        )
    lines.append("")
    return lines


def build_boundary_note() -> list[str]:
    return [
        "## 5. 边界提醒",
        "",
        "本报告只整理已有记录，不判断品种表现，不生成农事建议，也不替代育种人员的田间判断。",
        "",
        "如果要继续做成真实工具，下一步可以把这份摘要变成网页看板、日历提醒或小区进度追踪。",
        "",
    ]


def build_report(records: list[BreedingRecord]) -> str:
    lines = [
        "# Day 07 育种记录摘要报告",
        "",
        "这是一份由 CSV 数据自动生成的业务摘要。",
        "",
    ]
    lines.extend(build_overview(records))
    lines.extend(build_variety_summary(records))
    lines.extend(build_variety_batch_summary(records))
    lines.extend(build_recent_records(records))
    lines.extend(build_boundary_note())
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Day 07 breeding summary report.")
    parser.add_argument("--data", required=True, help="输入 CSV 文件")
    parser.add_argument("--out", required=True, help="输出 Markdown 文件")
    args = parser.parse_args()

    data_path = Path(args.data)
    out_path = Path(args.out)

    records = read_records(data_path)
    report = build_report(records)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")

    print("Day 07 育种记录摘要报告生成")
    print("=" * 42)
    print(f"读取记录数：{len(records)}")
    print(f"报告已生成：{out_path}")
    print()
    print("提示：本报告只整理已有记录，不判断品种表现或农事操作是否合理。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
