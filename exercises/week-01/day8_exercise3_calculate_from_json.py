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


inputs = load_inputs()
cost_per_mu = calculate_cost_per_mu(inputs)

print("每亩总成本：", cost_per_mu, "元")