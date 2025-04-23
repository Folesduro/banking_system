import hashlib

class User:
    def __init__(self, username, password_hash, balance=0.0, transactions=None):
        self.username = username
        self.password_hash = password_hash
        self.balance = balance
        self.transactions = transactions if transactions else []

    @classmethod
    def create(cls, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return cls(username, password_hash)

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append(f"Deposited ${amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append(f"Withdrew ${amount:.2f}")

    def view_balance(self):
        return self.balance

    def view_transaction_history(self):
        return self.transactions

    def to_dict(self):
        return {
            "password_hash": self.password_hash,
            "balance": self.balance,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, username, data):
        return cls(username, data["password_hash"], data["balance"], data.get("transactions", []))
