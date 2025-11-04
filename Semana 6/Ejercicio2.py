


# 1. Experimente con el concepto de scope:
#     a. Intente accesar a una variable definida dentro de una función desde afuera.
#     b.  Intente accesar a una variable global desde una función y cambiar su valor.

#a. 

#Variable con Scope Local
def first_function():
    local_variable = "Variable local"


first_function()
print(local_variable) #No se puede acceder a la variable local de la funcion.
#Outcome: "local_variable" is not defined


#Para acceder a la variable local de la funcion, podriamos accesarla por medio del return en la misma funcion:
#Variable con Scope Local
def first_function():
    local_variable = "Variable local"

    return local_variable


print(first_function())
#Outcome: "Variable Local"



#b. 

#Variable con Scope Global
global_variable = "Variable global"

def first_function():
    global_variable = "La Variable global ha sido modificada"
    
    return global_variable


print(first_function())
#Outcome: "La Variable global ha sido modificada"


#Tambien podemos acceder a la variable global de la forma correcta por medio de parametros ya que es un valor que va a ser modificado
def first_function(variable_global):
    variable_global = "La Variable global ha sido modificada"
    return variable_global


def main():
    global_variable = "Esta es una variable que enviamos como parametro a first_function"
    print(first_function(global_variable))


main()

