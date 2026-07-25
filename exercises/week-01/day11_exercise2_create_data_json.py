import json
from pathlib import Path

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
json_path = data_dir / "farm_inputs.json"

data_dir.mkdir(exist_ok=True)

inputs = [
    {"name": "种子", "cost_per_mu": 60.0},
    {"name": "肥料", "cost_per_mu": 200.0},
    {"name": "植保", "cost_per_mu": 95.0},
    {"name": "灌溉", "cost_per_mu": 120.0},
]

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(inputs, file, ensure_ascii=False, indent=4)

print("data/farm_inputs.json 创建完成。")
print("文件位置：", json_path)