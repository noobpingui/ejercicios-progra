import os

from Classes.csv_actions import export_csv_file, import_csv_file, CSV_FILE_PATH

from Classes.Figures import Figures
from Classes.Bus import Bus
from Classes.Classroom import Classroom
from Classes.Human import Human

#function to display the dashboard menu and handle user interactions
def dashboard_menu(current_option):
    
    #Instancing Bus Object and passing parameter for max_passengers
    bus_1 = Bus(6)

    #Instancing Classroom Object
    new_classroom = Classroom()

    #Instancing Figures Object
    new_figure = Figures()

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
                    #Calling method to calculate circule area and showing the outcome
                    print(f"The area is {new_figure.get_circle_area()}")
                
                case 2:
                    #2nd exercise - To add passengers
                    #The object Person gets created in the method itself every time a new passenger requires to be added.
                    bus_1.to_add_passengers()
                    print(f"List of passengers: {bus_1.bus_quota}")
                    
                case 3:
                    #3rd exercise - To remove passengers
                    # if(len(bus_1.bus_quota) == 0):
                    #     print("The bus is currently empty. Please consider adding passengers first")
                    #     break
                    # else:
                        bus_1.to_remove_passengers()
                        print(f"List of passengers: {bus_1.bus_quota}")

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