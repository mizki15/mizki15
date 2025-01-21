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
    n = len(vertex)
    
    # 頂点kの前後の頂点の座標
    p1 = np.array(vertex[vertex_num-1])  # vertex[k-1]
    p2 = np.array(vertex[vertex_num])    # vertex[k]
    p3 = np.array(vertex[(vertex_num+1) % n])  # vertex[k+1] (閉じた多角形に対応するためk+1の次は0になる)
    
    # ベクトルv1 (vertex[k-1]からvertex[k]へのベクトル)
    v1 = p2 - p1
    # ベクトルv2 (vertex[k]からvertex[k+1]へのベクトル)
    v2 = p3 - p2
    
    # v1 = v2の場合、二等分線方向はv1, v2に垂直なベクトル
    if np.allclose(v1, v2):
        # v1に垂直なベクトルを求める
        bisector = np.array([v1[1], -v1[0]])  # (v1_y, -v1_x)
    else:
        # 二等分線ベクトル (v1 - v2)
        bisector = v1-v2
    print(bisector)
    
    # ベクトルを正規化して単位ベクトルを求める
    if np.linalg.norm(bisector) != 0:
        bisector_normalized = bisector / np.linalg.norm(bisector)
    else:
        bisector_normalized = bisector  # ゼロベクトルの場合はそのまま返す
    
    return bisector_normalized


# 雪の結晶を成長させる関数
def grow_snowflake(vertex, grow_vertex_num_list, grow_length, wideness, interval):
    for i in grow_vertex_num_list:
        vec = calculate_middle_angle(vertex, i)
        wideness_range_abs = int(wideness / interval)
        for j in range(i-wideness_range_abs, i+wideness_range_abs + 1):
            vertex[(j) % len(vertex)] += vec * grow_length
    return vertex
    
def get_sharpness(vertex, vertex_num):
    n = len(vertex)
    
    # 頂点kの前後の頂点の座標
    p1 = np.array(vertex[vertex_num-1])  # vertex[k-1]
    p2 = np.array(vertex[vertex_num])    # vertex[k]
    p3 = np.array(vertex[(vertex_num+1) % n])  # vertex[k+1] (閉じた多角形に対応するためk+1の次は0になる)
    
    # ベクトルv1 (vertex[k-1]からvertex[k]へのベクトル)
    v1 = p2 - p1
    # ベクトルv2 (vertex[k]からvertex[k+1]へのベクトル)
    v2 = p3 - p2
    
    dot = np.dot(v1, v2)
    # 外積（2次元ベクトルの場合はスカラー値）
    det = v1[0] * v2[1] - v1[1] * v2[0]
    # atan2 で符号付き角度を求める
    angle = np.pi + np.arctan2(det, dot)
    return np.degrees(angle)

def get_sharp_vertex(vertex, border_sharpness):
    sharp_vertex_num_list = []
    for i in range(len(vertex)):
        sharpness = get_sharpness(vertex, i)
        if 0 <= sharpness <= border_sharpness:
            sharp_vertex_num_list.append(i)
    print(sharp_vertex_num_list)
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
border_sharpness = 150  # 鋭角の閾値
vertex = plot_equal_interval(vertex, new_interval)

vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 1.2 , 0.3, new_interval)
vertex = plot_equal_interval(vertex, new_interval)
draw_snowflake(vertex)
vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 0.7, 0.1, new_interval)
vertex = plot_equal_interval(vertex, 0.02)
draw_snowflake(vertex)
vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 0.3, 0.05, new_interval)
vertex = plot_equal_interval(vertex, 0.01)
draw_snowflake(vertex)
vertex = grow_snowflake(vertex, get_sharp_vertex(vertex, border_sharpness), 0.2, 0.02, new_interval)
vertex = plot_equal_interval(vertex, 0.01)

draw_snowflake(vertex)
