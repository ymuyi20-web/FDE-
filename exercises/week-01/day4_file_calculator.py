from pathlib import Path
import csv
import json


# 获取当前Python文件所在的文件夹
base_dir = Path(__file__).parent

# 输入文件和结果文件的位置
csv_path = base_dir / "inputs.csv"
json_path = base_dir / "result.json"


# 1. 从CSV读取农资数据
def load_inputs(file_path):
    items = []

    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            item = {
                "name": row["name"],
                "cost_per_mu": float(row["cost_per_mu"]),
            }

            items.append(item)

    return items


# 2. 计算每亩总成本
def calculate_cost_per_mu(items):
    total = 0.0

    for item in items:
        total = total + item["cost_per_mu"]

    return total


# 3. 计算全部面积的总成本
def calculate_total_cost(area, cost_per_mu):
    total_cost = area * cost_per_mu
    return total_cost


# 4. 把计算结果保存成JSON
def save_result(
    file_path,
    area,
    cost_per_mu,
    total_cost,
    items,
):
    result = {
        "area": area,
        "cost_per_mu": cost_per_mu,
        "total_cost": total_cost,
        "items": items,
    }

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            result,
            file,
            ensure_ascii=False,
            indent=4,
        )


# 5. 输出计算结果
def print_result(area, cost_per_mu, total_cost, items):
    print("\n各项投入成本：")

    for item in items:
        print(
            f"项目：{item['name']}，"
            f"亩成本：{item['cost_per_mu']:.2f}元"
        )

    print("--------------------")
    print(f"种植面积：{area:.2f}亩")
    print(f"每亩总成本：{cost_per_mu:.2f}元")
    print(f"预计总成本：{total_cost:.2f}元")


# 6. 主程序
def main():
    try:
        # 读取CSV
        items = load_inputs(csv_path)

        # 输入面积
        area = float(
            input("请输入水稻种植面积（亩）：")
        )

        if area <= 0:
            print("面积必须大于0。")
            return

        # 执行计算
        cost_per_mu = calculate_cost_per_mu(items)

        total_cost = calculate_total_cost(
            area,
            cost_per_mu,
        )

        # 显示结果
        print_result(
            area,
            cost_per_mu,
            total_cost,
            items,
        )

        # 保存JSON
        save_result(
            json_path,
            area,
            cost_per_mu,
            total_cost,
            items,
        )

        print("\n计算结果已经保存到result.json。")

    except FileNotFoundError:
        print("错误：没有找到inputs.csv文件。")

    except ValueError:
        print("错误：面积或CSV中的成本必须是数字。")

    except KeyError:
        print("错误：CSV缺少name或cost_per_mu字段。")


# 运行主程序
main()