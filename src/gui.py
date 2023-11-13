# import time
#
# from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QProgressBar
#
# from utils import Docker
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.title = '资金分析工具'
#         self.window_size = (int(1920/2), int(1080/2), 300, 250)
#         self.version = "1.0"
#         self.recover_button = QPushButton("恢复程序", self)
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar_text = QLabel("", self)
#         self.init_ui()
#
#     def init_ui(self):
#
#         # 设置窗口标题
#         self.setWindowTitle(self.title)
#
#         # 设置窗口大小
#         self.setGeometry(*self.window_size)
#
#         # 创建所有UI元素
#         self.set_recover_button()
#         self.set_progress_bar()
#         self.set_progress_bar_text()
#
#     # 设置恢复功能按钮
#     def set_recover_button(self):
#         self.recover_button.setGeometry(100, 50, 100, 40)
#         self.recover_button.clicked.connect(self.on_recover_button_click)
#
#     # 恢复功能按钮点击事件
#     def on_recover_button_click(self):
#         self.progress_bar.setValue(0)
#
#         if not Docker.is_exist_exe():
#             self.progress_bar_text.setText("Docker尚未安装")
#             return
#
#         self.progress_bar.setValue(20)
#
#         # 启动情况下，杀进程重启
#         if Docker.is_running():
#             self.progress_bar.setValue(40)
#             self.progress_bar_text.setText("Docker运行中")
#
#             if not Docker.stop():
#                 self.progress_bar.setValue(100)
#                 self.progress_bar_text.setText('Docker停止失败')
#                 return
#
#             self.progress_bar_text.setText("Docker已停止")
#             time.sleep(3)
#
#             if not Docker.start():
#                 self.progress_bar.setValue(100)
#                 self.progress_bar_text.setText('Docker启动失败')
#                 return
#
#             self.progress_bar.setValue(60)
#             self.progress_bar_text.setText("Docker已启动")
#
#         # 未启动情况下启动
#         else:
#             self.progress_bar.setValue(40)
#             self.progress_bar_text.setText("Docker已停止")
#
#             if not Docker.start():
#                 self.progress_bar.setValue(100)
#                 self.progress_bar_text.setText('Docker启动失败')
#                 return
#
#             self.progress_bar.setValue(60)
#             self.progress_bar_text.setText("Docker已启动")
#
#         self.progress_bar.setValue(100)
#         self.progress_bar_text.setText("恢复已完成")
#
#     # 设置进度条相关元素
#     def set_progress_bar(self):
#         self.progress_bar.setGeometry(40, 70, 220, 100)
#         self.progress_bar.setRange(0, 100)
#         self.progress_bar.setValue(0)
#
#     # 设置进度条文本元素
#     def set_progress_bar_text(self):
#         self.progress_bar_text.setGeometry(100, 130, 100, 30)
