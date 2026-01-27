from datetime import date

# 3. Cree una clase de `User` que:
#     - Tenga un atributo de `date_of_birth`.
#     - Tenga un property de `age`.
#     Luego cree un decorador para funciones que acepten un `User` como parámetro que se encargue 
#     de revisar si el `User` es mayor de edad y arroje una excepción de no ser así.


class User():
    def __init__(self, date_of_birth: date):
        self.date_of_birth = date_of_birth
        
    @property
    def user_age(self):

        today = date.today()
        
        age = today.year - self.date_of_birth.year
        if ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)):
            age -= 1
    
        return age


    def age_decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                if(self.user_age < 18):
                    raise ValueError (f"The user is underage!")
                
                return func(self, *args, **kwargs)
            
            except ValueError as e:
                return (f"{e}")
        
        return wrapper
    
    @age_decorator
    def age_validation(self):
        return f"The user is {self.user_age} years old"
    
