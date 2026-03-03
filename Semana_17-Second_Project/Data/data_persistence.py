import csv, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR)
CSV_FILE_PATH_TRANSACTIONS = os.path.join(DATA_FOLDER, 'transactions.csv')
CSV_FILE_PATH_CATEGORIES = os.path.join(DATA_FOLDER, 'categories.csv')

class Data():
    def __init__(self):
       pass


    def export_csv_file(self, file_path, data, headers):
        try:
            # if(len(data) == 0):
            #     raise ValueError(f"There's no available data to export")
            # # if(os.path.exists(file_path)):
            # #     raise FileExistsError(f"The file exists already")
            
            # else:
                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=headers, dialect='excel')
                    writer.writeheader()
                    writer.writerows(data)
                #print(f"The CSV File has been created successfully in the path: {file_path}")
                return{"success": data}
            
        except Exception as ex:
            return{"error": str(ex)}



    def import_csv_file(self, file_path):
        try:
            # if not (os.path.exists(file_path)):
            #     raise FileExistsError(f"There are not files to import. Please make sure that the file exists.")
            # else:
                with open(file_path, "r", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    data = list(reader)   
                # print(f"The CSV File has been imported successfully from the path: {file_path}")
                return{"success": data}

        except Exception as ex:
            return{"error": str(ex)}
        

    def export_categories(self, file_path, data, headers):
        try:
            
            #to turn categories_list to dics
            new_data = [{"Category": item} for item in data]

            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=headers, dialect='excel')
                writer.writeheader()
                writer.writerows(new_data)
            #print(f"The CSV File has been created successfully in the path: {file_path}")
            return{"success": new_data}
            
        except Exception as ex:
            return{"error": str(ex)}
        
    def import_categories(self, file_path):
        try:
            # if not (os.path.exists(file_path)):
            #     raise FileExistsError(f"There are not files to import. Please make sure that the file exists.")
            # else:
                with open(file_path, "r", newline="", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    data = list(reader)   
                # print(f"The CSV File has been imported successfully from the path: {file_path}")
                return{"success": data}

        except Exception as ex:
            return{"error": str(ex)}