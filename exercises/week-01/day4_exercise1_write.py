from pathlib import Path

# 当前Python文件所在的文件夹
base_dir = Path(__file__).parent

# 要生成的文本文件
file_path = base_dir / "farm_summary.txt"

# 写入文件
with open(file_path, "w", encoding="utf-8") as file:
    file.write("水稻种植面积：100亩\n")
    file.write("每亩成本：455元\n")
    file.write("预计总成本：45500元\n")

print("文件写入完成。")
print("文件位置：", file_path)