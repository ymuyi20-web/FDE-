import csv
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).parent

json_path = base_dir / "farm_inputs.json"
history_path = base_dir / "day10_history.csv"


def create_default_inputs():
    inputs = [
        {"name": "种子", "cost_per_mu": 60.0},
        {"name": "肥料", "cost_per_mu": 200.0},
        {"name": "植保", "cost_per_mu": 95.0},
        {"name": "灌溉", "cost_per_mu": 120.0},
    ]

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(inputs, file, ensure_ascii=False, indent=4)

    return inputs


def load_inputs():
    if not json_path.exists():
        print("没有找到 farm_inputs.json，已经自动创建默认配置。")
        return create_default_inputs()

    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def calculate_cost_per_mu(inputs):
    total = 0

    for item in inputs:
        total = total + float(item["cost_per_mu"])

    return total


def save_history(area, cost_per_mu, total_cost):
    file_exists = history_path.exists()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(history_path, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["created_at", "area", "cost_per_mu", "total_cost"])

        writer.writerow([created_at, area, cost_per_mu, total_cost])

    print("本次计算结果已经保存到 day10_history.csv。")


def show_history():
    if not history_path.exists():
        print("还没有历史记录，请先进行一次成本计算。")
        return

    with open(history_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("\n历史记录：")

        for row in reader:
            print(
                row["created_at"],
                "，面积：",
                row["area"],
                "亩，每亩成本：",
                row["cost_per_mu"],
                "元，总成本：",
                row["total_cost"],
                "元",
            )


def calculate_and_save():
    try:
        area = float(input("请输入水稻种植面积（亩）："))

        if area <= 0:
            print("面积必须大于0。")
            return

        inputs = load_inputs()
        cost_per_mu = calculate_cost_per_mu(inputs)
        total_cost = area * cost_per_mu

        print("\n计算结果：")
        print(f"种植面积：{area:.2f} 亩")
        print(f"每亩总成本：{cost_per_mu:.2f} 元")
        print(f"预计总成本：{total_cost:.2f} 元")

        save_history(area, cost_per_mu, total_cost)

    except ValueError:
        print("输入错误，请输入纯数字。")


def main():
    while True:
        print("\n====== 水稻成本历史记录管理器 ======")
        print("1. 计算成本并保存历史记录")
        print("2. 查看历史记录")
        print("0. 退出")

        choice = input("请选择功能：")

        if choice == "1":
            calculate_and_save()

        elif choice == "2":
            show_history()

        elif choice == "0":
            print("程序已退出。")
            break

        else:
            print("输入错误，请重新选择。")


main()