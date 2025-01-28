import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import struct

# 素材の種類を定義
AIR = 0
SOIL = 1
WOOD = 2
LEAF = 3
DRY_LEAF = 4
MATERIAL_COUNT = 5

# 状態
NORMAL = 0
BURNING = 1
BURNED = 2

# 自然環境条件
environment = {"windSpeed": 0.0}

# 素材のプロパティ
materialProperties = [
    {"t": 0.0, "I_0": float('inf'), "I_1": float('inf'), "E_out": [0.0, 0.0, 0.0]},  # AIR
    {"t": 0.0, "I_0": float('inf'), "I_1": float('inf'), "E_out": [0.0, 0.0, 0.0]},  # SOIL
    {"t": 20.0, "I_0": 5000.0, "I_1": 16000.0, "E_out": [0.0, 2000.0, 0.0]},  # WOOD
    {"t": 1.0, "I_0": 5000.0, "I_1": 16000.0, "E_out": [0.0, 2000.0, 0.0]},  # LEAF
    {"t": 1.0, "I_0": 5000.0, "I_1": 16000.0, "E_out": [0.0, 2000.0, 0.0]},  # DRY_LEAF
]

# セル構造を定義
class Cell:
    def __init__(self, state=0, material=0, energy=0.0, time=0.0):
        self.state = state
        self.material = material
        self.energy = energy
        self.time = time

# セル構造体を格納する配列（150x100のサイズ）
width = 150
height = 100
cells_state = np.empty((width, height), dtype=Cell)

# セルを初期化
for x in range(width):
    for y in range(height):
        cells_state[x, y] = Cell()

# 傾斜を生成
def gen_slope(deg):
    theta = np.pi * deg / 180
    a = np.tan(theta)
    for x in range(width):
        y = int(a * x)
        for y_0 in range(min(y, height)):  # y_0が100未満になるように制限
            cells_state[x, y_0].state = NORMAL
            cells_state[x, y_0].material = SOIL
            cells_state[x, y_0].energy = 0.0
            cells_state[x, y_0].time = 0.0

def gen_fallen_leaf(deg, thickness):
    theta = np.pi * deg / 180
    a = np.tan(theta)
    for x in range(width):
        y = int(a * x)
        for y_0 in range(y,min(y + thickness,height)):  # y_0が100未満になるように制限
            cells_state[x, y_0].state = NORMAL
            cells_state[x, y_0].material = DRY_LEAF
            cells_state[x, y_0].energy = 0.0
            cells_state[x, y_0].time = 0.0

# 木を生成
def gen_tree(base, height, thickness, trunk_height, sharpness=np.pi / 12, ratio=1.2):
    x_base, y_base = base
    height_new = int(height * ratio)
    
    # 葉の生成
    for y in range(trunk_height, height_new):
        width = int(np.tan(sharpness) * (height_new - y))
        for x in range(x_base - width, x_base + width + 1):
            cells_state[x, y_base + y].state = NORMAL
            cells_state[x, y_base + y].material = LEAF
            cells_state[x, y_base + y].energy = 0.0
            cells_state[x, y_base + y].time = 1.0
            
    # 幹の生成
    for y in range(y_base, y_base + height + 1):
        width = int(np.floor((thickness / height * (height - y)))) + 1
        for x in range(x_base - width, x_base + width + 1):
            cells_state[x, y].state = NORMAL
            cells_state[x, y].material = WOOD
            cells_state[x, y].energy = 0.0
            cells_state[x, y].time = 0.0
    
    # 枝の生成
    for y in range(trunk_height + 2, height, 3):
        width = int(np.tan(sharpness) * (height - y))
        for x in range(x_base - width, x_base + width + 1):
            cells_state[x, y_base + y].state = NORMAL
            cells_state[x, y_base + y].material = WOOD
            cells_state[x, y_base + y].energy = 0.0
            cells_state[x, y_base + y].time = 0.0

# 30度の傾斜を生成
gen_slope(30)

# 木を生成
gen_tree((40, 25), 50, 2, 10)

# 落ち葉を生成
gen_fallen_leaf(30, 3)

# 素材ごとの色を設定
material_colors = {
    AIR: 'skyblue',  # 空気
    SOIL: 'black',  # 土
    WOOD: 'brown',  # 木
    LEAF: 'green',  # 葉
    DRY_LEAF: 'yellow',  # 枯れ葉
}

# 素材ごとに色をつけるためのレイヤーを作成
material_layer = np.zeros((width, height), dtype=int)
for x in range(width):
    for y in range(height):
        material_layer[x, y] = cells_state[x, y].material

# カラーマップを作成
colors = [material_colors[i] for i in range(5)]
cmap = ListedColormap(colors)

print(material_layer)
print(cmap)
print(colors)
print(material_colors)


# セルを描画（素材を可視化）
plt.imshow(material_layer.T, cmap=cmap, origin='lower')  # 転置して表示
plt.colorbar(ticks=range(MATERIAL_COUNT), label='Material')  # カラーバーを追加
#plt.grid(visible=True, linestyle='-', linewidth=0.5, color='gray')
plt.show()

# バイナリファイルに保存
def save_cells_to_file(filename):
    with open(filename, 'wb') as file:
        for x in range(width):
            for y in range(height):
                cell = cells_state[x, y]
                # セルの情報をバイナリで書き込む
                file.write(struct.pack('4f', cell.state, cell.material, cell.energy, cell.time))

# セルデータをファイルに保存
save_cells_to_file('flame/cells_state.bin')

