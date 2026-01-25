from Classes.BankAccount import BankAccount


class SavingsAccount(BankAccount):
    def __init__(self, min_balance: int):
        self.min_balance = min_balance
        super().__init__(self.min_balance)

