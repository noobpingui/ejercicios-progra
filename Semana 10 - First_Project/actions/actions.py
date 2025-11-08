
#Functions to perform actions on student data
def add_student(student_List):

    while True:
        
        student_ScoreCard = {}

        while True:
            try:
                full_name = input("Enter the student's name: ")
                if(full_name.strip() == ""):
                    raise ValueError("The name cannot be empty.")
                elif not all(x.isalpha() or x.isspace() for x in full_name):
                    raise ValueError("The name can only contain alphabetic characters and spaces.")
                else:
                    student_ScoreCard["full_name"] = full_name 
                    break
            except ValueError as ex:
                print(f"Error: {ex}")    

        while True:
            try:
                classroom = input("Enter the student's classroom: ")
                if(classroom.strip() == ""):
                    raise ValueError("The classroom cannot be empty.")
                elif not all(x.isalnum() or x.isalpha() for x in classroom):
                    raise ValueError("The classroom can only contain alphanumeric characters.")
                else:
                    student_ScoreCard["classroom"] = classroom
                    break
            except ValueError as ex:
                print(f"Error: {ex}") 

        while True:
            try:
                is_empty = input("Enter the student's Spanish grade: ")
                if(is_empty.strip() == ""):
                    raise ValueError("The grade cannot be empty.")
                
                Spanish_grade = float(is_empty)
                if Spanish_grade < 0 or Spanish_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    student_ScoreCard["Spanish_grade"] = Spanish_grade
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                is_empty = input("Enter the student's English grade: ")
                if(is_empty.strip() == ""):
                    raise ValueError("The grade cannot be empty.")


                English_grade = float(is_empty)
                if English_grade < 0 or English_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    student_ScoreCard["English_grade"] = English_grade
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                is_empty = input("Enter the student's Social Studies grade: ")
                if(is_empty.strip() == ""):
                    raise ValueError("The grade cannot be empty.")

                Social_Studies_grade = float(is_empty)
                if Social_Studies_grade < 0 or Social_Studies_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    student_ScoreCard["Social_Studies_grade"] = Social_Studies_grade
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                is_empty = input("Enter the student's Science grade: ")
                if(is_empty.strip() == ""):
                    raise ValueError("The grade cannot be empty.")

                Science_grade = float(is_empty)
                if Science_grade < 0 or Science_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    student_ScoreCard["Science_grade"] = Science_grade
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        average_grade_point = (Spanish_grade + English_grade + Social_Studies_grade + Science_grade) / 4
        student_ScoreCard["average_grade_point"] = average_grade_point

        student_List.append(student_ScoreCard)

        print("Student added successfully!")
        continue_adding = input("Would like to add another student? (yes/no)")
        if continue_adding.lower() != "yes":
            break

    return student_List

def check_student_information(student_list):
    print("Students Information:")
    for data in student_list:
        print(f"Name: {data['full_name']}, Classroom: {data['classroom']}, Spanish Grade: {data['Spanish_grade']}, English Grade: {data['English_grade']}, Social Studies Grade: {data['Social_Studies_grade']}, Science Grade: {data['Science_grade']}, Average Grade Point: {data['average_grade_point']}")

def check_top_3_students(student):
    return student['average_grade_point']

def calculate_average_grade_point(student_list):
    total_grade_point = sum(student['average_grade_point'] for student in student_list)
    average_grade_point = total_grade_point / len(student_list)
    print(f"The average grade-point of all students is: {average_grade_point}")

   

