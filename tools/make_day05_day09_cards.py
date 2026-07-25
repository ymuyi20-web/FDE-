from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


PROJECT = Path(__file__).resolve().parents[1]
OUT_DIR = PROJECT / "docs" / "social-posts" / "day05-day09"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1080, 1440
FONT_BOLD = r"C:\Windows\Fonts\msyh.ttf"
FONT_HEAVY = r"C:\Windows\Fonts\simhei.ttf"
FONT_REGULAR = r"C:\Windows\Fonts\msyh.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_wrapped(draw, text, xy, max_width, fnt, fill, line_gap=14):
    x, y = xy
    line = ""
    for ch in text:
        test = line + ch
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + line_gap
            line = ch
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
    return y


def base_card(title, subtitle, tag, accent="#2563eb"):
    img = Image.new("RGB", (W, H), "#f7f2ea")
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([44, 44, W - 44, H - 44], radius=52, fill="#ffffff")
    draw.rounded_rectangle([44, 44, W - 44, 332], radius=52, fill="#edf6ff")
    draw.text((88, 92), title, font=font(FONT_HEAVY, 62), fill="#111827")
    draw.text((88, 178), subtitle, font=font(FONT_BOLD, 42), fill=accent)
    draw.text((88, 252), tag, font=font(FONT_REGULAR, 28), fill="#64748b")
    return img, draw


def add_footer(draw, page):
    draw.text((88, 1320), "FDE / Python学习记录", font=font(FONT_REGULAR, 24), fill="#94a3b8")
    draw.rounded_rectangle([884, 1302, 992, 1352], radius=24, fill="#dbeafe")
    draw.text((920, 1310), page, font=font(FONT_BOLD, 24), fill="#1d4ed8")


def add_code_panel(draw, y, lines):
    draw.rounded_rectangle([88, y, 992, y + 360], radius=28, fill="#111827")
    yy = y + 38
    for i, line in enumerate(lines):
        color = "#93c5fd" if i == 0 else "#e5e7eb"
        draw.text((128, yy), line, font=font(FONT_REGULAR, 31), fill=color)
        yy += 58


def save(img, name):
    img.save(OUT_DIR / name, quality=95)


def make_day5():
    img, draw = base_card("Day5", "调试与自动测试", "print / type / assert / breakpoint")
    draw.rounded_rectangle([88, 404, 992, 720], radius=30, fill="#f8fafc")
    draw.text((126, 444), "这一天我开始学会：", font=font(FONT_HEAVY, 42), fill="#111827")
    items = ["看报错定位问题", "用 print 和 type 检查变量", "用 assert 自动验证结果", "用断点观察程序运行过程"]
    for i, text in enumerate(items):
        yy = 520 + i * 58
        draw.rounded_rectangle([126, yy, 168, yy + 42], radius=21, fill="#dbeafe")
        draw.text((139, yy + 4), str(i + 1), font=font(FONT_BOLD, 24), fill="#1d4ed8")
        draw.text((192, yy), text, font=font(FONT_REGULAR, 31), fill="#1f2937")
    add_code_panel(draw, 790, ["assert calculate_total(100, 455) == 45500", "print(type(area))", "breakpoint: 看变量一步步变化"])
    add_footer(draw, "02")
    save(img, "02-day5-debug-test-final.png")


def make_day6():
    img, draw = base_card("Day6", "函数拆分和项目结构", "import / main / functions")
    draw.text((88, 410), "从“一个文件从上写到下”", font=font(FONT_HEAVY, 44), fill="#111827")
    draw.text((88, 470), "开始变成“多个功能互相配合”", font=font(FONT_HEAVY, 44), fill="#2563eb")
    rows = [("farm_math.py", "专门放计算函数"), ("day6_main.py", "负责调用和运行"), ("main()", "作为程序入口"), ("Git", "保存学习版本")]
    for i, (left, right) in enumerate(rows):
        y = 575 + i * 110
        draw.rounded_rectangle([88, y, 992, y + 78], radius=24, fill="#f8fafc")
        draw.text((126, y + 18), left, font=font(FONT_BOLD, 30), fill="#1d4ed8")
        draw.text((430, y + 18), right, font=font(FONT_REGULAR, 30), fill="#1f2937")
    add_code_panel(draw, 1050, ["def main():", "    ...", 'if __name__ == "__main__": main()'])
    add_footer(draw, "03")
    save(img, "03-day6-project-structure-final.png")


def make_day8():
    img, draw = base_card("Day8", "JSON 配置文件", "代码负责逻辑，JSON负责数据")
    draw.rounded_rectangle([88, 396, 992, 736], radius=30, fill="#111827")
    lines = [
        "[",
        '  {"name": "种子", "cost_per_mu": 60},',
        '  {"name": "肥料", "cost_per_mu": 220},',
        '  {"name": "灌溉", "cost_per_mu": 100}',
        "]",
    ]
    yy = 432
    for line in lines:
        draw.text((128, yy), line, font=font(FONT_REGULAR, 29), fill="#e5e7eb")
        yy += 58
    draw.text((88, 820), "这一天最重要的理解：", font=font(FONT_HEAVY, 42), fill="#111827")
    draw_wrapped(draw, "成本数据不一定要写死在 Python 代码里，可以放到 JSON 文件中。以后要改数据，就先改配置。", (88, 890), 880, font(FONT_REGULAR, 34), "#1f2937")
    add_footer(draw, "04")
    save(img, "04-day8-json-config-final.png")


def make_day9():
    img, draw = base_card("Day9", "菜单配置管理器", "查看 / 修改 / 保存 / 计算")
    add_code_panel(draw, 400, ["====== 水稻成本配置管理器 ======", "1. 查看农资成本配置", "2. 修改农资成本", "3. 计算水稻总成本", "0. 退出"])
    draw.text((88, 820), "这一天的小成品：", font=font(FONT_HEAVY, 42), fill="#111827")
    items = ["可以按菜单选择功能", "可以修改 JSON 里的成本", "修改后能保存，下次运行还在", "可以根据配置计算总成本"]
    for i, text in enumerate(items):
        y = 895 + i * 68
        draw.ellipse([92, y + 8, 126, y + 42], fill="#bfdbfe")
        draw.text((146, y), text, font=font(FONT_REGULAR, 33), fill="#1f2937")
    add_footer(draw, "05")
    save(img, "05-day9-menu-manager-final.png")


def make_summary():
    img, draw = base_card("阶段收获", "小工具开始像成品了", "从练习代码到可用小程序")
    draw.text((88, 410), "这 5 天的变化", font=font(FONT_HEAVY, 46), fill="#111827")
    rows = [
        ("以前", "只会运行单个 Python 文件"),
        ("现在", "能拆函数、读写配置、保存结果"),
        ("以前", "报错了容易慌"),
        ("现在", "会看报错、测试、逐步验证"),
        ("以前", "数据写死在代码里"),
        ("现在", "开始理解配置文件和小工具结构"),
    ]
    y = 500
    for left, right in rows:
        draw.rounded_rectangle([88, y, 196, y + 52], radius=22, fill="#dbeafe" if left == "现在" else "#f1f5f9")
        draw.text((116, y + 8), left, font=font(FONT_BOLD, 26), fill="#1d4ed8" if left == "现在" else "#64748b")
        draw.text((226, y + 6), right, font=font(FONT_REGULAR, 30), fill="#1f2937")
        y += 86
    draw.rounded_rectangle([88, 1080, 992, 1248], radius=30, fill="#fff7ed")
    draw.text((126, 1118), "下一步：继续把它做成更完整的小项目", font=font(FONT_BOLD, 34), fill="#9a3412")
    draw.text((126, 1174), "有输入、有配置、有历史、有菜单。", font=font(FONT_REGULAR, 30), fill="#7c2d12")
    add_footer(draw, "06")
    save(img, "06-stage-summary-final.png")


if __name__ == "__main__":
    make_day5()
    make_day6()
    make_day8()
    make_day9()
    make_summary()
    print(OUT_DIR)
