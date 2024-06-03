import cv2
import mediapipe as mp
from test_1.mp.angle_calculation import angle_if, calculate_angle
from test_1.mp.data_processing import calculate_frame_score, extract_landmark_info
from test_1.mp.score_calculation import calculate_score
from display_gui import visualize_frame_scores
from test_1.mp.rules_1 import load_required_list
import os



def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    mp_pose = mp.solutions.pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    frame_count = 0
    landmarks_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_pose.process(rgb_frame)

        if results.pose_landmarks:
            landmarks_info = {'frame_number': frame_count, 'landmarks': []}
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
            landmarks_data.append(landmarks_info)
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cap.release()

    return landmarks_data

def process_landmarks(landmarks_data, require_list):
    best_frame_scores = []
    best_frame_ids = []
    all_frame_scores = []
    try:

                # 初始化最低分数阈值
        min_score_threshold = 60  # 可根据实际情况调整

        # 初始化最大未找到最佳帧的动作数
        max_unscored_actions = 3  # 可根据实际情况调整
        for required in require_list:
            max_score = 0
            max_id = 0
            frame_scores = []

            for frame_info in landmarks_data:
                frame_number = frame_info['frame_number']
                landmarks = frame_info['landmarks']
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
                        if key=='shoulder_left_angle':
                    # 计算指定角度的分数
                            score_shoulder_left = calculate_score(
                                calculate_angle(elbow_left,shoulder_left,hip_left),
                                elbow_left,shoulder_left, hip_left,
                                text='Shoulder Left', required=value
                            )
                            angle_result,angle_value=angle_if(elbow_left,shoulder_left,hip_left,text='Shoulder Left',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_shoulder_left
                            joint_scores.append(score_shoulder_left)
                        elif key=='shoulder_right_angle':
                            score_shoulder_right = calculate_score(
                                calculate_angle(elbow_right,shoulder_right,hip_right),
                                elbow_right,shoulder_right,hip_right,
                                text='Shoulder Right', required=value
                            )
                            angle_result,angle_value=angle_if(elbow_right,shoulder_right,hip_right,text='Shoulder Right',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_shoulder_right
                            joint_scores.append(score_shoulder_right)
                        elif key=='hip_left_angle':    
                            score_hip_left = calculate_score(
                                calculate_angle(hip_right, hip_left, knee_left),
                                hip_right, hip_left, knee_left,
                                text='Hip Left', required=value
                            )
                            angle_result,angle_value=angle_if(hip_right, hip_left, knee_left,text='Hip Left',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_hip_left
                            joint_scores.append(score_hip_left)
                        elif key=='hip_right_angle':
                            score_hip_right = calculate_score(
                                calculate_angle(hip_left, hip_right, knee_right),
                                hip_left, hip_right, knee_right,
                                text='Hip Right', required=value
                            )
                            angle_result,angle_value=angle_if(hip_left, hip_right, knee_right,text='Hip Right',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_hip_right
                            joint_scores.append(score_hip_right)
                        elif key=='arm_left_angle':
                            score_arm_left = calculate_score(
                                calculate_angle(shoulder_left, elbow_left, wrist_left),
                                shoulder_left, elbow_left, wrist_left,
                                text='Arm Left', required=value
                            )
                            angle_result,angle_value=angle_if(shoulder_left, elbow_left, wrist_left,text='Arm Left',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_arm_left
                            joint_scores.append(score_arm_left)
                        elif key=='arm_right_angle':
                            score_arm_right = calculate_score(
                                calculate_angle(shoulder_right, elbow_right, wrist_right),
                                shoulder_right, elbow_right, wrist_right,
                                text='Arm Right', required=value
                            )
                            angle_result,angle_value=angle_if(shoulder_right, elbow_right, wrist_right,text='Arm Right',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_arm_right
                            joint_scores.append(score_arm_right)
                        elif key=='leg_left_angle':
                            score_leg_left = calculate_score(
                                calculate_angle(ankle_left, knee_left, hip_left),
                                ankle_left, knee_left, hip_right,
                                text='Leg Left', required=value
                            )
                            angle_result,angle_value=angle_if(ankle_left, knee_left, hip_left,text='Leg Left',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_leg_left
                            joint_scores.append(score_leg_left)
                        elif key=='leg_right_angle':
                            score_leg_right = calculate_score(
                                calculate_angle(ankle_right, knee_right, hip_right),
                                ankle_right, knee_right, hip_right,
                                text='Leg Right', required=value
                            )
                            angle_result,angle_value=angle_if(ankle_right, knee_right, hip_right,text='Leg Right',required=value)
                            if angle_result==False:
                                angle_condition_unsatisfied+=1
                            totalScore=totalScore+score_leg_right
                            joint_scores.append(score_leg_right)
        

                frame_scores.append(totalScore)
                totalScore_after = calculate_frame_score(joint_scores)

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
        
        print(f"TotalScore=", average_score)
             # 如果所有帧的得分都低于最低分数阈值，则认为视频无法评分
        if all(score < min_score_threshold for score in best_frame_scores):
            print("The video cannot be scored.")
            return None
        
        low_score_count = sum(score < min_score_threshold for score in best_frame_scores)
        if low_score_count >= 3:
            print("The video cannot be scored due to too many low-scoring frames.")
            return None

        # 如果对于太多的动作都找不到最佳帧，则判定无法评分
        if best_frame_ids.count(0) > max_unscored_actions:
            print("Too many actions cannot be scored.")
            return None
        # visualize_frame_scores(all_frame_scores)

        return best_frame_ids
    except Exception as e:
        print("An error occurred during processing:", str(e))
        return None
#
def display_best_frame(video_path, best_frame_ids):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    mp_pose = mp.solutions.pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        smooth_landmarks=True,
        enable_segmentation=False,
        smooth_segmentation=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    for frame_count in best_frame_ids:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_pose.process(rgb_frame)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        cv2.imshow('Best Frame', frame)
        cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()

def main():
    video_path = 'D:/openpose/examples/media/test_1.mp4'
    landmarks_data = process_video(video_path)

    require_list = load_required_list()
    best_frame_ids = process_landmarks(landmarks_data, require_list)

    # display_best_frame(video_path, best_frame_ids)

if __name__ == "__main__":
    main()
