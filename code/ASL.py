import HandTrackingModule as htm
import cv2
import numpy as np
from collections import deque
import getLetter as gl
import getGesture as gg

tracker = htm.HandTracker(maxHands=2, trackingConfidence=0.8, detectionConf=0.8)
cap = cv2.VideoCapture(0)
prev_letters = deque()
prev_gestures = deque()

s = ''

while True:
    suc, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img, draw=True)
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
    
    if len(right) > 0:
        norm_lndmrkPoints = tracker.normaliseLandmarks(right)
        prev_letters, letter = gl.get_prediction(right, prev_letters)
        if len(letter) > 0:
            if len(s) == 0 or s[-1] != letter:
                s += letter
            cv2.putText(img, s, (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
    
    if len(left) > 0:
        norm_lndmrkPoints = tracker.normaliseLandmarks(left)
        prev_gestures, gesture = gg.get_prediction(left, prev_gestures)
        if len(gesture) > 0:
            if gesture == 'Thumbs Up':
                break
    
    cv2.imshow("ASL", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()