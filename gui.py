import tkinter as tk
from tkinter import messagebox
import hashlib

# Sample users (replace with actual data storage in a real application)
users = {
    'user1': {'password': 'password123', 'balance': 1000.0},
    'user2': {'password': 'password456', 'balance': 1500.0}
}

current_user = None

def load_users():
    """Load user data (for now, it's hardcoded)"""
    pass

def save_users():
    """Save user data (for now, it's just in memory)"""
    pass

def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def show_login():
    """Display the login form"""
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        
        if username in users and users[username]['password'] == hash_password(password):
            global current_user
            current_user = username
            show_dashboard()
        else:
            messagebox.showerror("Login failed", "Invalid username or password")
    
    login_frame = tk.Frame(root)
    login_frame.pack(padx=10, pady=10)

    tk.Label(login_frame, text="Username").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(login_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(login_frame, text="Password").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(login_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    login_button = tk.Button(login_frame, text="Login", command=attempt_login)
    login_button.grid(row=2, column=0, columnspan=2, pady=10)

    signup_button = tk.Button(login_frame, text="Sign Up", command=show_signup)
    signup_button.grid(row=3, column=0, columnspan=2, pady=10)

def show_signup():
    """Display the signup form"""
    def attempt_signup():
        username = username_entry.get()
        password = password_entry.get()
        password_confirm = password_confirm_entry.get()

        if username in users:
            messagebox.showerror("Signup failed", "Username already exists")
        elif password != password_confirm:
            messagebox.showerror("Signup failed", "Passwords do not match")
        else:
            users[username] = {'password': hash_password(password), 'balance': 0.0}
            messagebox.showinfo("Signup successful", "Welcome, " + username)
            show_login()
    
    signup_frame = tk.Frame(root)
    signup_frame.pack(padx=10, pady=10)

    tk.Label(signup_frame, text="Username").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(signup_frame)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(signup_frame, text="Password").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(signup_frame, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(signup_frame, text="Confirm Password").grid(row=2, column=0, padx=10, pady=5)
    password_confirm_entry = tk.Entry(signup_frame, show="*")
    password_confirm_entry.grid(row=2, column=1, padx=10, pady=5)

    signup_button = tk.Button(signup_frame, text="Sign Up", command=attempt_signup)
    signup_button.grid(row=3, column=0, columnspan=2, pady=10)

def show_dashboard():
    """Display the main dashboard"""
    def logout():
        global current_user
        current_user = None
        show_login()

    if current_user:
        balance = users[current_user]['balance']
        dashboard_frame = tk.Frame(root)
        dashboard_frame.pack(padx=10, pady=10)

        tk.Label(dashboard_frame, text=f"Welcome, {current_user}", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(dashboard_frame, text=f"Balance: ${balance}", font=("Arial", 14)).grid(row=1, column=0, columnspan=2, pady=5)

        logout_button = tk.Button(dashboard_frame, text="Logout", command=logout)
        logout_button.grid(row=2, column=0, columnspan=2, pady=10)

# Main application window
if __name__ == "__main__":
    load_users()

    root = tk.Tk()
    root.title("Banking System")
    root.configure(bg="white")
    root.geometry("350x500")
    root.resizable(True, True)      # Allow manual resizing
    root.state('zoomed')            # Start maximized
    # root.attributes('-fullscreen', True)  # (Optional) Fully full-screen mode

    show_login()

    root.mainloop()
