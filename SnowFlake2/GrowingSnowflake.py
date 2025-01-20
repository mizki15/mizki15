import numpy as np
import matplotlib.pyplot as plt
import math

# 六角形を描画する関数
def draw_snowflake(vertex):
    for i in range(len(vertex)):
        plt.plot([vertex[i][0], vertex[(i + 1) % len(vertex)][0]], 
                 [vertex[i][1], vertex[(i + 1) % len(vertex)][1]], 'k-')
    plt.scatter(vertex[:, 0], vertex[:, 1], c='red', s=5)  # 頂点を赤色で表示し、サイズを指定
    plt.axis('equal')  # アスペクト比を等しく
    plt.show()

# 頂点間の距離（長さ）を計算する関数
def calculate_interval(vertex, vertex_num):
    interval = np.linalg.norm(vertex[vertex_num] - vertex[(vertex_num + 1) % len(vertex)])
    return interval

# 各辺を分割して新しい頂点を計算する関数
def plot_equal_interval(vertex, new_interval):
    new_vertex = np.array([])
    for i in range(len(vertex)):
        vec = vertex[(i + 1) % len(vertex)] - vertex[i]
        new_vertex = np.append(new_vertex, vertex[i])
        number_per_edge = int(calculate_interval(vertex, i) / new_interval)
        for j in range(1, number_per_edge):
            new_vertex = np.append(new_vertex, vertex[i] + vec * j / number_per_edge)
    new_vertex = new_vertex.reshape(-1, 2)

    return new_vertex

# 頂点の中間角度を計算する関数
def calculate_middle_angle(vertex, vertex_num):
    # 頂点を取得
    vertex1 = vertex[(vertex_num - 1) % len(vertex)]  # 頂点A
    vertex2 = vertex[vertex_num]    # 頂点B
    vertex3 = vertex[(vertex_num + 1) % len(vertex)]  # 頂点C

    # 頂点からのベクトルを計算
    vec1 = vertex1 - vertex2  # ベクトルBA
    vec2 = vertex3 - vertex2  # ベクトルBC

    # ベクトルの長さを計算
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # ゼロベクトルのチェック
    if norm_vec1 == 0 or norm_vec2 == 0:
        raise ValueError(f"Zero vector encountered at vertex {vertex_num}. Check input data.")

    # ベクトルの長さを正規化して方向を取得
    vec1_unit = vec1 / norm_vec1
    vec2_unit = vec2 / norm_vec2

    # 2つのベクトルを加算して二等分ベクトルを計算
    if vec1_unit[0] == -vec2_unit[0] and vec1_unit[1] == -vec2_unit[1]:
        v0 = np.array([-vec1_unit[1], vec1_unit[0]])
    else:
        v0 = vec1_unit + vec2_unit
    
    print(v0)

    # 逆ベクトルを計算
    v1 = -v0

    # v0 または v1 のうち、原点方向でないものを選択
    if np.dot(v0, vertex2) > 0:  # v0 が外向き
        v = v0
    else:  # v1 が外向き
        v = v1

    print(np.linalg.norm(v))
    # 単位ベクトルを計算して返す
    vu = v / np.linalg.norm(v)
    return vu


# 雪の結晶を成長させる関数
def grow_snowflake(vertex, grow_vertex_num_list, grow_length, wideness, interval):
    for i in grow_vertex_num_list:
        vec = calculate_middle_angle(vertex, i)
        wideness_range_abs = int(wideness / interval)
        for j in range(i-wideness_range_abs, i+wideness_range_abs + 1):
            vertex[(j) % len(vertex)] += vec * grow_length
    return vertex
    
def get_sharpness(vertex, vertex_num):
    # 頂点を取得
    vertex1 = vertex[(vertex_num - 1) % len(vertex)]  # 頂点A
    vertex2 = vertex[vertex_num]    # 頂点B
    vertex3 = vertex[(vertex_num + 1) % len(vertex)]  # 頂点C

    # 頂点からのベクトルを計算
    vec1 = vertex1 - vertex2  # ベクトルBA
    vec2 = vertex3 - vertex2  # ベクトルBC

    # ベクトルの長さを計算
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # ゼロベクトルのチェック
    if norm_vec1 == 0 or norm_vec2 == 0:
        raise ValueError(f"Zero vector encountered at vertex {vertex_num}. Check input data.")

    # ベクトルの長さを正規化して方向を取得
    vec1_unit = vec1 / norm_vec1
    vec2_unit = vec2 / norm_vec2

    # 2つのベクトルの内積を計算
    dot_product = np.dot(vec1_unit, vec2_unit)

    # 内積から角度を計算
    angle = np.arccos(dot_product)

    # 角度を度に変換
    angle_degrees = np.degrees(angle)

    return angle_degrees

def get_sharp_vertex(vertex, border_sharpness):
    sharp_vertex_num_list = []
    for i in range(len(vertex)):
        sharpness = get_sharpness(vertex, i)
        if sharpness <= border_sharpness:
            sharp_vertex_num_list.append(i)
    return sharp_vertex_num_list

# 初期六角形の頂点を定義
vertex = np.array([[0.5, math.sqrt(3) / 2], 
                   [1, 0], 
                   [0.5, -math.sqrt(3) / 2], 
                   [-0.5, -math.sqrt(3) / 2], 
                   [-1, 0], 
                   [-0.5, math.sqrt(3) / 2]])

#draw_snowflake(vertex)

# 各辺を等間隔に分割し、新しい頂点を追加
new_interval = 0.02  # 分割間隔
border_sharpness = 130
vertex = plot_equal_interval(vertex, new_interval)

vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 0.3, 0.1, new_interval)
vertex = plot_equal_interval(vertex, new_interval)
draw_snowflake(vertex)
vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 0.2, 0.2, new_interval)
vertex = plot_equal_interval(vertex, 0.02)
draw_snowflake(vertex)
