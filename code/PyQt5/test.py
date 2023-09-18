# import os
# import cv2
# img = cv2.imread("1.jpg");
# gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("1", gray_img)
# cv2.waitKey(0)
import cv2
import numpy as np

# # 读取原始图像
# img = cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)
#
# # 定义结构元素
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#
# # 底帽变换
# tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
#
# # 显示结果
# cv2.imshow('Original Image', img)
# cv2.imshow('Top-hat Image', tophat)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2

# 读取图像
# img = cv2.imread('detection/detection_2A/25_11182020 163136OK.bmp')
img = cv2.imread('D:/dataset/template/2A/1.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 顶帽变换
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# tophat = cv2.morphologyEx(gray_img, cv2.MORPH_TOPHAT, kernel)
# 创建矩形结构元素
kernel_img = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

# 进行闭运算操作
closing = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, kernel_img)

# 进行底帽变换操作
bottomhat = cv2.morphologyEx(gray_img, cv2.MORPH_BLACKHAT, kernel_img)
# 最大类间方差法阈值分割
_, binary = cv2.threshold(bottomhat, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
gray_img_1 = binary

# 显示结果
cv2.imshow('Original Image', gray_img_1)

cv2.waitKey(0)
cv2.destroyAllWindows()