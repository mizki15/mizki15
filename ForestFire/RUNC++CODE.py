import subprocess
import os

# ディレクトリとファイル名の入力を想定したフルパス
directory_path = input("フルパス（例: C:\\path\\to\\your_file.cpp）を入力してください: ")
directory_path = directory_path.strip('"')
# インクルードパスを指定（例: Eigen のパスを指定）
include_path = r"C:\Users\NKJ-M\Downloads\SFML-2.6.1"
# os.path を使ってディレクトリパスとファイル名を分離
path, file_name_with_ext = os.path.split(directory_path)  # ディレクトリパスとファイル名＋拡張子を分離
file_name, ext = os.path.splitext(file_name_with_ext)  # ファイル名と拡張子を分離

# 分離した結果を表示（確認用）
print(f"ディレクトリパス: {path}")
print(f"ファイル名: {file_name}")
print(f"拡張子: {ext}")



# 環境変数 PATH に g++ のパスを追加（例: MinGW のパスを追加）
gpp_path = r'C:\mingw64\bin'  # 必要な場合は MinGW のパスを指定
os.environ['PATH'] = os.environ['PATH'] + ';' + gpp_path

# 実行したい g++ コマンドを構築
convert_exe_file = f'g++ -I {include_path} {file_name_with_ext} -o {file_name}.exe'
run_exe_file = f'{file_name}.exe'

print(f"コンパイルコマンド: {convert_exe_file}")

def run_command(command, path):
    #  ディレクトリの存在確認
    if os.path.isdir(path):
        try:
            # subprocess.run を使用して、指定ディレクトリでコマンドを実行
            result = subprocess.run(['cmd.exe', '/c', command], cwd=path, capture_output=True, text=True)

            if result.stdout:
                # コマンドの標準出力を表示
                print("=== 標準出力 ===")
                print(result.stdout)

            # エラー出力があれば表示
            if result.stderr:
                print("=== エラー出力 ===")
                print(result.stderr)

        except Exception as e:
            print(f"エラーが発生しました: {e}")
    else:
        print(f"指定されたディレクトリが存在しません: {path}")


run_command(convert_exe_file, path)
run_command(run_exe_file, path)