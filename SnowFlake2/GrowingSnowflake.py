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
        
def calculate_middle_angle(vertex, vertex_num):
    # 頂点を取得
    vertex1 = vertex[(vertex_num - 1) % len(vertex)]  # 頂点A
    vertex2 = vertex[vertex_num]    # 頂点B
    vertex3 = vertex[(vertex_num + 1) % len(vertex)]  # 頂点C
    # 頂点からのベクトルを計算
    vec1 = vertex1 - vertex2  # ベクトルBA
    vec2 = vertex3 - vertex2  # ベクトルBC

    # ベクトルの長さを正規化して方向を取得
    vec1_unit = vec1 / np.linalg.norm(vec1)
    vec2_unit = vec2 / np.linalg.norm(vec2)

    # 2つのベクトルを加算して二等分ベクトルを計算
    v0 = vec1_unit + vec2_unit

    # 逆ベクトルを計算
    v1 = -v0

    # v0 または v1 のうち、原点方向でないものを選択
    # (原点方向にないものは、ベクトルが「外向き」である場合と解釈)
    if np.dot(v0, vertex2) > 0:  # v0 が外向き
        v = v0
    else:  # v1 が外向き
        v = v1

    # 単位ベクトルを計算して返す
    vu = v / np.linalg.norm(v)
    return vu

# 雪の結晶を成長させる関数
def grow_snowflake(vertex, grow_vertex_num_list, grow_length):
    new_vertex = np.array([])
    for i in range(len(vertex)):
        if i in grow_vertex_num_list:
            angle = calculate_middle_angle(vertex, i)
            new_vertex = np.append(new_vertex, vertex[i] + angle * grow_length)
        else:
            new_vertex = np.append(new_vertex, vertex[i])
            
    new_vertex = new_vertex.reshape(-1, 2)

    return new_vertex
    


# 初期六角形の頂点を定義
vertex = np.array([[0.5, math.sqrt(3) / 2], 
                   [1, 0], 
                   [0.5, -math.sqrt(3) / 2], 
                   [-0.5, -math.sqrt(3) / 2], 
                   [-1, 0], 
                   [-0.5, math.sqrt(3) / 2]])

draw_snowflake(vertex)

# 各辺を等間隔に分割し、新しい頂点を追加
new_interval = 0.05  # 分割間隔
vertex = plot_equal_interval(vertex, new_interval)

vertex = grow_snowflake(vertex, [1], 0.5)


draw_snowflake(vertex)
