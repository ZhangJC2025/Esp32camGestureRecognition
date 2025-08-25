import requests
import cv2
import numpy as np
import time
import math
import HANDTRACKINGMODULE as HTM
from ContorlComputer import control_computer


class HandGestureController:
    def __init__(self, ip_address="192.168.2.204", resolution_index=1):
        # List of available resolutions
        self.sizes = [
            "96x96", "160x120", "128x128", "176x144", "240x176", "240x240",
            "320x240", "320x320", "400x296", "480x320", "640x480", "800x600",
            "1024x768", "1280x720", "1280x1024", "1600x1200"
        ]

        # Initialize camera URL
        self.ip = ip_address
        self.url = f'http://{self.ip}/{self.sizes[resolution_index]}.mjpeg'

        # Initialize gesture detector
        self.detector = HTM.HandDetector()

        # FPS calculation variables
        self.previous_time = 0
        self.current_time = 0

        # Finger tip point IDs (thumb, index finger, middle finger, ring finger, pinky)
        self.tip_ids = [4, 8, 12, 16, 20]

    def process_frame(self, frame):
        """Process a single frame, detect gestures, and perform corresponding operations"""
        # Detect hands
        frame = self.detector.find_hands(frame)

        # Calculate and display FPS
        self.current_time = time.time()
        fps = 1 / (self.current_time - self.previous_time)
        self.previous_time = self.current_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Get hand landmark positions
        landmarks = self.detector.find_position(frame, 0, False)

        if landmarks:
            # Detect finger states (extended or bent)
            fingers = self.detect_fingers(landmarks)
            print(f"Fingers: {fingers}")

            # Detect specific gestures and perform corresponding operations
            self.detect_gestures(fingers)

        return frame

    def detect_fingers(self, landmarks):
        """Detect finger states"""
        fingers = []

        wrist = landmarks[0]

        # Detect thumb (compare x-coordinates)
        if math.fabs(landmarks[self.tip_ids[0]][1] - wrist[1]) > math.fabs(landmarks[self.tip_ids[0] - 2][1] - wrist[1]):
            fingers.append(1)  # Thumb extended
        else:
            fingers.append(0)  # Thumb bent

        # Detect the other four fingers (compare y-coordinates)
        for Id in range(1, 5):
            if landmarks[self.tip_ids[Id]][2] < landmarks[self.tip_ids[Id] - 2][2]:
                fingers.append(1)  # Finger extended
            else:
                fingers.append(0)  # Finger bent

        return fingers

    @staticmethod
    def detect_gestures(fingers):
        """Detect specific gestures and perform corresponding operations"""
        # Example gesture: Only middle finger extended (gesture code: [0, 0, 1, 0, 0])
        if fingers[1:] == [0, 1, 0, 0]:
            print("Shutdown gesture detected!")
            control_computer("shutdown")

        # Add more gesture detection logic here
        # elif fingers == [1, 1, 0, 0, 0]:
        #     print("Another gesture detected!")
        #     control_computer("another_command")

    def run(self, debug):
        """Run the main loop"""

        print(f"Connecting to ESP32-CAM at {self.url}")

        try:
            response = requests.get(self.url, stream=True, timeout=5)
            bytes_buffer = b''

            print("Press 'q' to quit...")

            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    bytes_buffer += chunk

                # Process JPEG data in the buffer
                while len(bytes_buffer) > 0:
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("Exiting...")
                        return

                    # Find JPEG start marker
                    start_index = bytes_buffer.find(b'\xff\xd8')
                    if start_index == -1:
                        bytes_buffer = b''
                        break

                    # Find JPEG end marker
                    end_index = bytes_buffer.find(b'\xff\xd9', start_index)
                    if end_index == -1:
                        break

                    # Extract complete JPEG image data
                    jpg_data = bytes_buffer[start_index:end_index + 2]
                    bytes_buffer = bytes_buffer[end_index + 2:]

                    if len(jpg_data) > 0:
                        try:
                            # Decode image
                            img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                            img = cv2.flip(img, 0)
                            if img is not None:
                                # Process frame
                                processed_img = self.process_frame(img)

                                if debug:
                                    # Display image
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
    # Create controller instance and run
    controller = HandGestureController()
    controller.run(True)  # Display debug images