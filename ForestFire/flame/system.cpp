#include <iostream>
#include <fstream>
#include <vector>
#include <array>
#include <cmath>     // std::max
#include <cstdint>   // for uint8_t
#include <limits>    // for std::numeric_limits

// 素材の種類
enum Material {
    AIR = 0,
    SOIL,
    WOOD,
    LEAF,
    DRY_LEAF,
    MATERIAL_COUNT
};

// 自然環境条件
struct Environment {
    float temperature; // 温度 [K]
    float windSpeed;   // 風速 [m/s]
};

const Environment environment = {298.0f, 0.0f};

// 素材ごとの定数構造
struct MaterialProperties {
    float t;       // 燃焼時間 [s/cell]
    float I_0;     // 発火定数
    float I_1;     // 無引火発火定数
    float E_out[3]; // 排出エネルギー定数
};

// 素材のプロパティを定義
const std::array<MaterialProperties, MATERIAL_COUNT> materialProperties = {
    MaterialProperties{0.0, std::numeric_limits<float>::infinity(), std::numeric_limits<float>::infinity(), {0.0, 0.0, 0.0}}, // AIR
    MaterialProperties{0.0, std::numeric_limits<float>::infinity(), std::numeric_limits<float>::infinity(), {0.0, 0.0, 0.0}}, // SOIL
    MaterialProperties{20.0, 5000.0, 16000.0, {0.0, 2000.0, 0.0}}, // WOOD
    MaterialProperties{1.0, 5000.0, 16000.0, {0.0, 2000.0, 0.0}},  // LEAF
    MaterialProperties{1.0, 5000.0, 16000.0, {0.0, 2000.0, 0.0}}   // DRY_LEAF
};

// セル構造
struct Cell {
    float state;    // 状態: 0=通常, 1=燃焼中, 2=燃焼後
    float material; // 素材: 0=空気, 1=土, 2=木, 3=葉, 4=枯れ葉
    float energy;   // 温度 [K]
    float time;     // 燃焼時間 [s]
};

// ファイルからセルデータを読み込む
void loadCellsFromFile(const std::string& filename, std::vector<std::vector<Cell>>& cells) {
    std::ifstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file: " << filename << std::endl;
        return;
    }

    for (auto& row : cells) {
        file.read(reinterpret_cast<char*>(row.data()), row.size() * sizeof(Cell));
    }

    file.close();
    std::cout << "File loaded: " << filename << std::endl;
}

// セルデータをファイルに保存
void saveCellsToFile(const std::string& filename, const std::vector<std::vector<Cell>>& cells) {
    std::ofstream file(filename, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file for saving: " << filename << std::endl;
        return;
    }

    for (const auto& row : cells) {
        file.write(reinterpret_cast<const char*>(row.data()), row.size() * sizeof(Cell));
    }

    file.close();
    std::cout << "File saved: " << filename << std::endl;
}

// セルの温度更新処理 (1世代分の処理①)
void updateTemperature(std::vector<std::vector<Cell>>& cells) {
    int width = cells.size();
    int height = cells[0].size();

    // 次の状態を保持する配列
    std::vector<std::vector<float>> nextTemperature(width, std::vector<float>(height, 0.0f));

    for (int x = 0; x < width; ++x) {
        for (int y = 0; y < height; ++y) {
            const Cell& cell = cells[x][y];
            const MaterialProperties& matProp = materialProperties[static_cast<int>(cell.material)];
            const Environment& env = environment;

            // 周囲8セルの排出エネルギーを計算
            float energySum = 0.0f;
            for (int dx = -1; dx <= 1; ++dx) {
                for (int dy = -1; dy <= 1; ++dy) {
                    if (dx == 0 && dy == 0) continue; // 自分自身は無視
                    int nx = x + dx;
                    int ny = y + dy;

                    // 範囲外チェック
                    if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;

                    energySum += materialProperties[static_cast<int>(cells[nx][ny].material)].E_out[static_cast<int>(cells[nx][ny].state)];
                }
            }

            nextTemperature[x][y] = energySum;
        }
    }

    // 更新後のエネルギーを適用
    for (int x = 0; x < width; ++x) {
        for (int y = 0; y < height; ++y) {
            cells[x][y].energy += nextTemperature[x][y];
        }
    }
}

// 発火判定と燃焼更新処理 (処理②)
void ifIgnite(std::vector<std::vector<Cell>>& cells) {
    int width = cells.size();
    int height = cells[0].size();

    for (int x = 0; x < width; ++x) {
        for (int y = 0; y < height; ++y) {
            Cell& cell = cells[x][y];
            const MaterialProperties& matProp = materialProperties[static_cast<int>(cell.material)];

            if (cell.material == AIR || cell.material == SOIL) continue; // 空気または土はスキップ

            if (cell.state == 1) { // 燃焼中のセル
                cell.time += 1.0f; // 燃焼時間を更新
                if (cell.time >= matProp.t) {
                    cell.state = 2; // 燃焼後
                }
                continue;
            }

            if (cell.state == 0) { // 通常状態のセル
                bool hasBurningNeighbor = false;

                // 隣接セルの発火判定
                for (int dx = -1; dx <= 1; ++dx) {
                    for (int dy = -1; dy <= 1; ++dy) {
                        if (dx == 0 && dy == 0) continue; // 自身をスキップ

                        int nx = x + dx;
                        int ny = y + dy;

                        // 範囲外チェック
                        if (nx < 0 || nx >= width || ny < 0 || ny >= height) continue;

                        const Cell& neighbor = cells[nx][ny];
                        if (neighbor.state == 1) { // 隣接セルが燃焼中
                            hasBurningNeighbor = true;
                            break;
                        }
                    }
                    if (hasBurningNeighbor) break; // 既に燃焼中の隣接セルがあればループを抜ける
                }

                // 発火条件をチェック
                if (hasBurningNeighbor && cell.energy >= matProp.I_0) {
                    cell.state = 1; // 燃焼中
                } else if (!hasBurningNeighbor && cell.energy >= matProp.I_1) {
                    cell.state = 1; // 燃焼中
                }
            }
        }
    }
}

int main() {
    const int width = 150;
    const int height = 100;

    // セルの初期化
    std::vector<std::vector<Cell>> cells(width, std::vector<Cell>(height));

    // ファイルからデータを読み込む
    loadCellsFromFile("cells_state.bin", cells);

    // シミュレーション
    const int steps = 100;
    for (int step = 0; step < steps; ++step) {
        updateTemperature(cells); // 処理①: 温度更新
        ifIgnite(cells);          // 処理②: 発火判定

        // 1ステップごとにセルデータを保存
        std::string filename = "cells_state_step_" + std::to_string(step + 1) + ".bin";
        saveCellsToFile(filename, cells);

        std::cout << "Step " << step + 1 << " completed." << std::endl;
    }

    return 0;
}
