from Classes.Circle import Circle

class Figures():
    def __init__(self):
        pass

    #Method to calculate circle area
    def get_circle_area(self):

        pi = 3.14159
        while True:
            try:
                self.radius = input("Enter the circle radius: ")
                if(self.radius.strip() == ""):
                    raise ValueError("The response cannot be empty.")
                
                self.radius = float(self.radius)
                if self.radius < 0:
                    raise ValueError("The radius must be a positive number")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        #Instancing Circle Object 
        new_circle = Circle(self.radius)
        area = pi * pow(new_circle.radius,2)

        return round(area,2)