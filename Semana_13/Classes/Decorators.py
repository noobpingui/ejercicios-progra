class math_operation():


#1st Exercise
#Cree un decorador que haga print de los parámetros y retorno de la función que decore.
    def my_decorator_1(func):        
        def wrapper(self, num1, num2):
            print(f"The first parameter is: {num1}")
            print(f"The second parameter is: {num2}") 
            
            return func(self, num1, num2)
        
        return wrapper


#2nd Exercise
#Cree un decorador que se encargue de revisar si todos los parámetros de la función que decore son números, y arroje una excepción de no ser así.
    def my_decorator_2(func):        
        def wrapper(self, num1, num2):
            try:
                if not isinstance(num1,int) or not isinstance(num2,int):
                    raise ValueError(f"Both parameters must be integers")
                
                return func(self, num1, num2)
            
            except ValueError as e:
                return (f"{e}")
                
        return wrapper


    @my_decorator_1
    @my_decorator_2
    def decorated_func(self, num1, num2: int) -> int:
        
        return (f"The result is: {num1 + num2}") 


    