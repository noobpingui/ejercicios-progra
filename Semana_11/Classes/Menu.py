import os

from Classes.csv_actions import export_csv_file, import_csv_file, CSV_FILE_PATH

from Classes.Bus import Bus
from Classes.Classroom import Classroom
from Classes.Human import Human
from Classes.Circle import Circle
from Classes.Person import Person

#function to display the dashboard menu and handle user interactions
def dashboard_menu(current_option):
    
    #Instancing Bus Object and passing parameter for max_passengers
    bus_1 = Bus(4)

    #Instancing Classroom Object
    new_classroom = Classroom()

    #Instancing Human Object
    new_human = Human()

    
    while True:

        try:
            
            print("Choose an option to proceed:")
            print("1. Calculate circle area")
            print("2. Add passengers into the bus")
            print("3. Remove passengers from the bus")
            print("4. Add a new student")
            print("5. Check students information")
            print("6. Check the Top 3 students with highest grade-point average")
            print("7. Check the average grade-point of all students")
            print("8. CSV - export")
            print("9. CSV - import")
            print("10. Human Anatomy")
            print("11. Exit")

            option = int(input("Choose an option from the control panel: "))

            match option:
                
                case 1:
                    #1st exercise - Circle Area
                    while True:
                        try:
                            radius = input("Enter the circle radius: ")
                            if(radius.strip() == ""):
                                raise ValueError("The response cannot be empty.")
                    
                            radius = float(radius)
                            if radius < 0:
                                raise ValueError("The radius must be a positive number")
                            else:
                                break
                        except ValueError as ex:
                            print(f"Error: {ex}")
                    
                    #Instancing Circle Object and calling its method
                    new_circle = Circle(radius)
                    print(f"The area is {new_circle.get_area()}")
                
                case 2:
                    #2nd exercise - To add passengers
                    while True:
                        if(len(bus_1.bus_quota) >= bus_1.max_passengers):
                            print("The bus is full of its capacity. You cannot add more passengers")
                            break
                        else:
                            answer = input("Would you like to add a new passenger? Yes/No ")
                            if(answer.lower() == "yes"):
                                passenger = Person()
                                bus_1.to_add_passengers(passenger)
                            elif(answer.lower() == "no"):
                                break
                            else:
                                pass
                    
                    print("List of passengers:")
                    for passenger in bus_1.bus_quota:
                        print(f"{passenger}")
                    
                case 3:
                    #3rd exercise - To remove passengers
                    if(len(bus_1.bus_quota) == 0):
                        print("The bus is currently empty. Please consider adding passengers first")
                    else:
                        bus_1.to_remove_passengers(passenger)
                        print("List of passengers:")
                        for passenger in bus_1.bus_quota:
                            print(f"{passenger}")

                case 4:
                    #4rd exercise - reassembling student-scorecard project to work with objects.
                    #Calling method to create a student
                    new_classroom.create_student()
      
                case 5:
                    #Showing the studing list
                    if(len(new_classroom.student_list) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                    else:
                        for student in new_classroom.student_list:
                            print(student)

                case 6:
                    #Calling method in order to show the top 3 students with the highest grade-point average
                    if(len(new_classroom.student_list) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                    else:
                        top_students = new_classroom.check_top_3_students()

                        print("Top 3 Students with Highest Grade-Point Average:")
                        for student in top_students[0:3]:
                            print(student)

                case 7:
                    #Calling method in order to show the average grade-point of all students
                    if(len(new_classroom.student_list) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                    else:
                        average_grade_point_for_all_students = new_classroom.calculate_average_grade_point_for_all_students()
                        print(f"The average grade-point of all students is: {average_grade_point_for_all_students}")

                case 8:
                    #Calling method to export the student list to a CSV file once the student objetcs have been changed to dicts.
                    if(len(new_classroom.student_list) == 0):
                        print("No students have been added yet. There's no data to export.")
                    else:
                        student_objects = new_classroom.student_list
                        data = [vars(student) for student in student_objects] #To turn student objets into dicts 
                        headers = data[0].keys()
                        new_classroom.student_list = export_csv_file(CSV_FILE_PATH, data, headers)
                     
                case 9:
                    #Calling method to import data from a CSV file. It was necessary to use a 
                    if not os.path.exists(CSV_FILE_PATH):
                        print("There are no files to import. Please make sure that the file exists.")
                    else:
                        new_classroom.student_list = import_csv_file(CSV_FILE_PATH)
    
                case 10:
                    for body_part in new_human.anatomy():
                            print(body_part)

                case 11:
                    print("Closing the app.")
                    break

                case _:
                    raise ValueError("Invalid option, please choose a valid option from the menu:")
            
        except ValueError:
            print("Error: Invalid option, please choose a valid option from the menu:")
        
        except Exception as e:
            print(f"Error: {e}")