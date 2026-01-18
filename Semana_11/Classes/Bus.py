from Classes.Person import Person 

class Bus:
    
    #Constructor
    def __init__(self, max_passengers):
        self.bus_quota = []
        self.max_passengers = max_passengers

    #Method to add passengers 
    def to_add_passengers(self):
        while True:
            if(len(self.bus_quota) >= self.max_passengers):
                print("The bus is full of its capacity. You cannot add more passengers")
                break
            else:
                answer = input("Would you like to add a new passenger? Yes/No ")
                if(answer.lower() == "yes"):
                    passenger = Person()
                    self.bus_quota.append(passenger.name)
                    print(f"The passenger {passenger.name} has been added successfully")
                elif(answer.lower() == "no"):
                    break
                else:
                    pass

        return self.bus_quota
        
    #Method to remove passengers
    def to_remove_passengers(self):
        
        if(len(self.bus_quota) == 0):
            print("The bus is currently empty. Please consider adding passengers first")
            pass
        else:
            while True:
                try:
                    answer = input("What passenger would you like to remove? Enter the passenger's name or 'Quit' to cancel this action ")
                    if(answer.lower() == "quit"):
                        break
                    else:
                        for passenger in self.bus_quota:
                            if(answer.strip() == ""):
                                raise ValueError("The name cannot be empty.")
                            elif not all(x.isalpha() or x.isspace() for x in answer):
                                raise ValueError("The name can only contain alphabetic characters and spaces.")
                            elif(passenger == answer):
                                self.bus_quota.remove(passenger)
                                print(f"The passenger {answer} has been successfully removed")
                            else:
                                pass
                except ValueError as ex:
                    print(f"Error: {ex}")
                
        return self.bus_quota
