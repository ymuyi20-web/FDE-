"""Day 06: validate a breeding-field CSV data template.

This exercise is intentionally small. It teaches one FDE habit:
before building features, define and validate the shape of incoming business data.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
from pathlib import Path


REQUIRED_COLUMNS = [
    "record_id",
    "variety_name",
    "sowing_batch",
    "plot_id",
    "plot_area_mu",
    "event_date",
    "growth_stage",
    "farm_operation",
    "operator",
    "note",
]

REQUIRED_NON_EMPTY_FIELDS = [
    "record_id",
    "variety_name",
    "sowing_batch",
    "plot_id",
    "plot_area_mu",
    "event_date",
    "growth_stage",
]

ALLOWED_GROWTH_STAGES = {
    "播种",
    "出苗",
    "分蘖",
    "拔节",
    "孕穗",
    "抽穗",
    "灌浆",
    "成熟",
    "收获",
}


class TemplateValidationError(Exception):
    """Raised when the CSV template does not match the field contract."""


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    if not csv_path.exists():
        raise TemplateValidationError(f"文件不存在：{csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        validate_columns(reader.fieldnames)
        return list(reader)


def validate_columns(fieldnames: list[str] | None) -> None:
    if fieldnames is None:
        raise TemplateValidationError("CSV 文件缺少表头。")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in fieldnames]
    extra_columns = [column for column in fieldnames if column not in REQUIRED_COLUMNS]

    if missing_columns:
        raise TemplateValidationError(f"缺少必需字段：{', '.join(missing_columns)}")

    if extra_columns:
        raise TemplateValidationError(f"发现未约定字段：{', '.join(extra_columns)}")


def parse_positive_float(value: str, field_name: str, row_number: int) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise TemplateValidationError(
            f"第 {row_number} 行 `{field_name}` 必须是数字。"
        ) from error

    if parsed <= 0:
        raise TemplateValidationError(
            f"第 {row_number} 行 `{field_name}` 必须大于 0。"
        )

    return parsed


def validate_date(value: str, field_name: str, row_number: int) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise TemplateValidationError(
            f"第 {row_number} 行 `{field_name}` 必须使用 YYYY-MM-DD 格式。"
        ) from error


def validate_rows(rows: list[dict[str, str]]) -> None:
    if not rows:
        raise TemplateValidationError("CSV 文件没有数据行。")

    seen_record_ids: set[str] = set()

    for index, row in enumerate(rows, start=2):
        for field_name in REQUIRED_NON_EMPTY_FIELDS:
            if not row[field_name].strip():
                raise TemplateValidationError(
                    f"第 {index} 行 `{field_name}` 不能为空。"
                )

        record_id = row["record_id"].strip()
        if record_id in seen_record_ids:
            raise TemplateValidationError(f"第 {index} 行记录编号重复：{record_id}")
        seen_record_ids.add(record_id)

        parse_positive_float(row["plot_area_mu"].strip(), "plot_area_mu", index)
        validate_date(row["event_date"].strip(), "event_date", index)

        growth_stage = row["growth_stage"].strip()
        if growth_stage not in ALLOWED_GROWTH_STAGES:
            allowed = "、".join(sorted(ALLOWED_GROWTH_STAGES))
            raise TemplateValidationError(
                f"第 {index} 行生育期阶段 `{growth_stage}` 不在允许列表中。允许值：{allowed}"
            )


def build_summary(rows: list[dict[str, str]]) -> dict[str, int]:
    varieties = {row["variety_name"].strip() for row in rows}
    sowing_batches = {row["sowing_batch"].strip() for row in rows}
    plots = {row["plot_id"].strip() for row in rows}

    return {
        "records": len(rows),
        "varieties": len(varieties),
        "sowing_batches": len(sowing_batches),
        "plots": len(plots),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Day 06 breeding CSV template.")
    parser.add_argument("--data", required=True, help="CSV 文件路径")
    args = parser.parse_args()

    try:
        rows = read_rows(Path(args.data))
        validate_rows(rows)
    except TemplateValidationError as error:
        print("Day 06 育种记录数据模板校验")
        print("=" * 42)
        print(f"校验失败：{error}")
        return 1

    summary = build_summary(rows)
    print("Day 06 育种记录数据模板校验")
    print("=" * 42)
    print("校验通过")
    print(f"记录数：{summary['records']}")
    print(f"品种数：{summary['varieties']}")
    print(f"播期数：{summary['sowing_batches']}")
    print(f"小区数：{summary['plots']}")
    print()
    print("提示：本脚本只校验数据模板，不判断品种表现或农事操作是否合理。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
