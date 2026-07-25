import json
from pathlib import Path

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
json_path = data_dir / "farm_inputs.json"


def load_inputs():
    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def save_inputs(inputs):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(inputs, file, ensure_ascii=False, indent=4)


def show_inputs(inputs):
    print("当前农资配置：")

    for index, item in enumerate(inputs, start=1):
        print(index, ".", item["name"], "：", item["cost_per_mu"], "元/亩")


inputs = load_inputs()
show_inputs(inputs)

name = input("请输入新增农资名称：")
cost_text = input("请输入新增农资亩成本：")

try:
    cost_per_mu = float(cost_text)

    if cost_per_mu < 0:
        print("成本不能小于0。")
    else:
        new_item = {
            "name": name,
            "cost_per_mu": cost_per_mu,
        }

        inputs.append(new_item)
        save_inputs(inputs)

        print("新增成功。")
        show_inputs(inputs)

except ValueError:
    print("输入错误，成本必须是数字。")