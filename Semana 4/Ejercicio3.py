
# Cree un programa que le pida al usuario su nombre, apellido, y edad, y muestre 
# si es un bebé, niño, preadolescente, adolescente, adulto joven, adulto, o adulto mayor.

#inputs para mis variables
name = input("Cual es su nombre? ")
last_name = input("Cual es su apellido? ")
age = int(input("Cual es su edad? "))

#Procesos
if(age<5):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un bebe")
elif(age<10):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un niño")
elif(age<15):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un preadolescente")
elif(age<18):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un adolescente")
elif(age<30):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un adulto joven")
elif(age<60):
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un adulto")
else:        
    print(f"Hola {name} {last_name}, tienes {age}, por lo tanto eres un adulto mayor")