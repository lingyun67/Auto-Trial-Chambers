import cv2
import numpy as np
import pyautogui
import time

def check_purple_in_center():
    screen_width, screen_height = pyautogui.size()
    center_x, center_y = screen_width // 2, screen_height // 2
    left_x, top_y = center_x - 75, center_y - 75  # 150x150的一半是75
    right_x, bottom_y = center_x + 75, center_y + 75
    
    # 截取屏幕中心区域的图像，区域大小150x150
    img = np.array(pyautogui.screenshot(region=(left_x, top_y, 150, 150)))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # 转换为OpenCV的BGR格式

    # 定义目标紫色RGB并转换为HSV
    target_purple_rgb = np.uint8([[[128, 0, 128]]])  # RGB
    target_purple_hsv = cv2.cvtColor(target_purple_rgb, cv2.COLOR_RGB2HSV)[0][0]
    
    # 设置HSV阈值范围以检测紫色，包括更暗的紫色
    lower_purple = np.array([target_purple_hsv[0] - 10, 50, 30])  # 降低亮度下限至30
    upper_purple = np.array([target_purple_hsv[0] + 10, 255, 255])
    
    # 创建HSV图像并应用颜色阈值
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    
    # 计算掩码中非零元素的比例
    non_zero_pixels = cv2.countNonZero(mask)
    total_pixels = mask.size
    purple_ratio = non_zero_pixels / total_pixels

    # 输出调试信息
    print(f"检测到的紫色占比: {purple_ratio:.2%}")

    # 检查是否有超过50%的紫色像素
    if purple_ratio > 0.45:
        return True
    return False

while True:
    if check_purple_in_center():
        pyautogui.click(button='right')  # 在中心范围内50%以上的像素为紫色时，立即右键点击
    time.sleep(0.01)  # 设置检查频率
