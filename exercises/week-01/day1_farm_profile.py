"""Day 1: 农场生产概况。

输入示例：
姓名：杨其琛
水稻面积：2692.51
目标亩产：1301

预期：输出总产量，并显示完整生产概况。
"""

name = input("请输入负责人姓名：")
area_text = input("请输入水稻面积（亩）：")
yield_text = input("请输入目标亩产（斤/亩）：")
area = float(area_text)
yield_per_mu = float(yield_text)
total_yield = area * yield_per_mu
print(f"负责人：{name}，水稻面积：{area}亩，目标亩产：{yield_per_mu}斤/亩，预计总产量：{total_yield:.2f}斤。")

# TODO 1: 将面积和亩产转换为小数。
# TODO 2: 计算总产量。
# TODO 3: 使用一条完整语句输出负责人、面积、亩产和总产量。

