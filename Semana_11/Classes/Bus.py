class Bus:
    
    #Constructor
    def __init__(self, max_passengers):
        self.bus_quota = []
        self.max_passengers = max_passengers

    #Method to add passengers 
    def to_add_passengers(self, person):
        
        self.bus_quota.append(person)
        print(f"The passenger {person.name} has been added successfully")

        return self.bus_quota
        
    #Method to remove passengers
    def to_remove_passengers(self, person):
               
        while True:
            try:
                answer = input("What passenger would you like to remove? Enter the passenger's name or 'Quit' to cancel this action ")
                if(answer.lower() == "quit"):
                    break
                else:
                    for person in self.bus_quota:
                        if(answer.strip() == ""):
                            raise ValueError("The name cannot be empty.")
                        elif not all(x.isalpha() or x.isspace() for x in answer):
                            raise ValueError("The name can only contain alphabetic characters and spaces.")
                        elif(person.name == answer):
                            self.bus_quota.remove(person)
                            print(f"The passenger {answer} has been successfully removed")
                        else:
                            pass
            except ValueError as ex:
                print(f"Error: {ex}")
                
        return self.bus_quota
