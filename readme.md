## 毕设代码

- PyQt5实现喷码错误检测系统，detection是需要检测的喷码，template是每种喷码制作的喷码图像
- 运行main.py运转可视化界面，点击选择图片，选择对应的需要检测的喷码；点击选择模型，选择用YOLOv5训练好的模型，检测出喷码区域。点击选择模板，选择这批待检测的喷码应该是什么类别，最后点击模板匹配可以输出错误喷码的第一张。

![show](Assets/show.png)

###说明
PyQt5界面借鉴https://github.com/zstar1003/yolov5_pyqt5
