from Classes.Shape import Shape
import math

class Circle(Shape):
    def __init__(self, radius: int):
        super().__init__()
        self.radius = radius
    
    def calculate_perimeter(self) -> int:
        perimeter = 2*math.pi*self.radius

        return round(perimeter,2)
    
    def calculate_area(self) -> int:
        area = math.pi*pow(self.radius,2)

        return round(area, 2)
    
class Square(Shape):
    def __init__(self, side: int):
        super().__init__()
        self.side = side

    def calculate_perimeter(self) -> int:
        perimeter = self.side * 4

        return round(perimeter,2)

    def calculate_area(self) -> int:
        area = pow(self.side,2)

        return round(area, 2)

class Rectangle(Shape):
    def __init__(self, lenght, width: int):
        super().__init__()
        self.lenght = lenght
        self.width = width
    
    def calculate_perimeter(self):
        perimeter = 2*(self.lenght+self.width)

        return round(perimeter,2)

    def calculate_area(self):
        area = self.lenght * self.width
    
        return round(area, 2)