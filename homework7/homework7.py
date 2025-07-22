class BankAccount:
    # Class attribute
    bank_name = "First National Bank"
    
    def __init__(self, account_holder: str, initial_balance: float = 0.0):
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount: float) -> None:
        if BankAccount.validate_amount(amount):
            self.balance += amount
            self.transactions.append(f"Deposit: +${amount:.2f}")
            print(f"Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("Invalid deposit amount. Amount must be positive.")

    def withdraw(self, amount: float) -> None:
        if not BankAccount.validate_amount(amount):
            print("Invalid withdrawal amount. Amount must be positive.")
        elif amount > self.balance:
            print("Insufficient funds. Withdrawal canceled.")
        else:
            self.balance -= amount
            self.transactions.append(f"Withdrawal: -${amount:.2f}")
            print(f"Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")

    def __str__(self) -> str:
        return f"Account Holder: {self.account_holder}, Balance: ${self.balance:.2f}"

    @classmethod
    def change_bank_name(cls, new_name: str) -> None:
        cls.bank_name = new_name
        print(f"Bank name changed to {new_name}")

    @staticmethod
    def validate_amount(amount: float) -> bool:
        return amount > 0

    def show_transactions(self) -> None:
        print(f"\nTransaction History for {self.account_holder}:")
        for i, transaction in enumerate(self.transactions, 1):
            print(f"{i}. {transaction}")
        print(f"Current Balance: ${self.balance:.2f}\n")


class SavingsAccount(BankAccount):
    def __init__(self, account_holder: str, initial_balance: float = 0.0, interest_rate: float = 0.01):
        super().__init__(account_holder, initial_balance)
        self.interest_rate = interest_rate

    def add_interest(self) -> None:
        interest = self.balance * (self.interest_rate / 12)
        self.balance += interest
        self.transactions.append(f"Interest Added: +${interest:.2f}")
        print(f"Added ${interest:.2f} interest. New balance: ${self.balance:.2f}")

    def __str__(self) -> str:
        return (f"Savings Account - Account Holder: {self.account_holder}, "
                f"Balance: ${self.balance:.2f}, Interest Rate: {self.interest_rate*100:.1f}%")



print("="*50)
print("**class testing** BankAccount")
print("="*50)

acc1 = BankAccount("Alice", 1000.0)

acc1.deposit(300)
acc1.withdraw(150)
acc1.deposit(-50)
acc1.withdraw(2000)

print("\nAccount Information:")
print(acc1)

BankAccount.change_bank_name("New City Bank")
print(f"Updated bank name: {BankAccount.bank_name}")

acc1.show_transactions()

print("\n" + "="*50)
print("(test) SavingsAccount")
print("="*50)

savings = SavingsAccount("Charlie", 1000.0, 0.05)
savings.deposit(100)
savings.add_interest()
print("\nAccount Information:")
print(savings)
savings.show_transactions()
