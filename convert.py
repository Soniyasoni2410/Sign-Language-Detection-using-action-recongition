import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import cv2
from PIL import Image, ImageTk
import os
import subprocess  # Import subprocess to run the homepage script

class ConvertApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Convert Text/Audio to Sign Language")
        self.master.geometry('990x660+50+50')
        self.master.config(bg="#f0f0f0")  # Light background color for the main window

        # Main frame to hold everything
        main_frame = tk.Frame(self.master, bg="#ffffff", bd=2, relief=tk.RAISED)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left frame for text entry, buttons, and detected signs
        left_frame = tk.Frame(main_frame, bg="#ffffff")
        left_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH)

        # Right frame for video display and detected signs
        right_frame = tk.Frame(main_frame, bg="#ffffff")
        right_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH)

        # Label for user instructions
        self.label = tk.Label(left_frame, text="Type your text or click on mic to speak", font=("Arial", 16), bg="#ffffff", fg="firebrick1")
        self.label.grid(row=0, column=0, columnspan=3, pady=20)

        # Text entry for user input
        self.text_entry = tk.Entry(left_frame, width=40, font=("Arial", 14), bd=2, relief=tk.SUNKEN)
        self.text_entry.grid(row=1, column=0, padx=10)

        # Convert button next to text entry
        self.convert_button = tk.Button(left_frame, text="Convert", command=self.convert_text, font=("Arial", 14), bg="firebrick1", fg="white", activebackground="white")
        self.convert_button.grid(row=1, column=1, padx=5)

        # Mic button with an image, placed next to Convert button
        self.mic_image = Image.open("mic.png")  # Replace with your mic image path
        self.mic_image = self.mic_image.resize((50, 50), Image.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(self.mic_image)
        self.speak_button = tk.Button(left_frame, image=self.mic_photo, command=self.speak_audio, borderwidth=0)
        self.speak_button.grid(row=1, column=2, padx=5)

        # Label to show detected signs
        self.detected_signs_label = tk.Label(left_frame, text="Detected Signs:", font=("Arial", 16), bg="#ffffff")
        self.detected_signs_label.grid(row=2, column=0, columnspan=2, pady=20)

        # Listbox for detected signs
        self.detected_signs_list = tk.Listbox(left_frame, width=40, height=10, font=("Arial", 12), bg="#f9f9f9", bd=2, relief=tk.SUNKEN)
        self.detected_signs_list.grid(row=3, column=0, columnspan=2, padx=10)

        # Placeholder for displaying videos in right frame
        self.video_label = tk.Label(right_frame)
        self.video_label.pack(padx=30, pady=(50, 50))  # Add more padding on the top to move it down

        # Load video paths from the dataset directory
        self.sign_dict = self.load_signs()

        # Button to navigate to homepage
        self.home_button = tk.Button(left_frame, text="Go to Homepage", command=self.go_to_homepage, font=("Arial", 14), bg="firebrick1", fg="white", activebackground="white")
        self.home_button.grid(row=4, column=0, pady=(20, 0), columnspan=2)

        # Footer for copyright notice
        self.footer = tk.Label(main_frame, text="© 2024 Sign Language Detection System", bg="#ffffff", font=("Arial", 10))
        self.footer.pack(side=tk.BOTTOM, pady=50)

    def load_signs(self):
        sign_dict = {}
        dataset_path = "C:/Users/soniy/Downloads/archive (1)/INDIAN SIGN LANGUAGE ANIMATED VIDEOS/"
        for filename in os.listdir(dataset_path):
            if filename.endswith('.mp4'):
                sign_name = filename[:-4].lower()  # Remove '.mp4' extension
                sign_dict[sign_name] = os.path.join(dataset_path, filename)
        return sign_dict

    def convert_text(self):
        user_input = self.text_entry.get()
        if user_input:
            self.play_sign_videos(user_input)
        else:
            messagebox.showwarning("Input Error", "Please enter some text.")

    def speak_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Listening...")
            audio = recognizer.listen(source)
            self.label.config(text="Recognizing...")
            try:
                user_input = recognizer.recognize_google(audio)
                self.text_entry.delete(0, tk.END)
                self.text_entry.insert(0, user_input)
                self.play_sign_videos(user_input)
            except sr.UnknownValueError:
                messagebox.showerror("Recognition Error", "Could not understand audio.")
            except sr.RequestError:
                messagebox.showerror("API Error", "Could not request results from the recognition service.")

    def play_sign_videos(self, sentence):
        # Clear previously detected signs
        self.detected_signs_list.delete(0, tk.END)

        words = sentence.lower().split()
        found_videos = []

        for word in words:
            video_path = self.sign_dict.get(word)
            if video_path and os.path.exists(video_path):
                found_videos.append((word, video_path))
            else:
                print(f"Video not found for word: {word}")
                self.detected_signs_list.insert(tk.END, f"Sign for '{word}' not found.")
                messagebox.showwarning("Missing Sign", f"Sign for '{word}' not available.")

        if found_videos:
            self.result_label = tk.Label(self.master, text="Playing available signs.", bg="#ffffff")
            self.result_label.pack()
            self.play_videos_in_sequence(found_videos)

    def play_videos_in_sequence(self, videos):
        if not videos:
            return

        word, video_path = videos[0]
        self.detected_signs_list.insert(tk.END, f"Showing sign for: {word}")  # Update detected sign list

        cap = cv2.VideoCapture(video_path)

        def show_frame():
            ret, frame = cap.read()
            if ret:
                # Convert the frame to a format suitable for Tkinter
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                img = img.resize((400, 300), Image.LANCZOS)

                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)

                # Repeat after 20 ms
                self.video_label.after(20, show_frame)
            else:
                cap.release()
                # After finishing this video, move to the next one
                if len(videos) > 1:
                    self.play_videos_in_sequence(videos[1:])  # Recursively play the next video

        show_frame()  # Start playing the first video

    def go_to_homepage(self):
        self.master.destroy()  # Close the current window
        subprocess.Popen(['python', 'homepage.py'])  # Open homepage.py

if __name__ == "__main__":
    root = tk.Tk()
    app = ConvertApp(root)
    root.mainloop()
