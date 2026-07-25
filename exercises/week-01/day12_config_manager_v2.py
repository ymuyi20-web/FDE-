import json
from pathlib import Path

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
json_path = data_dir / "farm_inputs.json"


def create_dirs():
    data_dir.mkdir(exist_ok=True)


def create_default_inputs():
    inputs = [
        {"name": "种子", "cost_per_mu": 60.0},
        {"name": "肥料", "cost_per_mu": 200.0},
        {"name": "植保", "cost_per_mu": 95.0},
        {"name": "灌溉", "cost_per_mu": 120.0},
    ]

    save_inputs(inputs)
    return inputs


def load_inputs():
    create_dirs()

    if not json_path.exists():
        print("没有找到 data/farm_inputs.json，已经自动创建默认配置。")
        return create_default_inputs()

    with open(json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def save_inputs(inputs):
    create_dirs()

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(inputs, file, ensure_ascii=False, indent=4)


def show_inputs(inputs):
    print("\n当前农资配置：")

    if len(inputs) == 0:
        print("当前没有任何农资项目。")
        return

    for index, item in enumerate(inputs, start=1):
        print(index, ".", item["name"], "：", f"{item['cost_per_mu']:.2f}", "元/亩")


def add_item(inputs):
    name = input("请输入新增农资名称：")
    cost_text = input("请输入新增农资亩成本：")

    try:
        cost_per_mu = float(cost_text)

        if cost_per_mu < 0:
            print("成本不能小于0。")
            return

        new_item = {
            "name": name,
            "cost_per_mu": cost_per_mu,
        }

        inputs.append(new_item)
        save_inputs(inputs)

        print("新增成功。")

    except ValueError:
        print("输入错误，成本必须是数字。")


def update_item(inputs):
    show_inputs(inputs)

    if len(inputs) == 0:
        return

    try:
        index_text = input("请输入要修改的项目编号：")
        index = int(index_text) - 1

        if index < 0 or index >= len(inputs):
            print("编号不存在。")
            return

        new_cost_text = input("请输入新的亩成本：")
        new_cost = float(new_cost_text)

        if new_cost < 0:
            print("成本不能小于0。")
            return

        old_name = inputs[index]["name"]
        inputs[index]["cost_per_mu"] = new_cost
        save_inputs(inputs)

        print("修改成功：", old_name, "新亩成本为", f"{new_cost:.2f}", "元/亩")

    except ValueError:
        print("输入错误，请输入正确数字。")


def delete_item(inputs):
    show_inputs(inputs)

    if len(inputs) == 0:
        return

    try:
        index_text = input("请输入要删除的项目编号：")
        index = int(index_text) - 1

        if index < 0 or index >= len(inputs):
            print("编号不存在。")
            return

        removed_item = inputs.pop(index)
        save_inputs(inputs)

        print("删除成功，已删除：", removed_item["name"])

    except ValueError:
        print("输入错误，请输入正确编号。")


def calculate_cost_per_mu(inputs):
    total = 0

    for item in inputs:
        total = total + float(item["cost_per_mu"])

    return total


def calculate_total_cost(inputs):
    if len(inputs) == 0:
        print("当前没有农资项目，无法计算。")
        return

    try:
        area = float(input("请输入水稻种植面积（亩）："))

        if area <= 0:
            print("面积必须大于0。")
            return

        cost_per_mu = calculate_cost_per_mu(inputs)
        total_cost = area * cost_per_mu

        print("\n计算结果：")
        print(f"种植面积：{area:.2f} 亩")
        print(f"每亩总成本：{cost_per_mu:.2f} 元")
        print(f"预计总成本：{total_cost:.2f} 元")

    except ValueError:
        print("输入错误，请输入纯数字。")


def show_menu():
    print("\n====== Day12 农资配置管理器 ======")
    print("1. 查看农资配置")
    print("2. 新增农资项目")
    print("3. 修改农资成本")
    print("4. 删除农资项目")
    print("5. 计算水稻总成本")
    print("0. 退出")


def main():
    inputs = load_inputs()

    while True:
        show_menu()

        choice = input("请选择功能：")

        if choice == "1":
            show_inputs(inputs)

        elif choice == "2":
            add_item(inputs)

        elif choice == "3":
            update_item(inputs)

        elif choice == "4":
            delete_item(inputs)

        elif choice == "5":
            calculate_total_cost(inputs)

        elif choice == "0":
            print("程序已退出。")
            break

        else:
            print("输入错误，请重新选择。")

        inputs = load_inputs()


main()