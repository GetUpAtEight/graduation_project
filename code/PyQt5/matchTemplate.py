import os
import cv2
import time

sum = 0
threshold = 0.6
output_path = 'error'
# 遍历所有待测图片
start_time = time.time()
for root, dirs, files in os.walk("D:/dataset/detection/detection_2A"):
# for root, dirs, files in os.walk("D:/dataset/YOLOArea/Mark_Final/images/test"):
# for root, dirs, files in os.walk("result/crop"):
    for file in files:
        # 加载待测图片
        img_path = os.path.join(root, file)
        img = cv2.imread(img_path)

        # 将待测图片转换成灰度图像
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 创建矩形结构元素
        kernel_img = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # 顶帽变换
        tophat_img = cv2.morphologyEx(gray_img, cv2.MORPH_TOPHAT, kernel_img)
        # 进行闭运算操作
        closing_img = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, kernel_img)
        # 进行底帽变换操作
        bottomhat_img = cv2.morphologyEx(gray_img, cv2.MORPH_BLACKHAT, kernel_img)
        # 最大类间方差法阈值分割
        _, binary_img = cv2.threshold(bottomhat_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # 遍历所有模板图片并进行匹配
        results = []
        for root2, dirs2, files2 in os.walk("D:/dataset/template/2A"):
            for template_file in files2:
                # 加载模板图片
                template_path = os.path.join(root2, template_file)
                template = cv2.imread(template_path)

                # 将模板图片转换成灰度图像
                gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                # 如果模板图像比待测图像大即跳过
                if gray_template.shape[0] > gray_img.shape[0] or gray_template.shape[1] > gray_img.shape[1]:
                    continue

                kernel_template = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                tophat_template = cv2.morphologyEx(gray_template, cv2.MORPH_TOPHAT, kernel_template)
                # 底帽变换
                closing_template = cv2.morphologyEx(gray_template, cv2.MORPH_CLOSE, kernel_img)
                # 进行底帽变换操作
                bottomhat_template = cv2.morphologyEx(gray_template, cv2.MORPH_BLACKHAT, kernel_img)
                # 最大类间方差法阈值分割
                _, binary_template = cv2.threshold(bottomhat_template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # 进行模板匹配
                # cv2.TM_SQDIFF平方差匹配
                # cv2.TM_SQDIFF_NORMED：归一化平方差匹配法
                # cv2.TM_CCORR：相关匹配法
                # cv2.TM_CCORR_NORMED：归一化相关匹配法
                # cv2.TM_CCOEFF：相关系数匹配法
                # cv2.TM_CCOEFF_NORMED：归一化相关系数匹配法
                result = cv2.matchTemplate(binary_img, binary_template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                # 存储匹配结果和模板图片
                #
                # if max_val < threshold:
                #     continue
                # else:
                results.append((max_val, template))
        # # 根据匹配结果对模板图片进行排序
        # end_time = time.time()
        # # 计算匹配时间
        # match_time = end_time - start_time
        # print("Match time: {:.2f}ms".format(match_time * 1000))
        results.sort(key=lambda x: x[0], reverse=True)
        print(results[0][0])

        if len(results) == 0:
            sum = sum + 1

            print(file)
            cv2.imwrite(file, img)
            # cv2.imshow("Image", img)
            # cv2.waitKey(0)


        result, template = results[0]
        w, h = template.shape[:-1]
        top_left = cv2.minMaxLoc(cv2.matchTemplate(binary_img, binary_template, cv2.TM_CCOEFF_NORMED))[3]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)


        # 显示待测图片和匹配结果
        # cv2.imshow("Image", img)
        # cv2.waitKey(0)
        # # 输出匹配时间
end_time = time.time()
# 计算匹配时间
match_time = end_time - start_time
print("Match time: {:.2f}ms".format(match_time * 1000))