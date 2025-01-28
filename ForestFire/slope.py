import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 横150×縦100のセル構造を作成（状態を初期化）
cells_state = np.zeros((150, 100), dtype=int)  # 各セルの状態: 0=空, 1=傾斜, 2=木, 3=葉

# 色を生成する関数
def gen_colors(num_states):
    default_colors = ['skyblue', 'black', 'brown', 'green', 'yellow', 'orange', 'red']
    if num_states > len(default_colors):
        # 指定された数が既存の色数を超える場合、ランダム色を追加
        extra_colors = [
            f'#{np.random.randint(0, 0xFFFFFF):06x}' for _ in range(num_states - len(default_colors))
        ]
        return default_colors + extra_colors
    return default_colors[:num_states]

# 傾斜を生成
def gen_slope(deg):
    theta = np.pi * deg / 180
    a = np.tan(theta)
    for x in range(150):
        y = int(a * x)
        for y_0 in range(min(y, 100)):  # y_0が100未満になるように制限
            cells_state[x, y_0] = 1  # 傾斜を1で設定

# 木を生成
def gen_tree(base, height, thickness, trunk_height, sharpness= np.pi / 6, ratio=1.1):
    x_base, y_base = base
    #leaf
    height_new = 
    for y in range(trunk_height, int((height - trunk_height) * ratio)):
        for x in range(x_base - , x_base + trunk_height - y // 8 + 5+  1):
            cells_state[x, y_base + y] = 3  
    for x in range(x_base - thickness, x_base + thickness + 1):
        for y in range(y_base, y_base + height + 1):
            cells_state[x, y] = 2  # 木を2で設定
    for y in range(trunk_height, height, 3):
        for x in range(x_base - trunk_height + y // 8, x_base + trunk_height - y // 8 + 1):
            cells_state[x, y_base + y] = 2  # 木を2で設定

# 30度の傾斜を生成
gen_slope(30)

# 木を生成
gen_tree((40, 20), 50, 2, 10)

# 状態数に応じてカラーマップを生成
num_states = np.max(cells_state) + 1  # 状態の数を取得
colors = gen_colors(num_states)
cmap = ListedColormap(colors)  # カラーマップを作成

# セルを描画（状態を可視化）
plt.imshow(cells_state.T, cmap=cmap, origin='lower')  # 転置して表示
plt.colorbar(ticks=range(num_states), label='State')  # カラーバーを追加
plt.grid(visible=True, linestyle='--', linewidth=0.5, color='gray')

plt.show()
