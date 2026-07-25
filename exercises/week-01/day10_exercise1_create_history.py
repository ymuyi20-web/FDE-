import csv
from pathlib import Path

base_dir = Path(__file__).parent
history_path = base_dir / "history.csv"

with open(history_path, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["area", "cost_per_mu", "total_cost"])

print("history.csv 创建完成。")
print("文件位置：", history_path)