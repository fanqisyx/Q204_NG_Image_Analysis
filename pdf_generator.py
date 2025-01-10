import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PILImage
from data_analysis import get_image_files
import socket
from datetime import datetime
from io import BytesIO  # 添加导入语句

# 注册SimHei字体
pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))

def create_first_page(elements, directory, folder_image_count, styles):
    # 获取计算机名称
    computer_name = socket.gethostname()

    # 获取文件生成时间
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 计算总图片数量
    total_images = sum(folder_image_count.values())

    # 添加信息到PDF
    elements.append(Paragraph(f"文件基本信息：", styles['LargeChinese']))
    elements.append(Spacer(1, 0.4 * inch))  # 空2行
    elements.append(Table([[Paragraph(f"计算机名称: {computer_name}", styles['Chinese'])]], style=[('LINEBELOW', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Table([[Paragraph(f"文件生成时间: {generation_time}", styles['Chinese'])]], style=[('LINEBELOW', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Table([[Paragraph(f"选取的统计的文件夹的绝对路径: {os.path.abspath(directory)}", styles['Chinese'])]], style=[('LINEBELOW', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Table([[Paragraph(f"查询到的图片的总数: {total_images}", styles['Chinese'])]], style=[('LINEBELOW', (0, 0), (-1, -1), 1, colors.black)]))
    elements.append(Spacer(1, 0.4 * inch))

    # 确定最大层级数
    max_depth = max(len(os.path.relpath(folder, directory).split(os.sep)) for folder in folder_image_count.keys())
    max_depth = min(max_depth, 4)  # 最多显示4层

    # PDF第一页：图片数量比例展示（表格）
    headers = [Paragraph(f"层级{i+1}", styles['Chinese']) for i in range(max_depth)] + ["图片数量", "百分比"]
    data = [headers]

    # 预处理数据以确定哪些单元格需要合并
    merged_cells = []
    for folder, count in folder_image_count.items():
        relative_folder = os.path.relpath(folder, directory)
        parts = relative_folder.split(os.sep)
        if len(parts) > max_depth:
            parts = parts[:max_depth-1] + [os.sep.join(parts[max_depth-1:])]
        else:
            parts += [''] * (max_depth - len(parts))  # 填充空白以确保有max_depth列

        percentage = f"{(count / total_images) * 100:.2f}%"
        row = [Paragraph(part, styles['Chinese']) for part in parts] + [count, percentage]
        data.append(row)

    # 确定需要合并的单元格
    for col in range(max_depth):
        prev_value = None
        start_row = 1  # 跳过表头行
        for row in range(1, len(data)):
            current_value = data[row][col].getPlainText()
            if current_value == prev_value:
                merged_cells.append(('SPAN', (col, start_row), (col, row)))
            else:
                prev_value = current_value
                start_row = row

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    # 应用合并单元格
    for cell in merged_cells:
        table.setStyle(TableStyle([cell]))

    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

def create_pdf(directory, output_pdf, folder_image_count, images_per_folder=6):
    """生成PDF文件"""
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Chinese', fontName='SimHei', fontSize=12))
    styles.add(ParagraphStyle(name='SmallChinese', fontName='SimHei', fontSize=8))  # 添加新的样式
    styles.add(ParagraphStyle(name='LargeChinese', fontName='SimHei', fontSize=16))  # 添加更大的字体样式

    # 创建第一页
    first_page_elements = []
    create_first_page(first_page_elements, directory, folder_image_count, styles)

    # 将第一页添加到文档中
    elements = first_page_elements + [PageBreak()]

    # 创建后续页面
    for folder, count in folder_image_count.items():
        subsequent_pages_elements = []  # 每个文件夹一个新的列表
        subsequent_pages_elements.append(Paragraph(f"文件夹: {os.path.relpath(folder, directory)}", styles['Chinese']))

        image_files = get_image_files(folder)[:images_per_folder]
        num_images = len(image_files)

        # 表格宽度为页面宽度的75%
        table_width = 0.75 * A4[0]

        # 计算列数和行数
        num_cols = int(num_images ** 0.5) + 1
        num_rows = num_cols * 2

        # 表格高度为页面高度的70%
        table_height = 0.7 * A4[1]
        row_height_odd = 2*(3 / 4) * table_height / num_rows
        row_height_even = 2*(1 / 4) * table_height / num_rows

        col_width = table_width / num_cols

        data = []
        for i in range(num_rows):
            row = []
            for j in range(num_cols):
                index = i // 2 * num_cols + j
                if index < num_images:
                    image_file = image_files[index]
                    #print(f"1--Opening image file: {image_file}")  # 添加打印信息
                    try:
                        img = PILImage.open(image_file)
                        
                        #print(f"2---Opening image file: {image_file}")  # 添加打印信息
                        # 计算新的图片宽度和高度，保持等比例缩放
                        ratio = min(col_width / img.width, row_height_odd / img.height)*0.9
                        new_width = img.width * ratio
                        new_height = img.height * ratio
                        img.thumbnail((new_width, new_height))
                        
                        # 使用BytesIO将PILImage对象保存到内存中
                        img_byte_arr = BytesIO()
                        img.save(img_byte_arr, format='PNG')
                        img_byte_arr.seek(0)
                        
                        image_flowable = Image(img_byte_arr, width=new_width, height=new_height)
                        filename_flowable = Paragraph(os.path.basename(image_file), styles['SmallChinese'])
                        if i % 2 == 0:
                            row.append([image_flowable])  # 奇数行放置图片
                        else:
                            row.append([filename_flowable])  # 偶数行放置文件名
                    except Exception as e:
                        print(f"Error opening image file {image_file}: {e}")  # 错误信息
                else:
                    row.append(None)  # 填充空白单元格
            data.append(row)

        table = Table(data, colWidths=[col_width]*num_cols, rowHeights=[row_height_odd if i % 2 == 0 else row_height_even for i in range(num_rows)])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))

        # 添加文件夹名称和图片总数
        subsequent_pages_elements.append(Paragraph(f"这个文件夹中的图片总数: {num_images}", styles['Chinese']))
        subsequent_pages_elements.append(Spacer(1, 0.2 * inch))
        subsequent_pages_elements.append(table)
        subsequent_pages_elements.append(Spacer(1, 0.2 * inch))  # 添加空行

        # 将当前文件夹的元素添加到文档中，并插入分页符
        elements.extend(subsequent_pages_elements + [PageBreak()])

    # 移除最后一个多余的分页符
    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()

    doc.build(elements)