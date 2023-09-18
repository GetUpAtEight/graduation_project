import os
import sys
import time

import cv2
import detect
import qdarkstyle
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QMessageBox, QScrollArea
from PyQt5.QtWidgets import QFileDialog
import shutil

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None): # 当创建一个类的实例时会自动调用这个方法
        super(Ui_MainWindow, self).__init__(parent)
        self.timer_detect = QtCore.QTimer()
        self.setupUi(self)
        self.init_logo()  # 初始化logo
        self.init_slots()  # 初始化槽函数
        # 初始化属性
        self.detect_folder_path = None  # 目标检测图片文件夹路径
        self.detect_file_path = None  # 目标检测图片路径
        self.model_path = None  # 目标检测模型路径
        self.template_folder_path = None  # 模板图片文件夹路径
        self.template_file_path = None  # 模板匹配图片路径
        self.crop_folder_path = "result/crop"  # 模板匹配待测图片路径
        self.result_path = "result"
        self.error_path = "error"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)  # 布局的左、上、右、下到窗体边缘的距离
        self.verticalLayout.setObjectName("verticalLayout")

        # 打开图片按钮
        self.pushButton_img = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_img.sizePolicy().hasHeightForWidth())
        self.pushButton_img.setSizePolicy(sizePolicy)
        self.pushButton_img.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_img.setMaximumSize(QtCore.QSize(150, 40))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        self.pushButton_img.setFont(font)
        self.pushButton_img.setObjectName("pushButton_img")
        self.verticalLayout.addWidget(self.pushButton_img, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)  # 增加垂直盒子内部对象间距

        # 加载模型按钮
        self.pushButton_model = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_model.sizePolicy().hasHeightForWidth())
        self.pushButton_model.setSizePolicy(sizePolicy)
        self.pushButton_model.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_model.setFont(font)
        self.pushButton_model.setObjectName("pushButton_model")
        self.verticalLayout.addWidget(self.pushButton_model, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 检测按钮
        self.pushButton_detect = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_detect.setSizePolicy(sizePolicy)
        self.pushButton_detect.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_detect.setFont(font)
        self.pushButton_detect.setObjectName("pushButton_detect")
        self.verticalLayout.addWidget(self.pushButton_detect, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 导入模板按钮
        self.pushButton_template = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect.sizePolicy().hasHeightForWidth())
        self.pushButton_template.setSizePolicy(sizePolicy)
        self.pushButton_template.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_template.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_template.setFont(font)
        self.pushButton_template.setObjectName("pushButton_template")
        self.verticalLayout.addWidget(self.pushButton_template, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 模板匹配按钮
        self.pushButton_matchTemplate = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_matchTemplate.sizePolicy().hasHeightForWidth())
        self.pushButton_matchTemplate.setSizePolicy(sizePolicy)
        self.pushButton_matchTemplate.setMinimumSize(QtCore.QSize(150, 40))
        self.pushButton_matchTemplate.setMaximumSize(QtCore.QSize(150, 40))
        self.pushButton_matchTemplate.setFont(font)
        self.pushButton_matchTemplate.setObjectName("pushButton_matchTemplate")
        self.verticalLayout.addWidget(self.pushButton_matchTemplate, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(30)

        # 显示导出目标检测结果按钮
        self.pushButton_detect_showdir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_detect_showdir.sizePolicy().hasHeightForWidth())
        self.pushButton_detect_showdir.setSizePolicy(sizePolicy)
        self.pushButton_detect_showdir.setMinimumSize(QtCore.QSize(150, 50))
        self.pushButton_detect_showdir.setMaximumSize(QtCore.QSize(150, 50))
        self.pushButton_detect_showdir.setFont(font)
        self.pushButton_detect_showdir.setObjectName("pushButton_detect_showdir")
        self.verticalLayout.addWidget(self.pushButton_detect_showdir, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addStretch(5)

        # 显示导出模板匹配结果按钮
        self.pushButton_template_showdir = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_template_showdir.sizePolicy().hasHeightForWidth())
        self.pushButton_template_showdir.setSizePolicy(sizePolicy)
        self.pushButton_template_showdir.setMinimumSize(QtCore.QSize(150, 50))
        self.pushButton_template_showdir.setMaximumSize(QtCore.QSize(150, 50))
        self.pushButton_template_showdir.setFont(font)
        self.pushButton_template_showdir.setObjectName("pushButton_template_showdir")
        self.verticalLayout.addWidget(self.pushButton_template_showdir, 0, QtCore.Qt.AlignHCenter)

        # 右侧图片填充区域
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label.setStyleSheet("border: 1px solid white;")  # 添加显示区域边框

        # 底部美化导航条
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23)) # 创建一个矩形区域，左上角坐标0，0.宽度800，高度23
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "喷码错误检测系统"))
        self.pushButton_img.setText(_translate("MainWindow", "选择图片"))
        self.pushButton_model.setText(_translate("MainWindow", "选择模型"))
        self.pushButton_detect.setText(_translate("MainWindow", "目标检测"))
        self.pushButton_template.setText(_translate("MainWindow", "选择模板"))
        self.pushButton_matchTemplate.setText(_translate("MainWindow", "模板匹配"))
        self.pushButton_detect_showdir.setText(_translate("MainWindow", "查看喷码区域"))
        self.pushButton_template_showdir.setText(_translate("MainWindow", "查看错误喷码"))
        self.label.setText(_translate("MainWindow", "TextLabel"))

    def init_slots(self):
        self.pushButton_img.clicked.connect(self.load_detect_img)
        self.pushButton_model.clicked.connect(self.select_model)
        self.pushButton_detect.clicked.connect(self.target_detect)
        self.pushButton_template.clicked.connect(self.load_template_img)
        self.pushButton_detect_showdir.clicked.connect(self.show_detect_dir)
        self.pushButton_template_showdir.clicked.connect(self.show_template_dir)
        self.pushButton_matchTemplate.clicked.connect(self.template_detect)

    def init_logo(self):
        pix = QtGui.QPixmap('')  # 绘制初始化图片
        self.label.setScaledContents(True)
        self.label.setPixmap(pix)

    # 加载目标检测的图片
    def load_detect_img(self):
        print('选择喷码图')
        detect_folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", 'D:/dataset/detection')

        if detect_folder_path:
            self.detect_folder_path = detect_folder_path
        print(detect_folder_path)

        if self.detect_folder_path == None:
            QMessageBox.information(self, '提示', '未选择文件夹')
            self.label.clear()
        else:
            # 用一个列表来存储文件夹中的喷码文件
            img_path = []
            for root, dirs, files in os.walk(detect_folder_path):
                for file_name in files:
                    detect_file_path = os.path.join(root, file_name)
                    img_path.append(detect_file_path)
            print(img_path)  # 检查一下是否都读取到了
            self.detect_file_path = img_path
            if len(img_path) == 0:
                QMessageBox.information(self, '提示', '文件夹为空')
                self.label.clear()
            # 显示第一张图片
            # self.detect_folder_path = detect_folder_path
            else:
                pixmap = QPixmap(img_path[0])
                pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
                self.label.setPixmap(pixmap)
                self.pushButton_img.setText(img_path[0].split('/')[-1])


    # 选择模型
    def select_model(self):
        model_path = QtWidgets.QFileDialog.getOpenFileName(self, "选择模型", "weights", "Model files(*.pt)")
        print(model_path)
        if not model_path[0]:
            QMessageBox.information(self, '提示', '未选择模型')
            self.label.clear()
        else:
            self.model_path = model_path
            self.pushButton_model.setText(self.model_path[0].split('/')[-1])

    # 目标检测
    def target_detect(self):
        # 检测前先清空result文件夹内容
        for root, dirs, files in os.walk(self.result_path):
            # 遍历子目录
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                # 删除子目录中的所有文件和子目录
                for file in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    else:
                        shutil.rmtree(file_path)
                # 删除子目录
                os.rmdir(dir_path)
            for file in os.listdir(self.result_path):
                file_data = self.result_path + "/" + file
                os.remove(file_data)

        detect_size = 640
        if self.check_detect_file():
            # 点击之后防止误触，禁用按钮
            self.pushButton_img.setEnabled(False)
            self.pushButton_model.setEnabled(False)
            self.pushButton_detect.setEnabled(False)
            self.pushButton_template.setEnabled(False)
            self.pushButton_matchTemplate.setEnabled(False)
            self.pushButton_detect_showdir.setEnabled(False)
            self.thread = DetectionThread(self.detect_folder_path, self.model_path, detect_size)
            self.thread.start()
            # 子线程运行结束之后signal_done，主线程执行UI更新操作
            self.thread.signal_done.connect(self.flash_detect_target)

    # 目标检测之前检查是否选择了数据和模型
    def check_detect_file(self):
        if self.detect_folder_path is None:
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if len(self.detect_file_path) == 0:
            QMessageBox.information(self, '提示', '请先导入数据')
            return False
        if self.model_path is None:
            QMessageBox.information(self, '提示', '请先选择模型')
            return False
        return True

    # 刷新
    def flash_detect_target(self):
        img_path = os.getcwd() + '/result/' + [f for f in os.listdir('result')][0]
        pixmap = QPixmap(img_path)
        pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
        self.label.setPixmap(pixmap)
        # 刷新完之后恢复按钮状态
        self.pushButton_img.setEnabled(True)
        self.pushButton_model.setEnabled(True)
        self.pushButton_detect.setEnabled(True)
        self.pushButton_matchTemplate.setEnabled(True)
        self.pushButton_template.setEnabled(True)
        self.pushButton_detect_showdir.setEnabled(True)

    # 加载模板匹配的图片
    def load_template_img(self):
        print('选择模板图')
        template_folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹", 'D:/dataset/template')
        if template_folder_path:
            self.template_folder_path = template_folder_path
        print(template_folder_path)

        if self.template_folder_path == None:
            QMessageBox.information(self, '提示', '未选择图片路径')
        else:
            # 用一个列表来存储文件夹中的喷码文件
            img_path = []
            for root, dirs, files in os.walk(template_folder_path):
                for file_name in files:
                    template_file_path = os.path.join(root, file_name)
                    img_path.append(template_file_path)
            print(img_path)  # 检查一下是否都读取到了
            self.template_file_path = img_path
            if len(img_path) == 0:
                QMessageBox.information(self, '提示', '文件夹为空')
            # 显示第一张图片
            # self.detect_folder_path = detect_folder_path
            else:
                self.pushButton_template.setText(template_folder_path.split('/')[-1])

    # 模板匹配
    def template_detect(self):
        # 清空error文件夹
        folder_path = self.error_path
        for file in os.listdir(folder_path):
            file_data = os.path.join(folder_path, file)
            os.remove(file_data)
        if self.check_template_file():
            # 点击之后防止误触，禁用按钮
            self.pushButton_img.setEnabled(False)
            self.pushButton_model.setEnabled(False)
            self.pushButton_detect.setEnabled(False)
            self.pushButton_template.setEnabled(False)
            self.pushButton_matchTemplate.setEnabled(False)
            self.pushButton_template_showdir.setEnabled(False)
            self.thread = MatchTemplateThread(self.crop_folder_path, self.template_folder_path)
            self.thread.start()
            # 子线程运行结束之后signal_done，主线程执行UI更新操作
            self.thread.signal_done.connect(self.flash_template_target)

    # 模板检测之前检查是否选择了模板
    def check_template_file(self):
        if self.template_folder_path is None:
            QMessageBox.information(self, '提示', '请先选择模板')
            return False
        if len(self.template_file_path) == 0:
            QMessageBox.information(self, '提示', '请先选择模板')
            return False
        return True

    # 刷新
    def flash_template_target(self):
        flag = os.listdir('error')
        if len(flag) == 0:
            pixmap = QPixmap("img.png")
            self.label.setPixmap(pixmap)
        else:
            img_path = os.getcwd() + '/error/' + [f for f in os.listdir('error')][0]
            pixmap = QPixmap(img_path)
            pixmap = pixmap.scaled(self.label.size(), Qt.IgnoreAspectRatio)
            self.label.setPixmap(pixmap)
            # 刷新完之后恢复按钮状态
        self.pushButton_img.setEnabled(True)
        self.pushButton_model.setEnabled(True)
        self.pushButton_detect.setEnabled(True)
        self.pushButton_matchTemplate.setEnabled(True)
        self.pushButton_template.setEnabled(True)
        self.pushButton_template_showdir.setEnabled(True)

    # 显示输出文件夹
    def show_detect_dir(self):
        path = "result"
        os.system(f"start explorer {path}")

    # 显示输出文件夹
    def show_template_dir(self):
        if len(os.listdir(self.error_path)) == 0:
            QMessageBox.information(self, '提示', '这批喷码没有错误')
        else:
            path = self.error_path
            os.system(f"start explorer {path}")


# DetectionThread子线程用来执行目标检测
class DetectionThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, detect_folder_path, model_path, detect_size):
        super(DetectionThread, self).__init__()
        self.detect_folder_path = detect_folder_path
        self.model_path = model_path
        self.detect_size = detect_size
        self.process = 0
        self.total = 0

    def run(self):
        # 目标检测
        detect.run(source=self.detect_folder_path, weights=self.model_path[0],
                   imgsz=(self.detect_size, self.detect_size))
        print(self.detect_folder_path)
        self.signal_done.emit(1)  # 发送结束信号

# MatchTemplateThread子线程用来执行模板匹配
class MatchTemplateThread(QThread):
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, crop_folder_path, template_folder_path):
        super(MatchTemplateThread, self).__init__()
        self.template_folder_path = template_folder_path
        self.crop_folder_path = crop_folder_path

    def run(self):
        # 模板匹配
        print(self.crop_folder_path)
        print(self.template_folder_path)
        self.match_template(self.crop_folder_path, self.template_folder_path)
        self.signal_done.emit(1)  # 发送结束信号

    def match_template(self, crop_folder_path, template_folder_path):
        sum = 0
        threshold = 0.4
        output_path = 'error'
        start_time = time.time()
        for root, dirs, files in os.walk(crop_folder_path):
            for file in files:
                # 加载待测图片
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)

                # 将待测图片转换成灰度图像
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # 创建矩形结构元素
                kernel_img = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

                # 进行闭运算操作
                closing_img = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, kernel_img)

                # 进行底帽变换操作
                bottomhat_img = cv2.morphologyEx(gray_img, cv2.MORPH_BLACKHAT, kernel_img)

                # 进行顶帽变换操作
                tophat_img = cv2.morphologyEx(gray_img, cv2.MORPH_TOPHAT, kernel_img)

                # 最大类间方差法阈值分割
                _, binary_img_t = cv2.threshold(tophat_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                _, binary_img_b = cv2.threshold(bottomhat_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # 遍历所有模板图片并进行匹配
                results = []

                for root2, dirs2, files2 in os.walk(template_folder_path):
                    for template_file in files2:
                        # 加载模板图片
                        template_path = os.path.join(root2, template_file)
                        template = cv2.imread(template_path)
                        # 将模板图片转换成灰度图像
                        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
                        # 如果模板图像比待测图像大即跳过
                        if gray_template.shape[0] > gray_img.shape[0] or gray_template.shape[1] > gray_img.shape[1]:
                            continue
                        # 创建矩形结构元素
                        kernel_template = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

                        # 进行顶帽变换操作
                        tophat_template = cv2.morphologyEx(gray_template, cv2.MORPH_TOPHAT, kernel_template)
                        # 最大类间方差法阈值分割
                        _, binary_template_t = cv2.threshold(tophat_template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        # 进行底帽变换操作
                        bottomhat_template = cv2.morphologyEx(gray_template, cv2.MORPH_BLACKHAT, kernel_img)
                        # 最大类间方差法阈值分割
                        _, binary_template_b = cv2.threshold(bottomhat_template, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        # 进行模板匹配
                        # cv2.TM_SQDIFF平方差匹配
                        # cv2.TM_SQDIFF_NORMED：归一化平方差匹配法
                        # cv2.TM_CCORR：相关匹配法
                        # cv2.TM_CCORR_NORMED：归一化相关匹配法
                        # cv2.TM_CCOEFF：相关系数匹配法
                        # cv2.TM_CCOEFF_NORMED：归一化相关系数匹配法
                        result = cv2.matchTemplate(binary_img_b, binary_template_b, cv2.TM_CCOEFF_NORMED)

                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                        if max_val < threshold:
                            continue
                        else:
                            results.append((max_val, template))
                results.sort(key=lambda x: x[0], reverse=True)
                if len(results) == 0:
                    sum = sum + 1
                    cv2.imwrite(os.path.join(output_path, file), img)
        end_time = time.time()
        match_time = end_time - start_time
        print("Match time: {:.2f}ms".format(match_time * 1000))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ui = Ui_MainWindow()
    # 设置窗口图标
    icon = QIcon()
    icon.addPixmap(QPixmap("./UI/icon.ico"), QIcon.Normal, QIcon.Off)
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
