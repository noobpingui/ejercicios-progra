import math

# 1. Cree una clase de `Circle` con:
#     1. Un atributo de `radius` (radio).
#     2. Un método de `get_area` que retorne su área.

class Circle:
    
    #Constructor
    def __init__(self, radius):
        self.radius = radius
    

    def get_area(self):

        area = math.pi * pow(self.radius,2)
        return round(area,2)