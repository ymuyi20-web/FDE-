def get_area():
    area_text = input("请输入水稻种植面积（亩）：")
    area = float(area_text)
    return area


def get_inputs():
    inputs = [
        {"name": "种子", "cost_per_mu": 60},
        {"name": "肥料", "cost_per_mu": 220},
        {"name": "植保", "cost_per_mu": 95},
        {"name": "灌溉", "cost_per_mu": 80},
    ]

    return inputs


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


def main():
    try:
        area = get_area()

        if area <= 0:
            print("面积必须大于0。")
            return

        inputs = get_inputs()
        cost_per_mu = calculate_cost_per_mu(inputs)
        total_cost = calculate_total_cost(area, cost_per_mu)

        show_inputs(inputs)
        show_result(area, cost_per_mu, total_cost)

    except ValueError:
        print("输入错误，请输入纯数字。")


if __name__ == "__main__":
    main()