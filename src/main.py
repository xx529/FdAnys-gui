from PyQt5.QtWidgets import QApplication
from gui import MainWindow
import sys

if __name__ == '__main__':

    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 创建主窗口实例
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 运行应用程序的事件循环
    sys.exit(app.exec_())
