# gui.py

import tkinter as tk
from tkinter import messagebox, simpledialog
from backend.user import User

# ——————————————————————
# 1) Set up your “database” of users
# ——————————————————————
# (You can later load this from a file—you already have to_dict()/from_dict())
USERS = {
    "User1": User("User1", "pass123"),
    "User2": User("User2", "shadow45"),
    "User3": User("User3", "sunshine22"),
    "User4": User("User4", "king456"),
}

current_user = None


# ——————————————————————
# 2) GUI callbacks
# ——————————————————————
def login():
    global current_user
    uname = entry_username.get().strip()
    pwd   = entry_password.get().strip()

    user = USERS.get(uname)
    if not user or not user.check_password(pwd):
        messagebox.showerror("Login Failed", "Invalid username or password")
        return

    current_user = user
    messagebox.showinfo("Welcome", f"Hello, {uname}!")
    login_frame.pack_forget()
    dashboard_frame.pack(padx=20, pady=20)


def do_deposit():
    amt = _get_amount()
    if amt is None: return
    try:
        current_user.deposit(amt)
        messagebox.showinfo("Success", f"Deposited ${amt:.2f}")
    except ValueError as e:
        messagebox.showerror("Deposit Error", str(e))


def do_withdraw():
    amt = _get_amount()
    if amt is None: return
    try:
        current_user.withdraw(amt)
        messagebox.showinfo("Success", f"Withdrew ${amt:.2f}")
    except ValueError as e:
        messagebox.showerror("Withdraw Error", str(e))


def show_balance():
    bal = current_user.view_balance()
    messagebox.showinfo("Balance", f"Your balance is: ${bal:.2f}")


def show_history():
    history = current_user.view_transaction_history()
    if not history:
        messagebox.showinfo("History", "No transactions yet.")
    else:
        messagebox.showinfo("History", "\n".join(history))


def _get_amount():
    """
    Helper to get and parse the amount entry.
    Returns float or None on failure (shows error).
    """
    s = entry_amount.get().strip()
    try:
        amt = float(s)
        return amt
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")
        return None


# ——————————————————————
# 3) Build the GUI
# ——————————————————————
root = tk.Tk()
root.title("Banking System")
root.geometry("350x300")

# — Login Frame —
login_frame = tk.Frame(root, padx=20, pady=20)
tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="e")
entry_username = tk.Entry(login_frame)
entry_username.grid(row=0, column=1, pady=5)

tk.Label(login_frame, text="Password:").grid(row=1, column=0, sticky="e")
entry_password = tk.Entry(login_frame, show="*")
entry_password.grid(row=1, column=1, pady=5)

tk.Button(login_frame, text="Login", width=20, command=login).grid(row=2, columnspan=2, pady=10)
login_frame.pack(expand=True)

# — Dashboard Frame —
dashboard_frame = tk.Frame(root)

tk.Label(dashboard_frame, text="Amount:").grid(row=0, column=0, pady=5, sticky="e")
entry_amount = tk.Entry(dashboard_frame)
entry_amount.grid(row=0, column=1, pady=5)

tk.Button(dashboard_frame, text="Deposit",   width=12, command=do_deposit).grid(row=1, column=0, pady=5)
tk.Button(dashboard_frame, text="Withdraw",  width=12, command=do_withdraw).grid(row=1, column=1, pady=5)
tk.Button(dashboard_frame, text="View Balance",   width=12, command=show_balance).grid(row=2, column=0, pady=5)
tk.Button(dashboard_frame, text="Transaction History", width=18, command=show_history).grid(row=2, column=1, pady=5)

root.mainloop()
