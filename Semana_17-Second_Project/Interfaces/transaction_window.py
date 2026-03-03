import FreeSimpleGUI as sg
from Interfaces.categories_window import Category_window

from Business_Logic.categories import Category_Logic
from Business_Logic.transaction import Transaction

class Transaction_window():
    def __init__(self, transaction, category_logic):
        self.transaction = transaction
        self.category_logic = category_logic
        self.category_window = Category_window(category_logic)
        self.transaction_window = None

    def open_transaction_window(self, transaction_type):
        
        income_layout = [
                [
                    sg.Text('Add a new income')
                ],
                [
                    sg.Text('Title:'), sg.Input(key='-INPUT-', size=(25,1), enable_events=True, focus=True) 
                ],
                [
                    sg.Text('Amount:'), sg.Input(key='-INPUT2-', size=(22,1), enable_events=True)
                ],
                [
                    sg.Button('Add a new category'), sg.Combo(self.category_logic.get_categories(), key='-COMBO-', readonly=True)
                ],
                [
                    sg.Button('Add', key='-ADD_BUTTON-'), sg.VSeparator(), sg.Button('Exit')
                ]
            ]
        
        expenses_layout = [
                [
                    sg.Text('Add a new expense')
                ],
                [
                    sg.Text('Title:'), sg.Input(key='-INPUT-', size=(25,1), enable_events=True, focus=True) 
                ],
                [
                    sg.Text('Amount:'), sg.Input(key='-INPUT2-', size=(22,1), enable_events=True)
                ],
                [
                    sg.Button('Add a new category'), sg.Combo(self.category_logic.get_categories(), key='-COMBO-', readonly=True)
                ],
                [
                    sg.Button('Add', key='-ADD_BUTTON-'), sg.VSeparator(), sg.Button('Exit')
                ]
            ]

        if transaction_type == 'income':
            self.transaction_window = sg.Window('Income', income_layout)
        else:
            self.transaction_window = sg.Window('Expenses', expenses_layout)
        
        while True:
            event, values = self.transaction_window.Read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Add a new category':


                self.transaction_window.Hide()
                categories = self.category_window.open_categories_window()
                self.transaction_window['-COMBO-'].Update(values=categories)
                self.transaction_window.UnHide()
                
            if event == "-ADD_BUTTON-":
                title = values['-INPUT-']
                amount = values['-INPUT2-']
                selected_category = values['-COMBO-']

                result = self.transaction.add_new_transaction(
                    title=title,
                    amount=amount,
                    category=selected_category,
                    transaction_type=transaction_type
                )

                if "error" in result:
                    sg.popup("Warning",result["error"], auto_close=True, auto_close_duration=5)

                else:
                    result["success"]
                    self.transaction_window['-INPUT-'].update("")
                    self.transaction_window['-INPUT2-'].update("")
                    
                
        self.transaction_window.Close()
        return self.transaction.get_transaction_data()