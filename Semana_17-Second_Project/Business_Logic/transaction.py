class Transaction():
    def __init__(self):
        self.transaction_data = []
        

    def add_new_transaction(self, title:str, amount: str, category: str, transaction_type: str ):
        title = title.strip().capitalize()
        amount = amount.strip()

        try:
            if title.strip() == "":
                raise ValueError(f"The title cannot be empty")
                
            elif not all(char.isalpha() for char in title):
                raise TypeError(f"The title can only contain alphabetic characters and no spaces")
            
            elif amount.strip() == "":
                raise ValueError(f"The amount cannot be empty")

            elif not amount.isnumeric():
                raise TypeError(f"The amount can only contain digits and no spaces")
            
            elif float(amount) < 0:
                raise ValueError(f"The amount cannot be a negative number")
            
            elif not category:
                raise ValueError(f"Please make sure to select a category")
            
            elif any(item["Title"] == title for item in self.transaction_data):
                raise ValueError(f"A transaction with that title has been previously registered already")

            else:

                if transaction_type == "income":

                    income_data = {
                    "Title": title,
                    "Amount": float(amount),
                    "Category": category,
                    "Income": "Yes",
                    "Expenses": "-"
                }
                    self.transaction_data.append(income_data)
                    return {"success": self.transaction_data}
                
                else:

                    expenses_data = {
                    "Title": title,
                    "Amount": float(amount),
                    "Category": category,
                    "Income": "-",
                    "Expenses": "Yes"
                }
                    self.transaction_data.append(expenses_data)
                    return {"success": self.transaction_data}
            
        except Exception as ex:
            return {"error": str(ex)}
    
    def delete_transaction_item(self, index: int):
        
        try:
            if not self.transaction_data:
                raise ValueError(f"There are no transactions to delete")
            
            else:
                self.transaction_data.pop(index)
                return  {"success": self.transaction_data}
                
        except Exception as ex:
            return {"error": str(ex)}
        
        
    def get_transaction_data(self):
        return self.transaction_data
    

    