
from PIL import Image, ImageDraw
import math


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


def read_obj_file_p(file_path, type='vertex'):
    if type == 'vertex':
        t = 0
    elif type == 'uv':
        t = 1
    primitive = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('f '):
                    parts = line.split()
                    vertex_indices = []
                    for part in parts[1:]:
                        vertex_index = int(part.split('/')[t])
                        vertex_indices.append(vertex_index)
                    primitive.append(list(vertex_indices))
    except FileNotFoundError:
        print(f"错误: 文件 {file_path} 未找到。")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return primitive



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



def draw_point(x, y, width, height, draw, color):
    def convert_coordinate(x, y):
        # 将 [-1, 1] 范围的坐标转换为图像像素坐标
        new_x = int((x + 1) / 2 * width)
        new_y = int((1 - y) / 2 * height)
        return new_x, new_y
    x1, y1 = convert_coordinate(x, y)
    draw.point((x1, y1), fill=color)

def convert_coordinate(x, y, width, height):
    # 将 [-1, 1] 范围的坐标转换为图像像素坐标
    new_x = int((x + 1) / 2 * width)
    new_y = int((1 - y) / 2 * height)
    return new_x, new_y

def draw_line_in_range(x0, y0, x1, y1, width, height, draw, color):


    # 转换输入的点坐标
    x2, y2 = convert_coordinate(x0, y0, width, height)
    x3, y3 = convert_coordinate(x1, y1, width, height)

    # 绘制直线
    draw.line((x2, y2, x3, y3), fill=color, width=1)


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


def barycentric(A, B, C, P):
    """
    计算点P在三角形ABC中的重心坐标
    :param A: 顶点A的三维坐标 (Ax, Ay, Az)
    :param B: 顶点B的三维坐标 (Bx, By, Bz)
    :param C: 顶点C的三维坐标 (Cx, Cy, Cz)
    :param P: 待判断点P的三维坐标 (Px, Py, Pz)
    :return: 返回重心坐标 (lambda1, lambda2, lambda3)
    """
    
    # 辅助函数：三维向量叉乘
    def cross(u, v):
        return (
            u[1]*v[2] - u[2]*v[1],  # x分量
            u[2]*v[0] - u[0]*v[2],  # y分量
            u[0]*v[1] - u[1]*v[0]   # z分量
        )
    
    # 1. 构建矩阵s (只使用x,y分量，隐式投影到2D)
    s = [
        [C[0]-A[0], B[0]-A[0], A[0]-P[0]],  # x轴分量 (i=0)
        [C[1]-A[1], B[1]-A[1], A[1]-P[1]]   # y轴分量 (i=1)
    ]
    
    # 2. 计算叉乘（实际只需要二维行列式）
    u = cross(
        (s[0][0], s[0][1], s[0][2]),  # s[0]向量
        (s[1][0], s[1][1], s[1][2])   # s[1]向量
    )
    
    # 3. 处理退化三角形（面积接近0）
    if abs(u[2]) > 1e-9:
        # 计算重心坐标（归一化处理）
        lambda1 = 1.0 - (u[0] + u[1]) / u[2]
        lambda2 = u[1] / u[2]
        lambda3 = u[0] / u[2]
        return (lambda1, lambda2, lambda3)
    
    # 4. 退化情况返回无效坐标
    return (-1, 1, 1)









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


def draw_tri_barycentric_zbuf(v0, v1, v2, zbuf, width, height, draw, color):
    bbox_min_x, bbox_min_y, bbox_max_x, bbox_max_y = get_bbox(v0, v1, v2)
    for x in range(int(bbox_min_x*width), int(bbox_max_x*width)):
        for y in range(int(bbox_min_y*width), int(bbox_max_y*width)):
            p = [x/width, y/height]
            # alpha, beta, gamma = barycentric_coordinates(v0, v1, v2, p)
            alpha, beta, gamma = barycentric(v0, v1, v2, p)
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
                if z > zbuf[(x+width+(y+height)*2*width)]:
                    zbuf[(x+width+(y+height)*2*width)] = z
                    draw_point(x/width, y/height, width, height, draw, color)
    return zbuf



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

def vector_div_w(v):
    v_unit = [x/v[-1] for x in v]
    return v_unit


def matrix_mult(mtx0, mtx1):
    if isinstance(mtx0, (int, float)) and isinstance(mtx1, (int, float)): #num*num
        ans = mtx0*mtx1
    elif (isinstance(mtx0, list) and isinstance(mtx0[0], (int, float)) and #vector*vector
          isinstance(mtx1, list) and isinstance(mtx1[0], (int, float))):
        # ans = [0] * len(mtx0)
        ans = [0 for _ in range(len(mtx0))]
        for i in range(len(mtx0)):
            ans[i] = mtx0[i] * mtx1[i]
    elif (isinstance(mtx0, list) and isinstance(mtx0[0], list) and #matrix*vector
          isinstance(mtx1, list) and isinstance(mtx1[0], (int, float)) and
          len(mtx0[0]) == len(mtx1)):
        # ans = ([0] * 1) * len(mtx0)
        ans = [0 for _ in range(len(mtx0))]
        for i in range(len(mtx0)):
            for j in range(len(mtx1)):
                ans[i] = ans[i] + mtx0[i][j] * mtx1[j]
    elif (isinstance(mtx0, list) and isinstance(mtx0[0], list) and #matrix*matrix
          isinstance(mtx1, list) and isinstance(mtx1[0], list) and
          len(mtx0[0]) == len(mtx1)):
        # ans = [[0] * len(mtx1[0])] * len(mtx0)
        ans = [[0 for _ in range(len(mtx1[0]))] for _ in range(len(mtx0))]
        for i in range(len(mtx0)):
            for j in range(len(mtx1[0])):
                ans[i][j] = 0
                for k in range(len(mtx0[0])):
                    ans[i][j] = ans[i][j] + mtx0[i][k] * mtx1[k][j]
    elif (isinstance(mtx0, list) and isinstance(mtx1, (int, float))):
        if isinstance(mtx0[0], list):                               # matrix*num
            # ans = ([0] * len(mtx0[0])) * len(mtx0)
            ans = [[0 for _ in range(len(mtx0))] for _ in range(len(mtx0))]
            for i in range(len(mtx0)):
                for j in range(len(mtx0[0])):
                    ans[i][j] = mtx0[i][j] * mtx1
        else:                                                       # vector*num
            # ans = ([0] * 1) * len(mtx0)
            ans = [0 for _ in range(len(mtx0))]
            for i in range(len(mtx0)):
                ans[i] = mtx0[i] * mtx1
    return ans










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

if __name__ == "__main__":
    mtx0 = [[1, 2, 3], [1, 2, 3]]
    mtx1 = [[1, 2], [1, 2], [1, 2]]
    print(matrix_mult(mtx1, mtx0))
    print(matrix_mult(mtx0, mtx1))