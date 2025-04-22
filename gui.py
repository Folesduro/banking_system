import tkinter as tk
from tkinter import messagebox, simpledialog
from backend.user import User
import json
import os

# ------------------ Data Persistence ------------------

USERS_FILE = "users.json"
users = {}

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
            for username, info in data.items():
                users[username] = User.from_dict(info)

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump({u: users[u].to_dict() for u in users}, f, indent=4)

# ------------------ GUI Functions ------------------

current_user = None

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username].check_password(password):
        current_user = users[username]
        messagebox.showinfo("Login", f"Welcome back, {username}!")
        show_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def signup():
    new_username = username_entry.get()
    new_password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if new_username in users:
        messagebox.showerror("Signup Failed", "Username already exists.")
        return

    if not new_username or not new_password or not confirm_password:
        messagebox.showerror("Signup Failed", "All fields are required.")
        return

    if new_password != confirm_password:
        messagebox.showerror("Signup Failed", "Passwords do not match.")
        return

    new_user = User(new_username, new_password)
    users[new_username] = new_user
    save_users()

    messagebox.showinfo("Signup Successful", f"Welcome to Project Bank, {new_username}!\nYour account has been created.")
    show_login()

def logout():
    global current_user
    current_user = None
    show_login()

def deposit():
    if not current_user:
        return
    try:
        amount = float(simpledialog.askstring("Deposit", "Enter amount to deposit:"))
        current_user.deposit(amount)
        save_users()
        messagebox.showinfo("Deposit", f"${amount:.2f} deposited successfully.")
        show_dashboard()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def withdraw():
    if not current_user:
        return
    try:
        amount = float(simpledialog.askstring("Withdraw", "Enter amount to withdraw:"))
        current_user.withdraw(amount)
        save_users()
        messagebox.showinfo("Withdraw", f"${amount:.2f} withdrawn successfully.")
        show_dashboard()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_balance():
    if not current_user:
        return
    balance = current_user.view_balance()
    messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")

def view_transactions():
    if not current_user:
        return
    history = current_user.view_transaction_history()
    if not history:
        messagebox.showinfo("Transactions", "No transactions yet.")
    else:
        history_str = "\n".join(history)
        messagebox.showinfo("Transactions", history_str)

# ------------------ UI Screens ------------------

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

def show_login():
    clear_screen()

    title_label = tk.Label(root, text="🏦 Project Bank", font=("Helvetica", 18, "bold"),
                           fg="dark blue", bg="light blue", pady=15)
    title_label.pack(fill="x")

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.pack(pady=30)

    global username_entry, password_entry, confirm_password_entry

    tk.Label(frame, text="Username:", font=("Helvetica", 11), bg="white").grid(row=0, column=0, sticky="w", pady=5)
    username_entry = tk.Entry(frame, font=("Helvetica", 11))
    username_entry.grid(row=0, column=1)

    tk.Label(frame, text="Password:", font=("Helvetica", 11), bg="white").grid(row=1, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(frame, show="*", font=("Helvetica", 11))
    password_entry.grid(row=1, column=1)

    tk.Label(frame, text="Confirm Password:", font=("Helvetica", 11), bg="white").grid(row=2, column=0, sticky="w", pady=5)
    confirm_password_entry = tk.Entry(frame, show="*", font=("Helvetica", 11))
    confirm_password_entry.grid(row=2, column=1)

    tk.Button(root, text="Login", command=login, font=("Helvetica", 11), bg="skyblue", width=15).pack(pady=5)
    tk.Button(root, text="Signup", command=signup, font=("Helvetica", 11), bg="lightgreen", width=15).pack()

def show_dashboard():
    clear_screen()

    title_label = tk.Label(root, text="🏦 Project Bank", font=("Helvetica", 18, "bold"),
                           fg="dark blue", bg="light blue", pady=15)
    title_label.pack(fill="x")

    tk.Label(root, text=f"Welcome, {current_user.username}", font=("Helvetica", 13), pady=10).pack()
    tk.Label(root, text=f"💰 Balance: ${current_user.view_balance():.2f}",
             font=("Helvetica", 12, "bold"), fg="green").pack(pady=5)

    btn_style = {"font": ("Helvetica", 11), "width": 22, "pady": 5}
    tk.Button(root, text="Deposit", command=deposit, **btn_style).pack(pady=4)
    tk.Button(root, text="Withdraw", command=withdraw, **btn_style).pack(pady=4)
    tk.Button(root, text="View Balance", command=view_balance, **btn_style).pack(pady=4)
    tk.Button(root, text="Transaction History", command=view_transactions, **btn_style).pack(pady=4)
    tk.Button(root, text="Logout", command=logout, bg="lightcoral", **btn_style).pack(pady=12)

# ------------------ Main App ------------------

if __name__ == "__main__":
    load_users()

    root = tk.Tk()
    root.title("Banking System")
    root.configure(bg="white")
    root.geometry("350x500")
    root.resizable(False, False)

    show_login()
    root.mainloop()
