import os
import cv2
import mediapipe as mp
import numpy as np
import json
import time

from test_1.mp.angle_calculation import angle_if, calculate_angle
from test_1.mp.data_processing import calculate_frame_score, extract_landmark_info
from test_1.mp.score_calculation import calculate_score
from display_gui import visualize_frame_scores
from test_1.mp.rules_1 import load_required_list

require_list = load_required_list()

# 指定视频文件路径
video_path = 'D:/openpose/examples/media/test.mp4'

# 创建保存帧的文件夹
frames_folder = 'frames'
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# 使用 OpenCV 的 VideoCapture 加载输入视频
cap = cv2.VideoCapture(video_path)

# 创建一个姿势估计器实例
mp_pose = mp.solutions.pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    enable_segmentation=False,
    smooth_segmentation=True,
    min_detection_confidence=0.1,
    min_tracking_confidence=0.5
)

# 循环读取视频的每一帧并处理
frame_count = 0
landmarks_data = []
start_time = time.time()
fps = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 计算帧率
    end_time = time.time()
    time_diff = end_time - start_time
    fps = 1 / time_diff
    start_time = end_time

    # 将 BGR 格式的帧转换为 RGB 格式
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 检测姿势并获取结果
    results = mp_pose.process(rgb_frame)

    if results.pose_landmarks:
        landmarks_info = {}
        landmarks_info['frame_number'] = frame_count
        landmarks_info['landmarks'] = []
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

        landmarks_data.append(landmarks_info)

        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

    # 在帧上显示 FPS
    cv2.putText(frame, f'FPS: {fps:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 显示处理后的帧
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# 将关键点信息保存到JSON文件中
with open('landmarks_info.json', 'w') as json_file:
    json.dump(landmarks_data, json_file, indent=4)

cap.release()
cv2.destroyAllWindows()

# 打开 JSON 文件
with open('landmarks_info.json', 'r') as json_file:
    landmarks_data = json.load(json_file)

best_frame_scores = []
best_frame_ids = []
all_frame_scores = []

for required in require_list:
    max_score = 0
    max_id = 0
    frame_scores = []
    for frame_info in landmarks_data:
        frame_number = frame_info['frame_number']
        landmarks = frame_info['landmarks']
        print(f"Processing frame {frame_number}...") 
        joint_scores = []
        angle_condition_unsatisfied = 0
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
        totalScore = 0

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
                totalScore += score_shoulder_left
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
                totalScore += score_shoulder_right
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
                totalScore += score_hip_left
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
                totalScore += score_hip_right
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
                totalScore += score_arm_left
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
                totalScore += score_arm_right
                joint_scores.append(score_arm_right)
            elif key == 'leg_left_angle':
                score_leg_left = calculate_score(
                    calculate_angle(ankle_left, knee_left, hip_left),
                    ankle_left, knee_left, hip_right,
                    text='Leg Left', required=value
                )
                angle_result, angle_value = angle_if(ankle_left, knee_left, hip_left, text='Leg Left', required=value)
                if not angle_result:
                    angle_condition_unsatisfied += 1
                totalScore += score_leg_left
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
                totalScore += score_leg_right
                joint_scores.append(score_leg_right)

        frame_scores.append(totalScore)
        totalScore_after = calculate_frame_score(joint_scores)
        print(f"frame_id:{frame_number} Score={totalScore} Score_after={totalScore_after}")
        if totalScore > max_score and angle_condition_unsatisfied <= 2:
            if not best_frame_ids or best_frame_ids[-1] < frame_number:
                max_score = totalScore
                max_id = frame_number
                max_score_after = totalScore_after

    best_frame_scores.append(max_score_after)
    best_frame_ids.append(max_id)
    all_frame_scores.append(frame_scores)

    print(f"best_frame:{max_id} max_score={max_score} max_score_after={max_score_after}")

average_score = sum(best_frame_scores) / len(best_frame_scores)
print(f"TotalScore={average_score}")

visualize_frame_scores(all_frame_scores)
