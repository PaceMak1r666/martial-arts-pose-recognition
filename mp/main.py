import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
parent_dir = os.path.dirname(current_dir)  # 获取父目录的绝对路径
sys.path.append(parent_dir)  # 添加父目录到Python解释器的搜索路径中
from mp.main_window import MyMainWindowMain
from mp.login_window import MyLoginWindow
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    # 创建并显示登录窗口
    # LoginWindow = MyLoginWindow()
    # LoginWindow.show()
    # 创建并显示主界面窗口
    MainWindow = MyMainWindowMain()
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()