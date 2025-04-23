import tkinter as tk
from tkinter import messagebox
import hashlib
import json
import os

DATA_FILE = "users.json"
current_user = None

# Load and Save Functions
def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Main GUI functions
def show_login():
    clear_window()
    
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        users = load_users()

        if username in users and users[username]['password'] == hash_password(password):
            global current_user
            current_user = username
            show_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_frame = tk.Frame(root, bg="lightblue")
    login_frame.pack(expand=True)

    tk.Label(login_frame, text="Login to Project Bank", font=("Helvetica", 18, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)
    
    tk.Label(login_frame, text="Username:", bg="lightblue").pack(pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.pack()

    tk.Label(login_frame, text="Password:", bg="lightblue").pack(pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.pack()

    tk.Button(login_frame, text="Login", command=attempt_login, bg="darkblue", fg="white").pack(pady=10)
    tk.Button(login_frame, text="Sign Up", command=show_signup, bg="white").pack(pady=5)

def show_signup():
    clear_window()

    def attempt_signup():
        username = username_entry.get()
        password = password_entry.get()
        confirm = confirm_entry.get()
        users = load_users()

        if username in users:
            messagebox.showerror("Signup Failed", "Username already exists.")
        elif password != confirm:
            messagebox.showerror("Signup Failed", "Passwords do not match.")
        else:
            users[username] = {
                'password': hash_password(password),
                'balance': 0.0
            }
            save_users(users)
            messagebox.showinfo("Signup Successful", f"Welcome to Project Bank, {username}!")
            show_login()

    signup_frame = tk.Frame(root, bg="lightblue")
    signup_frame.pack(expand=True)

    tk.Label(signup_frame, text="Create New Account", font=("Helvetica", 18, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)
    
    tk.Label(signup_frame, text="Username:", bg="lightblue").pack()
    username_entry = tk.Entry(signup_frame)
    username_entry.pack()

    tk.Label(signup_frame, text="Password:", bg="lightblue").pack()
    password_entry = tk.Entry(signup_frame, show="*")
    password_entry.pack()

    tk.Label(signup_frame, text="Confirm Password:", bg="lightblue").pack()
    confirm_entry = tk.Entry(signup_frame, show="*")
    confirm_entry.pack()

    tk.Button(signup_frame, text="Sign Up", command=attempt_signup, bg="darkblue", fg="white").pack(pady=10)
    tk.Button(signup_frame, text="Back to Login", command=show_login, bg="white").pack()

def show_dashboard():
    clear_window()
    users = load_users()
    balance = users[current_user]['balance']

    dashboard_frame = tk.Frame(root, bg="lightblue")
    dashboard_frame.pack(expand=True)

    tk.Label(dashboard_frame, text=f"Welcome, {current_user}!", font=("Helvetica", 20, "bold"), bg="lightblue", fg="darkblue").pack(pady=20)
    tk.Label(dashboard_frame, text=f"Your Balance: ${balance:.2f}", font=("Helvetica", 16), bg="lightblue").pack(pady=10)

    tk.Button(dashboard_frame, text="Logout", command=logout, bg="darkblue", fg="white").pack(pady=20)

def logout():
    global current_user
    current_user = None
    show_login()

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Main window setup
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Project Bank")
    root.state("zoomed")  # Full screen
    root.configure(bg="lightblue")
    show_login()
    root.mainloop()
