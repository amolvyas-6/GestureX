import cv2
import csv
import HandTrackingModule as HTM

cap =cv2.VideoCapture(0)
tracker = HTM.HandTracker(maxHands=1)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        break
    
    img = tracker.findHands(img)

    if ord('A') <= key <= ord('Z'):
        print(key)
        key -= ord('A')
        landmarks = tracker.getPoints(img)
        processedLandmarks = tracker.normaliseLandmarks(landmarks)

        with open('data/sign_data.csv', "a") as file:
            writer = csv.writer(file)
            writer.writerow((key, *processedLandmarks))
    
    cv2.imshow("A", img)


cap.release()
cv2.destroyAllWindows()
