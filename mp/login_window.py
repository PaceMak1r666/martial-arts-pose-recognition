
import os
import sys







current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
parent_dir = os.path.dirname(current_dir)  # 获取父目录的绝对路径
sys.path.append(parent_dir)  # 添加父目录到Python解释器的搜索路径中
from mp.main_window import MyMainWindowMain
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
from Ui_login import Ui_MainWindow  # 导入登录界面UI





# 导入主界面UI

class MyLoginWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.m_flag = False  # 拖动窗口标志
        self.m_Position = None  # 拖动位置
        self.label_6.hide()  # 隐藏错误提示标签
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        
        # 绑定登录按钮的点击事件
        self.pushButton.clicked.connect(self.login)
        
        # 创建定时器
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)  # 单次触发
        
        # 将定时器的timeout信号连接到hide_label槽函数
        self.timer.timeout.connect(self.hide_label)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.isMaximized():
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(Qt.OpenHandCursor)  # 更改鼠标图标
            
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:
            self.move(event.globalPos() - self.m_Position)  # 更改窗口位置
            event.accept()
    
    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(Qt.ArrowCursor)
        
    def login(self):
        # 获取输入的用户名和密码
        username = self.account.text().strip()
        password = self.lineEdit_2.text().strip()
        
        # 输入验证
        if not username or not password:
            self.display_error("用户名或密码不能为空")
            return
        
        # 这里假设用户名为 "admin"，密码为哈希值 "123456"
        if username == "admin" and self.hash_password(password) == self.hash_password("123456"):
            # 登录成功，关闭登录窗口
            self.close()
            # 打开主界面
            self.open_main_window()
        else:
            self.display_error("用户名或密码错误")
            
    def hash_password(self, password):
        # 使用 hashlib 模块进行密码散列
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()
    
    def display_error(self, message):
        self.label_6.setText(message)  # 设置错误信息
        self.label_6.show()  # 显示错误提示
        # 启动定时器，设置1.5秒后隐藏label_6
        self.timer.start(1500)
            
    def open_main_window(self):
        self.main_window = MyMainWindowMain()  # 创建主界面窗口
        self.main_window.show()

    def hide_label(self):
        self.label_6.hide()  # 隐藏错误提示标签
