
# 1. Cree un programa que itere e imprima los valores de dos listas del mismo tamaño al mismo tiempo.
#     a. Ejemplos:
#     b. `first_list = [’Hay’, ‘en’, ‘que’, ‘iteracion’, ‘indices’, ‘muy’]`
#     `second_list = [’casos’, 'los’, ‘la’, ‘por’, ‘es’, ‘util’]` ->
#     Hay casos
#     en los
#     que la
#     iteracion por
#     indice es
#     muy util

#Variables/Datos
first_list = ["Este", "un", "para", "valores", "dos", "de", "mismo"]
second_list = ["es", "ejemplo", "imprimir", "en", "listas", "un", "tamano"]

#Procesos
for index in range(0, len(first_list)):
    element_first_list = first_list[index]
    element_second_list = second_list[index]    
    print(f"{element_first_list} {element_second_list}")