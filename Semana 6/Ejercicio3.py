

# 1. Cree una función que retorne la suma de todos los números de una lista.
#     a. La función va a tener un parámetro (la lista) y retornar un numero (la suma de todos sus elementos).
#     b. [4, 6, 2, 29] → 41

#suma de elementos en una lista por medio de parametros
def sum_list(parameter_1):
    result = 0
    for element in parameter_1:
        result = (result + element) 
     
    return result


def main():
    my_list = [4, 6, 2, 29]
    print(sum_list(my_list))


main()

#Tambien se puede hacer de una forma mas elegante usando la funcion predeterminada sum() 
#(Me di cuenta cuando termine la solucion anterior)
def sum_list(parameter_1):
    result = sum(parameter_1)
    
    return result


def main():
    my_list = [4, 6, 2, 29]
    print(sum_list(my_list))


main()
