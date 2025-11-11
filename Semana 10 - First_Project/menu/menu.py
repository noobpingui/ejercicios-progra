import csv, os
from actions.actions import add_student, check_student_information, check_top_3_students, calculate_average_grade_point
from data.csv_actions import export_csv_file, import_csv_file, CSV_FILE_PATH


#function to display the dashboard menu and handle user interactions
def dashboard_menu(current_option):
    
    
    student_List = []

    while True:

        try:
            
            print("Choose an option to proceed:")
            print("1. Add a new student")
            print("2. Check student information")
            print("3. Check the Top 3 students with highest grade-point average")
            print("4. Check the average grade-point of all students")
            print("5. CSV - export")
            print("6. CSV - import")
            print("7. Exit")

            option = int(input("Choose an option from the control panel: "))

            match option:
                case 1:
                    
                    student_List = add_student(student_List)    
                               
                case 2:
                    if(len(student_List) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                        break
                    else:
                        check_student_information(student_List)
                  
                case 3:
                    if(len(student_List) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                    else:
                        top_students = sorted(student_List, 
                                   key=check_top_3_students, 
                                   reverse=True)

                        print("Top 3 Students with Highest Grade-Point Average:")
                        for student in top_students[0:3]:
                            print(f"Name: {student['full_name']}, Average Grade Point: {student['average_grade_point']}")

                case 4:
                    if(len(student_List) == 0):
                        print("No students have been added yet. Please consider adding students first.")
                    else:
                        calculate_average_grade_point(student_List)

                case 5:
                    if(len(student_List) == 0):
                        print("No students have been added yet. There's no data to export.")
                    else:
                        student_List = export_csv_file(CSV_FILE_PATH, student_List, student_List[0].keys())
                     
                case 6:
                    if not os.path.exists(CSV_FILE_PATH):
                        print("There are no files to import. Please make sure that the file exists.")
                    else:
                        student_List = import_csv_file(CSV_FILE_PATH)
                    
                case 7:
                    print("Closing the app.")
                    break

                case _:
                    raise ValueError("Invalid option, please choose a valid option from the menu:")
            
        except ValueError:
            print("Error: Invalid option, please choose a valid option from the menu:")
        
        except Exception as e:
            print(f"Error: {e}")


