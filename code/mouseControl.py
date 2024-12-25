import numpy as np
import HandTrackingModule as htm
import cv2
import pyautogui
from collections import deque
import getGesture as gg

cap = cv2.VideoCapture(0)
tracker = htm.HandTracker(maxHands=2)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
wScreen, hScreen = pyautogui.size()
wCap, hCap = 640, 480

THRESHOLD = 30
smoothening = 4
xMousePrev, yMousePrev = 0, 0
#xMouseCur, yMouseCur = 0, 0
prev_gestures = deque()

while True:
    res, img = cap.read()
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
        prev_gestures, gesture = gg.get_prediction(left, prev_gestures)
        if len(gesture) > 0:
            if gesture == 'Thumbs Up':
                break
    
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
        

    cv2.imshow('Mouse Control', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


def cursor_movement(img, right, tracker):
    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False
    wScreen, hScreen = pyautogui.size()
    wCap, hCap = 640, 480

    THRESHOLD = 30
    smoothening = 4
    xMousePrev, yMousePrev = 0, 0

    