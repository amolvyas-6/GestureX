import time
import numpy as np
import mediapipe as mp
import HandTrackingModule as htm
import cv2
import pyautogui

cap = cv2.VideoCapture(0)
tracker = htm.HandTracker(maxHands=1)
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
wScreen, hScreen = pyautogui.size()
wCap, hCap = 640, 480

THRESHOLD = 30
smoothening = 4
xMousePrev, yMousePrev = 0, 0
xMouseCur, yMouseCur = 0, 0

while True:
    res, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img)
    landmarks = tracker.getPoints(img)
    if len(landmarks) > 0:
        fingersUp = tracker.fingersUp(landmarks)
        if fingersUp[1] == 1 and fingersUp[2] == 0:
            xFinger, yFinger = landmarks[8]
            xMouse = np.interp(xFinger, (100, wCap), (0, wScreen))
            yMouse = np.interp(yFinger, (100,hCap), (0, hScreen))

            xMouse = xMousePrev + (xMouse - xMousePrev)/smoothening
            yMouse = yMousePrev + (yMouse - yMousePrev)/smoothening

            xMousePrev = xMouse
            yMousePrev = yMouse

            pyautogui.moveTo(xMouse, yMouse)
        
        if fingersUp[1] == 1 and fingersUp[2] == 1:
            length = tracker.getLength(landmarks[12], landmarks[8])
            print(length)
            if length < THRESHOLD:
                pyautogui.leftClick()
        

    cv2.imshow('Mouse Control', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
