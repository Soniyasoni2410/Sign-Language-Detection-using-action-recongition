import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os  # Import the os module to run other scripts

# Functionality Part
def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

# Function to validate login credentials
def validate_login():
    username = usernameEntry.get()
    password = passwordEntry.get()

    # Connecting to SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Querying the database for matching username and password
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        open_homepage()  # Open homepage if login is successful
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")

    # Closing the database connection
    conn.close()

# This function will be called when you click the "Create New One" button
def open_signup():
    login_window.destroy()  # Close the current login window
    os.system('python signup.py')  # Open signup.py script

# This function will be called when you click the "Forget Password" button
def open_forgetpassword():
    login_window.destroy()  # Close the current login window
    os.system('python forgetpassword.py')  # Open forgetpassword.py script

def open_homepage():
    login_window.destroy()
    os.system('python homepage.py')

# GUI part
login_window = Tk()
login_window.geometry('990x660+50+50')
login_window.resizable(0, 0)
login_window.title('Login Page')

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

# Adding the project title on the left side
title_label = Label(login_window, text='Sign Language Detection \nUsing Action Recognition',
                    font=('Microsoft Yahei UI Light', 20, 'bold'),bg='#FFECD9', fg='firebrick1')
title_label.place(x=168, y=100)

heading = Label(login_window, text='User Login', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white', fg='firebrick1')
heading.place(x=605, y=120)

usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=200)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame1 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=222)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=260)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=282)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.place(x=800, y=255)

# Forget Password button will now open the forgetpassword.py page
forgetButton = Button(login_window, text='Forget Password', bd=0, bg='white', activebackground='white', cursor='hand2',
                      font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', activeforeground='firebrick1',
                      command=open_forgetpassword)  # Added command to open forgetpassword.py
forgetButton.place(x=715, y=295)

# Login button now validates credentials against the database
loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'),
                     fg='white', bg='firebrick1', activeforeground='white', activebackground='firebrick1',
                     cursor='hand2', bd=0, width=19, command=validate_login)  # Link to validate_login function
loginButton.place(x=578, y=358)

signupLabel = Label(login_window, text='Dont have an account?', font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white')
signupLabel.place(x=590, y=435)

# Create New One button will now open the signup.py page
newaccountButton = Button(login_window, text='Create New One', font=('Open Sans', 9, 'bold underline'),
                          fg='blue', bg='white', activeforeground='blue', activebackground='white',
                          cursor='hand2', bd=0, command=open_signup)  # Added command to open signup.py
newaccountButton.place(x=730, y=435)

login_window.mainloop()
