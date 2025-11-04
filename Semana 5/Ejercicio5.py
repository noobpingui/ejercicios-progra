

# 1. Cree un programa que le pida al usuario 10 números, y al final le muestre todos los números que ingresó, seguido del numero ingresado más alto.
#     a. Ejemplos:
#     b. 86, 54, 23, 54, 67, 21, 2, 65, 10, 32 → [86, 54, 23, 54, 67, 21, 2, 65, 10, 32]. El más alto fue 86.


#Variables/Datos
my_list = []

#Procesos
for index in range(0, 10, 1):
    element = int(input(f"Ingrese el elemento {index+1} "))
    my_list.append(element)
    if(index == 0):
        highest_number = my_list[index]
    elif(my_list[index] > highest_number):
        highest_number = my_list[index]
    else:
        continue

print(my_list, highest_number)