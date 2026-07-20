def get_area():
    area_text = input("请输入水稻种植面积（亩）：")
    area = float(area_text)
    return area


def calculate_cost_per_mu(costs):
    total = 0

    for cost in costs:
        total = total + cost

    return total


def calculate_total_cost(area, cost_per_mu):
    return area * cost_per_mu


def main():
    costs = [60, 220, 95, 80]

    try:
        area = get_area()

        if area <= 0:
            print("面积必须大于0。")
        else:
            cost_per_mu = calculate_cost_per_mu(costs)
            total_cost = calculate_total_cost(area, cost_per_mu)

            print("种植面积：", area, "亩")
            print("每亩总成本：", cost_per_mu, "元")
            print("预计总成本：", total_cost, "元")

    except ValueError:
        print("输入错误，请输入纯数字。")


if __name__ == "__main__":
    main()