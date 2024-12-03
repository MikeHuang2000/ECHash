import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import winreg as reg
import sys

# 获取文件的哈希值
def get_hash(file_path, algorithm):
    BUF_SIZE = 65536
    if algorithm == "MD5":
        hash_algo = hashlib.md5()
    elif algorithm == "SHA256":
        hash_algo = hashlib.sha256()
    elif algorithm == "SHA1":
        hash_algo = hashlib.sha1()
    else:
        raise ValueError("Unknown algorithm")

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            hash_algo.update(data)
    return hash_algo.hexdigest().upper()

# 保存哈希值到文件
def save_hash(hash_value):
    history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json') # 获取程序所在目录的绝对路径，并拼接文件名 # 获取程序所在目录
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            data = json.load(f)
    else:
        data = []


    data.append(hash_value)

    if len(data) > 100:
        data = data[-100:]

    with open(history_file, 'w') as f:
        json.dump(data, f)

# 检查哈希值是否与历史记录中的最后一个相同
def check_hash(hash_value):
    history_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'history.json')
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            data = json.load(f)
            if len(data) > 0:
                return data[-1] == hash_value
    return False

# 主界面
def main_gui(file_path, algorithm):
    hash_value = get_hash(file_path, algorithm)

    root = tk.Tk()
    root.title('Hash Checker')

     # 设置窗口在屏幕上居中
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)
    root.geometry("+{}+{}".format(position_right, position_down))

    algo_label = tk.Label(root, text=f"Algorithm: {algorithm}")
    algo_label.pack(pady=10)

       # 使用文本框来显示哈希值，以便可以复制
    hash_entry = tk.Entry(root, width=70)
    hash_entry.insert(0, hash_value)
    hash_entry.pack(pady=10)

    if check_hash(hash_value):
        status_label = tk.Label(root, text='匹配！')
    else:
        status_label = tk.Label(root, text='不匹配！')
    status_label.pack(pady=10)

    save_hash(hash_value)

    root.mainloop()

# 添加到右键菜单
def add_to_context_menu():
    command_key_path = rf'Software\Classes\*\shell\EasyHash\shell\Adder\command'
    command_key = reg.CreateKey(reg.HKEY_CURRENT_USER, command_key_path)
        
    # 使用sys.executable代替python，并确保路径被双引号括起来
    temporary = "\Adder\Adder.exe"
    command = f'"{os.path.dirname(__file__) + temporary}" '
    reg.SetValue(command_key, '', reg.REG_SZ, command)
    
    reg.CloseKey(command_key)

    os.startfile(os.path.dirname(__file__) + "\EasyHash.bat")


    for algo in ["MD5", "SHA256","SHA1"]:
        command_key_path = rf'Software\Classes\*\shell\EasyHash\shell\\' + algo + '\command'
        command_key = reg.CreateKey(reg.HKEY_CURRENT_USER, command_key_path)
        
        # 使用sys.executable代替python，并确保路径被双引号括起来
        temporary = "\EasyHash.exe"
        command = f'"{os.path.dirname(__file__) + temporary}" "%1" {algo}'
        reg.SetValue(command_key, '', reg.REG_SZ, command)
        
        reg.CloseKey(command_key)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        file_path = sys.argv[1]
        algorithm = sys.argv[2]
        main_gui(file_path, algorithm)
    else:
        add_to_context_menu()
        print("Added to context menu.")
