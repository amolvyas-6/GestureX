import HandTrackingModule as htm
import tensorflow as tf
import cv2
import numpy as np
from collections import deque

tracker = htm.HandTracker(maxHands=1, trackingConfidence=0.8, detectionConf=0.8)
cap = cv2.VideoCapture(0)
model = tf.keras.models.load_model("ASL_stuff\ASL_model.h5")
prev_frames_labels = deque()

DELAY_IN_FRAMES = 30

def predict(x):
    logit = model(x)
    prediction = tf.nn.softmax(logit)
    label = chr(np.argmax(prediction[0]) + ord('A'))
    return label

def equal(q):
    prev = q[0]
    for i in q:
        if i != prev:
            return False
        prev = i
    return True

while True:
    suc, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img, draw=True)
    lndmrkPoints, hand_label = tracker.getPoints(img)

    if len(lndmrkPoints) > 0 and hand_label == 'Right':
        norm_lndmrkPoints = tracker.normaliseLandmarks(lndmrkPoints)
        label = predict(np.array([norm_lndmrkPoints]))
        prev_frames_labels.append(label)
        if len(prev_frames_labels) == DELAY_IN_FRAMES:
            if equal(prev_frames_labels):
                cv2.putText(img, label, (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)

            prev_frames_labels.popleft()

    
    cv2.imshow("ASL", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()