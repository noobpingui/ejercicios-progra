

# 1. Cree un programa que itere e imprima un string letra por letra de derecha a izquierda.
#     a. Pista: investigue de que otras maneras se puede usar el `range`.
#     b. Ejemplos:
#     c. `my_string = ‘Pizza con piña’` → 
#     a
#     ñ
#     i
#     p
    
#     n
#     o
#     c
    
#     a
#     z
#     z
#     i
#     p

#Variables/Datos
my_string = "Un chanchito volador"

#Procesos
for index in range(len(my_string), 0, -1):
    element_from_my_string = my_string[index-1]    
    print(f"{element_from_my_string}")