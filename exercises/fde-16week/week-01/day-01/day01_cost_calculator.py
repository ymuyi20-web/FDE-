"""Day 01 基线程序：水稻农资成本计算器。

今天的重点不是增加功能，而是读懂以下数据流：
JSON 农资数据 + 用户输入面积 -> 校验 -> 确定性计算 -> 屏幕输出。
"""

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
INPUT_PATH = BASE_DIR / "farm_inputs.example.json"


def load_items(path):
    """读取并检查农资配置。"""
    with open(path, "r", encoding="utf-8") as file:
        items = json.load(file)

    if not isinstance(items, list):
        raise ValueError("农资配置最外层必须是列表。")

    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"第 {index} 项农资必须是对象。")

        if "name" not in item or "cost_per_mu" not in item:
            raise ValueError(
                f"第 {index} 项农资缺少 name 或 cost_per_mu 字段。"
            )

        if not isinstance(item["name"], str) or not item["name"].strip():
            raise ValueError(f"第 {index} 项农资名称不能为空。")

        cost = item["cost_per_mu"]
        if not isinstance(cost, (int, float)) or isinstance(cost, bool):
            raise ValueError(f"第 {index} 项农资亩成本必须是数字。")

        if cost < 0:
            raise ValueError(f"第 {index} 项农资亩成本不能小于 0。")

    return items


def read_area():
    """读取并检查种植面积。"""
    area_text = input("请输入水稻种植面积（亩）：").strip()
    try:
        area = float(area_text)
    except ValueError as error:
        raise ValueError("种植面积必须填写为数字。") from error

    if area <= 0:
        raise ValueError("种植面积必须大于 0。")

    return area


def calculate_cost_per_mu(items):
    """计算每亩农资总成本。"""
    return sum(item["cost_per_mu"] for item in items)


def calculate_total_cost(area_mu, cost_per_mu):
    """计算指定面积的预计总成本。"""
    return area_mu * cost_per_mu


def show_result(area_mu, items, cost_per_mu, total_cost):
    """显示输入明细和计算结果。"""
    print("\n农资投入明细")
    print("-" * 32)

    for item in items:
        print(f"{item['name']:<8} {item['cost_per_mu']:>10.2f} 元/亩")

    print("-" * 32)
    print(f"种植面积：   {area_mu:.2f} 亩")
    print(f"每亩总成本： {cost_per_mu:.2f} 元/亩")
    print(f"预计总成本： {total_cost:.2f} 元")
    print("\n提示：本结果仅用于成本核算，不构成施肥处方或农艺建议。")


def main():
    try:
        items = load_items(INPUT_PATH)
        area_mu = read_area()
        cost_per_mu = calculate_cost_per_mu(items)
        total_cost = calculate_total_cost(area_mu, cost_per_mu)
        show_result(area_mu, items, cost_per_mu, total_cost)
    except FileNotFoundError:
        print(f"错误：没有找到配置文件 {INPUT_PATH.name}。")
    except json.JSONDecodeError:
        print(f"错误：{INPUT_PATH.name} 不是有效的 JSON。")
    except ValueError as error:
        print(f"输入或配置错误：{error}")


if __name__ == "__main__":
    main()
