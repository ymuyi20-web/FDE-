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

try:
    index_text = input("请输入要修改的项目编号：")
    index = int(index_text) - 1

    if index < 0 or index >= len(inputs):
        print("编号不存在。")
    else:
        new_cost_text = input("请输入新的亩成本：")
        new_cost = float(new_cost_text)

        if new_cost < 0:
            print("成本不能小于0。")
        else:
            inputs[index]["cost_per_mu"] = new_cost
            save_inputs(inputs)

            print("修改成功。")
            show_inputs(inputs)

except ValueError:
    print("输入错误，请输入正确数字。")