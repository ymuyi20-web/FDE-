"""Day 03 demo runner for the rice input cost calculator."""

import argparse
import json
from pathlib import Path
import sys

from src.farm_cost import CostInputError, build_cost_report, load_items


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "farm_inputs.example.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="计算水稻农资投入成本。本工具只做成本核算，不构成施肥处方。"
    )
    parser.add_argument("--area", type=float, required=True, help="水稻种植面积，单位：亩")
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="农资成本 JSON 文件路径",
    )
    return parser.parse_args()


def print_report(report):
    print("\nDay 03 水稻农资成本核算")
    print("-" * 36)
    for item in report["items"]:
        print(f"{item['name']:<8} {item['cost_per_mu']:>10.2f} 元/亩")
    print("-" * 36)
    print(f"种植面积：    {report['area_mu']:.2f} 亩")
    print(f"每亩总成本：  {report['cost_per_mu']:.2f} 元/亩")
    print(f"预计总成本：  {report['total_cost']:.2f} 元")
    print("\n提示：本结果仅用于成本核算，不构成施肥处方、采购依据或农艺建议。")


def main():
    args = parse_args()
    try:
        items = load_items(args.data)
        report = build_cost_report(args.area, items)
    except FileNotFoundError:
        print(f"输入或配置错误：未找到数据文件 {args.data}")
        return 1
    except json.JSONDecodeError:
        print(f"输入或配置错误：{args.data} 不是有效 JSON。")
        return 1
    except CostInputError as error:
        print(f"输入或配置错误：{error}")
        return 1

    print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
