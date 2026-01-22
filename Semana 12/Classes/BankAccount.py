
class BankAccount:
    
    def __init__(self, balance: int):
        self.balance = balance

    def deposit_money(self, amount: int) -> int:
        
        self.balance += amount
        
        return self.balance


    def withdraw_money(self, amount: int) -> int:
        
        if(amount > self.balance):
            print("Insufficient funds")
        else:
            self.balance -= amount
        
        return self.balance