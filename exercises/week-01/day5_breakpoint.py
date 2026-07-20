def calculate_total(area, costs):
    cost_per_mu = 0

    for cost in costs:
        cost_per_mu = cost_per_mu + cost

    total_cost = area * cost_per_mu
    return total_cost


area = 100
costs = [60, 220, 95, 80]

result = calculate_total(area, costs)

print("每亩总成本：", sum(costs), "元")
print("预计总成本：", result, "元")