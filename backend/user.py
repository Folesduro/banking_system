import hashlib
from datetime import datetime

class User:
    def __init__(self, username, password, balance=0.0, transaction_history=None):
        self.username = username
        self.password = password
        self.balance = balance
        self.transaction_history = transaction_history if transaction_history else []

    @classmethod
    def create(cls, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return cls(username, password_hash)

    def check_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - Deposited ${amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"{timestamp} - Withdrew ${amount:.2f}")

    def view_balance(self):
        return self.balance

    def view_transaction_history(self):
        return self.transaction_history

    def to_dict(self):
        return {
            "password": self.password,
            "balance": self.balance,
            "transaction_history": self.transaction_history
        }

    @classmethod
    def from_dict(cls, username, info):
        info = info.copy()
        info.pop('username', None)
        return cls(username, **info)
