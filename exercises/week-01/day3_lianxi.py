# #练习1
# def show_title():
#     print("水稻成本计算器")


# show_title()

# #练习2
# def calculate_total(area, cost_per_mu):
#     total_cost = area * cost_per_mu
#     return total_cost


# result = calculate_total(100, 455)

# print("预计总成本：", result, "元")

# #练习3
# inputs = [
#     {"name": "种子", "cost_per_mu": 60.0},
#     {"name": "肥料", "cost_per_mu": 220.0},
#     {"name": "植保", "cost_per_mu": 95.0},
#     {"name": "灌溉", "cost_per_mu": 80.0},
# ]


# def calculate_cost_per_mu(items):
#     total = 0.0

#     for item in items:
#         total = total + item["cost_per_mu"]

#     return total


# cost_per_mu = calculate_cost_per_mu(inputs)

# print("每亩总成本：", cost_per_mu, "元")

#练习4
try:
    area = float(input("请输入水稻种植面积（亩）："))

    if area <= 0:
        print("面积必须大于0。")
    else:
        print("输入的面积是：", area, "亩")

except ValueError:
    print("输入错误，请输入纯数字。")
