from Classes.SavingsAccount import SavingsAccount
from Classes.My_Shapes import Square
from Classes.My_Shapes import Circle 
from Classes.My_Shapes import Rectangle
from Classes.Multiple_inheritance import Manager

def dashboard_menu(current_option):

    owned_account = False
    current_balance = 0
    
    while True:

        try:
            
            print("Choose an option to proceed:")
            print(f"1. To create a new Savings Account - Current Balance: {current_balance} USD")
            print("2. To make a deposit")
            print("3. To make a withdrawal")
            print("4. To calculate perimeter")
            print("5. To calculate area")
            print("6. Multiple inheritance example")
            print("7. Exit")

            option = int(input("Choose an option from the control panel: "))

            match option:
                
                case 1:
                    
                    #create a new Savings Account
                    my_savings_account = SavingsAccount(10)
                    print(f"Congratulations!, your savings account has been successfully created with a balance of {my_savings_account.min_balance} USD")
                    owned_account = True
                    current_balance = my_savings_account.balance
                
                case 2:
                    
                    #deposit
                    if (owned_account == False):
                        raise Exception("You do not own a savings account yet, please consider creating a new one first")
                        
                    else:
                        while True:
                            try:    
                                amount = input("Please indicate te amount that you would like to deposit: ")
                                if(amount.strip() == ""):
                                    raise ValueError("The response cannot be empty.")
                                amount = int(amount)
                                if amount < 0:
                                    raise ValueError("The amount must be a positive number")
                                else:
                                    break
                            except ValueError as ex:
                                print(f"Error: {ex}")
                        
                        current_balance = my_savings_account.deposit_money(amount)
                        print(f"The deposit of {amount} USD has been completed") 

                case 3:
                    
                    #withdrawal
                    if (owned_account == False):
                        raise Exception("You do not own a savings account yet, please consider creating a new one first")
                    elif(current_balance == my_savings_account.min_balance):
                        raise Exception(f"You cannot withdraw below the minimum balance, which is {my_savings_account.min_balance} USD")
                    else:
                        while True:
                            try:
                                amount = input("Please indicate te amount that you would like to withdraw: ")
                                if(amount.strip() == ""):
                                    raise ValueError("The response cannot be empty.")
                                amount = int(amount)
                                if ((current_balance - amount) < my_savings_account.min_balance):
                                    raise ValueError(f"You cannot withdraw below the minimum balance, which is {my_savings_account.min_balance} USD")                                    
                                if amount < 0:
                                    raise ValueError("The amount must be a positive number")
                                else:
                                    break

                            except ValueError as ex:
                                print(f"Error: {ex}")
                        
                        current_balance = my_savings_account.withdraw_money(amount)
                        print(f"The withdrawl of {amount} USD has been completed")

                case 4:
                    
                    #Perimeter
                    while True:
                        try:
                            shape = input("What shape would like to calculate the perimeter for? Circle/Square/Rectangle ")
                            if(shape.strip() == ""):
                                raise ValueError("The response cannot be empty.")
                            elif not all(x.isalpha() for x in shape):
                                raise ValueError("The input can only contain alphabetic characters")
                            elif(shape.lower() == "circle"):
                                radius = int(input("Please indicate the measure of the radius "))
                                new_circle = Circle(radius)
                                perimeter = new_circle.calculate_perimeter()
                                print(f"The circle perimeter is {perimeter}")
                                break
                            elif(shape.lower() == "square"):
                                side = int(input("Please indicate the measure of one side of the square "))
                                new_square = Square(side)
                                perimeter = new_square.calculate_perimeter()
                                print(f"The square perimeter is {perimeter}")
                                break
                            elif(shape.lower() == "rectangle"):
                                lenght = int(input("Please indicate the measure of the length "))
                                width = int(input("Please indicate the measure of the width "))
                                new_rectangle = Rectangle(lenght,width)
                                perimeter = new_rectangle.calculate_perimeter()
                                print(f"The rectangle perimeter is {perimeter}")
                                break
                            else:
                                 pass
                        except ValueError as ex:
                            print(f"Error: {ex}")
    
                case 5:
                    
                    #Area
                    while True:
                        try:
                            shape = input("What shape would like to calculate the area for? Circle/Square/Rectangle ")
                            if(shape.strip() == ""):
                                raise ValueError("The response cannot be empty.")
                            elif not all(x.isalpha() for x in shape):
                                raise ValueError("The input can only contain alphabetic characters")
                            elif(shape.lower() == "circle"):
                                radius = int(input("Please indicate the measure of the radius "))
                                new_circle = Circle(radius)
                                area = new_circle.calculate_area()
                                print(f"The circle area is {area}")
                                break
                            elif(shape.lower() == "square"):
                                side = int(input("Please indicate the measure of one side of the square "))
                                new_square = Square(side)
                                area = new_square.calculate_area()
                                print(f"The square area is {area}")
                                break
                            elif(shape.lower() == "rectangle"):
                                lenght = int(input("Please indicate the measure of the length "))
                                width = int(input("Please indicate the measure of the width "))
                                new_rectangle = Rectangle(lenght,width)
                                area = new_rectangle.calculate_area()
                                print(f"The rectangle area is {area}")
                                break
                            else:
                                 pass
                        except ValueError as ex:
                            print(f"Error: {ex}")

                case 6:
                    
                    #Multiple inheritance example
                    new_manager = Manager("Beto",2500)
                    print(new_manager.introduce()) #Inherits from father class Person
                    print(new_manager.show_salary()) #Inherits from father class Employee

                case 7:
                    
                    print("Closing the app.")
                    break

                case _:
                    raise ValueError("Invalid option, please choose a valid option from the menu:")
            
        except ValueError:
            print("Error: Invalid option, please choose a valid option from the menu:")
        
        except Exception as e:
            print(f"Error: {e}")

