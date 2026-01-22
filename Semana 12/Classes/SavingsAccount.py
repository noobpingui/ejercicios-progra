from Classes.BankAccount import BankAccount


class SavingsAccount(BankAccount):
    def __init__(self, min_balance: int):
        super().__init__(min_balance)

