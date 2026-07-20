area = float(input("请输入水稻种植面积（亩）："))
cost_per_mu = 455
print("area的内容：", area)
print("area的数据类型：", type(area))
total_cost = area * cost_per_mu

print(f"种植面积：{area}亩")
print(f"预计总成本：{total_cost:.2f}元")