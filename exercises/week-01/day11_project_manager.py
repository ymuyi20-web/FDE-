import csv
import json
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).parent

data_dir = base_dir / "data"
outputs_dir = base_dir / "outputs"
docs_dir = base_dir / "docs"

json_path = data_dir / "farm_inputs.json"
history_path = outputs_dir / "day11_history.csv"
report_path = docs_dir / "day11_report.txt"


def create_dirs():
    data_dir.mkdir(exist_ok=True)
    outputs_dir.mkdir(exist_ok=True)
    docs_dir.mkdir(exist_ok=True)


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
        print("没有找到 data/farm_inputs.json，已经自动创建默认配置。")
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

    print("历史记录已经保存到 outputs/day11_history.csv。")


def save_report(area, cost_per_mu, total_cost):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("Day11 水稻成本计算报告\n")
        file.write("====================\n\n")
        file.write(f"生成时间：{created_at}\n")
        file.write(f"种植面积：{area:.2f} 亩\n")
        file.write(f"每亩总成本：{cost_per_mu:.2f} 元\n")
        file.write(f"预计总成本：{total_cost:.2f} 元\n")

    print("文字报告已经保存到 docs/day11_report.txt。")


def main():
    create_dirs()

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
        save_report(area, cost_per_mu, total_cost)

    except ValueError:
        print("输入错误，请输入纯数字。")


main()