from farm_math import calculate_total

area = 100
cost_per_mu = 455

total_cost = calculate_total(area, cost_per_mu)

print("种植面积：", area, "亩")
print("每亩成本：", cost_per_mu, "元")
print("预计总成本：", total_cost, "元")