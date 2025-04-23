import tkinter as tk
from tkinter import messagebox
from backend import User
import os

current_user = None
users = {}

if os.path.exists("users.txt"):
    with open("users.txt", "r") as f:
        for line in f:
            username, password, balance = line.strip().split(',')
            users[username] = User(username, password, float(balance))

def save_users():
    with open("users.txt", "w") as f:
        for user in users.values():
            f.write(f"{user.username},{user.password},{user.balance}\n")

def signup():
    username = signup_username_entry.get()
    password = signup_password_entry.get()
    confirm_password = signup_confirm_entry.get()
    if username in users:
        messagebox.showerror("Error", "User already exists.")
    elif password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
    else:
        user = User(username, password)
        users[username] = user
        save_users()
        messagebox.showinfo("Welcome!", f"Welcome to Project Bank, {username}!")
        show_login_frame()

def login():
    global current_user
    username = login_username_entry.get()
    password = login_password_entry.get()
    user = users.get(username)
    if user and user.password == password:
        current_user = user
        show_dashboard()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def logout():
    global current_user
    current_user = None
    show_login_frame()

def show_signup_frame():
    login_frame.pack_forget()
    dashboard_frame.pack_forget()
    signup_frame.pack(pady=50)

def show_login_frame():
    signup_frame.pack_forget()
    dashboard_frame.pack_forget()
    login_frame.pack(pady=50)

def show_dashboard():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    dashboard_frame.pack(pady=50)
    balance_label.config(text=f"Balance: ${current_user.balance:.2f}")

# GUI
root = tk.Tk()
root.title("Project Bank")
root.geometry("500x500")
root.configure(bg="#E0F7FA")

# Header
header_frame = tk.Frame(root, bg="#0D47A1", height=80)
header_frame.pack(fill=tk.X)

tk.Label(header_frame, text="🏦 Project Bank", bg="#0D47A1", fg="white",
         font=("Helvetica", 24, "bold")).pack(pady=20)

# Login Frame
login_frame = tk.Frame(root, bg="#E0F7FA")
tk.Label(login_frame, text="Login", font=("Helvetica", 20), bg="#E0F7FA").pack()
tk.Label(login_frame, text="Username:", bg="#E0F7FA").pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()
tk.Label(login_frame, text="Password:", bg="#E0F7FA").pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()
tk.Button(login_frame, text="Login", command=login).pack(pady=10)
tk.Button(login_frame, text="Signup", command=show_signup_frame).pack()

# Signup Frame
signup_frame = tk.Frame(root, bg="#E0F7FA")
tk.Label(signup_frame, text="Signup", font=("Helvetica", 20), bg="#E0F7FA").pack()
tk.Label(signup_frame, text="Username:", bg="#E0F7FA").pack()
signup_username_entry = tk.Entry(signup_frame)
signup_username_entry.pack()
tk.Label(signup_frame, text="Password:", bg="#E0F7FA").pack()
signup_password_entry = tk.Entry(signup_frame, show="*")
signup_password_entry.pack()
tk.Label(signup_frame, text="Confirm Password:", bg="#E0F7FA").pack()
signup_confirm_entry = tk.Entry(signup_frame, show="*")
signup_confirm_entry.pack()
tk.Button(signup_frame, text="Signup", command=signup).pack(pady=10)
tk.Button(signup_frame, text="Back to Login", command=show_login_frame).pack()

# Dashboard Frame
dashboard_frame = tk.Frame(root, bg="#E0F7FA")
tk.Label(dashboard_frame, text="Welcome to Your Dashboard", font=("Helvetica", 18), bg="#E0F7FA").pack()
balance_label = tk.Label(dashboard_frame, text="", font=("Helvetica", 16), bg="#E0F7FA")
balance_label.pack(pady=10)
tk.Button(dashboard_frame, text="Logout", command=logout).pack(pady=10)

# Show login first
show_login_frame()
root.mainloop()
