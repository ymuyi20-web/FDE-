import json
from pathlib import Path

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
json_path = data_dir / "farm_inputs.json"


def load_inputs():
    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def show_inputs(inputs):
    print("当前农资配置：")

    for index, item in enumerate(inputs, start=1):
        print(index, ".", item["name"], "：", item["cost_per_mu"], "元/亩")


inputs = load_inputs()
show_inputs(inputs)