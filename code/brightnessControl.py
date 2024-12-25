import cv2
import HandTrackingModule as HTM
import screen_brightness_control as sbc
import getGesture as gg
from collections import deque
import subprocess
import sys

'''cap = cv2.VideoCapture(0)
tracker = HTM.HandTracker(maxHands=2, detectionConf=0.7)

maxLen, minLen = 200, 25
maxBrightness, minBrightness = 100, 0
OldRange = (maxLen - minLen)
NewRange = (maxBrightness - minBrightness) 

prev_gestures = deque()

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
            prev_gestures, gesture = gg.get_prediction(left, prev_gestures)
            if len(gesture) > 0:
                if gesture == 'Thumbs Up':
                    break
                if gesture == 'One':
                    cap.release()
                    cv2.destroyAllWindows()
                    subprocess.run([sys.executable, 'code/volumeControl.py'])
                    sys.exit()

        if len(right) > 0:
            img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, right))
            length = tracker.getLength(right[8], right[4])
            brightness = (((length - minLen) * NewRange) / OldRange) + minBrightness
            brightness = round(brightness / 20) * 20
            brightness = max(0, min(100, round(brightness)))
            sbc.set_brightness(brightness)
    
    cv2.imshow("Brightness Control", img)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
'''
def set_brightness(img, right, tracker):
    maxLen, minLen = 200, 25
    maxBrightness, minBrightness = 100, 0
    OldRange = (maxLen - minLen)
    NewRange = (maxBrightness - minBrightness)
    if len(right) > 0:
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, right))
        length = tracker.getLength(right[8], right[4])
        brightness = (((length - minLen) * NewRange) / OldRange) + minBrightness
        brightness = round(brightness / 20) * 20
        brightness = max(0, min(100, round(brightness)))
        sbc.set_brightness(brightness)
    
    return img