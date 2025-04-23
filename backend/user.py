import hashlib
import time

class User:
    def __init__(self, username, password):
        self.username = username
        self.hashed_password = self._hash_password(password)
        self.balance = 0.0
        self.transaction_history = []

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self._hash_password(password) == self.hashed_password

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction("Deposit", amount)
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        elif amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        else:
            self.balance -= amount
            self._log_transaction("Withdraw", amount)

    def view_balance(self):
        return self.balance

    def view_transaction_history(self):
        return self.transaction_history

    def _log_transaction(self, type, amount):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.transaction_history.append(f"{timestamp} - {type}: ${amount:.2f}")

    def to_dict(self):
        return {
            "username": self.username,
            "hashed_password": self.hashed_password,
            "balance": self.balance,
            "transaction_history": self.transaction_history
        }

    @staticmethod
    def from_dict(data):
        user = User.__new__(User)  # Avoid __init__ to not re-hash password
        user.username = data["username"]
        user.hashed_password = data["hashed_password"]
        user.balance = data["balance"]
        user.transaction_history = data["transaction_history"]
        user.hasher = PasswordHasher()
        return user
