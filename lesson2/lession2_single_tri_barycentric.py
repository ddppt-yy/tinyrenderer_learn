# -------------------------------------------------------
# Created by     : xx
# Filename       : lession2_single_tri_barycentric.py
# Author         : name
# Created On     : 2025/04/03 19:15
# Last Modified  : 2025/04/03 19:15
# Version        : v1.0
# Description    :
# -------------------------------------------------------
from PIL import Image, ImageDraw
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *


def draw_point(x, y, width, height, draw, color):
    def convert_coordinate(x, y):
        # 将 [-1, 1] 范围的坐标转换为图像像素坐标
        new_x = int((x + 1) / 2 * width)
        new_y = int((1 - y) / 2 * height)
        return new_x, new_y
    x1, y1 = convert_coordinate(x, y)
    draw.point((x1, y1), fill=color)



def barycentric_coordinates(A, B, C, P):
    # 计算分母
    denominator = (B[1] - C[1]) * (A[0] - C[0]) + (C[0] - B[0]) * (A[1] - C[1])
    # 计算 alpha
    alpha = ((B[1] - C[1]) * (P[0] - C[0]) + (C[0] - B[0]) * (P[1] - C[1])) / denominator
    # 计算 beta
    beta = ((C[1] - A[1]) * (P[0] - C[0]) + (A[0] - C[0]) * (P[1] - C[1])) / denominator
    # 计算 gamma
    gamma = 1 - alpha - beta
    return alpha, beta, gamma


def get_bbox(v0, v1, v2):
    bbox_min_x = min(v0[0], v1[0], v2[0])
    bbox_max_x = max(v0[0], v1[0], v2[0])
    bbox_min_y = min(v0[1], v1[1], v2[1])
    bbox_max_y = max(v0[1], v1[1], v2[1])
    return bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y

def draw_tri_barycentric(v0, v1, v2, width, height, draw, color):
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = get_bbox(v0, v1, v2)
    for x in range(int(bbox_min_x*width), int(bbox_max_x*width)):
        for y in range(int(bbox_min_y*width), int(bbox_max_y*width)):
            p = [x/width, y/height]
            alpha, beta, gamma = barycentric_coordinates(v0, v1, v2, p)
            if alpha >= 0 and beta >= 0 and gamma >= 0:
                draw_point(x/width, y/height, width, height, draw, color)


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
# draw_tri_line_sweeping(a, b, c, width, height, draw, 'green')
draw_tri_barycentric(a, b, c, width, height, draw, 'green')


image.save("lession2_single_tri_barycentric.png")


