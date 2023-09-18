import os
import shutil

# 源文件夹的路径
source_dir = 'D:/dataset/AllCategory/W4'

# 目标文件夹的路径
target_dir = 'D:/dataset/detection/detection_FM'

# 遍历源文件夹中的所有JPG文件
for filename in os.listdir(source_dir):
    if filename.endswith('.jpg'):
        # 复制JPG文件到目标文件夹中
        shutil.copy(os.path.join(source_dir, filename), os.path.join(target_dir, filename))