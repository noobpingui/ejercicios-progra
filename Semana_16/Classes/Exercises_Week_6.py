

#3. suma de elementos en una lista por medio de parametros
def sum_list(parameter_1):
    result = 0
    if not isinstance(parameter_1, list):
        raise TypeError("The parameter is not a list")
    else:
        for element in parameter_1:
            result = (result + element) 
     
    return result

#4. Cree una función que le de la vuelta a un string y lo retorne.
#     a. Esto ya lo hicimos en iterables.
#     b. “Hola mundo” → “odnum aloH”

def reverse_string(string):
    if not isinstance(string, str):
        raise TypeError("The parameter is not a string")
    else:
        my_list = []
        for index in range(len(string)-1, -1, -1):
            result = string[index]    
            my_list.append(result)
    
    return "".join(my_list)



#5. Cree una función que imprima el numero de mayúsculas y el numero de minúsculas en un string.
# “I love Nación Sushi” → “There’s 3 upper cases and 13 lower cases”

#Funcion para sacar las Mayusculas
def get_upper_case(string, uppers = 0):
    if not isinstance(string, str):
        raise TypeError("The parameter is not a string")
    else:
        for index in range(0, len(string), 1):
            if(string[index] ==  string[index].upper()) & (string[index] != " "):
                uppers = uppers+1 
            else:
                continue

    return uppers 

#Funcion para sacar las Minusculas
def get_lower_case(string, lowers = 0):
    if not isinstance(string, str):
        raise TypeError("The parameter is not a string")
    else:
        for index in range(0, len(string), 1):
            if(string[index] ==  string[index].lower()) & (string[index] != " "):
                lowers = lowers+1 
            else:
                continue

    return lowers   


#6. Cree una función que acepte un string con palabras separadas por un guión y retorne un string igual pero ordenado alfabéticamente.
#     a. Hay que convertirlo a lista, ordenarlo, y convertirlo nuevamente a string.
#     b. “python-variable-funcion-computadora-monitor” → “computadora-funcion-monitor-python-variable”

def sort_list(parameter_1):
    if not isinstance(parameter_1, str):
        raise TypeError("The parameter is not a string")
    else:
        my_list = parameter_1.split("-") #Divido las palabras del string y creo la lista con los elementos
        sorted_list = sorted(my_list) #Ordeno los elementos de la lista y los guardo en una nueva lista ordenada
        
    return "-".join(sorted_list) #Retorno la lista ordenada como un nuevo string



#7. #Funcion para sacar las Numeros primos
def get_prime_numbers(my_list, my_new_list):
    if not isinstance(my_list, list):
        raise TypeError("The parameter is not a list")
    else:
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

