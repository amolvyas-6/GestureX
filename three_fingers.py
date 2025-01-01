import cv2
import mediapipe as mp
import pyautogui
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

previous_y_positions = None

def is_swipe_up(landmarks, previous_positions):

    current_y_positions = [
        landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
        landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
        landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
    ]
    
    pip_y_positions = [
        landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
        landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y,
        landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y
    ]

    if previous_positions is not None:
        motion = [previous - current for previous, current in zip(previous_positions, current_y_positions)]
        
        if all(m > 0.05 for m in motion):
            if all(tip < pip for tip, pip in zip(current_y_positions, pip_y_positions)):
                return True
    
    return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_swipe_up(hand_landmarks.landmark, previous_y_positions):
                print("Swipe Up Gesture Detected!")
                #pyautogui.hotkey('win', 'tab') 
                previous_y_positions = None
                break

            previous_y_positions = [
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y,
                hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
            ]

    cv2.imshow('Hand Gesture Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
