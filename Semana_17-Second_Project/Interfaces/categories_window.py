import FreeSimpleGUI as sg
from Business_Logic.categories import Category_Logic
from Data.data_persistence import Data, CSV_FILE_PATH_CATEGORIES

from Business_Logic.categories import Category_Logic

class Category_window:

    def __init__(self, category_logic):
        
        self.category_logic = category_logic
        self.categories_window = None

    def open_categories_window(self):

        data_persistance_object = Data()

        headers = ["Category"]

        layout = [
                [
                    sg.Text('Add a new category')
                ],
                [
                    sg.Input(key='-INPUT-', size=(30,1), enable_events=True, focus=True) 
                ],
                [
                    sg.Text('List of categories'), sg.Combo(self.category_logic.get_categories(), key='-COMBO-', readonly=True)
                ],
                [
                    sg.Button('Add', key='-ADD_BUTTON-'), sg.Button('Remove', key='-REMOVE_BUTTON-'), sg.VSeparator(), sg.Button('Exit')
                ]
            ]

        self.categories_window = sg.Window('Categories', layout)
        
        while True:

            event, values = self.categories_window.Read()

            #Event to close window
            if event == sg.WIN_CLOSED or event == 'Exit':
                data = self.category_logic.get_categories()
                result = data_persistance_object.export_categories(CSV_FILE_PATH_CATEGORIES, data, headers)
                if "error" not in result:
                    result["success"]
                else:
                    pass    

                break
            
            #Event to add categories
            if event == '-ADD_BUTTON-':
                new_category = values['-INPUT-']
                
                result = self.category_logic.add_new_category(new_category)
                if "error" in result:
                     sg.popup("Warning",result["error"], auto_close=True, auto_close_duration=5)

                else:
                    categories = result["success"]
                    self.categories_window['-COMBO-'].update(values=categories)
                    self.categories_window['-INPUT-'].update("")
            
            #Event to remove categories
            if event == '-REMOVE_BUTTON-':
                selected_category = values['-COMBO-']
                
                result = self.category_logic.delete_category(selected_category)
                if "error" in result:
                     sg.popup("Warning",result["error"], auto_close=True, auto_close_duration=5)

                else:
                    categories = result["success"]
                    self.categories_window['-COMBO-'].update(values=categories)
                    self.categories_window['-INPUT-'].update("")
        
        self.categories_window.Close()
        return self.category_logic.get_categories()
    
    