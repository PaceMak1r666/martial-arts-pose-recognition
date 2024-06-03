from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
import json
import os
import sys



current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
parent_dir = os.path.dirname(current_dir)  # 获取父目录的绝对路径
sys.path.append(parent_dir)  # 添加父目录到Python解释器的搜索路径中
from mp.video_processor import VideoProcessor
import cv2

from PyQt5.QtWidgets import  QMainWindow, QFileDialog, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer, QDateTime

from Ui_main import Ui_MainWindow as Ui_MainWindow_main


class MyMainWindowMain(QMainWindow, Ui_MainWindow_main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.video_processor = None
        self.action_recognition_running = False  # 动作识别运行状态
        self.pushButton_5.setEnabled(True)  # 初始化按钮可用
        self.landmarks_data = None  # 初始化 landmarks_data
        self.best_frame_ids = None  # 初始化 best_frame_ids
        self.rule_file=None
        self.best_frame_scores=None
        self.label_13.setVisible(False)
        self.label_14.setVisible(False)
        self.pushButton_9.setEnabled(False)  # 初始状态设为不可用
 
        self.save_frames=False
        self.save_log = False  # 初始化保存日志的状态
        
        # 其他初始化代码...
        self.show_skeleton = False  # 初始化为不显示骨架

        # 绑定复选框状态变化事件

        # 绑定按钮点击事件
        self.pushButton_6.pressed.connect(self.load_video)  # 点击按钮加载视频
        self.pushButton_8.pressed.connect(self.play_pause_video)  # 点击按钮播放/暂停视频
        self.horizontalSlider.sliderPressed.connect(self.slider_pressed)  # 滑块按下事件
        self.horizontalSlider.sliderReleased.connect(self.slider_released)  # 滑块释放事件
        self.pushButton_5.pressed.connect(self.start_action_recognition)  # 点击按钮开始动作识别
        self.checkBox_3.stateChanged.connect(self.toggle_skeleton_visualization) # 绑定复选框状态变化事件
        self.checkBox.stateChanged.connect(self.toggle_logging) # 绑定复选框状态变化事件
        self.pushButton_9.pressed.connect(self.show_best_frames_dialog)
        self.pushButton_7.pressed.connect(self.load_rules)  # 绑定按钮点击事件
          # 绑定复选框状态变化事件
        self.checkBox_2.stateChanged.connect(self.toggle_save_frames)

        # 初始化保存帧图片的标志
        self.save_frames = False

        self.radioButton.setChecked(True)

        
    
        self.progressBar_2.setValue(0)  # 初始化进度条值为0

        self.video_timer = QTimer(self)  # 创建视频更新定时器
        self.video_timer.timeout.connect(self.update_video_frame)  # 定时器触发更新视频帧

        self.cap = None  # 视频捕捉对象
        self.playing = False  # 视频播放状态标志
        self.slider_pressed_flag = False  # 滑块按下标志

        self.time_timer = QTimer(self)  # 创建时间更新定时器
        self.time_timer.timeout.connect(self.update_time)  # 定时器触发更新时间
        self.time_timer.start(1000)  # 每秒更新一次时间

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
    
    def play_pause_video(self):
        """播放/暂停视频"""
        if self.cap is not None:
            if not self.playing:
                self.video_timer.start(33)  # 设置视频帧更新间隔
                self.playing = True
                self.label_13.setVisible(True)  # 播放时显示label_13
                self.label_6.setVisible(False)  # 播放时隐藏label_6
                
             

                
            else:
                self.video_timer.stop()  # 停止定时器
                self.playing = False
                self.label_13.setVisible(False)  # 播放时显示label_13
                self.label_6.setVisible(True)  # 播放时隐藏label_6

    def slider_pressed(self):
        """滑块按下事件"""
        self.slider_pressed_flag = True

    def slider_released(self):
        """滑块释放事件"""
        if self.cap is not None:
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            target_frame = int(self.horizontalSlider.value() * total_frames / 100)
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)  # 设置视频位置
            self.update_video_frame()
            if self.playing:
                self.video_timer.start(33)  # 继续播放

            # 更新滑块位置
            self.slider_pressed_flag = False  # 重置滑块按下标志
            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.horizontalSlider.setValue(int(current_frame / total_frames * 100))

    def load_video(self):
        """加载视频文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi)")
        if file_path:
            self.cap = cv2.VideoCapture(file_path)
            self.horizontalSlider.setMaximum(100)
            self.horizontalSlider.setValue(0)
            ret, frame = self.cap.read()
            self.update_text_browser(f"成功载入视频，当前载入视频为{os.path.basename(file_path)}")
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio))  # 保持原始比例
                self.pushButton_6.setText(os.path.basename(file_path))  # 设置按钮文本为文件名
                self.video_path = file_path  # 将文件路径保存在实例变量中


    def load_rules(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择规则库文件", "", "JSON 文件 (*.json)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    rules_data = json.load(file)
                
                # 验证 JSON 数据是否符合要求
                if self.validate_rules(rules_data):
                    self.rule_file = file_path
                    self.pushButton_7.setText(os.path.basename(file_path))
                    self.update_text_browser(f"成功配置规则！您要识别的武术项目是：{os.path.basename(file_path)}")
                else:
                    raise ValueError("规则文件格式不正确")

            except (json.JSONDecodeError, ValueError) as e:
                QMessageBox.critical(self, "Error", f"Error loading rules: {str(e)}")
                self.update_text_browser(f"加载规则文件失败：{str(e)}")

    def validate_rules(self, rules_data):
        """
        验证规则数据是否符合要求
        :param rules_data: 从 JSON 文件加载的规则数据
        :return: bool 表示规则数据是否有效
        """
        if not isinstance(rules_data, list):
            self.update_text_browser("rules_data 不是列表")
            return False
        
        for index, rule in enumerate(rules_data):
            if not isinstance(rule, dict):
                self.update_text_browser(f"规则 {index} 不是字典: {rule}")
                return False
            
            for key, value in rule.items():
                if not isinstance(value, list) or len(value) != 2:
                    self.update_text_browser(f"规则 {index} 中的键 '{key}' 对应的值不是长度为2的列表: {value}")
                    return False
                # 检查列表的第一个元素是否是数字，第二个元素是否是整数
                if not isinstance(value[0], (int, float)):
                    self.update_text_browser(f"规则 {index} 中的键 '{key}' 的第一个值不是数字: {value[0]}")
                    return False
                if not isinstance(value[1], int):
                    self.update_text_browser(f"规则 {index} 中的键 '{key}' 的第二个值不是整数: {value[1]}")
                    return False

        return True





    def update_video_frame(self):
        """更新视频帧"""
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                qimage = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimage)
                self.label_3.setPixmap(pixmap.scaled(self.label_3.size(), Qt.KeepAspectRatio))  # 保持原始比例
                if not self.slider_pressed_flag:
                    current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    self.horizontalSlider.setValue(int(current_frame / total_frames * 100))
            else:
            # 视频播放结束
                self.video_timer.stop()  # 停止定时器
                self.playing = False
                self.label_13.setVisible(False)  # 隐藏播放图标
                self.label_6.setVisible(True)  # 显示暂停图标
                print("视频播放结束了")
    def start_action_recognition(self):
        """开始动作识别"""
        try:
            if self.cap is not None and not self.action_recognition_running:
                if not self.rule_file:  # 检查是否加载了规则库文件
                    # 如果没有加载规则库文件，弹出对话框询问用户是否继续
                    reply = QMessageBox.question(self, 'No Rule File', 
                                                "当前没有选择规则库文件，确定要继续吗？", 
                                                QMessageBox.Yes | QMessageBox.No, 
                                                QMessageBox.No)
                    self.update_text_browser("用户没有选择规则库，不打分，只识别")
                    if reply == QMessageBox.No:
                        return  # 如果用户选择不继续，则直接返回

            if self.cap is not None and not self.action_recognition_running:
                # 禁用按钮并修改样式
                self.pushButton_5.setEnabled(False)
                self.pushButton_9.setEnabled(False)  # 初始状态设为不可用
                self.pushButton_6.setEnabled(False)  # 初始状态设为不可用
                self.pushButton_7.setEnabled(False)  # 初始状态设为不可用
                self.pushButton_5.setStyleSheet("""
                    QPushButton:disabled {  /* 添加禁用状态样式 */
                        color: rgb(255, 255, 255);
                        background-color: #b9b9b9;
                        alternate-background-color: rgb(212, 38, 255);
                        gridline-color: rgb(255, 249, 235);
                        border-radius: 8px;
                        border: 2px solid;
                    }
                """) 
                self.radioButton.setEnabled(False)  # 禁用 radioButton
                self.radioButton_2.setEnabled(False)  # 禁用 radioButton_2
                self.label_9.setVisible(False)
                self.label_14.setVisible(True)
                self.checkBox.setEnabled(False)
                self.checkBox_2.setEnabled(False)
                
                # 获取用户选择的模型复杂度
                model_complexity = 1 if self.radioButton.isChecked() else 2

                # 创建视频处理线程，传递模型复杂度参数
                self.video_processor = VideoProcessor(self.video_path, self.show_skeleton, model_complexity, self.rule_file, self.save_frames)
                self.video_processor.frame_processed.connect(self.update_label_4)
                self.video_processor.progress_updated.connect(self.update_progress_bar)
                self.video_processor.action_recognition_info.connect(self.update_text_browser)
                self.video_processor.recognition_finished.connect(self.action_recognition_finished)  # 连接识别完成的信号
                self.video_processor.score_calculated.connect(self.handle_score)  # 连接评分结果的信号
                # self.video_processor.landmarks_processed.connect(self.process_landmarks_data)  # 连接landmarks_data的信号
                current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                formatted_info = f"{current_datetime}"  # 添加日期时间信息
                self.update_text_browser(formatted_info)  # 将带有日期时间的信息添加到 textBrowser

                # 添加用户配置信息到文本框
                self.update_text_browser(f"视频路径：{self.video_path}")
                self.update_text_browser(f"规则库文件：{self.rule_file}")
                self.update_text_browser(f"选择的模型：{'Full(快)' if model_complexity == 1 else 'Heavy(慢)'}")
                self.update_text_browser(f"是否保存日志：{'是' if self.save_log else '否'}")
                self.update_text_browser(f"是否保存图片：{'是' if self.save_frames else '否'}")

                self.video_processor.start()
                self.action_recognition_running = True
                
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"发生错误: {str(e)}")
            self.update_text_browser(f"发生错误: {str(e)}")
            # 恢复按钮和控件状态
            self.pushButton_5.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
            self.radioButton.setEnabled(True)
            self.radioButton_2.setEnabled(True)
            self.label_9.setVisible(True)
            self.label_14.setVisible(False)
            self.checkBox.setEnabled(True)
            self.checkBox_2.setEnabled(True)
            self.action_recognition_running = False


    def action_recognition_finished(self):
        """动作识别完成后恢复按钮状态并进行评分"""
    
        self.pushButton_5.setEnabled(True)  # 恢复按钮状态
        self.pushButton_6.setEnabled(True)  # 初始状态设为不可用
        self.pushButton_7.setEnabled(True)  # 初始状态设为不可用
        self.checkBox_2.setEnabled(True)
        
        
        self.checkBox.setEnabled(True)
        self.label_9.setVisible(True)
        self.label_14.setVisible(False)
        self.radioButton.setEnabled(True)  # 恢复 radioButton
        self.radioButton_2.setEnabled(True)  # 恢复 radioButton_2
        self.pushButton_5.setStyleSheet("""
            QPushButton {
                color: rgb(255, 255, 255);
                background-color: rgb(0, 0, 0);
                alternate-background-color: rgb(212, 38, 255);
                gridline-color: rgb(255, 249, 235);
                border-radius: 8px;
                border:2px solid;
            }
            QPushButton:hover{
                background-color:#d5d5d5;/* 设置按钮被点击时的背景颜色 */
                padding:2px;
            }
            QPushButton:pressed {
                background-color: #a7a7a7; /* 设置按钮被点击时的背景颜色 */
            }
            QPushButton:disabled {  /* 添加禁用状态样式 */
                color: rgb(255, 255, 255);
                background-color: #b9b9b9;
                alternate-background-color: rgb(212, 38, 255);
                gridline-color: rgb(255, 249, 235);
                border-radius: 8px;
                border: 2px solid;
            }
        """)
    
        self.action_recognition_running = False
     
    def show_best_frames(self, best_frame_ids, best_frame_scores):
        try:
            if len(best_frame_ids) == 0:
                # 如果没有最佳帧可供显示，显示一条消息给用户
                QMessageBox.information(self, "No Best Frames", "No best frames available for display.")
                return

            if self.cap is not None:
                dialog = BestFramesDialog(self)
                row, col = 0, 0
                for frame_id, score in zip(best_frame_ids, best_frame_scores):
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)
                    ret, frame = self.cap.read()
                    if ret:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                        dialog.add_frame(qimage, score, row, col)  # 将分数传递给add_frame方法
                        col += 1
                        if col == 3:
                            col = 0
                            row += 2  # 增加2以留出分数标签的空间
                dialog.exec_()
        except Exception as e:
            print("显示最佳帧时发生错误:", e)

    def show_best_frames_dialog(self):
        if self.best_frame_ids:  # 如果有最佳帧
            self.show_best_frames(self.best_frame_ids, self.best_frame_scores)
        else:
            self.show_best_frames([], [])  # 没有最佳帧，传递 None 给处理函数
            
    def handle_score(self, best_frame_ids, best_frame_scores):
        self.best_frame_ids = best_frame_ids
        self.best_frame_scores = best_frame_scores
        print("Received best frame IDs:", best_frame_ids)
        print("Received best frame scores:", best_frame_scores)
        self.pushButton_9.setEnabled(True)  # 恢复按钮状态
        print(111111111111111111111111111111111111111111111111111111)


        # 保存日志
        if self.save_log:
            print(22222222222222222222222)
            self.update_text_browser("成功保存日志！")

            self.save_log_info()

        # 其他处理...
    def toggle_logging(self, state):
        """根据复选框状态切换是否保存日志"""
        if state == Qt.Checked:  # 复选框被选中
            self.save_log = True
        else:
            self.save_log = False

    def toggle_save_frames(self, state):
        """切换保存帧图片的标志"""
        if state == Qt.Checked:
            self.save_frames = True
        else:
            self.save_frames = False
    def toggle_skeleton_visualization(self, state):
            """根据复选框状态切换骨架可视化"""
            if state == Qt.Checked:  # 复选框被选中
                self.show_skeleton = True
            else:
                self.show_skeleton = False

            # 更新label_4中的图像
            if self.video_processor is not None:
                self.video_processor.show_skeleton = self.show_skeleton  # 传递给视频处理线程
    def update_label_4(self, qimage):
        """更新label_4中的图像"""
        pixmap = QPixmap.fromImage(qimage)
        self.label_4.setPixmap(pixmap.scaled(self.label_4.size(), Qt.KeepAspectRatio))
    def update_text_browser(self, info):
        """更新textBrowser中的动作识别信息"""
        self.textBrowser.append(info)
    def save_log_info(self):
        """保存日志信息"""
        try:
            # ... 现有的保存日志的代码 ...
            """保存日志信息"""
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # 获取当前日期和时间并格式化
            log_file_name = f"action_recognition_log_{current_datetime}.txt"  # 拼接文件名
            log_file_path = os.path.join(os.getcwd(), log_file_name)  # 构建文件路径

            with open(log_file_path, "a") as f:
                f.write(f"Date and Time: {current_datetime}\n")  # 写入当前日期和时间
                f.write(self.textBrowser.toPlainText())  # 保存 textBrowser 中的文本
                f.write("\n\n")

        except Exception as e:
            print(f"Error occurred while saving log: {e}")
            # 考虑将错误信息写入一个全局的临时日志文件

    def update_progress_bar(self, progress):
        """更新进度条"""
        self.progressBar_2.setValue(progress)
    def update_time(self):
        """更新时间"""
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
        self.label_2.setText(current_time)

    def closeEvent(self, event):
        """窗口关闭事件"""
        if self.cap is not None:
            self.cap.release()  # 释放视频对象
        event.accept()



class BestFramesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("最佳帧")
        self.layout = QGridLayout()
        self.setLayout(self.layout)

    def add_frame(self, frame, score, row, col):
        label = QLabel()
        pixmap = QPixmap.fromImage(frame)
        scaled_pixmap = pixmap.scaled(400, 400, aspectRatioMode=Qt.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        self.layout.addWidget(label, row, col)

        score_label = QLabel(f"<font size='4'>分数: {score}</font>")  # 创建用于显示分数的标签
        score_label.setAlignment(Qt.AlignCenter)  # 设置文本居中对齐
        self.layout.addWidget(score_label, row + 1, col)  # 将分数标签添加在帧下方