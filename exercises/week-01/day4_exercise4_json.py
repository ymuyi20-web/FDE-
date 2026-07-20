from pathlib import Path
import json

base_dir = Path(__file__).parent
json_path = base_dir / "result.json"

# Python字典
result = {
    "area": 100.0,
    "cost_per_mu": 455.0,
    "total_cost": 45500.0,
}

# 第一步：写入JSON文件
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(
        result,
        file,
        ensure_ascii=False,
        indent=4,
    )

print("result.json写入完成。")

# 第二步：读取JSON文件
with open(json_path, "r", encoding="utf-8") as file:
    loaded_result = json.load(file)

print("\n从JSON中读取到的结果：")
print("种植面积：", loaded_result["area"], "亩")
print("每亩成本：", loaded_result["cost_per_mu"], "元")
print("预计总成本：", loaded_result["total_cost"], "元")