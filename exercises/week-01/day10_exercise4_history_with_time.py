import csv
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).parent
history_path = base_dir / "history_with_time.csv"

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

print("带时间的历史记录已经保存。")
print("保存时间：", created_at)