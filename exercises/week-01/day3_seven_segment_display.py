"""Day 3：使用 turtle 绘制七段数码管。

运行程序后输入一串数字；直接按回车则显示当天日期。
关闭绘图窗口即可结束程序。
"""

from datetime import datetime
import turtle


# 七个位置依次表示：上、右上、右下、下、左下、左上、中。
SEGMENTS = {
    "0": (1, 1, 1, 1, 1, 1, 0),
    "1": (0, 1, 1, 0, 0, 0, 0),
    "2": (1, 1, 0, 1, 1, 0, 1),
    "3": (1, 1, 1, 1, 0, 0, 1),
    "4": (0, 1, 1, 0, 0, 1, 1),
    "5": (1, 0, 1, 1, 0, 1, 1),
    "6": (1, 0, 1, 1, 1, 1, 1),
    "7": (1, 1, 1, 0, 0, 0, 0),
    "8": (1, 1, 1, 1, 1, 1, 1),
    "9": (1, 1, 1, 1, 0, 1, 1),
}

ON_COLOR = "#ff453a"
OFF_COLOR = "#303030"
BACKGROUND_COLOR = "#111111"


def read_number():
    """读取要显示的数字，输入不合法时返回 None。"""
    default_number = datetime.now().strftime("%Y%m%d")
    text = input(
        f"请输入要显示的数字（直接回车显示 {default_number}）："
    ).strip()

    if text == "":
        return default_number

    if not text.isdigit():
        print("输入无效：只能输入0到9之间的数字。")
        return None

    if len(text) > 12:
        print("输入无效：最多显示12位数字。")
        return None

    return text


def draw_rectangle(pen, x, y, width, height, color):
    """从左下角坐标开始绘制一个填充矩形。"""
    pen.penup()
    pen.goto(x, y)
    pen.setheading(0)
    pen.color(color)
    pen.begin_fill()
    pen.pendown()

    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    pen.end_fill()
    pen.penup()


def draw_digit(pen, digit, x, y, size):
    """在指定位置绘制一个数字。"""
    thickness = size * 0.14
    horizontal_length = size - 2 * thickness
    vertical_length = size - 2 * thickness

    positions = (
        (x + thickness, y + 2 * size - thickness, horizontal_length, thickness),
        (x + size - thickness, y + size + thickness, thickness, vertical_length),
        (x + size - thickness, y + thickness, thickness, vertical_length),
        (x + thickness, y, horizontal_length, thickness),
        (x, y + thickness, thickness, vertical_length),
        (x, y + size + thickness, thickness, vertical_length),
        (x + thickness, y + size - thickness / 2, horizontal_length, thickness),
    )

    for is_on, position in zip(SEGMENTS[digit], positions):
        color = ON_COLOR if is_on else OFF_COLOR
        draw_rectangle(pen, *position, color)


def draw_number(number):
    """根据数字位数调整大小，并依次绘制全部数字。"""
    screen = turtle.Screen()
    screen.setup(width=1100, height=440)
    screen.title("七段数码管绘制")
    screen.bgcolor(BACKGROUND_COLOR)
    screen.tracer(False)

    pen = turtle.Turtle(visible=False)
    pen.speed(0)

    size = min(85, 900 / (len(number) * 1.3))
    gap = size * 0.3
    total_width = len(number) * size + (len(number) - 1) * gap
    start_x = -total_width / 2
    start_y = -size

    for index, digit in enumerate(number):
        x = start_x + index * (size + gap)
        draw_digit(pen, digit, x, start_y, size)

    screen.update()
    turtle.done()


def main():
    """组织输入和绘制流程。"""
    number = read_number()

    if number is None:
        return

    draw_number(number)


if __name__ == "__main__":
    main()