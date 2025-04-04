import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Initialize OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Function to apply effects
def apply_effects(frame, effect):
    if effect == 'grayscale':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif effect == 'sepia':
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        return cv2.transform(frame, sepia_filter)
    elif effect == 'blur':
        return cv2.GaussianBlur(frame, (15, 15), 0)
    return frame

# State variables
zoom_level = 1.0
current_effect = None
previous_finger_count = -1

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        finger_count = 0

        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = hand_landmarks.landmark
                lm = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]

                # Count fingers
                if lm[4][0] > lm[3][0]:  # Thumb
                    finger_count += 1

                for tip, pip in zip([8, 12, 16, 20], [6, 10, 14, 18]):
                    if lm[tip][1] < lm[pip][1]:
                        finger_count += 1

                # Handle transitions
                if previous_finger_count == 1 and finger_count != 1:
                    zoom_level = 1.0  # Reset zoom if 1 finger is removed

                # Handle actions
                if finger_count == 0:
                    current_effect = None
                elif finger_count == 1:
                    zoom_level = 2.0
                elif finger_count == 2:
                    current_effect = 'sepia'
                elif finger_count == 3:
                    current_effect = 'blur'
                elif finger_count == 4:
                    current_effect = 'grayscale'
                elif finger_count == 5:
                    zoom_level = 1.0
                    current_effect = None

                previous_finger_count = finger_count

        # Apply zoom
        frame = cv2.resize(frame, (int(w * zoom_level), int(h * zoom_level)))
        h_zoom, w_zoom, _ = frame.shape
        if zoom_level > 1.0:
            x_start = (w_zoom - w) // 2
            y_start = (h_zoom - h) // 2
            frame = frame[y_start:y_start + h, x_start:x_start + w]

        # Apply selected effect
        if current_effect:
            frame = apply_effects(frame, current_effect)
            if current_effect == 'grayscale':
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Display info
        cv2.putText(frame, f'Fingers: {finger_count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
        cv2.putText(frame, f'Effect: {current_effect or "None"}', (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
        cv2.putText(frame, f'Zoom: {zoom_level:.1f}x', (10, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Gesture Zoom & Effects', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
