from Classes.Student import Student

class Classroom():
    
    def __init__(self):
        
        self.student_list = []

    def create_student(self):

        while True:
            try:
                self.name = input("Enter the student's name: ")
                if(self.name.strip() == ""):
                    raise ValueError("The name cannot be empty.")
                elif not all(x.isalpha() or x.isspace() for x in self.name):
                    raise ValueError("The name can only contain alphabetic characters and spaces.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                self.classroom = input("Enter the student's classroom: ")
                if(self.classroom.strip() == ""):
                    raise ValueError("The classroom cannot be empty.")
                elif not all(x.isalnum() or x.isalpha() for x in self.classroom):
                    raise ValueError("The classroom can only contain alphanumeric characters.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}") 
        
        while True:
            try:
                self.Spanish_grade = input("Enter the student's Spanish grade: ")
                if(self.Spanish_grade.strip() == ""):
                    raise ValueError("The grade cannot be empty.")
                
                self.Spanish_grade = float(self.Spanish_grade)
                if self.Spanish_grade < 0 or self.Spanish_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")
        
        while True:
            try:
                self.English_grade = input("Enter the student's English grade: ")
                if(self.English_grade.strip() == ""):
                    raise ValueError("The grade cannot be empty.")
                
                self.English_grade = float(self.English_grade)
                if self.English_grade < 0 or self.English_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                self.Social_Studies_grade = input("Enter the student's Social Studies grade: ")
                if(self.Social_Studies_grade.strip() == ""):
                    raise ValueError("The grade cannot be empty.")

                self.Social_Studies_grade = float(self.Social_Studies_grade)
                if self.Social_Studies_grade < 0 or self.Social_Studies_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")

        while True:
            try:
                self.Science_grade = input("Enter the student's Science grade: ")
                if(self.Science_grade.strip() == ""):
                    raise ValueError("The grade cannot be empty.")

                self.Science_grade = float(self.Science_grade)
                if self.Science_grade < 0 or self.Science_grade > 100:
                    raise ValueError("The grade must be between 0 and 100.")
                else:
                    break
            except ValueError as ex:
                print(f"Error: {ex}")
        
        self.average_grade_point = (self.Spanish_grade + self.English_grade + self.Social_Studies_grade + self.Science_grade) / 4

        new_student = Student(self.name, self.classroom, self.Spanish_grade, self.English_grade, self.Social_Studies_grade, self.Science_grade, self.average_grade_point)
        self.student_list.append(new_student)
        return self.student_list


    def check_top_3_students(self):
        
        top_3_students = sorted(self.student_list,
                                key=lambda sorted_list: sorted_list.average_grade_point,
                                reverse=True)
        
        return top_3_students
    
    def calculate_average_grade_point_for_all_students(self):
        total_grade_point = 0
        
        for student in self.student_list:
            total_grade_point += student.average_grade_point

        average_grade_point_for_all_students = total_grade_point / len(self.student_list)

        return round(average_grade_point_for_all_students,2)