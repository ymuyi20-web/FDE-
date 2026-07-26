"""Run the seasonal N-P2O5-K2O calculator with a JSON plan."""

import argparse
import json
from pathlib import Path
import sys

from src.season_npk import NutrientInputError, build_season_report, load_plan


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "sample_plan.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="核算一季水稻 N-P2O5-K2O 投入量，不构成施肥处方。"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="施肥方案 JSON 文件路径",
    )
    return parser.parse_args()


def print_report(report):
    print("\n水稻当季 N-P2O5-K2O 投入量核算")
    print("=" * 46)
    print(f"作物：{report['crop']}")
    print(f"养分口径：{report['nutrient_basis']}")

    for stage in report["stages"]:
        print("\n" + stage["stage_name"])
        print("-" * 46)
        for fertilizer in stage["fertilizers"]:
            print(
                f"{fertilizer['fertilizer_name']:<12}"
                f"{fertilizer['amount_kg_per_mu']:>8.2f} kg/亩 "
                f"N {fertilizer['n_percent']:>5.2f}% "
                f"P2O5 {fertilizer['p2o5_percent']:>5.2f}% "
                f"K2O {fertilizer['k2o_percent']:>5.2f}%"
            )
        totals = stage["totals"]
        print(
            f"阶段合计：N {totals['n_kg_per_mu']:.2f} kg/亩，"
            f"P2O5 {totals['p2o5_kg_per_mu']:.2f} kg/亩，"
            f"K2O {totals['k2o_kg_per_mu']:.2f} kg/亩"
        )

    season = report["season_totals"]
    print("\n全季合计")
    print("-" * 46)
    print(f"N    {season['n_kg_per_mu']:.2f} kg/亩")
    print(f"P2O5 {season['p2o5_kg_per_mu']:.2f} kg/亩")
    print(f"K2O  {season['k2o_kg_per_mu']:.2f} kg/亩")
    print("\n提示：本结果仅用于养分投入量核算，不构成施肥处方或农艺建议。")


def main():
    args = parse_args()
    try:
        plan = load_plan(args.data)
        report = build_season_report(plan)
    except FileNotFoundError:
        print(f"输入或配置错误：未找到数据文件 {args.data}")
        return 1
    except json.JSONDecodeError:
        print(f"输入或配置错误：{args.data} 不是有效 JSON。")
        return 1
    except NutrientInputError as error:
        print(f"输入或配置错误：{error}")
        return 1

    print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
