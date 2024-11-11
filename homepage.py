from tkinter import *
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow
import os  # Import the os module to run other scripts

class HomePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Sign Language Detection")
        self.root.geometry("990x660+50+50")

        # Load background image using PIL
        self.bg_image = Image.open("firebrick.png")  # Ensure the file path is correct
        self.bg_image = self.bg_image.resize((990, 660), Image.LANCZOS)  # Resize image to fit window
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)  # Convert image for Tkinter

        # Set background image
        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a navigation menu with enhanced style
        self.create_menu()

        # Create a frame for displaying content with a border and set the same pink color
        self.content_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        self.content_frame.place(x=50, y=100, width=890, height=500)

        # Create a canvas for scrolling
        self.canvas = Canvas(self.content_frame, bg="white")
        self.scrollbar = Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Show the home page content by default
        self.show_home_page()

    def create_menu(self):
        # Create a styled frame for the menu bar with the exact pink color
        menu_frame = Frame(self.root, bg="white")  # Use exact deep pink color
        menu_frame.pack(side=TOP, fill=X)

        # Create labels for navigation with modern font and hover effects
        self.create_menu_label(menu_frame, "Home", self.show_home_page)
        self.create_menu_label(menu_frame, "About Us", self.show_about_us)
        self.create_menu_label(menu_frame, "Convert", self.open_convert)
        self.create_menu_label(menu_frame, "Sign Detection", self.open_sign_detection)
        self.create_menu_label(menu_frame, "Logout", self.logout)

    def create_menu_label(self, parent, text, command):
        label = Label(parent, text=text, bg="white", fg="Black", font=("Arial", 12, "bold"))  # Use the same pink color
        label.pack(side=LEFT, padx=20, pady=10)
        label.bind("<Button-1>", lambda e: command())
        label.bind("<Enter>", lambda e: label.config(fg="#FF6347"))  # Change color on hover (tomato color)
        label.bind("<Leave>", lambda e: label.config(fg="Black"))  # Reset color on leave

    def clear_content(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_home_page(self):
        self.clear_content()
        title = Label(self.scrollable_frame, text="Sign Language Detection Using Action Recognition", font=("Helvetica", 24, "bold"), bg="white", fg="light coral")
        title.pack(pady=20)

        subtitle = Label(self.scrollable_frame, text="Revolutionizing Communication Accessibility", font=("Arial", 16), bg="white", wraplength=800)
        subtitle.pack(pady=10)

        description = Label(self.scrollable_frame,
                            text="Our innovative technology utilizes computer vision and machine learning to recognize and interpret sign language gestures in real-time, bridging the communication gap between the deaf and hearing communities.",
                            font=("Arial", 14), bg="white", wraplength=800)
        description.pack(pady=10)

    def show_about_us(self):
        self.clear_content()
        label = Label(self.scrollable_frame, text="About Us", font=("Helvetica", 24, "bold"), bg="white")
        label.pack(pady=20)

        about_text = ("Sign Language Detection Using Action Recognition is an innovative project aimed at bridging "
                      "the communication gap between the hearing and speech-impaired community and the rest of the world. "
                      "Our solution uses advanced machine learning algorithms and computer vision technology to recognize "
                      "and interpret sign language in real time, providing an intuitive way to convert hand gestures into meaningful text or speech.")
        about_label = Label(self.scrollable_frame, text=about_text, font=("Arial", 14), bg="white", wraplength=800, justify="left")
        about_label.pack(pady=10)

        mission_label = Label(self.scrollable_frame, text="Our Mission", font=("Helvetica", 20, "bold"), bg="white")
        mission_label.pack(pady=10)

        mission_text = ("Our mission is to make communication more inclusive and accessible for everyone. By leveraging "
                        "the power of technology, we strive to empower individuals who rely on sign language as their primary means of communication, "
                        "enabling them to interact seamlessly with people who may not understand it.")
        mission_description = Label(self.scrollable_frame, text=mission_text, font=("Arial", 14), bg="white", wraplength=800, justify="left")
        mission_description.pack(pady=10)

        how_it_works_label = Label(self.scrollable_frame, text="How It Works", font=("Helvetica", 20, "bold"), bg="white")
        how_it_works_label.pack(pady=10)

        works_text = ("The project utilizes action recognition techniques through machine learning and computer vision tools such as MediaPipe, OpenCV, and TensorFlow. "
                      "These technologies work together to detect hand movements, identify specific gestures, and translate them into recognizable characters, words, or phrases. "
                      "Whether through live video feeds or pre-recorded clips, our system ensures accurate and fast sign language recognition.")
        works_description = Label(self.scrollable_frame, text=works_text, font=("Arial", 14), bg="white", wraplength=800, justify="left")
        works_description.pack(pady=10)

    def open_convert(self):
        os.system('python convert.py')  # Open convert.py script

    def open_sign_detection(self):
        os.system('python detection.py')  # Open detection.py script

    def logout(self):
        os.system('python signin.py')  # Open signin.py script

if __name__ == "__main__":
    root = Tk()
    app = HomePage(root)
    root.mainloop()
