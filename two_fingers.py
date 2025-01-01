import cv2
import mediapipe as mp
import time
import pyautogui

# Initialize Mediapipe and PyAutoGUI
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)

# Variables for gesture detection
two_fingers_start_time = None
static_threshold = 2  # Seconds to detect static gesture
previous_y_positions = None

# Helper function to check if two fingers are static
def is_two_fingers_static(landmarks):
    index_finger_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_finger_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    wrist = landmarks[mp_hands.HandLandmark.WRIST]

    # Check if both fingers are extended and above the wrist
    return (index_finger_tip.y < wrist.y and
            middle_finger_tip.y < wrist.y and
            abs(index_finger_tip.x - middle_finger_tip.x) < 0.05)

# Helper function to check for two-finger swipe down
def is_two_finger_swipe_down(landmarks, previous_positions):
    if previous_positions is None:
        return False

    current_positions = [
        landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
        landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    ]

    # Check if both fingers moved downward significantly
    return (current_positions[0] - previous_positions[0] > 0.05 and
            current_positions[1] - previous_positions[1] > 0.05)

# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam.")
        break

    # Flip and preprocess frame
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect two-finger static gesture
            if is_two_fingers_static(hand_landmarks.landmark):
                if two_fingers_start_time is None:
                    two_fingers_start_time = time.time()  # Start the timer
                elif time.time() - two_fingers_start_time >= static_threshold:
                    print("Two Fingers Static Gesture Detected!")
                    #pyautogui.hotkey('alt', 'space') # Open the window menu
                    #pyautogui.press('n')  # Minimize the current window
                    two_fingers_start_time = None  # Reset the timer
            else:
                two_fingers_start_time = None  # Reset if fingers aren't static

            # Detect two-finger swipe down gesture
            if is_two_finger_swipe_down(hand_landmarks.landmark, previous_y_positions):
                print("Two-Finger Swipe Down Gesture Detected!")
                #pyautogui.hotkey('win', 'm')  # Minimize all windows
                previous_y_positions = None  # Reset tracking to avoid repeated actions
                break

            # Update previous positions for swipe detection
            previous_y_positions = [
                hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y,
                hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ]
    else:
        print("No hand landmarks detected.")  # Debugging message

    # Display the frame
    cv2.imshow('Hand Gesture Recognition', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
