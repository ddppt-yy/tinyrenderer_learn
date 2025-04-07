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

print(primitives)
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
    print(v0, v1, v2)



    zbuf = draw_tri_barycentric_zbuf(v0, v1, v2, zbuf, width, height, draw, "black")






tga.close()
image.save("lession4.png")
