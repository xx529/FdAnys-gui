from PyQt5.QtWidgets import QApplication
import sys


import subprocess
from pathlib import Path

import time

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QProgressBar

from utils import Docker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = '资金分析工具'
        self.window_size = (int(1920/2), int(1080/2), 300, 250)
        self.version = "1.0"
        self.recover_button = QPushButton("恢复程序", self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar_text = QLabel("", self)
        self.init_ui()

    def init_ui(self):

        # 设置窗口标题
        self.setWindowTitle(self.title)

        # 设置窗口大小
        self.setGeometry(*self.window_size)

        # 创建所有UI元素
        self.set_recover_button()
        self.set_progress_bar()
        self.set_progress_bar_text()

    # 设置恢复功能按钮
    def set_recover_button(self):
        self.recover_button.setGeometry(100, 50, 100, 40)
        self.recover_button.clicked.connect(self.on_recover_button_click)

    # 恢复功能按钮点击事件
    def on_recover_button_click(self):
        self.progress_bar.setValue(0)

        if not Docker.is_exist_exe():
            self.progress_bar_text.setText("Docker尚未安装")
            return

        self.progress_bar.setValue(20)

        # 启动情况下，杀进程重启
        if Docker.is_running():
            self.progress_bar.setValue(40)
            self.progress_bar_text.setText("Docker运行中")

            if not Docker.stop():
                self.progress_bar.setValue(100)
                self.progress_bar_text.setText('Docker停止失败')
                return

            self.progress_bar_text.setText("Docker已停止")
            time.sleep(3)

            if not Docker.start():
                self.progress_bar.setValue(100)
                self.progress_bar_text.setText('Docker启动失败')
                return

            self.progress_bar.setValue(60)
            self.progress_bar_text.setText("Docker已启动")

        # 未启动情况下启动
        else:
            self.progress_bar.setValue(40)
            self.progress_bar_text.setText("Docker已停止")

            if not Docker.start():
                self.progress_bar.setValue(100)
                self.progress_bar_text.setText('Docker启动失败')
                return

            self.progress_bar.setValue(60)
            self.progress_bar_text.setText("Docker已启动")

        self.progress_bar.setValue(100)
        self.progress_bar_text.setText("恢复已完成")

    # 设置进度条相关元素
    def set_progress_bar(self):
        self.progress_bar.setGeometry(40, 70, 220, 100)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)

    # 设置进度条文本元素
    def set_progress_bar_text(self):
        self.progress_bar_text.setGeometry(100, 130, 100, 30)


class Cmd:

    @staticmethod
    def run(command) -> (bool, str):
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, ''


class Docker:

    CHECK_COUNT = 120
    EXE_FILE = '/Applications/Docker.app'
    # EXE_FILE = 'C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe'

    @staticmethod
    def start():
        is_success, _ = Cmd.run(['open', Docker.EXE_FILE])
        # is_success, _ = Cmd.run([Docker.EXE_FILE])
        if not is_success:
            return False

        for i in range(Docker.CHECK_COUNT):
            time.sleep(1)
            if Docker.is_running():
                return True
        else:
            return False

    @staticmethod
    def stop():
        is_success, _ = Cmd.run(['pkill', 'Docker'])
        # is_success, _ = Cmd.run(['taskkill', '/IM', 'Docker Desktop.exe', '/F'])
        if not is_success:
            return False

        for i in range(Docker.CHECK_COUNT):
            time.sleep(1)
            if not Docker.is_running():
                return True
        else:
            return False

    @staticmethod
    def is_running() -> bool:
        is_success, _ = Cmd.run(['docker', 'ps'])
        return is_success

    @staticmethod
    def is_exist_exe() -> bool:
        return Path(Docker.EXE_FILE).exists()

    @staticmethod
    def get_version() -> str:
        _, version = Cmd.run(['docker', 'version', '--format', '{{.Client.Version}}'])
        return version

    @staticmethod
    def get_docker_compose_version() -> str:
        _, version = Cmd.run(["docker", "compose", "version", "--short"])
        return version


if __name__ == '__main__':

    # 创建 QApplication 实例
    app = QApplication(sys.argv)

    # 创建主窗口实例
    window = MainWindow()

    # 显示主窗口
    window.show()

    # 运行应用程序的事件循环
    sys.exit(app.exec_())
