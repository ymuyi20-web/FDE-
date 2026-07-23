import json
from pathlib import Path

base_dir = Path(__file__).parent
json_path = base_dir / "farm_inputs.json"

inputs = [
    {"name": "种子", "cost_per_mu": 60},
    {"name": "肥料", "cost_per_mu": 220},
    {"name": "植保", "cost_per_mu": 95},
    {"name": "灌溉", "cost_per_mu": 80},
]

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(inputs, file, ensure_ascii=False, indent=4)

print("farm_inputs.json 创建完成。")
print("文件位置：", json_path)