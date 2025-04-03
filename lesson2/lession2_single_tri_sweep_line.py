# -------------------------------------------------------
# Created by     : xx
# Filename       : lession2_single_tri.py
# Author         : name
# Created On     : 2025/04/03 17:39
# Last Modified  : 2025/04/03 17:39
# Version        : v1.0
# Description    :
# -------------------------------------------------------

from PIL import Image, ImageDraw


def draw_line_in_range(x0, y0, x1, y1, width, height, draw, color):

    def convert_coordinate(x, y):
        # 将 [-1, 1] 范围的坐标转换为图像像素坐标
        new_x = int((x + 1) / 2 * width)
        new_y = int((1 - y) / 2 * height)
        return new_x, new_y

    # 转换输入的点坐标
    x2, y2 = convert_coordinate(x0, y0)
    x3, y3 = convert_coordinate(x1, y1)

    # 绘制直线
    draw.line((x2, y2, x3, y3), fill=color, width=2)


def swap_vtx_by_y(v0, v1):
    v_tmp = [0, 0]
    if v0[1] > v1[1]:
        v_tmp = v0
        v0 = v1
        v1 = v_tmp
    return v0, v1


def draw_tri_line_sweeping(v0, v1, v2, width, height, draw, color):
    v0, v1 = swap_vtx_by_y(v0, v1)
    v1, v2 = swap_vtx_by_y(v1, v2)
    v0, v1 = swap_vtx_by_y(v0, v1)
    height_2_0 = v2[1]-v0[0]

    for i in range(int(v0[1]*height), int(v1[1]*height)):
        height_1_0 = v1[1]-v0[1]
        alpha = float((i/height-v0[1])/height_2_0)
        beta = float((i/height-v0[1])/height_1_0)
        # a = v0 + (v2-v0)*alpha
        # b = v0 + (v1-v0)*beta
        a = [v0[i] + (v2[i] - v0[i]) * alpha for i in range(len(v0))]
        b = [v0[i] + (v1[i] - v0[i]) * beta for i in range(len(v0))]

        a, b = swap_vtx_by_y(a, b)
        print(a, b)
        draw_line_in_range(a[0], a[1], b[0], b[1], width, height, draw, color)

    for i in range(int(v1[1]*height), int(v2[1]*height)):
        height_1_0 = v2[1]-v1[1]
        alpha = float((i/height-v0[1])/height_2_0)
        beta = float((i/height-v1[1])/height_1_0)
        # a = v0 + (v2-v0)*alpha
        # b = v0 + (v1-v0)*beta
        a = [v0[i] + (v2[i] - v0[i]) * alpha for i in range(len(v0))]
        b = [v1[i] + (v2[i] - v1[i]) * beta for i in range(len(v0))]

        a, b = swap_vtx_by_y(a, b)
        print(a, b)
        draw_line_in_range(a[0], a[1], b[0], b[1], width, height, draw, 'color')


# max(x)==100
# max(y)==100
width = 1000
height = 1000
a = [0.10, 0.10]
b = [0.30, 0.90]
c = [0.66, 0.55]

image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)


draw_line_in_range(a[0], a[1], b[0], b[1], width, height, draw, 'black')
draw_line_in_range(b[0], b[1], c[0], c[1], width, height, draw, 'black')
draw_line_in_range(c[0], c[1], a[0], a[1], width, height, draw, 'black')
draw_tri_line_sweeping(a, b, c, width, height, draw, 'green')
image.save("lession2_single_tri_sweep_line.png")
