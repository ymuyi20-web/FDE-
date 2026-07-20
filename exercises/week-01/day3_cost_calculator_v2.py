# 第3天正式作业：水稻成本计算器 V2
# 学习重点：函数、参数、返回值、循环和异常处理


# 1. 输入并检查种植面积
def read_area():
    try:
        area = float(input("请输入水稻种植面积（亩）："))

        if area <= 0:
            print("面积必须大于0。")
            return None

        return area

    except ValueError:
        print("输入错误，请输入纯数字。")
        return None


# 2. 计算每亩总成本
def calculate_cost_per_mu(items):
    total = 0.0

    for item in items:
        total = total + item["cost_per_mu"]

    return total


# 3. 计算全部面积的预计总成本
def calculate_total_cost(area, cost_per_mu):
    total_cost = area * cost_per_mu
    return total_cost


# 4. 输出计算结果
def print_result(area, cost_per_mu, total_cost):
    print("\n各项投入成本：")

    for item in inputs:
        print(
            f"项目：{item['name']}，"
            f"亩成本：{item['cost_per_mu']:.2f}元"
        )

    print("--------------------")
    print(f"种植面积：{area:.2f}亩")
    print(f"每亩总成本：{cost_per_mu:.2f}元")
    print(f"预计总成本：{total_cost:.2f}元")


# 各项农业投入成本
inputs = [
    {"name": "种子", "cost_per_mu": 60.0},
    {"name": "肥料", "cost_per_mu": 220.0},
    {"name": "植保", "cost_per_mu": 95.0},
    {"name": "灌溉", "cost_per_mu": 80.0},
]


# 程序从这里开始执行
area = read_area()

if area is not None:
    cost_per_mu = calculate_cost_per_mu(inputs)
    total_cost = calculate_total_cost(area, cost_per_mu)
    print_result(area, cost_per_mu, total_cost)