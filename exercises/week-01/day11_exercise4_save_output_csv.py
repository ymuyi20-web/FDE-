import csv
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).parent
outputs_dir = base_dir / "outputs"
history_path = outputs_dir / "day11_history.csv"

outputs_dir.mkdir(exist_ok=True)

area = 100
cost_per_mu = 475
total_cost = area * cost_per_mu
created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

file_exists = history_path.exists()

with open(history_path, "a", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)

    if not file_exists:
        writer.writerow(["created_at", "area", "cost_per_mu", "total_cost"])

    writer.writerow([created_at, area, cost_per_mu, total_cost])

print("历史记录已经保存到 outputs/day11_history.csv。")
print("文件位置：", history_path)