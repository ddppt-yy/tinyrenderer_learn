# -------------------------------------------------------
# Created by     : xx
# Filename       : lession1.py
# Author         : name
# Created On     : 2025/04/03 15:48
# Last Modified  : 2025/04/03 15:48
# Version        : v1.0
# Description    : 
# -------------------------------------------------------

from PIL import Image, ImageDraw


def read_obj_file_v(file_path):
    vertices = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('v '):
                    parts = line.split()
                    if len(parts) == 4:
                        try:
                            vertex = tuple(float(part) for part in parts[1:])
                            vertices.append(vertex)
                        except ValueError:
                            print(f"无法将行 '{line}' 中的内容转换为浮点数。")
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return vertices


def read_obj_file_p(file_path):
    primitive = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('f '):
                    parts = line.split()
                    vertex_indices = []
                    for part in parts[1:]:
                        vertex_index = int(part.split('/')[0])
                        vertex_indices.append(vertex_index)
                    if len(vertex_indices) == 3:
                        primitive.append(tuple(vertex_indices))
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return primitive


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









obj_file = "./african_head.obj"

vertices = read_obj_file_v(obj_file)
primitives = read_obj_file_p(obj_file)
# print(vertices)
# print(primitives)

width = 1000
height = 1000

image = Image.new('RGB', (width, height), 'white')
draw = ImageDraw.Draw(image)

for p in primitives:
    v0x = vertices[p[0]-1][0]
    v0y = vertices[p[0]-1][1]

    v1x = vertices[p[1]-1][0]
    v1y = vertices[p[1]-1][1]

    v2x = vertices[p[2]-1][0]
    v2y = vertices[p[2]-1][1]

    draw_line_in_range(v0x, v0y, v1x, v1y, width, height, draw, 'black')
    draw_line_in_range(v1x, v1y, v2x, v2y, width, height, draw, 'black')
    draw_line_in_range(v2x, v2y, v0x, v0y, width, height, draw, 'black')

image.save("lession1.png")




