# rules.py

def load_required_list():
    required_list = [
        # 0139
    #   {
    #         'shoulder_left_angle':[154.6, 40],#1 5 6
    #         'shoulder_right_angle':[124.8, 40],#1 2 3
    #         'hip_left_angle': [150.4, 40],#8，12，13
    #         'hip_right_angle':[152.6, 40],#8，9，10
    #         'arm_left_angle': [68.9, 40],#5，6，7
    #         'arm_right_angle': [104.2, 40],#2，3，4
    #         'leg_left_angle': [111.2, 40],#12，13，14
    #         'leg_right_angle': [113.2, 40]#9,10,11
    #         # 其他关节角度要求...
    #     },
        # 0161
        {
            'shoulder_left_angle': [26.47, 40],#1 5 6
            'shoulder_right_angle': [89.3, 40],#1 2 3
            'hip_left_angle': [122.71, 40],#8，12，13
            'hip_right_angle': [139.27, 40],#8，9，10
            'arm_left_angle': [131.44 ,40],#5，6，7
            'arm_right_angle': [148.36, 40],#2，3，4
            'leg_left_angle': [129.7, 40],#12，13，14
            'leg_right_angle': [173.0, 40]#9,10,11
            # 其他关节角度要求...
        },
        # 0179
        {
            'shoulder_left_angle': [78.15, 40],#1 5 6
            'shoulder_right_angle': [22.91, 40],#1 2 3
            # 'hip_left_angle': [100.03, 40],#8，12，13
            # 'hip_right_angle': [88.69, 40],#8，9，10
            'arm_left_angle': [157.86, 40],#5，6，7
            'arm_right_angle': [63.97, 40],#2，3，4
            'leg_left_angle': [178.6, 40],#12，13，14
            'leg_right_angle': [146.9, 40]#9,10,11
        },
        # 0186
        # {
        #     'shoulder_left_angle': [168.0, 40],#1 5 6
        #     'shoulder_right_angle': [125.7, 40],#1 2 3
        #     'hip_left_angle': [ 176.6, 40],#8，12，13
        #     'hip_right_angle': [119.9, 40],#8，9，10
        #     'arm_left_angle': [163.3, 40],#5，6，7
        #     'arm_right_angle': [61.2, 40],#2，3，4
        #     'leg_left_angle': [52.1, 40],#12，13，14
        #     'leg_right_angle': [176.1, 40]#9,10,11
        # },
        # 0207
        {
            'shoulder_left_angle': [176.2, 40],#1 5 6
            'shoulder_right_angle': [109.17, 40],#1 2 3
            'hip_left_angle': [143.85, 40],#8，12，13
            'hip_right_angle': [163.1, 40],#8，9，10
            'arm_left_angle': [154.90, 40],#5，6，7
            'arm_right_angle': [178.88, 40],#2，3，4
            'leg_left_angle': [122.22, 40],#12，13，14
            'leg_right_angle': [115.88, 40]#9,10,11
        },
        # 0238
        # {
        #     'shoulder_left_angle': [121.2, 40],#1 5 6
        #     'shoulder_right_angle': [149.7, 40],#1 2 3
        #     'hip_left_angle': [41.1, 40],#8，12，13
        #     'hip_right_angle': [106.6, 40],#8，9，10
        #     'arm_left_angle': [76.2, 40],#5，6，7
        #     'arm_right_angle': [179.7, 40],#2，3，4
        #     'leg_left_angle': [58.6, 40],#12，13，14
        #     'leg_right_angle': [175.6, 40]#9,10,11
        # },
        #264
        {
            'shoulder_left_angle': [105.14, 40],#1 5 6
            'shoulder_right_angle': [29.64, 40],#1 2 3
            # 'hip_left_angle': [91.46, 40],#8，12，13
            # 'hip_right_angle': [115.8, 40],#8，9，10
            'arm_left_angle': [159, 40],#5，6，7
            'arm_right_angle': [110.24, 40],#2，3，4
            'leg_left_angle': [156.85, 40],#12，13，14
            'leg_right_angle': [160.27, 40]#9,10,11

        },
        # 288
        # {
        #     'shoulder_left_angle': [60.6, 40],#1 5 6
        #     'shoulder_right_angle': [155.2, 40],#1 2 3
        #     'hip_left_angle': [93.4, 40],#8，12，13
        #     'hip_right_angle': [86.9,40],#8，9，10
        #     'arm_left_angle': [70.2, 40],#5，6，7
        #     'arm_right_angle': [172.9, 40],#2，3，4
        #     'leg_left_angle': [24.8, 40],#12，13，14
        #     'leg_right_angle': [176.2, 40]#9,10,11
        # },
        # 0319
        {
            'shoulder_left_angle': [61.11, 40],#1 5 6
            'shoulder_right_angle': [139.35, 40],#1 2 3
            # 'hip_left_angle': [140.8, 40],#8，12，13
            # 'hip_right_angle': [138.7,40],#8，9，10
            'arm_left_angle': [167.68, 40],#5，6，7
            'arm_right_angle': [176.29, 40],#2，3，4
            'leg_left_angle': [130.18, 40],#12，13，14
            'leg_right_angle': [67.00, 40]#9,10,11
        },
        # 0353
        # {   'shoulder_left_angle': [114.5, 40],#1 5 6
        #     'shoulder_right_angle': [139.2, 40],#1 2 3
        #     'hip_left_angle': [80.4, 40],#8，12，13
        #     'hip_right_angle': [93.6, 40],#8，9，10
        #     'arm_left_angle': [109.6, 40],#5，6，7
        #     'arm_right_angle': [88.5, 40],#2，3，4
        #     'leg_left_angle': [178.3, 40],#12，13，14
        #     'leg_right_angle': [174.8, 40]#9,10,11
        # },
        # 0386
        {
            'shoulder_left_angle': [128.58, 40],#1 5 6
            'shoulder_right_angle': [76.975, 40],#1 2 3
            'hip_left_angle': [79.49, 40],#8，12，13
            'hip_right_angle': [135.24, 40],#8，9，10
            'arm_left_angle': [163.91, 40],#5，6，7
            'arm_right_angle': [146.78, 40],#2，3，4
            'leg_left_angle': [154.56, 40],#12，13，14
            'leg_right_angle': [143.24, 40]#9,10,11
        }
       
        # 其他动作对应的required字典...
    ]
    return required_list
