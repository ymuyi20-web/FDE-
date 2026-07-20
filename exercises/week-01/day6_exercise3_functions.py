def get_area():
    area = float(input("请输入水稻种植面积（亩）："))
    return area

def calculate_cost_per_mu(costs):
    total = 0

    for cost in costs:
        total = total + cost

    return total

def calculate_total_cost(area, cost_per_mu):
    total_cost = area * cost_per_mu
    return total_cost


def show_result(area, cost_per_mu, total_cost):
    print("种植面积：", area, "亩")
    print("每亩总成本：", cost_per_mu, "元")
    print("预计总成本：", total_cost, "元")


def main():
    costs = [60, 220, 95, 80]

    area = get_area()
    cost_per_mu = calculate_cost_per_mu(costs)
    total_cost = calculate_total_cost(area, cost_per_mu)

    show_result(area, cost_per_mu, total_cost)


if __name__ == "__main__":
    main()