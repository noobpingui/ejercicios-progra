

class Student():
    
    #Contructor
    def __init__(self, name, classroom, Spanish_grade, English_grade, Social_Studies_grade, Science_grade, average_grade_point):
        self.name = name
        self.classroom = classroom
        self.Spanish_grade = Spanish_grade
        self.English_grade = English_grade
        self.Social_Studies_grade = Social_Studies_grade
        self.Science_grade = Science_grade
        self.average_grade_point = average_grade_point


    #To turn dics into a new student object once the csv file has been imported
    @classmethod
    def from_dict(cls, row: dict):
        return cls(
            name=row["name"],
            classroom=row["classroom"],
            Spanish_grade=float(row["Spanish_grade"]),
            English_grade=float(row["English_grade"]),
            Social_Studies_grade=float(row["Social_Studies_grade"]),
            Science_grade=float(row["Science_grade"]),
            average_grade_point=float(row["average_grade_point"]),
        )

    #To format the data for student object
    def __str__(self):
        return(
            f"Name: {self.name} -  "
            f"Classroom: {self.classroom} -  "
            f"Spanish grade: {self.Spanish_grade} -  "
            f"English grade: {self.English_grade} -  "
            f"Social Studies grade: {self.Social_Studies_grade} -  "
            f"Science grade: {self.Science_grade} -  "
            f"Average grade point: {self.average_grade_point}"
        )