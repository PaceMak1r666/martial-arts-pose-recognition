import numpy as np
# def calculate_angle(joint1, joint2, joint3):
#     """Calculate the angle between three joints in degrees."""
#     # 计算两个关节点的向量
#     vector1 = np.array([joint1['x'], joint1['y'], joint1['z']])
#     vector2 = np.array([joint2['x'], joint2['y'], joint2['z']])
#     vector3 = np.array([joint3['x'], joint3['y'], joint3['z']])

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






def calculate_angle(joint1, joint2, joint3):
    """Calculate the angle between three joints in degrees."""
    # 计算两个关节点的向量，忽略 Z 坐标
    vector1 = np.array([joint1['x'], joint1['y']])
    vector2 = np.array([joint2['x'], joint2['y']])
    vector3 = np.array([joint3['x'], joint3['y']])

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


# 判断角度是否符合要求
def angle_if(beginkey, middlekey, endkey, text='', required=None):
    result = "Angle not calculated"
    angle = calculate_angle(beginkey,  middlekey ,endkey)
    result = text + str(angle)
    
    # 检查角度是否在预期范围内
    if required and abs(angle - required[0]) > required[1]:
        print(text,"=",angle,"度")
        print("Angle deviates too much from the expected range")
        return False,angle
    
    result = text + ": " + str(angle) + "度"
    print(text, ":", result)
    return True,angle