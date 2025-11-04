

# 1. Cree una calculadora por linea de comando. Esta debe de tener un número actual, y un menú para decidir qué operación hacer con otro número:
# 1. Suma
# 2. Resta
# 3. Multiplicación
# 4. División
# 5. Borrar resultado
# Al seleccionar una opción, el usuario debe ingresar el nuevo número a sumar, restar, multiplicar, o dividir por el actual. El resultado debe pasar a ser el nuevo numero actual.
# Debe de mostrar mensajes de error si el usuario selecciona una opción invalida, o si ingresa un número invalido a la hora de hacer la operación.

def addition(current_number):
    while True:
        try:    
            sum_number = int(input("Enter a number to sum: "))
        except ValueError:  
            print("Error: A valid number must be entered")
        else:
            current_number += sum_number
            return current_number
        
def subtraction(current_number):
    while True:
        try:    
            subtraction_number = int(input("Enter a number to subtract: "))            
        except ValueError:  
            print("Error: A valid number must be entered")
        else:
            current_number -= subtraction_number
            return current_number

def multiplication(current_number):
    while True:
        try:    
            multiplication_number = int(input("Enter a number to multiply: "))            
        except ValueError:  
            print("Error: A valid number must be entered")
        else:
            current_number *= multiplication_number
            return current_number
        

def division(current_number):
    if current_number == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    

    while True:
        try:    
            divided_by_number = int(input("Enter a number to divide: "))
            current_number /= divided_by_number         
        except ValueError:  
            print("Error: A valid number must be entered")  
        except ZeroDivisionError:
            print("Error: Cannot divide by zero")
        else:
            current_number /= divided_by_number
            return current_number
        

def clear_current_number():
    current_number = 0
    return current_number

def calculator(current_number):
    

    while True:

        try:
            
            print("Choose an option to proceed:")
            print("1. Sum")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Clear result")
            print("6. Exit")
            print(f"current Number: {current_number}")

            opcion = int(input("Choose an option from the calculator panel: "))

            match opcion:
                case 1:
                    current_number = addition(current_number)
                              
                case 2:
                    current_number= subtraction(current_number)
                  
                case 3:
                    current_number = multiplication(current_number)
                    
                case 4:
                    current_number = division(current_number)
                    
                case 5:
                    current_number = clear_current_number()
                     
                case 6:
                    print("Closing the app)")
                    break

                case _:
                    raise ValueError("Invalid option, please choose a valid option from the calculator panel:")
            
        except ValueError:
            print("Error: Invalid option, please choose a valid option from the calculator panel:")
        
        except Exception as e:
            print(f"Error: {e}") 

current_number = 0
calculator(current_number)