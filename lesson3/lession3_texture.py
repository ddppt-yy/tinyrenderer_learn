# -------------------------------------------------------
# Created by     : xx
# Filename       : lession3_texture.py
# Author         : name
# Created On     : 2025/04/05 13:40
# Last Modified  : 2025/04/05 13:40
# Version        : v1.0
# Description    : 
# -------------------------------------------------------


from PIL import Image, ImageDraw, ImageFont
import math
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *


def read_obj_file_uv(file_path):
    # 定义一个空列表uvs，用于存储读取到的UV坐标
    uvs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('vt '):
                    parts = line.split()
                    if len(parts) == 4:
                        try:
                            uv = tuple(float(part) for part in parts[1:])
                            uvs.append(uv)
                        except ValueError:
                            print(f"无法将行 '{line}' 中的内容转换为浮点数。")
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return uvs

def get_pixel_value_from_uv(image, u, v):
    width, height = image.size
    # print(width, height)

    # 将 UV 坐标转换为像素坐标 (0, 0) 表示左上角，(1, 1) 表示右下角
    # 且uv坐标全为正值
    x, y = convert_coordinate(u, v, width, height)
    x = int(u * width)
    y = int((1-v) * height)

    # 获取像素值
    pixel = image.getpixel((x, y))
    return pixel



def draw_tri_barycentric_zbuf_texture(v0, v1, v2, v0uv, v1uv, v2uv, zbuf, width, height, cos, draw, tga): 
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = get_bbox(v0, v1, v2)
    for x in range(int(bbox_min_x*width), int(bbox_max_x*width)):
        for y in range(int(bbox_min_y*width), int(bbox_max_y*width)):
            p = [x/width, y/height]
            alpha, beta, gamma = barycentric(v0, v1, v2, p)
            if alpha >= 0 and beta >= 0 and gamma >= 0:
                z = alpha*v0[2] + beta*v1[2] + gamma*v2[2]
                if z > zbuf[(x+width+(y+height)*2*width)]:
                    zbuf[(x+width+(y+height)*2*width)] = z
                    uv_x = alpha*v0uv[0] + beta*v1uv[0] + gamma*v2uv[0]
                    uv_y = alpha*v0uv[1] + beta*v1uv[1] + gamma*v2uv[1]
                    pixel = get_pixel_value_from_uv(tga, uv_x, uv_y)
                    color = (int(pixel[0]*cos), int(pixel[1]*cos), int(pixel[2]*cos))
                    draw_point(x/width, y/height, width, height, draw, color)
    return zbuf



obj_file = "../obj/african_head.obj"
tga_file = "../obj/african_head_diffuse.tga"
vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)
primitives_uvs = read_obj_file_p(obj_file, 'uv')
uvs = read_obj_file_uv(obj_file)


width = 1000
height = width

image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(image)
# 设置字体
font = ImageFont.load_default()

tga = Image.open(tga_file)
tga_width, tga_height = image.size

light_vct = [0, 0, -1]
zbuf = [-100.0] * 2 * width * 2 * height

for p, puv in zip(primitives, primitives_uvs):
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

    uv0x = uvs[puv[0]-1][0]
    uv0y = uvs[puv[0]-1][1]
    uv0z = uvs[puv[0]-1][2]

    uv1x = uvs[puv[1]-1][0]
    uv1y = uvs[puv[1]-1][1]
    uv1z = uvs[puv[1]-1][2]

    uv2x = uvs[puv[2]-1][0]
    uv2y = uvs[puv[2]-1][1]
    uv2z = uvs[puv[2]-1][2]

    v0uv = [uv0x, uv0y, uv0z]
    v1uv = [uv1x, uv1y, uv1z]
    v2uv = [uv2x, uv2y, uv2z]


    tri_f = get_tri_f(v0, v1, v2)

    cos = vector_cosine(tri_f, light_vct)
    if cos < 0:
        continue

    color = (int(255*cos), int(255*cos), int(255*cos))

    zbuf = draw_tri_barycentric_zbuf_texture(v0, v1, v2, v0uv, v1uv, v2uv, zbuf, width, height, cos, draw, tga)

tga.close()
image.save("lession3_texture.png")