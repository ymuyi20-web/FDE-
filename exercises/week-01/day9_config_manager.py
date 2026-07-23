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


def show_menu():
    print()
    print("====== 水稻成本配置管理器 ======")
    print("1. 查看农资成本配置")
    print("2. 修改农资成本")
    print("3. 计算水稻总成本")
    print("0. 退出")


def show_inputs(inputs):
    print()
    print("当前农资成本配置：")

    for index, item in enumerate(inputs, start=1):
        print(index, ".", item["name"], "：", f"{item['cost_per_mu']:.2f}", "元/亩")


def update_input_cost(inputs):
    show_inputs(inputs)

    index_text = input("请输入要修改的项目编号：")
    new_cost_text = input("请输入新的亩成本：")

    index = int(index_text)
    new_cost = float(new_cost_text)

    if index < 1 or index > len(inputs):
        print("项目编号不存在。")
        return

    item = inputs[index - 1]
    item["cost_per_mu"] = new_cost

    save_inputs(inputs)

    print("修改已保存。")
    print("修改项目：", item["name"], "，新亩成本：", f"{new_cost:.2f}", "元/亩")


def calculate_cost_per_mu(inputs):
    total = 0

    for item in inputs:
        total = total + item["cost_per_mu"]

    return total


def calculate_total_cost(inputs):
    area_text = input("请输入水稻种植面积（亩）：")
    area = float(area_text)

    if area <= 0:
        print("面积必须大于0。")
        return

    cost_per_mu = calculate_cost_per_mu(inputs)
    total_cost = area * cost_per_mu

    print()
    print("种植面积：", f"{area:.2f}", "亩")
    print("每亩总成本：", f"{cost_per_mu:.2f}", "元")
    print("预计总成本：", f"{total_cost:.2f}", "元")


def main():
    try:
        inputs = load_inputs()

        while True:
            show_menu()
            choice = input("请选择功能：")

            if choice == "1":
                show_inputs(inputs)

            elif choice == "2":
                update_input_cost(inputs)
                inputs = load_inputs()

            elif choice == "3":
                calculate_total_cost(inputs)

            elif choice == "0":
                print("程序已退出。")
                break

            else:
                print("输入错误，请重新选择。")

    except FileNotFoundError:
        print("错误：没有找到 farm_inputs.json，请先创建配置文件。")

    except ValueError:
        print("输入错误，请输入正确的数字。")

    except KeyError:
        print("错误：farm_inputs.json 中缺少 name 或 cost_per_mu 字段。")


if __name__ == "__main__":
    main()