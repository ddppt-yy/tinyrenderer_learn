# -------------------------------------------------------
# Created by     : xx
# Filename       : lession3_zbuffer.py
# Author         : name
# Created On     : 2025/04/04 19:16
# Last Modified  : 2025/04/04 19:16
# Version        : v1.0
# Description    : 
# -------------------------------------------------------

from PIL import Image, ImageDraw, ImageFont
import math
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *


def draw_tri_barycentric_zbuf(v0, v1, v2, zbuf, width, height, draw, color, debug):
    num= 0
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = get_bbox(v0, v1, v2)
    if debug == -1:
        print("bbox:", bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y)
    for x in range(int(bbox_min_x*width), int(bbox_max_x*width)):
        for y in range(int(bbox_min_y*width), int(bbox_max_y*width)):
            p = [x/width, y/height]
            # alpha, beta, gamma = barycentric_coordinates(v0, v1, v2, p)
            alpha, beta, gamma = barycentric(v0, v1, v2, p)
            if debug == -1:
                print("------")
                print("xybc:", x, y, alpha, beta, gamma)
            if alpha >= 0 and beta >= 0 and gamma >= 0:
                # 使用uv坐标进行差值的原理
                # if u + v > 1:
                #     u = 1 - u
                #     v = 1 - v
                #     # 计算点 P 的坐标
                #     x = u * A[0] + v * B[0] + (1 - u - v) * C[0]
                #     y = u * A[1] + v * B[1] + (1 - u - v) * C[1]
                #     z = u * A[2] + v * B[2] + (1 - u - v) * C[2]
                z = alpha*v0[2] + beta*v1[2] + gamma*v2[2]
                if debug == -1:
                    print("z: ", z)
                    print("z_buf: ", zbuf[int(x+y*width)])
                if z > zbuf[(x+width+(y+height)*2*width)]:
                    zbuf[(x+width+(y+height)*2*width)] = z
                    draw_point(x/width, y/height, width, height, draw, color)
                    # print("draw")
                    num += 1
                else:
                    pass
                    # print("zbuf:", zbuf[(x+y*width)])
    # print("num:", num)
    return zbuf





def draw_line_with_label_simple(draw, start, end, label, text_color="red", offset=5):
    """
    在线段起点处添加坐标标签（带智能偏移）
    :param draw: ImageDraw对象
    :param start: 线段起点 (x1, y1)
    :param end: 线段终点 (x2, y2)
    :param text_color: 文字颜色（默认红色）
    :param offset: 文字与起点的偏移像素（默认5）
    """
    # 生成坐标标签文本
    start = convert_coordinate(start[0], start[1] ,width, height)
    end = convert_coordinate(end[0], end[1] ,width, height)

    # 获取默认字体
    font = ImageFont.load_default()
    
    # 计算文本尺寸
    text_bbox = draw.textbbox((0, 0), label, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # 智能偏移方向判断
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # 根据线段方向自动调整偏移位置
    if abs(dx) > abs(dy):  # 水平方向线段
        text_x = start[0] + offset
        text_y = start[1] - text_height - offset
    else:  # 垂直方向线段
        text_x = start[0] + offset
        text_y = start[1] + offset
    
    # 绘制文字（带黑色描边增强可读性）
    draw.text(
        (text_x, text_y),
        label,
        fill=text_color,
        font=font,
        anchor="lt",  # 左对齐，顶部对齐
        stroke_width=1,
        stroke_fill="black"
    )



obj_file = "../obj/debug.obj"
obj_file = "../obj/african_head.obj"
vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)

width = 1000
height = width

image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(image)
# 设置字体
font = ImageFont.load_default()

light_vct = [0, 0, -1]

zbuf = [-100.0] * 2 * width * 2 * height

face = 0
for p in primitives:
    v0x = vertices[p[0]-1][0]
    v0y = vertices[p[0]-1][1]
    v0z = vertices[p[0]-1][2]

    v1x = vertices[p[1]-1][0]
    v1y = vertices[p[1]-1][1]
    v1z = vertices[p[1]-1][2]

    v2x = vertices[p[2]-1][0]
    v2y = vertices[p[2]-1][1]
    v2z = vertices[p[2]-1][2]

    v0 = [v0x, v0y, v0z]
    v1 = [v1x, v1y, v1z]
    v2 = [v2x, v2y, v2z]

    tri_f = get_tri_f(v0, v1, v2)

    cos = vector_cosine(tri_f, light_vct)
    if cos < 0:
        continue

    if face == 190:
        color = "red"
    elif face == 191:
        color = "blue"
    else:
        color = "white"
    color = (int(255*cos), int(255*cos), int(255*cos))

    # draw_line_in_range(v0x, v0y, v1x, v1y, width, height, draw, 'green')
    # draw_line_in_range(v1x, v1y, v2x, v2y, width, height, draw, 'green')
    # draw_line_in_range(v2x, v2y, v0x, v0y, width, height, draw, 'green')

    zbuf = draw_tri_barycentric_zbuf([v0x, v0y, v0z], [v1x, v1y, v1z], [v2x, v2y, v2z], zbuf, width, height, draw, color, face)
    # print("face:", face)
    face += 1
    # image.save(str(face)+".png")



if 0: #debug
    face = 0
    for p in primitives:
        v0x = vertices[p[0]-1][0]
        v0y = vertices[p[0]-1][1]
        v0z = vertices[p[0]-1][2]

        v1x = vertices[p[1]-1][0]
        v1y = vertices[p[1]-1][1]
        v1z = vertices[p[1]-1][2]

        v2x = vertices[p[2]-1][0]
        v2y = vertices[p[2]-1][1]
        v2z = vertices[p[2]-1][2]

        v0 = [v0x, v0y, v0z]
        v1 = [v1x, v1y, v1z]
        v2 = [v2x, v2y, v2z]

        tri_f = get_tri_f(v0, v1, v2)

        cos = vector_cosine(tri_f, light_vct)
        if cos < 0:
            continue

        if face == 190:
            color = "red"
        elif face == 191:
            color = "blue"
        else:
            color = "white"
        color = (int(255*cos), int(255*cos), int(255*cos))

        draw_line_in_range(v0x, v0y, v1x, v1y, width, height, draw, 'green')
        label = "[" + str(p[0]) + "," + str(p[1]) + "]."+str(face)
        draw_line_with_label_simple(draw, [v0x, v0y], [v1x, v1y], label=label, text_color="red", offset=5)

        draw_line_in_range(v1x, v1y, v2x, v2y, width, height, draw, 'green')
        label = "[" + str(p[1]) + "," + str(p[2]) + "]."+str(face)
        draw_line_with_label_simple(draw, [v1x, v1y], [v2x, v2y], label=label, text_color="yellow", offset=5)

        draw_line_in_range(v2x, v2y, v0x, v0y, width, height, draw, 'green')
        label = "[" + str(p[2]) + "," + str(p[0]) + "]."+str(face)
        draw_line_with_label_simple(draw, [v2x, v2y], [v0x, v0y], label=label, text_color="blue", offset=5)
        face += 1








image.save("lession3_zbuffer.png")

# print(zbuf)
# for i in range(0, width*height):
#     if i % width == 0:
#         print("\n")
#     print(zbuf[i], end=", ")


