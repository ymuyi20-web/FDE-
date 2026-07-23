import json
from pathlib import Path

base_dir = Path(__file__).parent
json_path = base_dir / "farm_inputs.json"


def load_inputs():
    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def calculate_cost_per_mu(inputs):
    total = 0

    for item in inputs:
        total = total + item["cost_per_mu"]

    return total


def show_inputs(inputs):
    print("当前农资成本配置：")

    for item in inputs:
        print("项目：", item["name"], "，亩成本：", item["cost_per_mu"], "元")


inputs = load_inputs()
cost_per_mu = calculate_cost_per_mu(inputs)

show_inputs(inputs)
print("每亩总成本：", cost_per_mu, "元")