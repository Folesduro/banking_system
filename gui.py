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
                # Pass both username and info to from_dict
                users[username] = User.from_dict(username, info)

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump({u: users[u].to_dict() for u in users}, f, indent=4)

# ------------------ GUI Setup ------------------

current_user = None

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username].check_password(password):
        current_user = users[username]
        messagebox.showinfo("Login", f"Welcome, {username}!")
        show_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

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
        update_balance_summary()
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
        update_balance_summary()
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

# ------------------ Graphical Balance Summary ------------------

def update_balance_summary():
    if not current_user:
        return
    balance = current_user.view_balance()
    # Update the balance visualization with a simple bar chart.
    balance_canvas.delete("all")
    balance_canvas.create_rectangle(10, 10, 290, 60, fill="lightgreen", outline="black")
    balance_canvas.create_text(150, 35, text=f"Balance: ${balance:.2f}", font=("Arial", 14), fill="dark blue")

# ------------------ UI Windows ------------------

def show_login():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="light blue")

    # Header
    title_label = tk.Label(root, text="Project Bank", font=("Arial", 16, "bold"),
                           fg="dark blue", bg="light blue", pady=10)
    title_label.pack(fill="x")

    tk.Label(root, text="Username:", bg="light blue").pack(pady=(20, 5))
    global username_entry
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password:", bg="light blue").pack(pady=5)
    global password_entry
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    tk.Button(root, text="Login", command=login, bg="skyblue").pack(pady=20)

def show_dashboard():
    for widget in root.winfo_children():
        widget.destroy()

    root.config(bg="light blue")

    title_label = tk.Label(root, text="Project Bank", font=("Arial", 16, "bold"),
                           fg="dark blue", bg="light blue", pady=10)
    title_label.pack(fill="x")

    tk.Label(root, text=f"Welcome, {current_user.username}", font=("Arial", 12), bg="light blue").pack(pady=10)

    # Add balance summary graphic
    global balance_canvas
    balance_canvas = tk.Canvas(root, width=300, height=80, bg="white", bd=2, relief="sunken")
    balance_canvas.pack(pady=20)
    update_balance_summary()

    tk.Button(root, text="Deposit", width=20, command=deposit).pack(pady=5)
    tk.Button(root, text="Withdraw", width=20, command=withdraw).pack(pady=5)
    tk.Button(root, text="View Balance", width=20, command=view_balance).pack(pady=5)
    tk.Button(root, text="Transaction History", width=20, command=view_transactions).pack(pady=5)
    tk.Button(root, text="Logout", width=20, command=logout, bg="lightcoral").pack(pady=15)

# ------------------ Main ------------------

if __name__ == "__main__":
    load_users()

    root = tk.Tk()
    root.title("Banking System")
    root.geometry("350x500")
    show_login()
    root.mainloop()
