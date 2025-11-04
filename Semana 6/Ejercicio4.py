

# 1. Cree una función que le de la vuelta a un string y lo retorne.
#     a. Esto ya lo hicimos en iterables.
#     b. “Hola mundo” → “odnum aloH”

def reverse_string(string):
    my_list = []
    for index in range(len(string)-1, -1, -1):
        result = string[index]    
        my_list.append(result)
        

    return "".join(my_list)    

def main():
    my_string = "Hola mundo" 
    print(reverse_string(my_string))


main() 