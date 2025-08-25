import cv2
import mediapipe as mp
import time

class HandDetector:

    def __init__(self, mode=False, max_hands=2, model_com=1, detection_con=0.5, track_con=0.5):

        self.results = None
        self.mode = mode
        self.maxHands =max_hands
        self.modelCom = model_com
        self.detectionCon = detection_con
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelCom, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)

        return img

    def find_position(self, img, hand_id=0, draw=True):

        List = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[hand_id]
            for Id, lm in enumerate(myhand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                List.append([Id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
        return List


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    ctime = 0
    ptime = 0

    while cap.isOpened():
        success, img = cap.read()
        img = detector.find_hands(img)
        List = detector.find_position(img, 0, False)
        if List:
            print(List[4])
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()