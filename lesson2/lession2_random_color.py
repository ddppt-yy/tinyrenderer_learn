# -------------------------------------------------------
# Created by     : xx
# Filename       : lession2_random_color.py
# Author         : name
# Created On     : 2025/04/03 19:42
# Last Modified  : 2025/04/03 19:42
# Version        : v1.0
# Description    :
# -------------------------------------------------------


from PIL import Image, ImageDraw
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *
import random





obj_file = "../obj/african_head.obj"

vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)


width = 1000
height = 1000

image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

rainbow_colors = [
    (255, 0, 0),      # 红色
    (255, 165, 0),    # 橙色
    (255, 255, 0),    # 黄色
    (0, 128, 0),      # 绿色
    (0, 0, 255),      # 蓝色
    (75, 0, 130),     # 靛色
    (238, 130, 238)   # 紫色
]



for p in primitives:
    v0x = vertices[p[0]-1][0]
    v0y = vertices[p[0]-1][1]

    v1x = vertices[p[1]-1][0]
    v1y = vertices[p[1]-1][1]

    v2x = vertices[p[2]-1][0]
    v2y = vertices[p[2]-1][1]

    random_color = random.choice(rainbow_colors)
    draw_line_in_range(v0x, v0y, v1x, v1y, width, height, draw, 'black')
    draw_line_in_range(v1x, v1y, v2x, v2y, width, height, draw, 'black')
    draw_line_in_range(v2x, v2y, v0x, v0y, width, height, draw, 'black')
    draw_tri_barycentric([v0x, v0y], [v1x, v1y], [v2x, v2y], width, height, draw, random_color)

image.save("lession2_random_color.png")

