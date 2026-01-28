from Classes.Decorators import math_operation
from Classes.User import User
from datetime import date


#Insting object for 1st and 2nd exercise / Calling decorated method.

new_operation = math_operation()
print(new_operation.decorated_func(7,10))

#Insting object for 3rd exercise / Calling decorated method.
new_user = User(date(2000,2,21)) #year,month,day
print(new_user.age_validation())
