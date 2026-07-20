def calculate_total(area, cost_per_mu):
    return area * cost_per_mu


assert calculate_total(100, 455) == 45500, "整数面积计算错误"
assert calculate_total(100.5, 455) == 45727.5, "小数面积计算错误"

print("所有测试通过")