import mediapipe as mp
import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import cv2
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Matplotlib
plt.ion()  # Interactive mode ON
fig, ax = plt.subplots()
ax.set_title("Slide Controller")
ax.set_xlim(0, 640)
ax.set_ylim(0, 480)
line, = ax.plot([], [], 'ro', markersize=10)

# Cooldown Variables
last_gesture = None
gesture_time = time.time()

# Open Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Convert to RGB (for MediaPipe)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Clear previous points
    line.set_data([], [])

    # If a hand is detected
    raised_fingers = 0
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get landmarks
            landmark_list = [(lm.x * 640, lm.y * 480) for lm in hand_landmarks.landmark]

            # Draw hand landmarks in Matplotlib
            x_vals, y_vals = zip(*landmark_list)
            line.set_data(x_vals, y_vals)

            # Count raised fingers (1 = index, 2 = middle, 3 = ring, 4 = pinky)
            finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
            raised_fingers = sum(1 for tip in finger_tips if landmark_list[tip][1] < landmark_list[tip - 2][1])

            # Detect gestures (with cooldown)
            current_time = time.time()
            if raised_fingers == 2 and last_gesture != "prev" and (current_time - gesture_time > 1):
                print("Previous Slide")
                pyautogui.press("left")  # Works for PowerPoint, Google Slides, PDFs
                last_gesture = "prev"
                gesture_time = current_time

            elif raised_fingers == 4 and last_gesture != "next" and (current_time - gesture_time > 1):
                print("Next Slide")
                pyautogui.press("right")  # Works for PowerPoint, Google Slides, PDFs
                last_gesture = "next"
                gesture_time = current_time

            # Reset when hand is closed
            elif raised_fingers == 0:
                last_gesture = None  # Ready for next gesture

    # Update Matplotlib plot
    ax.set_title(f"Detected Fingers: {raised_fingers}")
    plt.draw()
    plt.pause(0.001)

# Release camera
cap.release()
plt.close()
