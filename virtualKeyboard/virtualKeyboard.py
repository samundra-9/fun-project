import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller

# Initialize
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
keyboard = Controller()

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"]
]

# To track fingertip position changes
previous_finger_y = None
tap_detected = False  # Flag to prevent multiple key presses per tap

def draw_keyboard(img, keys):
    """Draws the keyboard layout on the screen."""
    for row_index, row in enumerate(keys):
        for key_index, key in enumerate(row):
            x, y = key_index * 60 + 50, row_index * 60 + 200
            cv2.rectangle(img, (x, y), (x + 50, y + 50), (255, 0, 0), 2)
            cv2.putText(img, key, (x + 15, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def detect_finger_tap(hand_landmarks, img):
    """Detects a downward finger tap and presses a key when detected."""
    global previous_finger_y, tap_detected

    # Get index fingertip position
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    x, y = int(index_tip.x * img.shape[1]), int(index_tip.y * img.shape[0])

    # Check if finger moved downward
    if previous_finger_y is not None:
        movement = y - previous_finger_y  # Positive value means downward motion

        if movement > 10:  # Finger moved down
            tap_detected = True

        if movement < -10 and tap_detected:  # Finger moved up after tap
            tap_detected = False  # Reset flag

            # Check if fingertip is over a key
            for row_index, row in enumerate(keys):
                for key_index, key in enumerate(row):
                    key_x, key_y = key_index * 60 + 50, row_index * 60 + 200
                    if key_x < x < key_x + 50 and key_y < y < key_y + 50:
                        keyboard.press(key)
                        keyboard.release(key)
                        print(f"Key Pressed: {key}")

    # Update previous finger y-position
    previous_finger_y = y

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(rgb_frame)
    
    draw_keyboard(frame, keys)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            detect_finger_tap(hand_landmarks, frame)
    
    cv2.imshow("Gesture-Based Virtual Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

