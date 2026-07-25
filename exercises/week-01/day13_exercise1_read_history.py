import csv
from pathlib import Path

base_dir = Path(__file__).parent
outputs_dir = base_dir / "outputs"
history_path = outputs_dir / "day11_history.csv"

if not history_path.exists():
    print("没有找到历史记录文件，请先运行 Day11 正式作业。")
else:
    with open(history_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        print("历史记录：")

        for row in reader:
            print(
                row["created_at"],
                "，面积：",
                row["area"],
                "亩，亩成本：",
                row["cost_per_mu"],
                "元，总成本：",
                row["total_cost"],
                "元",
            )