import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import mplcursors


def display_images(image_paths, scores):
    # 读取所有图片并获取它们的尺寸
    images = [cv2.imread(image_path) for image_path in image_paths]
    image_height, image_width, _ = images[0].shape

    # 计算每行显示的图片数量以及画布的高度和宽度
    num_images = len(image_paths)
    max_images_per_row = min(3, num_images)  # 每行最多显示3张图片
    num_rows = (num_images + max_images_per_row - 1) // max_images_per_row
    total_height = num_rows * image_height
    total_width = max_images_per_row * image_width

    # 创建空白画布
    merged_image = 255 * np.ones((total_height, total_width, 3), dtype=np.uint8)

    # 在画布上绘制每张图片和对应的得分
    row = col = 0
    for i, (image, score) in enumerate(zip(images, scores)):
        start_y = row * image_height
        start_x = col * image_width
        end_y = start_y + image_height
        end_x = start_x + image_width

        # 绘制图片
        merged_image[start_y:end_y, start_x:end_x, :] = image

        # 绘制得分
        text = f"Score: {score:.2f}"  # 得分文本
        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
        font_scale = 2.5  # 字体缩放比例
        font_thickness = 5  # 字体粗细
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)  # 获取文本尺寸
        text_x = start_x + 15  # 文本的起始x坐标
        text_y = start_y +70  # 文本的起始y坐标
        cv2.putText(merged_image, text, (text_x, text_y), font, font_scale, (0, 255, 255), font_thickness)  # 绘制文本

        col += 1
        if col == max_images_per_row:
            col = 0
            row += 1

    # 调整窗口大小并显示图片
    cv2.namedWindow("Merged Images with Scores", cv2.WINDOW_NORMAL)  # 创建窗口
    cv2.imshow("Merged Images with Scores", merged_image)  # 显示图片
    cv2.waitKey(0)  # 等待用户按键
    cv2.destroyAllWindows()  # 关闭窗口

import plotly.graph_objects as go

# def visualize_frame_scores(frame_scores):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=list(range(len(frame_scores))), y=frame_scores, mode='lines+markers'))
#     fig.update_layout(title='Frame Scores', xaxis_title='Frame Number', yaxis_title='Score', hovermode='closest')
#     fig.show()
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualize_frame_scores(frame_scores_list):
    num_iterations = len(frame_scores_list)
    fig = make_subplots(rows=num_iterations, cols=1, shared_xaxes=True, subplot_titles=[f'Iteration {i+1}' for i in range(num_iterations)], row_heights=[10] * num_iterations)

    for i, frame_scores in enumerate(frame_scores_list):
        fig.add_trace(go.Scatter(x=list(range(len(frame_scores))), y=frame_scores, mode='lines+markers'), row=i+1, col=1)

    fig.update_layout(title='Frame Scores', xaxis_title='Frame Number', yaxis_title='Score', hovermode='closest', height=1000, width=1200)
    fig.show()