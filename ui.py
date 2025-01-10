import os
from tkinter import Tk, filedialog, simpledialog, messagebox, Button, Label

def get_user_input():
    root = Tk()
    root.title("图片统计与PDF生成工具")
    root.geometry("400x350")

    # 定义变量存储用户输入
    input_directory = None
    output_directory = None
    images_per_folder = 6

    # 定义标签用于显示统计信息
    label_total_folders = Label(root, text="总文件夹数量: 未统计")
    label_total_images = Label(root, text="总图片数量: 未统计")
    label_progress = Label(root, text="已统计文件夹数量: 0")

    def select_input_directory():
        nonlocal input_directory
        input_directory = filedialog.askdirectory(title="选择要统计的文件夹")
        if not input_directory:
            messagebox.showerror("错误", "未选择文件夹")
        else:
            label_input_dir.config(text=f"已选文件夹: {input_directory}")
            update_statistics()

    def select_output_directory():
        nonlocal output_directory
        output_directory = filedialog.askdirectory(title="选择导出PDF的文件夹")
        if not output_directory:
            output_directory = os.getcwd()  # 默认当前工作目录
        label_output_dir.config(text=f"已选输出路径: {output_directory}")

    def analyze_and_generate_pdf():
        nonlocal images_per_folder
        images_per_folder_input = simpledialog.askinteger("输入", "每个文件夹展示的图片数量", minvalue=0, maxvalue=100)
        if images_per_folder_input is not None:
            images_per_folder = images_per_folder_input

        if input_directory and output_directory:
            from data_analysis import count_images_by_folder
            from pdf_generator import create_pdf

            folder_image_count = count_images_by_folder(input_directory, update_progress)
            output_pdf = os.path.join(output_directory, "output.pdf")
            create_pdf(input_directory, output_pdf, folder_image_count, images_per_folder)
            messagebox.showinfo("完成", f"PDF已生成: {output_pdf}")
        else:
            messagebox.showerror("错误", "请先选择文件夹和输出路径")

    def show_help():
        help_message = (
            "1. 选择要统计的图片文件夹。\n"
            "2. 选择导出PDF文件的保存位置。\n"
            "3. 输入每个文件夹展示的图片数量（默认为6张）。"
        )
        messagebox.showinfo("帮助", help_message)

    def update_statistics():
        if input_directory:
            from data_analysis import count_images_by_folder
            folder_image_count = count_images_by_folder(input_directory)
            total_folders = len(folder_image_count)
            total_images = sum(folder_image_count.values())
            label_total_folders.config(text=f"总文件夹数量: {total_folders}")
            label_total_images.config(text=f"总图片数量: {total_images}")

    def update_progress(current, total):
        label_progress.config(text=f"已统计文件夹数量: {current}/{total}")

    # 创建按钮和标签
    Button(root, text="选择文件夹", command=select_input_directory).pack(pady=5)
    label_input_dir = Label(root, text="已选文件夹: 未选择")
    label_input_dir.pack(pady=5)

    Button(root, text="选择输出路径", command=select_output_directory).pack(pady=5)
    label_output_dir = Label(root, text="已选输出路径: 未选择")
    label_output_dir.pack(pady=5)

    Button(root, text="开始分析并生成PDF", command=analyze_and_generate_pdf).pack(pady=10)

    # 显示统计信息的标签
    label_total_folders.pack(pady=5)
    label_total_images.pack(pady=5)
    label_progress.pack(pady=5)

    # 帮助按钮
    Button(root, text="帮助", command=show_help).pack(side='bottom', pady=10)

    root.mainloop()

if __name__ == "__main__":
    get_user_input()
