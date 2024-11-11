import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pickle
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import threading
import subprocess

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Labels dictionary
labels_dict = {0: 'Hello', 1: 'Peace', 2: 'Love_you'}

# Create a tkinter window
root = tk.Tk()
root.title("Sign Detection")
root.geometry("990x660+50+50")

# Title label
title_label = Label(root, text="Sign Detection", font=("Helvetica", 24, "bold"), fg="firebrick1")
title_label.pack(pady=20)

# Video label for displaying camera feed
video_label = Label(root)
video_label.pack()

# Control variables
detection_active = False

def detect_signs():
    global detection_active
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Set a lower width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Set a lower height

    while detection_active:
        ret, frame = cap.read()
        if not ret:
            break

        # Process every 3rd frame to reduce lag
        frame_counter = 0
        if frame_counter % 3 == 0:
            data_aux = []
            x_ = []
            y_ = []

            H, W, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Extract landmark positions
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

                    # Make predictions
                    try:
                        prediction = model.predict([np.asarray(data_aux)])
                        predicted_character = labels_dict[int(prediction[0])]
                        print("Predicted character: ", predicted_character)

                        # Draw bounding box and prediction text
                        x1 = int(min(x_) * W) - 10
                        y1 = int(min(y_) * H) - 10
                        x2 = int(max(x_) * W) - 10
                        y2 = int(max(y_) * H) - 10

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)

                    except Exception as e:
                        print("Error during prediction:", e)

            # Convert frame to PhotoImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
            img = Image.fromarray(frame)
            img = img.resize((640, 480), Image.LANCZOS)  # Resize for better fit
            img_tk = ImageTk.PhotoImage(image=img)

            # Update the label with the new frame
            if root.winfo_exists():
                video_label.imgtk = img_tk
                video_label.configure(image=img_tk)
                video_label.update_idletasks()  # Process idle tasks

        frame_counter += 1

    cap.release()

def start_detection():
    global detection_active
    detection_active = True
    threading.Thread(target=detect_signs).start()  # Start detection in a new thread

def stop_detection():
    global detection_active
    detection_active = False
    root.destroy()  # Close the current window
    subprocess.Popen(['python', 'homepage.py'])  # Open homepage.py

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

# Start and Stop buttons
start_button = Button(button_frame, text="Start Detection", command=start_detection, bg='firebrick1', font=("Helvetica", 14))
start_button.pack(side=tk.LEFT, padx=10)

stop_button = Button(button_frame, text="Stop Detection", command=stop_detection, bg='firebrick1', font=("Helvetica", 14))
stop_button.pack(side=tk.LEFT, padx=10)

# Run the tkinter main loop
root.mainloop()
