import csv
from pathlib import Path

base_dir = Path(__file__).parent
history_path = base_dir / "history.csv"

with open(history_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    print("历史记录：")

    for row in reader:
        print(
            "面积：",
            row["area"],
            "亩，每亩成本：",
            row["cost_per_mu"],
            "元，总成本：",
            row["total_cost"],
            "元",
        )