from backend.user import User

def test_user_actions(
    user,
    correct_password,
    wrong_password,
    deposit_amount,
    withdraw_amount,
    test_negative_deposit=False,
    test_insufficient_funds=False,
    test_negative_withdraw=False
):
    print(f"\n--- Testing user: {user.username} ---")

    # Password Tests
    print("Correct password:", user.check_password(correct_password))
    print("Wrong password:", user.check_password(wrong_password))

    # Deposit Test
    try:
        user.deposit(deposit_amount)
        print(f" Deposited ${deposit_amount}. Balance: ${user.view_balance():.2f}")
    except ValueError as e:
        print(" Deposit error:", e)

    if test_negative_deposit:
        try:
            user.deposit(-50)
        except ValueError as e:
            print(" Deposit error (negative amount):", e)

    # Withdraw Test
    try:
        user.withdraw(withdraw_amount)
        print(f" Withdrew ${withdraw_amount}. Balance: ${user.view_balance():.2f}")
    except ValueError as e:
        print(" Withdraw error:", e)

    if test_insufficient_funds:
        try:
            user.withdraw(1000)
        except ValueError as e:
            print(" Withdraw error (insufficient funds):", e)

    if test_negative_withdraw:
        try:
            user.withdraw(-10)
        except ValueError as e:
            print(" Withdraw error (negative amount):", e)

    # Transaction History
    print(" Transaction History:")
    for txn in user.view_transaction_history():
        print(" -", txn)


# Create users
user1 = User("User1", "pass123")
user2 = User("User2", "shadow45")
user3 = User("User3", "sunshine22")
user4 = User("User4", "king456")

# Run tests for each user
test_user_actions(user1, "pass123", "wrongpass", deposit_amount=100, withdraw_amount=30,
                  test_negative_deposit=True, test_insufficient_funds=True, test_negative_withdraw=True)

test_user_actions(user2, "shadow45", "123456", deposit_amount=200, withdraw_amount=400)

test_user_actions(user3, "sunshine22", "sun123", deposit_amount=150, withdraw_amount=40)

test_user_actions(user4, "king456", "wrong123", deposit_amount=300, withdraw_amount=120)
