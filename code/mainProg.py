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
from GUI import dict

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

# for gesture
prev_right_lndmarks = []
prev_gesture = ''
SWIPE_THRESHOLD = 50
DEBOUNCE_TIME = 1  # seconds
last_swipe_time = 0


# Define the rectangle's position and size
rect_x, rect_y = 100, 40  # Top-left corner of the rectangle
rect_w, rect_h = 500, 400  # Width and height of the rectangle

# for gesture recognition
prev_frames_left = deque()
prev_frames_right = deque()

############################################################## FUNCTION DEFINITIONS ############################################################################

def is_hand_inside_rectangle(hand_landmarks, rect_x, rect_y, rect_w, rect_h):
    for point in hand_landmarks:
        if not (rect_x <= point[0] <= rect_x + rect_w and rect_y <= point[1] <= rect_y + rect_h):
            return False
    return True

def detect_swipe(prev_landmarks, curr_landmarks):
    x_diff = curr_landmarks[8][0] - prev_landmarks[8][0]
    y_diff = curr_landmarks[8][1] - prev_landmarks[8][1]

    if abs(x_diff) > SWIPE_THRESHOLD and abs(y_diff) < SWIPE_THRESHOLD / 2:
        return "right" if x_diff > 0 else "left"
    return None

def switch_tab_right():
    pyautogui.hotkey('alt', 'tab')

def switch_tab_left():
    pyautogui.hotkey('alt', 'shift', 'tab')

def play_pause():
    pyautogui.press('space')

def arrow_key_right():
    pyautogui.press('right')

def arrow_key_left():
    pyautogui.press('left')

def minimize_window():
    pyautogui.hotkey('win', 'down')

def close_window():
    pyautogui.hotkey('alt', 'f4')

def maximize_window():
    pyautogui.hotkey('win', 'up')

def display_all_apps():
    pyautogui.hotkey('win', 'tab')

def minimize_all_apps():
    pyautogui.hotkey('win', 'd')
def Enter():
    pyautogui.hotkey('enter')
############################################################# END OF FUNCTION DEFINITIONS #######################################################################

for gesture, action in dict.items():
    print(gesture, action)

    if action == 'Play/Pause':
        dict[gesture] = play_pause
    
    elif action == 'Left Arrow Key':
        dict[gesture] = arrow_key_left
    
    elif action == 'Right Arrow Key':
        dict[gesture] = arrow_key_right
    
    elif action == 'Switch App':
        dict[gesture] = switch_tab_right

    elif action == 'Display All Apps':
        dict[gesture] = display_all_apps
    
    elif action == 'Minimize All Apps':
        dict[gesture] = minimize_all_apps
    elif action == 'Press enter key':
        dict[gesture] = Enter


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_w, rect_y + rect_h), (0, 255, 0), 2)

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
        prev_frames_left, label = gg.get_prediction(left, prev_frames_left, DELAY_IN_FRAMES=25)
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
        cv2.putText(img, 'GESTURE', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0: #and is_hand_inside_rectangle(right, rect_x, rect_y, rect_w, rect_h):
            prev_frames_right, label = gg.get_prediction(right, prev_frames_right, DELAY_IN_FRAMES=1)
            if prev_right_lndmarks:
                direction = detect_swipe(prev_right_lndmarks, right)
                current_time = time.time()
                if direction and current_time - last_swipe_time > DEBOUNCE_TIME:
                    if label == 'Three' or prev_gesture == 'Three':
                        print("3 finger " + direction + " swipe detected")

                        if direction == "right":
                            dict['Three Finger Swipe Right']()
                        else:
                            dict['Three Finger Swipe Left']()

                        last_swipe_time = current_time
                    else:
                        print(f"Detected swipe: {direction}")
                        
                        if direction == "left" or direction == "right":
                            dict['Hand Swipe']()

                        last_swipe_time = current_time
                    prev_right_lndmarks = []
                    continue

            if label == 'Fist' and prev_gesture == 'Five':
                print("Make Fist")
                dict['Make Fist']()
            elif label == 'Three' and prev_gesture == 'Fist':
                print("Three Finger Swipe Up")
                dict['Three Finger Swipe Up']()
            elif label == 'Fist' and prev_gesture == 'Two':
                print("Two Finger Swipe Down")
                dict['Two Finger Swipe Down']()
            elif label == 'Fist' and prev_gesture == 'One':
                print("Index finger down")
                dict['One Finger Down']()
                

            # Update previous landmarks
            prev_right_lndmarks = right
            prev_gesture = label



    elif MODE == 2:
        cv2.putText(img, 'BRIGHTNESS', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if is_hand_inside_rectangle(right, rect_x + 50, rect_y + 50, rect_w - 50, rect_h - 50):
            img = set_brightness(img, right, tracker)
    
    
    
    elif MODE == 3:
        cv2.putText(img, 'VOLUME', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if is_hand_inside_rectangle(right, rect_x + 50, rect_y + 50, rect_w - 50, rect_h - 50):
            img, volumePrev = set_volume(img, right, tracker, volumePrev)
    

    
    elif MODE == 4:
        cv2.putText(img, 'CURSOR', (100, 60), fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=2, color=(0, 0, 255), thickness=2)
        if len(right) > 0:
            fingersUp = tracker.fingersUp(right)
            if fingersUp[1] == 1 and fingersUp[2] == 0:
                xFinger, yFinger = right[8]
                xMouse = np.interp(xFinger, (rect_x + 50, rect_x + rect_w - 150), (0, wScreen))
                yMouse = np.interp(yFinger, (rect_y + 50, rect_y + rect_h - 150), (0, hScreen))

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
        
        cv2.putText(img, text, (100, 120), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)

    if cv2.waitKey(1) & 0xFF == ord('-'):
        break

    cv2.imshow('Main', img)

cap.release()
cv2.destroyAllWindows()
    