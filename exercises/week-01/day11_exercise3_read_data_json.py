import json
from pathlib import Path

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
json_path = data_dir / "farm_inputs.json"

with open(json_path, "r", encoding="utf-8") as file:
    inputs = json.load(file)

print("当前农资成本配置：")

for item in inputs:
    print("项目：", item["name"], "，亩成本：", item["cost_per_mu"], "元")