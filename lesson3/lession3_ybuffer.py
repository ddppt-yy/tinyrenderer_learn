# -------------------------------------------------------
# Created by     : xx
# Filename       : lession2_ybuffer.py
# Author         : name
# Created On     : 2025/04/04 17:25
# Last Modified  : 2025/04/04 17:25
# Version        : v1.0
# Description    : 
# -------------------------------------------------------



from PIL import Image, ImageDraw
import math
import sys
sys.path.append('../common')
from tinyrenderer_learn_common import *



def rasterize(v0, v1, width, height, draw, color, y_buf):
    for i in range(len(y_buf)):
        x = i/width
        if x<v0[0] or x>v1[0]:
            continue
        y = (x-v0[0])/(v1[0]-v0[0])*(v1[1]-v0[1])+v0[1]
        if y < y_buf[i]:
            continue
        y_buf[i] = y
        draw_point(x, 0.010, width, height, draw, color)
    return y_buf
















width = 1000
height = 1000

image = Image.new('RGB', (width, height), 'black')
draw = ImageDraw.Draw(image)



v0 = [0.020, 0.034] 
v1 = [0.744, 0.400]
v2 = [0.120, 0.434]
v3 = [0.444, 0.400]
v4 = [0.330, 0.463]
v5 = [0.594, 0.200]


v6 = [0.010, 0.010]
v7 = [0.790, 0.010]





draw_line_in_range(v0[0], v0[1], v1[0], v1[1], width, height, draw, "red")
draw_line_in_range(v2[0], v2[1], v3[0], v3[1], width, height, draw, "green")
draw_line_in_range(v4[0], v4[1], v5[0], v5[1], width, height, draw, "blue")

draw_line_in_range(v6[0], v6[1], v7[0], v7[1], width, height, draw, "white")


image.save("lession3_before_rast.png")


y_buf = [0] * width

y_buf = rasterize(v6, v7, width, height, draw, "white", y_buf)
y_buf = rasterize(v0, v1, width, height, draw, "red", y_buf)
y_buf = rasterize(v2, v3, width, height, draw, "green", y_buf)
y_buf = rasterize(v4, v5, width, height, draw, "blue", y_buf)

image.save("lession3_rast.png")




