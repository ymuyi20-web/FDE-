from pathlib import Path

base_dir = Path(__file__).parent

src_dir = base_dir / "src"
data_dir = base_dir / "data"
outputs_dir = base_dir / "outputs"
docs_dir = base_dir / "docs"

src_dir.mkdir(exist_ok=True)
data_dir.mkdir(exist_ok=True)
outputs_dir.mkdir(exist_ok=True)
docs_dir.mkdir(exist_ok=True)

print("项目文件夹创建完成。")
print("代码文件夹：", src_dir)
print("数据文件夹：", data_dir)
print("输出文件夹：", outputs_dir)
print("文档文件夹：", docs_dir)