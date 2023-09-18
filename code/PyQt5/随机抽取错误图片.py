import os
import random
import shutil

# 源文件夹的路径
source_dir = 'D:/dataset/error'

# 目标文件夹的路径
target_dir = 'D:/dataset/detection/detection_VD'

# 获取源文件夹中所有JPG文件的路径
jpg_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith('.jpg')]

# 从JPG文件列表中随机选择五个文件
selected_files = random.sample(jpg_files, 5)

# 将选定的五个文件复制到目标文件夹中
for i, filename in enumerate(selected_files):
    new_filename = f'image_{i}.jpg'  # 为每个文件创建新文件名
    shutil.copy(filename, os.path.join(target_dir, new_filename))