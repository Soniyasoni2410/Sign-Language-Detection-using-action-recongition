import sqlite3  # For database connection
from tkinter import *
from tkinter import messagebox  # For pop-up messages
from PIL import ImageTk
import os  # To run the signin.py script

# Functionality for the forget password window
def forget_password():
    # Create a new window for forget password
    forget_window = Tk()
    forget_window.geometry('990x660+50+50')
    forget_window.resizable(0, 0)
    forget_window.title('Forget Password')

    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bgLabel = Label(forget_window, image=bgImage)
    bgLabel.place(x=0, y=0)

    # Heading for the forget password page
    heading = Label(forget_window, text='Reset Password', font=('Microsoft Yahei UI Light', 23, 'bold'), bg='white', fg='firebrick1')
    heading.place(x=605, y=100)

    # Username Entry
    usernameEntry = Entry(forget_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1')
    usernameEntry.place(x=580, y=180)
    usernameEntry.insert(0, 'Username')

    frame1 = Frame(forget_window, width=250, height=2, bg='firebrick1')
    frame1.place(x=580, y=202)

    # Adding the project title on the left side
    title_label = Label(forget_window, text='Sign Language Detection \nUsing Action Recognition',
                        font=('Microsoft Yahei UI Light', 20, 'bold'), bg='#FFECD9', fg='firebrick1')
    title_label.place(x=168, y=100)

    # New Password Entry
    newPasswordEntry = Entry(forget_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1', show='')
    newPasswordEntry.place(x=580, y=240)
    newPasswordEntry.insert(0, 'New Password')

    frame2 = Frame(forget_window, width=250, height=2, bg='firebrick1')
    frame2.place(x=580, y=262)

    # Confirm Password Entry
    confirmPasswordEntry = Entry(forget_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='firebrick1', show='')
    confirmPasswordEntry.place(x=580, y=300)
    confirmPasswordEntry.insert(0, 'Confirm Password')

    frame3 = Frame(forget_window, width=250, height=2, bg='firebrick1')
    frame3.place(x=580, y=322)

    # Function to change password in the database
    def submit():
        username = usernameEntry.get()
        new_password = newPasswordEntry.get()
        confirm_password = confirmPasswordEntry.get()

        if new_password == confirm_password:
            # Connect to the SQLite database
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            # Check if the user exists
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

            if user:
                # Update the password in the database
                cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
                conn.commit()  # Save changes
                messagebox.showinfo("Success", "Password changed successfully!")
                forget_window.destroy()  # Close the forget password window
                os.system('python signin.py')  # Open the login page (signin.py)
            else:
                # Show error message if username is not found
                messagebox.showerror("Error", "Username not found")

            # Closing the database connection
            conn.close()
        else:
            # Show error message if passwords do not match
            messagebox.showerror("Error", "Passwords do not match")

    # Submit Button
    submitButton = Button(forget_window, text='Submit', font=('Open Sans', 16, 'bold'),
                          fg='white', bg='firebrick1', activeforeground='white', activebackground='firebrick1',
                          cursor='hand2', bd=0, width=19, command=submit)  # Added submit function
    submitButton.place(x=578, y=380)

    forget_window.mainloop()

# Call forget_password to test the window
forget_password()
