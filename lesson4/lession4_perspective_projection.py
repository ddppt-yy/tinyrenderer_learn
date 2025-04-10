# -------------------------------------------------------
# Created by     : xx
# Filename       : lession4_perspective_projection.py
# Author         : name
# Created On     : 2025/04/05 21:47
# Last Modified  : 2025/04/05 21:47
# Version        : v1.0
# Description    : 
# -------------------------------------------------------


from PIL import Image, ImageDraw, ImageFont
import math
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *












obj_file = "../obj/lesson4/cube.obj"
tga_file = "../obj/african_head_diffuse.tga"
vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)
primitives_uvs = read_obj_file_p(obj_file, 'uv')
uvs = read_obj_file_uv(obj_file)


width = 1000
height = width


image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)
# 设置字体
font = ImageFont.load_default()

tga = Image.open(tga_file)
tga_width, tga_height = image.size

zbuf = [-100.0] * 2 * width * 2 * height

color = "red"

p = primitives[0]
p_list = p + [p[0]]


for v_num in range(len(p)):
    v_start = [vertices[p_list[v_num]-1][0],
               vertices[p_list[v_num]-1][1]]

    v_end = [vertices[p_list[v_num+1]-1][0],
             vertices[p_list[v_num+1]-1][1]]

    draw_line_in_range(v_start[0], v_start[1], v_end[0], v_end[1], width, height, draw, color)

    #scaling along coordinate axes 
    scaling = [[0.5, 0], [0, 0.5]]
    v_start_scaling = matrix_mult(scaling, v_start)
    v_end_scaling = matrix_mult(scaling, v_end)

    draw_line_in_range(v_start_scaling[0], v_start_scaling[1], v_end_scaling[0], v_end_scaling[1], width, height, draw, "blue")


    #rotation 
    scaling = [[0.8, 0], [0, 0.8]]
    rad = math.radians(45)
    rotation = [[math.cos(rad), -math.sin(rad)], [math.sin(rad), math.cos(rad)]]
    # rotation = [[1, 0], [0, 1]]

    op = matrix_mult(scaling, rotation)
    # op = matrix_mult(rotation, scaling)
    # print(op)

    v_start_op = matrix_mult(op, v_start)
    v_end_op = matrix_mult(op, v_end)

    draw_line_in_range(v_start_op[0], v_start_op[1], v_end_op[0], v_end_op[1], width, height, draw, "green")





tga.close()
image.save("lession4.png")
