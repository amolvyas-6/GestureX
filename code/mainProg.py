import HandTrackingModule as htm
import cv2
import getGesture as gg
import getLetter as gl
from brightnessControl import set_brightness
from volumeControl import set_volume
from collections import deque
import pyautogui
import numpy as np
import time

cap = cv2.VideoCapture(0)
tracker = htm.HandTracker(maxHands=2, detectionConf=0.7)
MODE = 1

# for mouse control
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
wScreen, hScreen = pyautogui.size()
wCap, hCap = 640, 480
THRESHOLD = 30
smoothening = 7
xMousePrev, yMousePrev = 0, 0

# for volume control
volumePrev = 0

# for ASL
text = ''
prev_letters = deque()

# for navigation
prev_right_lndmarks = []

# Define the rectangle's position and size
rect_x, rect_y = 100, 40  # Top-left corner of the rectangle
rect_w, rect_h = 500, 400  # Width and height of the rectangle

# for gesture recognition
prev_frames_left = deque()
prev_frames_right = deque()

def is_hand_inside_rectangle(hand_landmarks, rect_x, rect_y, rect_w, rect_h):
    for point in hand_landmarks:
        if not (rect_x <= point[0] <= rect_x + rect_w and rect_y <= point[1] <= rect_y + rect_h):
            return False
    return True

def detect_swipe(prev_landmarks, current_landmarks, threshold_x=100, threshold_y=0):
    wrist_prev = prev_landmarks[0]
    wrist_curr = current_landmarks[0]
    
    index_prev = prev_landmarks[8]
    index_curr = current_landmarks[8]
    
    # Calculate the horizontal movement of the wrist and index finger
    x_move_curr = wrist_curr[0] - wrist_prev[0]

    y_move_curr = wrist_curr[1] - wrist_prev[1]
    
    # If the difference in x-direction is significant, we assume a swipe
    if abs(x_move_curr) > threshold_x:
        if x_move_curr > 0:
            return "right"  # Right swipe
        elif x_move_curr < 0:
            return "left"  # Left swipe
    
    # if abs(y_move_curr) > threshold_y:
    #     if y_move_curr > 0:
    #         return "down"  # Down swipe
    #     elif y_move_curr < 0:
    #         return "up" # Up swipe
        
    return None

# Simulate tab switching
def switch_tab(direction):
    if direction == "right":
        pyautogui.hotkey('alt', 'tab')  # Switch to next tab
    elif direction == "left":
        pyautogui.hotkey('alt', 'shift', 'tab')  # Switch to previous tab
    
    # elif direction == "up":
    #     pyautogui.hotkey('win', 'up')  # Maximize window
    # elif direction == "down":
    #     pyautogui.hotkey('win', 'd')

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (0, 255, 0), 2)

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
        prev_frames_left, label = gg.get_prediction(left, prev_frames_left)
        if len(label) > 0:
            if label == 'One':
                MODE = 1
            if label == 'Two':
                MODE = 2
            elif label == 'Three':
                MODE = 3
            elif label == 'Four':
                MODE = 4
            elif label == 'Five':
                MODE = 5

    # reset ASL text
    if MODE != 5:
        text = ''
    
    if MODE == 1:
        cv2.putText(img, 'NAVIGATION', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0 and is_hand_inside_rectangle(right, rect_x, rect_y, rect_w, rect_h):
            if prev_right_lndmarks:
                direction = detect_swipe(prev_right_lndmarks, right)
                if direction:
                    print(f"Detected swipe: {direction}")
                    switch_tab(direction)
                    time.sleep(1)

            # Update previous landmarks
            prev_right_lndmarks = right



    elif MODE == 2:
        cv2.putText(img, 'BRIGHTNESS', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if is_hand_inside_rectangle(right, rect_x, rect_y, rect_w, rect_h):
            img = set_brightness(img, right, tracker)
    
    
    
    elif MODE == 3:
        cv2.putText(img, 'VOLUME', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if is_hand_inside_rectangle(right, rect_x, rect_y, rect_w, rect_h):
            img, volumePrev = set_volume(img, right, tracker, volumePrev)
    
    
    
    elif MODE == 4:
        cv2.putText(img, 'CURSOR', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0:
            fingersUp = tracker.fingersUp(right)
            if fingersUp[1] == 1 and fingersUp[2] == 0:
                xFinger, yFinger = right[8]
                xMouse = np.interp(xFinger, (rect_x, rect_x + rect_w), (0, wScreen))
                yMouse = np.interp(yFinger, (rect_y, rect_y + rect_h), (0, hScreen))

                # Apply smoothening
                xMouse = xMousePrev + (xMouse - xMousePrev) / smoothening
                yMouse = yMousePrev + (yMouse - yMousePrev) / smoothening

                pyautogui.moveTo(xMouse, yMouse)

                xMousePrev, yMousePrev = xMouse, yMouse
            
            if fingersUp[1] == 1 and fingersUp[2] == 1:
                length = tracker.getLength(right[12], right[8])
                if length < THRESHOLD:
                    pyautogui.leftClick()
    
    
    
    elif MODE == 5:
        cv2.putText(img, 'ASL', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0:
            norm_lndmrkPoints = tracker.normaliseLandmarks(right)
            prev_letters, letter = gl.get_prediction(right, prev_letters)
            if len(letter) > 0:
                if len(text) == 0 or text[-1] != letter:
                    text += letter
        
        cv2.putText(img, text, (100, 120), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(255, 0, 0), thickness=2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Main', img)

cap.release()
cv2.destroyAllWindows()
    