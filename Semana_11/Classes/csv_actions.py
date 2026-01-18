import csv, os
from Classes.Student import Student

#I had to investigate a little bit about file paths in order to be able to create the CSV file in the correct folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
CSV_FILE_PATH = os.path.join(DATA_FOLDER, 'student_data.csv')


#functions to export and import CSV files
def export_csv_file(file_path, data, headers):
    try:
        with open(file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=headers, dialect='excel')
            writer.writeheader()
            writer.writerows(data)
        print(f"The CSV File has been created successfully in the path: {file_path}")
    except FileExistsError:
        print(f"The file {file_path} already exists.")
    except Exception as ex:
        print(f"An error occurred while creating the file: {ex}")
    return data

def import_csv_file(file_path):
    student_list = []
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student_list.append(Student.from_dict(row))
                
        print(f"The CSV File has been imported successfully from the path: {file_path}")
    except FileNotFoundError:
        print(f"There are no files to import. Please make sure that the file exists.")
    except Exception as ex:
        print(f"An error occurred while importing the file: {ex}")
    
    return student_list