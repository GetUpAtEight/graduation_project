import os

folder_path = "D:/dataset/template/W4"  # 替换为您的文件夹路径

counter = 1  # 计数器

for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, str(counter) + ".jpg")
        os.rename(old_path, new_path)
        counter += 1