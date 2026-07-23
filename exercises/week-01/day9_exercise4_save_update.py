import json
from pathlib import Path

base_dir = Path(__file__).parent
json_path = base_dir / "farm_inputs.json"


def load_inputs():
    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def save_inputs(inputs):
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(inputs, file, ensure_ascii=False, indent=4)


def show_inputs(inputs):
    print("当前农资成本配置：")

    for index, item in enumerate(inputs, start=1):
        print(index, ".", item["name"], "：", item["cost_per_mu"], "元/亩")


inputs = load_inputs()
show_inputs(inputs)

index_text = input("请输入要修改的项目编号：")
new_cost_text = input("请输入新的亩成本：")

index = int(index_text)
new_cost = float(new_cost_text)

item = inputs[index - 1]
item["cost_per_mu"] = new_cost

save_inputs(inputs)

print("修改已保存。")
print("修改后的结果：")
show_inputs(inputs)