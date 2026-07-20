# 计算每亩总成本
def calculate_cost_per_mu(costs):
    total = 0

    for cost in costs:
        total = total + cost

    return total


# 计算预计总成本
def calculate_total_cost(area, cost_per_mu):
    return area * cost_per_mu


# 农资成本
costs = [60, 220, 95, 80]

# 自动测试
assert calculate_cost_per_mu(costs) == 450, "每亩总成本计算错误"
assert calculate_total_cost(100, 455) == 45500, "整数面积计算错误"
assert calculate_total_cost(100.5, 455) == 45727.5, "小数面积计算错误"

print("自动测试全部通过！")
print("--------------------")

# 正式运行
try:
    area = float(input("请输入水稻种植面积（亩）："))

    if area <= 0:
        print("面积必须大于0。")
    else:
        cost_per_mu = calculate_cost_per_mu(costs)
        total_cost = calculate_total_cost(area, cost_per_mu)

        print(f"种植面积：{area:.2f}亩")
        print(f"每亩总成本：{cost_per_mu:.2f}元")
        print(f"预计总成本：{total_cost:.2f}元")

except ValueError:
    print("输入错误，请输入纯数字。")