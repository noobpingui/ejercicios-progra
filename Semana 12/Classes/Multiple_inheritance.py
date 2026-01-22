
#Multiple inheritance example

class Person:
    def __init__(self, name: str):
        self.name = name
    
    def introduce(self):
        return (f"My name is {self.name}")


class Employee:
    def __init__(self, salary: int):
        self.salary = salary
    
    def show_salary(self):
        return (f"My salary is {self.salary}")

#Inherits from Person and Employee
class Manager(Person, Employee):
    def __init__(self, name: str, salary: int):
        Person.__init__(self, name)
        Employee.__init__(self, salary)