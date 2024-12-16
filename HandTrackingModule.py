import cv2
import time
import numpy as np
import mediapipe as mp

fingerTipPoints = [4, 8, 12,16, 20]

class HandTracker():
    def __init__(self, mode = False, maxHands = 2, detectionConf = 0.5, trackingConfidence = 0.5):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=mode,
                                        max_num_hands=maxHands,
                                        min_detection_confidence=detectionConf,
                                        min_tracking_confidence=trackingConfidence)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLandmarks in self.results.multi_hand_landmarks:                    
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmarks, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def getPoints(self, img, handNo=0):
        landmarkList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, landmark in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    landmarkList.append((x, y))
        return landmarkList

    def numOfHands(self, img):
        if self.results.multi_hand_landmarks:
            return len(self.results.multi_hand_landmarks)
        return 0
    
    def fingersUp(self, landmarks):
        fingersUpList = []
        if landmarks[fingerTipPoints[0]][1] > landmarks[fingerTipPoints[0] - 1][1]:
            fingersUpList.append(0)
        else:
            fingersUpList.append(1)
        
        for i in range(1, 5):
            if landmarks[fingerTipPoints[i]][1] > landmarks[fingerTipPoints[i] - 2][1]:
                fingersUpList.append(0)
            else:
                fingersUpList.append(1)
        
        return fingersUpList

    def getLength(self, point1, point2):
        return (pow(point1[0] - point2[0], 2) + pow(point1[1] - point2[1], 2))**0.5
    
    def getBoundingBox(self, img, landmarks, padding = 10):
        h, w, c = img.shape
        temp_array = np.array([
            (min(landmark[0], w - 1),
            min(landmark[1], h - 1))
            for landmark in landmarks  
        ], dtype=int)

        x_min = max(0, np.min(temp_array[:, 0]) - padding)
        y_min = max(0, np.min(temp_array[:, 1]) - padding)
        x_max = min(w - 1, np.max(temp_array[:, 0]) + padding)
        y_max = min(h - 1, np.max(temp_array[:, 1]) + padding)

        return (x_min, y_min, x_max, y_max)

    def drawBoundingBox(self, img, points, color = [255, 0, 0]):
        start = (points[0], points[1])
        end = (points[2], points[3])
        cv2.rectangle(img, start, end, color=color, thickness=2)
        return img
    
    def putPredictedGestureOnScreen(self, img, label, boundingBox):

        text_position = (boundingBox[0], boundingBox[1] - 10)  # Slightly above the box
        cv2.putText(img, label, text_position, cv2.FONT_HERSHEY_COMPLEX, fontScale=1, color=(255, 0, 0))
        return img
    
    def normaliseLandmarks(self, landmarks):
        temp_landmark_array = np.array(landmarks, dtype=float)
        base_x, base_y = temp_landmark_array[0]
        temp_landmark_array -= [base_x, base_y]  # landmark 0 will always be 0, 0
        
        temp_landmark_array = temp_landmark_array.flatten() # convert to 1d array for LLM use
        
        # Normalize
        max_value = np.max(np.abs(temp_landmark_array))
        if max_value > 0:  # Avoid division by zero
            temp_landmark_array /= max_value
        
        return temp_landmark_array.tolist()


#Basically Useless
def main():
    cap = cv2.VideoCapture(0)
    prevTime, curTime = 0, 0
    tracker = HandTracker(detectionConf=0.7)
    while True:
        success, img = cap.read()
        if not success:
            print("Error capturing Video")
            continue
        img = cv2.flip(img, 1)
        img = tracker.findHands(img)
        landmarkList = tracker.getPoints(img, handNo=0)
        landmarkList2 = tracker.getPoints(img, handNo=1)

        if len(landmarkList) > 0:
            print("First Hand = ", landmarkList[1])
        
        if len(landmarkList2) > 0:
            print("Second Hand = ", landmarkList2[1])
        curTime = time.time()
        fps = 1 / (curTime - prevTime)
        prevTime = curTime
        cv2.putText(img, str(int(fps)), (30, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 3)
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
