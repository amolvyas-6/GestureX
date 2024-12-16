import cv2
import HandTrackingModule as HTM
import tensorflow as tf
import numpy as np
import csv
from collections import deque

tracker = HTM.HandTracker(maxHands=1)
model = tf.keras.models.load_model("D:\Sem 3\EL\data\MyModel2.h5")
labels = []
prev_frames_labels = deque()
DELAY_IN_FRAMES = 40

with open('data/gestureLabels.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        labels.append(row[0])

def get_label(X):
    logits = model(X)
    prediction = tf.nn.softmax(logits)
    return labels[np.argmax(prediction[0])]

def equal(q):
    prev = q[0]
    for i in q:
        if i != prev:
            return False
        prev = i
    return True

def main():
    cap = cv2.VideoCapture(0)
    while True:
        suc, img = cap.read()
        img = cv2.flip(img, 1)

        img = tracker.findHands(img)
        landmarks = tracker.getPoints(img)
        if len(landmarks) > 0:
            input = np.array([tracker.normaliseLandmarks(landmarks)], dtype=float)
            label = get_label(input)
            prev_frames_labels.append(label)
            if len(prev_frames_labels) == DELAY_IN_FRAMES:
                if equal(prev_frames_labels):
                    boundingBox = tracker.getBoundingBox(img, landmarks)
                    img = tracker.putPredictedGestureOnScreen(img, label, boundingBox)
                prev_frames_labels.popleft()

        cv2.imshow("A", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()