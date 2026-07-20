from pathlib import Path
import csv

base_dir = Path(__file__).parent
csv_path = base_dir / "inputs.csv"

# 准备农资数据
items = [
    {"name": "种子", "cost_per_mu": 60.0},
    {"name": "肥料", "cost_per_mu": 220.0},
    {"name": "植保", "cost_per_mu": 95.0},
    {"name": "灌溉", "cost_per_mu": 80.0},
]

# 第一步：写入CSV文件
with open(csv_path, "w", encoding="utf-8-sig", newline="") as file:
    fieldnames = ["name", "cost_per_mu"]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(items)

print("inputs.csv写入完成。")

# 第二步：读取CSV文件
print("\n读取到的农资数据：")

with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(
            "农资名称：",
            row["name"],
            "，每亩成本：",
            row["cost_per_mu"],
            "元",
        )