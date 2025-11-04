

# 1. Cree un programa que intercambie el primer y ultimo elemento de una lista. Debe funcionar con listas de cualquier tamaño.
#     a. Ejemplos:
#     b. `my_list = [4, 3, 6, 1, 7]` → `[7, 3, 6, 1, 4]`

#Variables/Datos
my_list = [32, 2, 44, 6, 1, 11]

#Procesos
print(f"Lista Original: {my_list}")

for index in range(0, len(my_list), 1):
    if(index == 0):
        first_element = my_list.pop(index)
        my_list.append(first_element)
    elif(index == (len(my_list)-1)):
        last_element = my_list.pop(index-1) 
        my_list.insert(0, last_element)           
    else:
        continue

print(f"Lista modificada: {my_list}")