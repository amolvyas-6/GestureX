import cv2
import csv
import HandTrackingModule as HTM

cap =cv2.VideoCapture(0)
tracker = HTM.HandTracker(maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    
    img = tracker.findHands(img)

    if ord('0') <= key <= ord('9'):
        print(key)
        key -= ord('0')
        landmarks, hand_label = tracker.getPoints(img)
        print(landmarks)
        processedLandmarks = tracker.normaliseLandmarks(landmarks)

        with open('data/gestureData.csv', "a") as file:
            writer = csv.writer(file)
            writer.writerow((key, *processedLandmarks))
            
    cv2.imshow("Gesture", img)


cap.release()
cv2.destroyAllWindows()
