import tkinter as tk
import json
import os
import sys

if len(sys.argv) != 0:
    # 创建主窗口
    root = tk.Tk()
    root.title("输入历史记录")

    # 设置窗口在屏幕上居中
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth()/2 - window_width/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2)
    root.geometry("+{}+{}".format(position_right, position_down))

    # 创建一个输入框
    entry = tk.Entry(root)
    entry.pack(pady=10)

    # 当点击按钮时执行的函数
    def add_to_history():
        # 获取输入框的内容
        input_text = entry.get()

        hash_value = input_text
        history_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'history.json')
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

        # 关闭主窗口
        root.destroy()

    # 创建一个确认按钮
    button = tk.Button(root, text="确认", command=add_to_history)
    button.pack()

    # 进入主循环
    root.mainloop()
