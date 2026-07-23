import json
from pathlib import Path

base_dir = Path(__file__).parent
input_json_path = base_dir / "farm_inputs.json"
result_json_path = base_dir / "day8_result.json"


def load_inputs():
    with open(input_json_path, "r", encoding="utf-8") as file:
        inputs = json.load(file)

    return inputs


def get_area():
    area_text = input("请输入水稻种植面积（亩）：")
    area = float(area_text)
    return area


def calculate_cost_per_mu(inputs):
    total = 0

    for item in inputs:
        total = total + item["cost_per_mu"]

    return total


def calculate_total_cost(area, cost_per_mu):
    total_cost = area * cost_per_mu
    return total_cost


def show_inputs(inputs):
    print()
    print("各项投入成本：")

    for item in inputs:
        print("项目：", item["name"], "，亩成本：", f"{item['cost_per_mu']:.2f}", "元")


def show_result(area, cost_per_mu, total_cost):
    print("--------------------")
    print("种植面积：", f"{area:.2f}", "亩")
    print("每亩总成本：", f"{cost_per_mu:.2f}", "元")
    print("预计总成本：", f"{total_cost:.2f}", "元")


def save_result(area, cost_per_mu, total_cost, inputs):
    result = {
        "area": area,
        "cost_per_mu": cost_per_mu,
        "total_cost": total_cost,
        "inputs": inputs,
    }

    with open(result_json_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

    print()
    print("计算结果已经保存到 day8_result.json。")


def main():
    try:
        inputs = load_inputs()

        area = get_area()

        if area <= 0:
            print("面积必须大于0。")
            return

        cost_per_mu = calculate_cost_per_mu(inputs)
        total_cost = calculate_total_cost(area, cost_per_mu)

        show_inputs(inputs)
        show_result(area, cost_per_mu, total_cost)
        save_result(area, cost_per_mu, total_cost, inputs)

    except FileNotFoundError:
        print("错误：没有找到 farm_inputs.json，请先运行练习一创建配置文件。")

    except ValueError:
        print("输入错误，请输入纯数字。")

    except KeyError:
        print("错误：farm_inputs.json 中缺少 name 或 cost_per_mu 字段。")


if __name__ == "__main__":
    main()