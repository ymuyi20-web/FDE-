"""Day 2: 水稻投入成本计算器。

要求：计算每亩成本和指定面积的总成本；面积小于等于0时给出提示。
"""

"""Day 2：水稻投入成本计算器。"""

inputs = [
    {"name": "种子", "cost_per_mu": 60.0},
    {"name": "肥料", "cost_per_mu": 220.0},
    {"name": "植保", "cost_per_mu": 95.0},
    {"name": "灌溉", "cost_per_mu": 80.0},
]

area = float(input("请输入水稻种植面积（亩）："))

if area <= 0:
    print("面积必须大于0，请重新输入。")
else:
    cost_per_mu = 0.0

    print("各项投入成本：")

    for item in inputs:
        item_total_cost = item["cost_per_mu"] * area
        cost_per_mu += item["cost_per_mu"]

        print(
            f"项目：{item['name']}，"
            f"亩成本：{item['cost_per_mu']:.2f}元，"
            f"总成本：{item_total_cost:.2f}元"
        )

    total_cost = cost_per_mu * area

    print("--------------------")
    print(f"种植面积：{area:.2f}亩")
    print(f"每亩总成本：{cost_per_mu:.2f}元")
    print(f"预计总成本：{total_cost:.2f}元")
# TODO 1: 判断面积是否合法。
# TODO 2: 使用for循环累计每亩成本。
# TODO 3: 计算总成本，并按“项目、亩成本、总成本”输出。
# TODO 4: 新增“灌溉”项目，确认累计逻辑不需要修改。

