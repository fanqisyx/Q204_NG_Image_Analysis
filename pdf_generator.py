import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PILImage
from data_analysis import get_image_files

# 注册SimHei字体
pdfmetrics.registerFont(TTFont('SimHei', 'simhei.ttf'))

def create_pdf(directory, output_pdf, folder_image_count, images_per_folder=6):
    """生成PDF文件"""
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Chinese', fontName='SimHei', fontSize=12))

    # 计算总图片数量
    total_images = sum(folder_image_count.values())

    # PDF第一页：图片数量比例展示（表格）
    data = [[Paragraph("文件夹", styles['Chinese']), "图片数量", "百分比"]]
    for folder, count in folder_image_count.items():
        relative_folder = os.path.relpath(folder, directory)
        percentage = f"{(count / total_images) * 100:.2f}%"
        data.append([Paragraph(relative_folder, styles['Chinese']), count, percentage])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'SimHei'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.2 * inch))

    # PDF第二页开始：图片展示
    for folder, count in folder_image_count.items():
        elements.append(Paragraph(f"文件夹: {os.path.relpath(folder, directory)}", styles['Chinese']))
        image_files = get_image_files(folder)[:images_per_folder]
        image_row = []
        for i, image_file in enumerate(image_files):
            img = PILImage.open(image_file)
            img.thumbnail((100, 100))
            img.save("temp.jpg")
            image_row.append(Image("temp.jpg", width=100, height=100))
            if (i + 1) % 4 == 0:
                elements.append(Table([image_row], colWidths=[100]*4))
                image_row = []
        if image_row:
            elements.append(Table([image_row], colWidths=[100]*4))
        elements.append(Spacer(1, 0.2 * inch))  # 添加空行

    doc.build(elements)
