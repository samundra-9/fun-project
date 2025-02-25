import cv2
import mediapipe as mp
import numpy as np
import math
import os

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

def set_volume(volume_percentage):
    """Set system volume on Linux using pactl."""
    volume_percentage = max(0, min(100, volume_percentage))
    os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {volume_percentage}%")

# Start webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if len(lm_list) >= 8:
                x1, y1 = lm_list[4][1], lm_list[4][2]  # Thumb tip
                x2, y2 = lm_list[8][1], lm_list[8][2]  # Index finger tip

                # Draw line & circles
                cv2.circle(frame, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

                # Calculate distance
                length = math.hypot(x2 - x1, y2 - y1)

                # Map distance to volume range (0-100%)
                volume_level = int(np.interp(length, [20, 200], [0, 100]))
                set_volume(volume_level)  # Set volume

                # Display volume
                cv2.putText(frame, f'Volume: {volume_level}%', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Gesture Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

