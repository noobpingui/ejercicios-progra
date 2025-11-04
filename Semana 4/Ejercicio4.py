
# 1. **Cree un programa con un numero secreto del 1 al 10. El programa no debe cerrarse hasta que el usuario adivine el numero.**
#     a. **Debe investigar cómo generar un número aleatorio distinto cada vez que se ejecute.**

import random

#Variables a utilizar
secret_number = random.randint(1, 10)
flag = True

#Procesos
while(flag):
    guess = int(input("Adivina el numero secreto entre 1 y 10 "))
    if(guess != secret_number):
        print(f"{guess} no es el numero secreto. Vuelve a intentarlo")
    else:
        print(f"{guess} es el numero secreto. Felicidades, haz adivinado!")    
        flag = False