from backend.user import User

# Create a test user
user1 = User("folasade", "mypassword")

# Check password
print("Password correct:", user1.check_password("mypassword"))  # True
print("Password wrong:", user1.check_password("wrong"))         # False

# Deposit money
user1.deposit(100)
print("Balance after deposit:", user1.view_balance())

# Withdraw money
user1.withdraw(40)
print("Balance after withdrawal:", user1.view_balance())

# View transaction history
print("Transaction history:")
for entry in user1.view_transaction_history():
    print(entry)
