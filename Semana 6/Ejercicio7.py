

# 1. Cree una función que acepte una lista de números y retorne una lista con los números primos de la misma.
#     a. [1, 4, 6, 7, 13, 9, 67] → [7, 13, 67]
#     b. Tip 1: Investigue la logica matematica para averiguar si un numero es primo, y conviertala a codigo. No busque el codigo, eso no ayudaria.
#     c. *Tip 2: Aquí hay que hacer varias cosas (recorrer la lista, revisar si cada numero es primo, y agregarlo a otra lista). Así que lo mejor es agregar **otra función** para revisar si el numero es primo o no.*


#Funcion para sacar las Numeros primos
def get_prime_numbers(my_list, my_new_list):
    for element in my_list:
        if(element == 1): #Condicion especial en caso que sea 1.
            continue
        else: #Empezamos a recorrer la lista para buscar los numeros primos
            contador = 0 #Variable para determinar la cantidad de divisores que tiene un numero
            for index in range(1, (element+1), 1):
                if((element%index) == 0):
                    contador = contador+1
                else:
                    continue
            if(contador<=2): #Si la cantidad de divisores es igual o menor a 2, entones el numero SI es primo
                my_new_list.append(element) #Como el numero es primo, lo agregamos a la nueva lista de solamente numeros primos.
            else:
                continue

    return my_new_list #Retornamos la nueva lista que incluye unicamente los numeros primos.


#Funcion con la lista de los numeros, la nueva lista vacia para los numeros primos e imprimir los resultados retornados del metodo get_prime_numbers
def main():
    my_list = [1, 4, 6, 7, 13, 9, 67] 
    my_new_list = []
    print(f"Lista de numeros primos: {get_prime_numbers(my_list, my_new_list)}")
    



main()

