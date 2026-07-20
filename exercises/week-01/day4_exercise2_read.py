from pathlib import Path

base_dir = Path(__file__).parent
file_path = base_dir / "farm_summary.txt"

try:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    print("文件内容：")
    print(content)

except FileNotFoundError:
    print("没有找到farm_summary.txt，请先运行练习1。")