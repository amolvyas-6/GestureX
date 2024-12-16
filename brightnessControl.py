import time
import cv2
import mediapipe as mp
import HandTrackingModule as HTM
import screen_brightness_control as sbc
import math

cap = cv2.VideoCapture(0)
tracker = HTM.HandTracker(maxHands=2, detectionConf=0.7)

maxLen, minLen = 200, 25
maxBrightness, minBrightness = 100, 0
OldRange = (maxLen - minLen)  
NewRange = (maxBrightness - minBrightness) 

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img)
    landmarkPoints = []
    landmarkPoints2 = []

    num_hands = tracker.numOfHands(img)
    if num_hands == 1:
        landmarkPoints = tracker.getPoints(img, handNo=0)
    elif num_hands == 2:
        landmarkPoints = tracker.getPoints(img, handNo=1)
        landmarkPoints2 = tracker.getPoints(img, handNo=0)

    if len(landmarkPoints2) > 0:
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, landmarkPoints2), color=(0,0,255))

    if len(landmarkPoints) > 0:
        
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, landmarkPoints))
        x1, y1 = landmarkPoints[8]
        x2, y2 = landmarkPoints[4]
        length = math.sqrt(math.pow(x2-x1, 2) + math.pow(y2-y1, 2))
        brightness = int((((length - minLen) * NewRange) / OldRange) + minBrightness)
        sbc.set_brightness(brightness)
    
    cv2.imshow("Brightness Control", img)
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    
