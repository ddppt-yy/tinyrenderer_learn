
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


def draw_point(x, y, width, height, draw, color):
    def convert_coordinate(x, y):
        # 将 [-1, 1] 范围的坐标转换为图像像素坐标
        new_x = int((x + 1) / 2 * width)
        new_y = int((1 - y) / 2 * height)
        return new_x, new_y
    x1, y1 = convert_coordinate(x, y)
    draw.point((x1, y1), fill=color)


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


def swap_vtx_by_y(v0, v1):
    v_tmp = [0, 0]
    if v0[1] > v1[1]:
        v_tmp = v0
        v0 = v1
        v1 = v_tmp
    return v0, v1


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

