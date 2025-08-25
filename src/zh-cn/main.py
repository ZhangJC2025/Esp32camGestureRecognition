import requests
import cv2
import numpy as np
import time
import math
import HANDTRACKINGMODULE as HTM
from ContorlComputer import control_computer


class HandGestureController:
    def __init__(self, ip_address="192.168.2.204", resolution_index=1):
        # 可用的分辨率列表
        self.sizes = [
            "96x96", "160x120", "128x128", "176x144", "240x176", "240x240",
            "320x240", "320x320", "400x296", "480x320", "640x480", "800x600",
            "1024x768", "1280x720", "1280x1024", "1600x1200"
        ]

        # 初始化摄像头URL
        self.ip = ip_address
        self.url = f'http://{self.ip}/{self.sizes[resolution_index]}.mjpeg'

        # 初始化手势检测器
        self.detector = HTM.HandDetector()

        # FPS计算变量
        self.previous_time = 0
        self.current_time = 0

        # 手指尖点的ID（拇指、食指、中指、无名指、小指）
        self.tip_ids = [4, 8, 12, 16, 20]

    def process_frame(self, frame):
        """处理单帧图像，检测手势并执行相应操作"""
        # 检测手部
        frame = self.detector.find_hands(frame)

        # 计算并显示FPS
        self.current_time = time.time()
        fps = 1 / (self.current_time - self.previous_time)
        self.previous_time = self.current_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 获取手部关键点位置
        landmarks = self.detector.find_position(frame, 0, False)

        if landmarks:
            # 检测手指状态（伸直或弯曲）
            fingers = self.detect_fingers(landmarks)
            print(f"Fingers: {fingers}")

            # 检测特定手势并执行相应操作
            self.detect_gestures(fingers)

        return frame

    def detect_fingers(self, landmarks):
        """检测手指状态"""
        fingers = []

        wrist = landmarks[0]
        # 检测拇指（比较x坐标）
        if math.fabs(landmarks[self.tip_ids[0]][1] - wrist[1]) > math.fabs(landmarks[self.tip_ids[0] - 2][1] - wrist[1]):
            fingers.append(1)  # 拇指伸直
        else:
            fingers.append(0)  # 拇指弯曲

        # 检测其他四指（比较y坐标）
        for Id in range(1, 5):
            if math.fabs(landmarks[self.tip_ids[Id]][2] - wrist[2]) > math.fabs(landmarks[self.tip_ids[Id] - 2][2] - wrist[2]):
                fingers.append(1)  # 手指伸直
            else:
                fingers.append(0)  # 手指弯曲

        return fingers

    @staticmethod
    def detect_gestures(fingers):
        """检测特定手势并执行相应操作"""
        # 示例手势：只有中指伸直（手势代码：[0, 0, 1, 0, 0]）
        if fingers[1:] == [0, 1, 0, 0]:
            print("Shutdown gesture detected!")
            control_computer("shutdown")

        # 在这里添加更多手势检测逻辑
        # elif fingers == [1, 1, 0, 0, 0]:
        #     print("Another gesture detected!")
        #     control_computer("another_command")

    def run(self, debug):
        """运行主循环"""

        print(f"Connecting to ESP32-CAM at {self.url}")

        try:
            response = requests.get(self.url, stream=True, timeout=5)
            bytes_buffer = b''

            print("Press 'q' to quit...")

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    bytes_buffer += chunk

                # 处理缓冲区中的JPEG数据
                while len(bytes_buffer) > 0:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Exiting...")
                        return

                    # 查找JPEG起始标记
                    start_index = bytes_buffer.find(b'\xff\xd8')
                    if start_index == -1:
                        bytes_buffer = b''
                        break

                    # 查找JPEG结束标记
                    end_index = bytes_buffer.find(b'\xff\xd9', start_index)
                    if end_index == -1:
                        break

                    # 提取完整的JPEG图像数据
                    jpg_data = bytes_buffer[start_index:end_index + 2]
                    bytes_buffer = bytes_buffer[end_index + 2:]

                    if len(jpg_data) > 0:
                        try:
                            # 解码图像
                            img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                            img = cv2.flip(img, 0)
                            if img is not None:
                                # 处理帧
                                processed_img = self.process_frame(img)

                                if debug:
                                    # 显示图像
                                    cv2.imshow('ESP32-CAM Hand Gesture Control', processed_img)

                        except Exception as e:
                            print(f"Frame processing error: {e}")
                            continue

        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            print("Please check:")
            print(f"1. The ESP32-CAM is connected to the same network")
            print(f"2. The IP address {self.ip} is correct")
            print(f"3. The ESP32-CAM is streaming video")

        finally:
            if 'response' in locals():
                response.close()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    # 创建控制器实例并运行
    controller = HandGestureController()
    controller.run(True) # 显示调试图像