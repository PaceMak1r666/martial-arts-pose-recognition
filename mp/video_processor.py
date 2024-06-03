from datetime import datetime

import os
import sys

import traceback



current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在目录的绝对路径
parent_dir = os.path.dirname(current_dir)  # 获取父目录的绝对路径
sys.path.append(parent_dir)  # 添加父目录到Python解释器的搜索路径中

import cv2
import mediapipe as mp

from PyQt5.QtGui import QImage
from PyQt5.QtCore import  pyqtSignal, QThread

from mp.rules_1 import load_json_to_dict
from mp.score_calculation import calculate_score
from mp.angle_calculation import calculate_angle,angle_if
from mp.data_processing import calculate_frame_score, extract_landmark_info
class VideoProcessor(QThread):
    frame_processed = pyqtSignal(QImage)
    progress_updated = pyqtSignal(int)
    recognition_finished = pyqtSignal()
    landmarks_processed = pyqtSignal(list)  # 新增一个发送landmarks_data的信号
    action_recognition_info = pyqtSignal(str)
    score_calculated = pyqtSignal(list, list)  # 传递best_frame_ids和best_frame_scores

    def __init__(self, video_path, show_skeleton=False, model_complexity=1, rules_path=None, save_frames=False):  
        super().__init__()
        self.video_path = video_path
        self.total_frames = 0
        self.processed_frames = 0
        self.paused = False
        self.landmarks_data = []  # 初始化landmarks_data为空列表
        self.best_frame_ids = []
        self.best_frame_scores = []
        self.model_complexity = model_complexity  # 保存模型复杂度参数
        self.show_skeleton = show_skeleton  # 保存是否显示骨架可视化的状态
        self.start_time = None  # 记录开始识别时间
        self.end_time = None  # 记录结束识别时间
        self.rules_path = rules_path  # 规则库路径
        self.save_frames = save_frames  # 保存帧图片的标志
        if self.save_frames:
            self.save_path = os.path.join(os.getcwd(), f"frames_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")  # 使用当前工作目录下的带有时间戳的 frames 文件夹作为保存路径
            # 确保保存路径存在，如果不存在则创建
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)


    def run(self):
        try:
            self.start_time = datetime.now()  # 记录开始识别时间
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                info = "Error: Unable to open video file."
                self.action_recognition_info.emit(info)

            mp_pose = mp.solutions.pose.Pose(
                static_image_mode=False,
                model_complexity=self.model_complexity,
                smooth_landmarks=True,
                enable_segmentation=False,
                smooth_segmentation=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )

            self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_count = 0

            while cap.isOpened() and not self.paused:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = mp_pose.process(rgb_frame)
    

                if results.pose_landmarks:
                    landmarks_info = {'frame_number': frame_count, 'landmarks': []}
                    if self.show_skeleton:  # 如果需要显示骨架
                        mp.solutions.drawing_utils.draw_landmarks(
                            frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                    for landmark_id, landmark in enumerate(results.pose_landmarks.landmark):
                        x, y, z, visibility = extract_landmark_info(landmark)
                        landmark_info = {
                            'landmark_id': landmark_id,
                            'x': x,
                            'y': y,
                            'z': z,
                            'visibility': visibility
                        }
                        landmarks_info['landmarks'].append(landmark_info)
                        # Print landmark info
                        info = f"Frame {frame_count}, Landmark {landmark_id}: x={x}, y={y}, z={z}, visibility={visibility}"
                        self.action_recognition_info.emit(info)  # 发射动作识别信息
                        print(info)

                    self.landmarks_data.append(landmarks_info)
                if self.save_frames:
                    # 保存帧图片
                    frame_path = os.path.join(self.save_path, f"frame_{frame_count}.jpg")
                    cv2.imwrite(frame_path, frame)

                qimage = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.frame_processed.emit(qimage)
                self.processed_frames += 1
                progress = int((self.processed_frames / self.total_frames) * 100)
                self.progress_updated.emit(progress)

                # Print frame processing info
                processing_info = f"-------------------------\nFrame {frame_count} processing completed."
                self.action_recognition_info.emit(processing_info)  # 发射帧处理信息
                print(processing_info)

                frame_count += 1

            cap.release()
            self.end_time = datetime.now()  # 记录结束识别时间
            elapsed_time = self.end_time - self.start_time
            elapsed_time_str = f"Total elapsed time: {elapsed_time}"
            self.action_recognition_info.emit(elapsed_time_str)  # 发送总时间信息

            self.recognition_finished.emit()  # 发出识别完成的信号
            self.landmarks_processed.emit(self.landmarks_data)  # 发出landmarks_data的信号

            if self.rules_path:  # 如果提供了规则库路径
                require_list = load_json_to_dict(self.rules_path)  # 加载规则库
                self.best_frame_ids, self.best_frame_scores = self.process_landmarks_with_require_list(self.landmarks_data, require_list)
                if self.best_frame_ids and self.best_frame_scores:  # 如果最佳帧不是空的
                    score_info = "The Best frame IDs: " + ", ".join(map(str, self.best_frame_ids))
                else:
                    score_info = "The Best frame IDs: None"
                self.action_recognition_info.emit(score_info)  # 发射评分信息
                self.score_calculated.emit(self.best_frame_ids, self.best_frame_scores)
            else:
                self.process_landmarks(self.landmarks_data)

        

            

            del self.landmarks_data
        except Exception as e:
            info = f"处理过程中发生错误: {str(e)}"
            traceback_str = traceback.format_exc()  # 获取完整的错误回溯信息
            self.action_recognition_info.emit(info)
            self.action_recognition_info.emit(traceback_str)  # 发送完整的错误回溯信息以供调试
            
    def process_landmarks_with_require_list(self, landmarks_data, require_list):
        """
        处理标记数据并根据指定的动作规则列表进行评分，找到每个动作的最佳帧。

        参数:
        landmarks_data: list of dict
            包含每帧动作数据的列表，每个元素是一个字典，包含帧号和关节点坐标。
        require_list: list of dict
            每个字典包含动作规则，指定了各个关节点的角度要求。

        返回:
        best_frame_ids: list of int
            每个动作的最佳帧号列表。
        best_frame_scores_after: list of float
            每个动作最佳帧的得分列表。
        """

        best_frame_scores = []
        best_frame_scores_after = []
        best_frame_ids = []
        all_frame_scores = []

        try:
            # 初始化最低分数阈值
            min_score_threshold = 85  # 可根据实际情况调整
            # 初始化最大未找到最佳帧的动作数
            max_unscored_actions = 2  # 可根据实际情况调整
            unscored_actions = 0  # 未找到最佳帧的动作数
            scoring_possible = True

            # 遍历每一个动作规则
            for idx, required in enumerate(require_list):
                max_score = 0
                max_id = 0
                frame_scores = []

                # 遍历每一帧的数据
                for frame_info in landmarks_data:
                    frame_number = frame_info['frame_number']
                    landmarks = frame_info['landmarks']
                    joint_scores = []
                    angle_condition_unsatisfied = 0

                    # 关节点的坐标（假设已经按顺序提供）
                    shoulder_left = landmarks[11]
                    shoulder_right = landmarks[12]
                    hip_left = landmarks[23]
                    hip_right = landmarks[24]
                    elbow_left = landmarks[13]
                    elbow_right = landmarks[14]
                    knee_left = landmarks[25]
                    knee_right = landmarks[26]
                    ankle_left = landmarks[27]
                    ankle_right = landmarks[28]
                    wrist_left = landmarks[15]
                    wrist_right = landmarks[16]
                    total_score = 0

                    # 根据规则计算各个关节点的角度得分
                    for key, value in required.items():
                        if key == 'shoulder_left_angle':
                            score_shoulder_left = calculate_score(
                                calculate_angle(elbow_left, shoulder_left, hip_left),
                                elbow_left, shoulder_left, hip_left,
                                text='Shoulder Left', required=value
                            )
                            angle_result, angle_value = angle_if(elbow_left, shoulder_left, hip_left, text='Shoulder Left', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_shoulder_left
                            joint_scores.append(score_shoulder_left)
                        elif key == 'shoulder_right_angle':
                            score_shoulder_right = calculate_score(
                                calculate_angle(elbow_right, shoulder_right, hip_right),
                                elbow_right, shoulder_right, hip_right,
                                text='Shoulder Right', required=value
                            )
                            angle_result, angle_value = angle_if(elbow_right, shoulder_right, hip_right, text='Shoulder Right', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_shoulder_right
                            joint_scores.append(score_shoulder_right)
                        elif key == 'hip_left_angle':
                            score_hip_left = calculate_score(
                                calculate_angle(hip_right, hip_left, knee_left),
                                hip_right, hip_left, knee_left,
                                text='Hip Left', required=value
                            )
                            angle_result, angle_value = angle_if(hip_right, hip_left, knee_left, text='Hip Left', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_hip_left
                            joint_scores.append(score_hip_left)
                        elif key == 'hip_right_angle':
                            score_hip_right = calculate_score(
                                calculate_angle(hip_left, hip_right, knee_right),
                                hip_left, hip_right, knee_right,
                                text='Hip Right', required=value
                            )
                            angle_result, angle_value = angle_if(hip_left, hip_right, knee_right, text='Hip Right', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_hip_right
                            joint_scores.append(score_hip_right)
                        elif key == 'arm_left_angle':
                            score_arm_left = calculate_score(
                                calculate_angle(shoulder_left, elbow_left, wrist_left),
                                shoulder_left, elbow_left, wrist_left,
                                text='Arm Left', required=value
                            )
                            angle_result, angle_value = angle_if(shoulder_left, elbow_left, wrist_left, text='Arm Left', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_arm_left
                            joint_scores.append(score_arm_left)
                        elif key == 'arm_right_angle':
                            score_arm_right = calculate_score(
                                calculate_angle(shoulder_right, elbow_right, wrist_right),
                                shoulder_right, elbow_right, wrist_right,
                                text='Arm Right', required=value
                            )
                            angle_result, angle_value = angle_if(shoulder_right, elbow_right, wrist_right, text='Arm Right', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_arm_right
                            joint_scores.append(score_arm_right)
                        elif key == 'leg_left_angle':
                            score_leg_left = calculate_score(
                                calculate_angle(ankle_left, knee_left, hip_left),
                                ankle_left, knee_left, hip_left,
                                text='Leg Left', required=value
                            )
                            angle_result, angle_value = angle_if(ankle_left, knee_left, hip_left, text='Leg Left', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_leg_left
                            joint_scores.append(score_leg_left)
                        elif key == 'leg_right_angle':
                            score_leg_right = calculate_score(
                                calculate_angle(ankle_right, knee_right, hip_right),
                                ankle_right, knee_right, hip_right,
                                text='Leg Right', required=value
                            )
                            angle_result, angle_value = angle_if(ankle_right, knee_right, hip_right, text='Leg Right', required=value)
                            if not angle_result:
                                angle_condition_unsatisfied += 1
                            total_score += score_leg_right
                            joint_scores.append(score_leg_right)

                    # 添加当前帧的总得分
                    frame_scores.append(total_score)

                    # 检查当前帧是否为当前动作的最佳帧
                    if total_score > max_score and angle_condition_unsatisfied < 2:
                        if not best_frame_ids or best_frame_ids[-1] < frame_number:
                            max_score = total_score
                            max_id = frame_number
                            max_score_after = calculate_frame_score(joint_scores)
                            print("Current frame total score:", total_score)
                            print("Joint scores:", joint_scores)
                            print("Max score after:", max_score_after)

                # 如果找到最佳帧，记录其信息
                if max_id > 0:
                    best_frame_scores.append(max_score)
                    best_frame_scores_after.append(max_score_after)
                    best_frame_ids.append(max_id)
                    all_frame_scores.append(frame_scores)
                else:  # 如果未找到最佳帧，发送提示信息
                    info = f"在第 {idx + 1} 个动作规则中未找到最佳帧"
                    self.action_recognition_info.emit(info)
                    unscored_actions += 1

                if not scoring_possible:
                    break  # 如果无法评分，直接退出循环

            # 如果所有帧的得分都低于最低分数阈值，则认为视频无法评分
            if all(score < min_score_threshold for score in best_frame_scores_after):
                info = f"所有的帧得分都低于 {min_score_threshold}, 认为该视频无法评分"
                self.action_recognition_info.emit(info)
                scoring_possible = False

            # 如果低分帧的数量超过阈值，则认为视频无效
            low_score_count = sum(score < min_score_threshold for score in best_frame_scores_after)
            if low_score_count >= 2:
                info = f"最佳动作帧中的低分帧有 {low_score_count} 个，认为该视频无效"
                self.action_recognition_info.emit(info)
                scoring_possible = False

            # 如果对于太多的动作都找不到最佳帧，则判定无法评分
            if unscored_actions >= max_unscored_actions:
                info = f"超过 {max_unscored_actions} 个动作找不到最佳帧，无法评分"
                self.action_recognition_info.emit(info)
                scoring_possible = False

            if not scoring_possible:
                return [], []

            # 发送每个动作的最佳帧信息
            for max_id, max_score, max_score_after in zip(best_frame_ids, best_frame_scores, best_frame_scores_after):
                info = f"Best frame: {max_id}, Max score: {max_score}, Max score after: {max_score_after}"
                self.action_recognition_info.emit(info)

            # 计算并发送所有最佳帧得分的平均值
            average_score = sum(best_frame_scores_after) / len(best_frame_scores_after)
            info = f"TotalScore = {average_score}"
            self.action_recognition_info.emit(info)

            return best_frame_ids, best_frame_scores_after

        except Exception as e:
            info = "An error occurred during processing: " + str(e)
            self.action_recognition_info.emit(info)

    def process_landmarks(self, landmarks_data):
        try:
            for frame_info in landmarks_data:
                frame_number = frame_info['frame_number']
                info = f"第{frame_number}帧------------------------------------------"
                self.action_recognition_info.emit(info)
                landmarks = frame_info['landmarks']
                frame_angles = {}

                # 定义需要计算角度的关键点
                shoulder_left = landmarks[11]
                shoulder_right = landmarks[12]
                hip_left = landmarks[23]
                hip_right = landmarks[24]
                elbow_left = landmarks[13]
                elbow_right = landmarks[14]
                knee_left = landmarks[25]
                knee_right = landmarks[26]
                ankle_left = landmarks[27]
                ankle_right = landmarks[28]
                wrist_left = landmarks[15]
                wrist_right = landmarks[16]

                # 计算并记录各个角度
                frame_angles['shoulder_left_angle'] = calculate_angle(elbow_left, shoulder_left, hip_left)
                frame_angles['shoulder_right_angle'] = calculate_angle(elbow_right, shoulder_right, hip_right)
                frame_angles['hip_left_angle'] = calculate_angle(hip_right, hip_left, knee_left)
                frame_angles['hip_right_angle'] = calculate_angle(hip_left, hip_right, knee_right)
                frame_angles['arm_left_angle'] = calculate_angle(shoulder_left, elbow_left, wrist_left)
                frame_angles['arm_right_angle'] = calculate_angle(shoulder_right, elbow_right, wrist_right)
                frame_angles['leg_left_angle'] = calculate_angle(ankle_left, knee_left, hip_left)
                frame_angles['leg_right_angle'] = calculate_angle(ankle_right, knee_right, hip_right)

                # 输出每个角度的信息
                for key, value in frame_angles.items():
                    info = f"{key}={value}"
                    self.action_recognition_info.emit(info)
                
            self.action_recognition_info.emit("识别完成！")
        except Exception as e:
            info = "An error occurred during processing: " + str(e)
            self.action_recognition_info.emit(info)