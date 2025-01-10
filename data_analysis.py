import os

def get_image_files(directory):
    """递归获取目录下的所有图片文件"""
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.bmp', '.png')):
                image_files.append(os.path.join(root, file))
    return image_files

def count_images_by_folder(directory):
    """统计每个文件夹下的图片数量"""
    folder_image_count = {}
    for root, _, files in os.walk(directory):
        count = sum(1 for file in files if file.lower().endswith(('.jpg', '.jpeg', '.bmp', '.png')))
        if count > 0:
            folder_image_count[root] = count
    return folder_image_count
