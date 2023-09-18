# import cv2
# import numpy as np
#
# # 读取目标图像和模板图像
# target_img = cv2.imread('result/crop/25_11182020 165044OK.jpg')
# template_img = cv2.imread('1.jpg')
#
# # 将模板图像转换为灰度图像
# template_gray = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
#
# # 使用ORB算法提取模板图像的特征
# orb = cv2.ORB_create()
# kp1, des1 = orb.detectAndCompute(template_gray, None)
#
# # 在目标图像中寻找匹配区域
# target_gray = cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY)
# kp2, des2 = orb.detectAndCompute(target_gray, None)
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
# matches = bf.match(des1, des2)
#
# # 筛选最优匹配
# matches = sorted(matches, key=lambda x: x.distance)
# good_matches = matches[:10]
#
#
# # 绘制匹配结果
# if len(good_matches) > 0:
#     src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#     dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
#     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
#     h, w = template_gray.shape
#     pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
#     dst = cv2.perspectiveTransform(pts, M)
#     target_img = cv2.polylines(target_img, [np.int32(dst)], True, (0, 0, 255), 2, cv2.LINE_AA)
#
# # 显示匹配结果
# cv2.imshow('Match Result', target_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

import cv2

# 读取待匹配图像和模板图像
img = cv2.imread('result/crop/25_11182020 165044OK.jpg')
template = cv2.imread('1.jpg')
# target_img = cv2.imread('result/crop/25_11182020 165044OK.jpg')
# template_img = cv2.imread('1.jpg')

# 初始化ORB特征检测器和描述子提取器
orb = cv2.ORB_create()

# 提取待匹配图像和模板图像的特征点和特征描述子
kp1, des1 = orb.detectAndCompute(img, None)
kp2, des2 = orb.detectAndCompute(template, None)

# 初始化暴力匹配器
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# 对待匹配图像和模板图像的特征描述子进行匹配
matches = bf.match(des1, des2)

# 根据匹配结果排序
matches = sorted(matches, key=lambda x:x.distance)

# 取最佳匹配结果
best_match = matches[0]
print(best_match)
# 绘制匹配结果
img_match = cv2.drawMatches(img, kp1, template, kp2, [best_match], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# 显示匹配结果
cv2.imshow('Match Result', img_match)
cv2.waitKey(0)
cv2.destroyAllWindows()