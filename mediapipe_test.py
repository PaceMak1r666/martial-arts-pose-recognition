import os
import cv2
import mediapipe as mp
import numpy as np

from rules import load_required_list

# 提取关键点信息
def extract_landmark_info(landmark_msg):
    x = landmark_msg.x
    y = landmark_msg.y
    z = landmark_msg.z
    visibility = landmark_msg.visibility
    return x, y, z, visibility


# 计算角度
def calculate_angle(joint1, joint2, joint3):
    """Calculate the angle between three joints in degrees."""
    # 计算两个关节点的向量
    vector1 = np.array([joint1.x, joint1.y, joint1.z])
    vector2 = np.array([joint2.x, joint2.y, joint2.z])
    vector3 = np.array([joint3.x, joint3.y, joint3.z])

    # 计算两个向量
    vector_a = vector1 - vector2
    vector_b = vector3 - vector2

    # 计算夹角的余弦值
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    cosine_angle = dot_product / (norm_a * norm_b)

    # 将余弦值转换为角度值
    angle_in_radians = np.arccos(cosine_angle)
    angle_in_degrees = np.degrees(angle_in_radians)

    return angle_in_degrees



# def calculate_angle(joint1, joint2, joint3):
#     """Calculate the angle between three joints in degrees."""
#     # 计算两个关节点的向量，只考虑 x 和 y 坐标
#     vector1 = np.array([joint1.x, joint1.y])
#     vector2 = np.array([joint2.x, joint2.y])
#     vector3 = np.array([joint3.x, joint3.y])

#     # 计算两个向量
#     vector_a = vector1 - vector2
#     vector_b = vector3 - vector2

#     # 计算夹角的余弦值
#     dot_product = np.dot(vector_a, vector_b)
#     norm_a = np.linalg.norm(vector_a)
#     norm_b = np.linalg.norm(vector_b)
#     cosine_angle = dot_product / (norm_a * norm_b)

#     # 将余弦值转换为角度值
#     angle_in_radians = np.arccos(cosine_angle)
#     angle_in_degrees = np.degrees(angle_in_radians)

#     return angle_in_degrees


require_list=load_required_list()
# 指定视频文件路径
video_path = 'D:/openpose/examples/media/test_1.mp4'

# 创建保存帧的文件夹
frames_folder = 'frames'
if not os.path.exists(frames_folder):
    os.makedirs(frames_folder)

# 使用 OpenCV 的 VideoCapture 加载输入视频
cap = cv2.VideoCapture(video_path)

# 检查视频是否成功打开
if not cap.isOpened():
    print("Error: Unable to open video file.")
    exit()

# 创建一个姿势估计器实例
mp_pose = mp.solutions.pose.Pose(
    static_image_mode=False,  # 是否将输入图像视为一批静态且可能不相关的图像，或者视频流
    model_complexity=1,  # 姿势估计模型的复杂度：0、1 或 2
    smooth_landmarks=True,  # 是否在不同输入图像之间过滤关键点，以减少抖动
    enable_segmentation=False,  # 是否预测分割蒙版
    smooth_segmentation=True,  # 是否在不同输入图像之间过滤分割，以减少抖动
    min_detection_confidence=0.5,  # 人物检测被视为成功的最小置信度值（[0.0, 1.0]）
    min_tracking_confidence=0.5  # 姿势关键点被视为成功跟踪的最小置信度值（[0.0, 1.0]）
)

# 循环读取视频的每一帧并处理
frame_count = 0
while cap.isOpened():
    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        break

    # 将 BGR 格式的帧转换为 RGB 格式
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 检测姿势并获取结果
    results = mp_pose.process(rgb_frame)

    # 如果检测到姿势，则输出关键点信息并进行可视化处理
    if results.pose_landmarks:
        print(f"Frame {frame_count} Landmarks:")  # 输出当前帧的关键点信息
        # for landmark_id, landmark in enumerate(results.pose_landmarks.landmark):
        #     print(f"Landmark {landmark_id}: ({landmark.x}, {landmark.y}, {landmark.z},{landmark.visibility})")
        #     # 输出关键点坐标及可见度信息
        # # 输出世界坐标系中的关键点信息
        # if results.pose_world_landmarks:
        #     print(f"Frame {frame_count} World Landmarks:")
        #     for landmark_id, landmark in enumerate(results.pose_world_landmarks.landmark):
        #         print(f"World Landmark {landmark_id}: ({landmark.x}, {landmark.y}, {landmark.z}, {landmark.visibility})")
        #         # 输出世界坐标系中的关键点坐标及可见度信息
        # print(results.pose_landmarks.landmark[12])
        # print(results.pose_landmarks.landmark[14])
        # print(results.pose_landmarks.landmark[16])
        # arm_right_angle=calculate_angle(results.pose_landmarks.landmark[12],results.pose_landmarks.landmark[14],results.pose_landmarks.landmark[16])
        # print("arm_right_angle=", arm_right_angle)
        # arm_left_angle=calculate_angle(results.pose_landmarks.landmark[11],results.pose_landmarks.landmark[13],results.pose_landmarks.landmark[15])
        # print("arm_left_angle=", arm_left_angle)
        # print("right_shoulder=",results.pose_world_landmarks.landmark[12])
        # print("right_elbow=",results.pose_world_landmarks.landmark[14])
        # print("right_wrist=",results.pose_world_landmarks.landmark[16])
       
        # print("left_shoulder=",results.pose_world_landmarks.landmark[11])
        # print("left_elbow=",results.pose_world_landmarks.landmark[13])
        # print("left_wrist=",results.pose_world_landmarks.landmark[15])
        shoulder_left_angle=calculate_angle(results.pose_world_landmarks.landmark[23],results.pose_world_landmarks.landmark[11],results.pose_world_landmarks.landmark[13])
        print("shoulder_left_angle=", shoulder_left_angle)
        shoulder_right_angle=calculate_angle(results.pose_world_landmarks.landmark[24],results.pose_world_landmarks.landmark[12],results.pose_world_landmarks.landmark[14])
        print("shoulder_right_angle=", shoulder_right_angle) 
        arm_right_angle=calculate_angle(results.pose_world_landmarks.landmark[12],results.pose_world_landmarks.landmark[14],results.pose_world_landmarks.landmark[16])
        print("arm_right_angle=", arm_right_angle)
        arm_left_angle=calculate_angle(results.pose_world_landmarks.landmark[11],results.pose_world_landmarks.landmark[13],results.pose_world_landmarks.landmark[15])
        print("arm_left_angle=", arm_left_angle)
        hip_left_angle=calculate_angle(results.pose_world_landmarks.landmark[25],results.pose_world_landmarks.landmark[23],results.pose_world_landmarks.landmark[24])
        print("hip_left_angle=", hip_left_angle)
        hip_right_angle=calculate_angle(results.pose_world_landmarks.landmark[26],results.pose_world_landmarks.landmark[24],results.pose_world_landmarks.landmark[23])
        print("hip_right_angle=", hip_right_angle)
        leg_left_angle=calculate_angle(results.pose_world_landmarks.landmark[23],results.pose_world_landmarks.landmark[25],results.pose_world_landmarks.landmark[27])
        print("leg_left_angle=",  leg_left_angle)
        leg_right_angle=calculate_angle(results.pose_world_landmarks.landmark[24],results.pose_world_landmarks.landmark[26],results.pose_world_landmarks.landmark[28])
        print("leg_right_angle=",leg_right_angle)
        

        # 可视化处理，将检测到的姿势关键点在图像上进行标记
        mp.solutions.drawing_utils.draw_landmarks(
            frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        
        # 保存处理后的帧为图片
        cv2.imwrite(os.path.join(frames_folder, f'frame_{frame_count}.jpg'), frame)

    # 显示处理后的帧
    cv2.imshow('Video', frame)

    # 按下 'q' 键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1

# 释放资源
cap.release()
cv2.destroyAllWindows()
