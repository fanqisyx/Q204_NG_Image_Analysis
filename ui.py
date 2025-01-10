import os
from tkinter import Tk, filedialog, simpledialog, messagebox

def get_user_input():
    root = Tk()
    root.withdraw()  # 隐藏主窗口

    # 选择要统计的文件夹
    input_directory = filedialog.askdirectory(title="选择要统计的文件夹")
    if not input_directory:
        messagebox.showerror("错误", "未选择文件夹")
        return None, None, None

    # 选择导出PDF的文件夹
    output_directory = filedialog.askdirectory(title="选择导出PDF的文件夹")
    if not output_directory:
        output_directory = os.getcwd()  # 默认当前工作目录

    # 输入每个文件夹展示的图片数量
    images_per_folder = simpledialog.askinteger("输入", "每个文件夹展示的图片数量", minvalue=1, maxvalue=100)

    return input_directory, output_directory, images_per_folder
