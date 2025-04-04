# tests/test_user.py

from backend.User import User

# Create a test user
shruti = User("shruti", "test123")

# --- Test password check ---
assert shruti.check_password("test123") == True
assert shruti.check_password("wrongpass") == False

# --- Test deposit ---
shruti.deposit(200)
shruti.deposit(50)

# --- Test invalid deposit ---
try:
    shruti.deposit(-10)
except ValueError as e:
    print("Invalid deposit test passed:", e)

# --- Test withdraw ---
shruti.withdraw(100)

# --- Test over-withdraw ---
try:
    shruti.withdraw(1000)
except ValueError as e:
    print("Over-withdraw test passed:", e)

# --- Final balance ---
print("Final balance:", shruti.view_balance())

# --- Transaction history (with timestamps) ---
print("\n Transaction history:")
for txn in shruti.view_transaction_history():
    print(txn)
