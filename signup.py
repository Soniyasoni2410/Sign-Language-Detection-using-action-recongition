import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import os  # Import os module to run other scripts

# Functionality Part
def hide_password():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    confirmPasswordEntry.config(show='*')
    eyeButton.config(command=show_password)

def show_password():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    confirmPasswordEntry.config(show='')
    eyeButton.config(command=hide_password)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def email_enter(event):
    if emailEntry.get() == 'Email':
        emailEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

def confirm_password_enter(event):
    if confirmPasswordEntry.get() == 'Confirm Password':
        confirmPasswordEntry.delete(0, END)

# Function to store user data in the database
def store_in_database():
    username = usernameEntry.get()
    email = emailEntry.get()
    password = passwordEntry.get()
    confirm_password = confirmPasswordEntry.get()

    # Basic validation to check if all fields are filled
    if username == "Username" or email == "Email" or password == "Password" or confirm_password == "Confirm Password":
        messagebox.showwarning("Input Error", "Please fill out all the fields.")
        return

    if password != confirm_password:
        messagebox.showerror("Password Error", "Passwords do not match.")
        return

    # Connecting to SQLite database
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Check if username or email already exists
    cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        messagebox.showerror("Duplicate Error", "Username or Email already exists. Please choose a different one.")
        conn.close()  # Close the database connection
        return

    # Creating a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Inserting the user data into the table
    cursor.execute('''
        INSERT INTO users (username, email, password) 
        VALUES (?, ?, ?)
    ''', (username, email, password))

    # Committing the transaction and closing the connection
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Account created successfully!")
    open_signin()  # Call to open the signin window after signup

# This function will be called when you click the "Login" button
def open_signin():
    signup_window.destroy()  # Close the current signup window
    os.system('python signin.py')  # Open signin.py script

# GUI part
signup_window = Tk()
signup_window.geometry('990x660+50+50')
signup_window.resizable(0, 0)
signup_window.title('Signup Page')

bgImage = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(signup_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(signup_window, text='Create Account', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white', fg='firebrick1')
heading.place(x=605, y=100)

# Username Entry
usernameEntry = Entry(signup_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
usernameEntry.place(x=580, y=180)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame1 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame1.place(x=580, y=202)

# Email Entry
emailEntry = Entry(signup_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
emailEntry.place(x=580, y=240)
emailEntry.insert(0, 'Email')
emailEntry.bind('<FocusIn>', email_enter)

frame2 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame2.place(x=580, y=262)

# Password Entry
passwordEntry = Entry(signup_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
passwordEntry.place(x=580, y=300)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame3 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame3.place(x=580, y=322)

# Confirm Password Entry
confirmPasswordEntry = Entry(signup_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
confirmPasswordEntry.place(x=580, y=360)
confirmPasswordEntry.insert(0, 'Confirm Password')
confirmPasswordEntry.bind('<FocusIn>', confirm_password_enter)

frame4 = Frame(signup_window, width=250, height=2, bg='firebrick1')
frame4.place(x=580, y=382)

# Eye Button for Show/Hide Password
openeye = PhotoImage(file='openeye.png')
eyeButton = Button(signup_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide_password)
eyeButton.place(x=800, y=297)

# Adding the project title on the left side
title_label = Label(signup_window, text='Sign Language Detection \nUsing Action Recognition',
                    font=('Microsoft Yahei UI Light', 20, 'bold'),bg='#FFECD9', fg='firebrick1')
title_label.place(x=168, y=100)

# Signup Button
signupButton = Button(signup_window, text='Signup', font=('Open Sans', 16, 'bold'),
                      fg='white', bg='firebrick1', activeforeground='white', activebackground='firebrick1',
                      cursor='hand2', bd=0, width=19, command=store_in_database)  # Link to store_in_database function
signupButton.place(x=578, y=420)

# Already have an account Label and Button
loginLabel = Label(signup_window, text='Already have an account?', font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white')
loginLabel.place(x=590, y=490)

# Login button will now open the signin.py page
loginButton = Button(signup_window, text='Login', font=('Open Sans', 9, 'bold underline'),
                     fg='blue', bg='white', activeforeground='blue', activebackground='white',
                     cursor='hand2', bd=0, command=open_signin)
loginButton.place(x=760, y=490)

signup_window.mainloop()
