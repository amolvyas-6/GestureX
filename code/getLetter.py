import tensorflow as tf
import numpy as np
import csv
import HandTrackingModule as htm
from collections import deque

tracker = htm.HandTracker()
model = tf.keras.models.load_model("models\ASL_model.h5")
prev_frames_labels = deque()
DELAY_IN_FRAMES = 20

def get_label(X):
    logits = model(X)
    prediction = tf.nn.softmax(logits)
    return chr(np.argmax(prediction[0]) + ord('A'))

def equal(q):
    prev = q[0]
    for i in q:
        if i != prev:
            return False
        prev = i
    return True

def get_prediction(landmarks, prev_frames):
    label = get_label(np.array([tracker.normaliseLandmarks(landmarks)], dtype=float))
    if len(prev_frames) < DELAY_IN_FRAMES:
        prev_frames.append(label)
    else:
        prev_frames.popleft()
        prev_frames.append(label)
        if equal(prev_frames):
            return prev_frames, prev_frames[-1]
    
    return prev_frames, ''