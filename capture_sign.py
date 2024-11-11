import cv2
import mediapipe as mp
import os
import pickle
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to load custom signs
def load_custom_signs(data_folder='./sign_data/'):
    custom_signs = {}
    for file_name in os.listdir(data_folder):
        if file_name.endswith('.pkl'):
            file_path = os.path.join(data_folder, file_name)
            label = file_name.split('.')[0]  # Get label from the file name
            with open(file_path, 'rb') as f:
                sign_data = pickle.load(f)
            custom_signs[label] = sign_data
    return custom_signs

# Function to compare hand landmarks with custom signs
def match_sign(landmarks, custom_sign_data):
    threshold = 0.02  # Set a threshold for comparing the landmarks
    diff = np.linalg.norm(np.array(landmarks) - np.array(custom_sign_data))
    return diff < threshold

# Load all saved custom signs
custom_signs = load_custom_signs()

# Start capturing from the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            data_aux = []
            x_ = []
            y_ = []

            # Collect landmark data
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

            # Default label when no sign is matched
            detected_label = "Unknown Sign"

            # Check if the captured landmarks match any custom sign
            for label, custom_sign_data in custom_signs.items():
                if match_sign(data_aux, custom_sign_data):
                    detected_label = label
                    print(f"Sign Detected: {label}")
                    break  # Stop searching after the first match

            # Draw bounding box and show detected label
            x_min = int(min(x_) * frame.shape[1])
            y_min = int(min(y_) * frame.shape[0])
            x_max = int(max(x_) * frame.shape[1])
            y_max = int(max(y_) * frame.shape[0])

            # Draw rectangle around the detected hand
            cv2.rectangle(frame, (x_min - 10, y_min - 10), (x_max + 10, y_max + 10), (0, 255, 0), 2)
            # Put the detected label above the bounding box
            cv2.putText(frame, f"Sign: {detected_label}", (x_min, y_min - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Draw hand landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the captured frame with the label
    cv2.imshow("Sign Detection", frame)

    # Press 'q' to stop the video feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
