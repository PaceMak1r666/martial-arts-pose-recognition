def calculate_frame_score(joint_scores):
    # 计算八个关节角度分数的总和
    total_score = sum(joint_scores)
    
    # 将总和归一化到0到100的范围内
    max_total_score = len(joint_scores) * 100  # 全部关节角度分数都为最高分时的总和
    frame_score = (total_score / max_total_score) * 100
    
    return frame_score

# 提取关键点信息
def extract_landmark_info(landmark_msg):
    x = landmark_msg.x
    y = landmark_msg.y
    z = landmark_msg.z
    visibility = landmark_msg.visibility
    return x, y, z, visibility
