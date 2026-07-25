import csv
from pathlib import Path

base_dir = Path(__file__).parent
history_path = base_dir / "history.csv"

area = 100
cost_per_mu = 475
total_cost = area * cost_per_mu

with open(history_path, "a", encoding="utf-8-sig", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([area, cost_per_mu, total_cost])

print("已经追加一条历史记录。")