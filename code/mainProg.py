import HandTrackingModule as htm
import cv2
import getGesture as gg
from brightnessControl import set_brightness
from volumeControl import set_volume
from collections import deque
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)
tracker = htm.HandTracker(maxHands=2, detectionConf=0.7)
MODE = 2

# for mouse control
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
wScreen, hScreen = pyautogui.size()
wCap, hCap = 640, 480
THRESHOLD = 30
smoothening = 4
xMousePrev, yMousePrev = 0, 0

prev_frames = deque()

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img)
    landmarkPoints = []
    landmarkPoints2 = []
    
    num_hands = tracker.numOfHands(img)

    left = []
    right = []

    if num_hands > 0:
        if num_hands == 1:
            landmarkPoints, hand1_label = tracker.getPoints(img, handNo=0)
            if hand1_label == 'Left':
                left = landmarkPoints
                right = []
            else:
                left = []
                right = landmarkPoints

        elif num_hands == 2:
            landmarkPoints, hand1_label = tracker.getPoints(img, handNo=1)
            landmarkPoints2, hand2_label = tracker.getPoints(img, handNo=0)
            
            if hand1_label == 'Left' and hand2_label == 'Right':
                left = landmarkPoints
                right = landmarkPoints2
            else:
                right = landmarkPoints
                left = landmarkPoints2

    if len(left) > 0:
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, left), color=(0,0,255))
        prev_frames, label = gg.get_prediction(left, prev_frames)
        if len(label) > 0:
            if label == 'Two':
                #img = cv2.putText(img, text='BRIGHTNESS', org = (20, 30), font = cv2.FONT_HERSHEY_COMPLEX, color = (0, 255, 0), thickness=2)
                MODE = 2
            elif label == 'Three':
                #img = cv2.putText(img, text='VOLUME', org = (20, 30), font = cv2.FONT_HERSHEY_COMPLEX, color = (0, 255, 0), thickness=2)
                MODE = 3
            elif label == 'Four':
                #img = cv2.putText(img, text='ASL', org = (20, 30), font = cv2.FONT_HERSHEY_COMPLEX, color = (0, 255, 0), thickness=2)
                MODE = 4
            
    if MODE == 2:
        cv2.putText(img, 'BRIGHTNESS', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        img = set_brightness(img, right, tracker)
    elif MODE == 3:
        cv2.putText(img, 'VOLUME', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        img = set_volume(img, right, tracker)
    elif MODE == 4:
        cv2.putText(img, 'CURSOR', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0:
            fingersUp = tracker.fingersUp(right)
            if fingersUp[1] == 1 and fingersUp[2] == 0:
                xFinger, yFinger = right[8]
                xMouse = np.interp(xFinger, (100, wCap), (0, wScreen))
                yMouse = np.interp(yFinger, (100,hCap), (0, hScreen))

                xMouse = xMousePrev + (xMouse - xMousePrev)/smoothening
                yMouse = yMousePrev + (yMouse - yMousePrev)/smoothening

                xMousePrev = xMouse
                yMousePrev = yMouse

                pyautogui.moveTo(xMouse, yMouse)
            
            if fingersUp[1] == 1 and fingersUp[2] == 1:
                length = tracker.getLength(right[12], right[8])
                if length < THRESHOLD:
                    pyautogui.leftClick()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Main', img)

cap.release()
cv2.destroyAllWindows()
    