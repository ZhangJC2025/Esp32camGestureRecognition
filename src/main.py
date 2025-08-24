import requests
import cv2
import numpy as np
import time
import HANDTRACKINGMODULE as HTM
from ContorlComputer import shutdown
sizes = [
    "96x96",
    "160x120",
    "128x128",
    "176x144",
    "240x176",
    "240x240",
    "320x240",
    "320x320",
    "400x296",
    "480x320",
    "640x480",
    "800x600",
    "1024x768",
    "1280x720",
    "1280x1024",
    "1600x1200"
]

url = f'http://192.168.2.204/{sizes[1]}.mjpeg'
detector = HTM.HandDetector()
cTime = 0
pTime = 0
tipIds = [4, 8, 12, 16, 20]


response = requests.get(url, stream=True, timeout=5)
bytes_buffer = b''

jpg_data = b''
in_frame = False

try:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            bytes_buffer += chunk

        while len(bytes_buffer) > 0:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()
            start_index = bytes_buffer.find(b'\xff\xd8')
            if start_index == -1:
                bytes_buffer = b''
                break

            end_index = bytes_buffer.find(b'\xff\xd9', start_index)
            if end_index == -1:
                break

            jpg_data = bytes_buffer[start_index:end_index + 2]
            bytes_buffer = bytes_buffer[end_index + 2:]

            if len(jpg_data) > 0:
                try:
                    img = cv2.imdecode(np.frombuffer(jpg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
                    if img is not None:
                        img = detector.find_hands(img)
                        cTime = time.time()
                        fps = 1 / (cTime - pTime)
                        pTime = cTime

                        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        List = detector.find_position(img, 0, False)
                        if List:
                            fingers = []
                            if List[tipIds[0]][1] > List[tipIds[0] - 1][1]:
                                fingers.append(1)
                            else:
                                fingers.append(0)
                            for Id in range(1, 5):
                                if List[tipIds[Id]][2] < List[tipIds[Id] - 2][2]:
                                    fingers.append(1)
                                else:
                                    fingers.append(0)
                            print(fingers)
                            if fingers[1:] == [0, 1, 0, 0]:
                                shutdown()
                        cv2.imshow('Image', img)

                except Exception as e:
                    print(f"Decoding Error: {e}")
                    continue

finally:
    response.close()
    cv2.destroyAllWindows()