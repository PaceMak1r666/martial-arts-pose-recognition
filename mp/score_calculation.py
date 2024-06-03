# 计算分数
def calculate_score(angle, beginkey, middlekey, endkey, text='', required=None):
    # 获取关键点的置信度
    confidence = (beginkey['visibility'] + middlekey['visibility'] + endkey['visibility'])/3
    # 计算角度偏差
    deviation = abs(angle - required[0])
    #说明至少有一个关键点未被识别
    if beginkey['visibility']<0.5 or middlekey['visibility']<0.5 or endkey['visibility']<0.5:
        score =100-deviation+deviation*confidence
    else:
     
        
        # 计算加权得分，考虑关键点置信度作为权重
        score = 100 - deviation*confidence
        
        # 如果在规定范围内
        if deviation <= required[1]:
            min_score=60
            score = max(score, min_score)
        else:
            score = 100 - deviation
            if score<0:
                score=0

    
    print(f"Score for {text}: {score}")
    return score