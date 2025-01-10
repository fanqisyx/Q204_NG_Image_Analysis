# 图片统计与PDF生成工具

## 简介

该工具用于递归统计指定文件夹下的所有图片，并将统计结果和图片以表格形式导出为PDF文件。支持多种图片格式（如JPG、JPEG、BMP、PNG），并允许用户自定义每个文件夹展示的图片数量。

## 功能特点

- **递归统计**：自动递归遍历指定目录下的所有子目录，统计每层目录中的图片数量。
- **PDF导出**：将统计结果和图片以表格形式导出为PDF文件，便于查看和分享。
- **自定义设置**：用户可以自定义每个文件夹展示的图片数量。

## 使用说明

### 安装依赖

首先，确保你已经安装了Python环境。然后，使用以下命令安装所需的第三方库：

```bash
pip install reportlab pillow pyinstaller
```

### 运行工具

1. **克隆项目**：
    ```bash
    git clone https://github.com/your-repo-name/image-statistics-pdf-generator.git
    cd image-statistics-pdf-generator
    ```

2. **运行主程序**：
    ```bash
    python main.py
    ```

3. **选择文件夹**：
    - 选择要统计的图片文件夹。
    - 选择导出PDF文件的保存位置。
    - 输入每个文件夹展示的图片数量（默认为6张）。

4. **生成PDF**：
    工具会自动生成一个包含统计结果和图片的PDF文件，并保存到指定目录中。

## 代码结构

- `main.py`：主程序入口，负责调用用户输入获取函数和PDF生成函数。
- `ui.py`：用户界面模块，使用Tkinter库实现图形化用户交互。
- `data_analysis.py`：数据处理模块，包含递归统计图片数量的函数。
- `pdf_generator.py`：PDF生成模块，负责创建PDF文档并添加内容。
- `.gitignore`：忽略文件列表，用于版本控制。
- `readme.md`：项目说明文档。


## 联系方式

- **作者**：[fanqi]
- **邮箱**：[fanqisyx@163.com]
- **GitHub**：[https://github.com/fanqisyx]



