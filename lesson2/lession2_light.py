# -------------------------------------------------------
# Created by     : xx
# Filename       : lession2_light.py
# Author         : name
# Created On     : 2025/04/04 11:19
# Last Modified  : 2025/04/04 11:19
# Version        : v1.0
# Description    : 
# -------------------------------------------------------



from PIL import Image, ImageDraw
import math
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *




def vector_cross_product(v0, v1):
    # A X B =
    # | i  j  k |
    # | Ax Ay Az|
    # | Bx By Bz| 
    # = (AyBz-AzBy)i - (AxBz-AzBx)j + (AxBy-AyBx)k
    # = ||A||*||B||*SINx

    # 计算向量v0和v1的叉积
    i = v0[1]*v1[2] - v0[2]*v1[1]  # 计算叉积的i分量
    j = v0[2]*v1[0] - v0[0]*v1[2]  # 计算叉积的j分量
    k = v0[0]*v1[1] - v0[1]*v1[0]  # 计算叉积的k分量
    return [i, j, k]  # 返回叉积结果


def vector_dot_product(v0, v1):
    # 计算向量v0和v1的点积
    dot_product = sum(i*j for i, j in zip(v0, v1))
    return dot_product

def vector_cosine(v0, v1):
    # 计算向量v0和v1的夹角余弦值
    cos = vector_dot_product(v0, v1) / (vector_norm(v0) * vector_norm(v1))
    return cos


def vector_norm(v):
    # 计算向量的范数，即向量的模
    norm = math.sqrt(sum(i**2 for i in v))
    # 返回向量的范数
    return norm


def get_tri_f(v0, v1, v2):
    # 定义一个函数，用于计算三角形法向量
    # 计算向量v0到v1的向量
    vct02 = [(v2[0]-v0[0]), (v2[1]-v0[1]), (v2[2]-v0[2])]
    # 计算向量v1到v2的向量
    vct01 = [(v1[0]-v0[0]), (v1[1]-v0[1]), (v1[2]-v0[2])]
    # 计算向量v0到v2的向量
    vctf = vector_cross_product(vct02, vct01)
    # 计算向量v0到v2的向量的模
    vctf_norm = vector_norm(vctf)
    # 计算向量v0到v2的向量的单位向量
    vctf_unit = [i/vctf_norm for i in vctf]
    # 返回向量v0到v2的单位向量
    return vctf_unit












obj_file = "../obj/african_head.obj"
vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)

width = 1000
height = 1000

image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(image)

light_vct = [0, 0, -1]

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

    color = (int(255*cos), int(255*cos), int(255*cos))

    draw_line_in_range(v0x, v0y, v1x, v1y, width, height, draw, color)
    draw_line_in_range(v1x, v1y, v2x, v2y, width, height, draw, color)
    draw_line_in_range(v2x, v2y, v0x, v0y, width, height, draw, color)
    draw_tri_barycentric([v0x, v0y], [v1x, v1y], [v2x, v2y], width, height, draw, color)


image.save("lession2_light.png")




