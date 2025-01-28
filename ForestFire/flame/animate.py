import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 素材の種類を定義
AIR = 0
SOIL = 1
WOOD = 2
LEAF = 3
DRY_LEAF = 4
MATERIAL_COUNT = 5

# セル構造を定義
class Cell:
    def __init__(self, state=0, material=0, energy=0.0, time=0.0):
        self.state = state
        self.material = material
        self.energy = energy
        self.time = time

# アニメーションのための関数
def load_cells_from_file(filename, width, height):
    cells = np.empty((width, height), dtype=Cell)
    with open(filename, 'rb') as file:
        for x in range(width):
            for y in range(height):
                data = file.read(16)  # 4つのfloat（4バイト×4）= 16バイト
                if len(data) == 16:
                    state, material, energy, time = struct.unpack('4f', data)
                    cells[x, y] = Cell(state=int(state), material=int(material), energy=energy, time=time)
    return cells

# 素材ごとの色を設定
material_colors = {
    AIR: 'skyblue',  # 空気
    SOIL: 'black',  # 土
    WOOD: 'brown',  # 木
    LEAF: 'green',  # 葉
    DRY_LEAF: 'yellow',  # 枯れ葉
}

# カラーマップを作成
colors = [material_colors[i] for i in range(5)]
cmap = ListedColormap(colors)

# アニメーションを描画する関数
def animate_cells(filename_format, width, height, steps):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for step in range(steps):
        # セルデータを読み込み
        filename = filename_format.format(step + 1)  # ファイル名を動的に作成
        cells = load_cells_from_file(filename, width, height)

        # 素材ごとに色をつけるためのレイヤーを作成
        material_layer = np.zeros((width, height), dtype=int)
        for x in range(width):
            for y in range(height):
                material_layer[x, y] = cells[x, y].material

        # セルを描画（素材を可視化）
        ax.clear()
        ax.imshow(material_layer.T, cmap=cmap, origin='lower')  # 転置して表示
        ax.set_title(f'Step {step + 1}')
        ax.set_xticks([])  # x軸の目盛りを非表示
        ax.set_yticks([])  # y軸の目盛りを非表示
        plt.pause(0.1)  # 0.1秒の間隔で更新

    plt.show()

# ファイル名のフォーマットとステップ数
filename_format = 'flame/cells_state_step_{}.bin'
width = 150
height = 100
steps = 100  # 100ステップのアニメーション

# アニメーションを実行
animate_cells(filename_format, width, height, steps)
