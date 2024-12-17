import os
import HandTrackingModule as htm
import numpy as np
import cv2
import csv

cur_label = 'A'
path = 'ASL_Dataset\\train\\' + cur_label
tracker = htm.HandTracker()

for filename in os.listdir(path):
    file_path = os.path.join(path, filename)
    img = cv2.imread(file_path)
    img = cv2.resize(img, (640, 480))
    img = tracker.findHands(img, draw=True)
    lndmrkPoints = tracker.getPoints(img)
    if len(lndmrkPoints) > 0:
        norm_lndmrkPoints = tracker.normaliseLandmarks(lndmrkPoints)
        with open('ASL_Dataset\\sign_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(((ord(cur_label) - ord('A')), *norm_lndmrkPoints))
    