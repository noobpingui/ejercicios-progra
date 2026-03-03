import FreeSimpleGUI as sg

from Interfaces.transaction_window import Transaction_window
from Interfaces.data_visualization_window import Visualization

from Business_Logic.categories import Category_Logic
from Business_Logic.transaction import Transaction

from Data.data_persistence import Data, CSV_FILE_PATH_TRANSACTIONS, CSV_FILE_PATH_CATEGORIES

def run():

    sg.theme('DarkGrey13')

    #---- Table Data ----

    transaction_data = Transaction()
    categories_data = Category_Logic()
    data_persistance_object = Data()
    visualization_object = Visualization()

    transaction_window = Transaction_window(transaction_data, categories_data)

    headings = ["Title", "Category", "Amount", "Income", "Expenses"]

    table_data = []

    table_column = [
        [sg.Table(
            values=table_data, 
            headings=headings, 
            max_col_width=25, 
            background_color='Black',
            auto_size_columns=True,
            display_row_numbers=False,
            justification='right',
            num_rows=10,
            #alternating_row_color='Blue',
            key='-TABLE-',
            tooltip='Data table')]
    ]


    button_column = [
        [sg.Button('Add Income', size=(12,2))],
        [sg.Button('Add Expenses', size=(12,2))],
        [sg.Button('Delete Item', size=(12,2))],
        #[sg.Button('Show Summary', key='-SHOW_SUMMARY-', size=(12,2))],
        [sg.HSeparator()],
        [sg.Button('Bonus', size=(12,2))],
        [sg.Button('Exit', size=(12,2))]
    ]


    #---- GUI Elements ----
    layout = [
        [sg.Image(r'C:\Users\alber\source\repos\Lyfter_Ejercicios\Semana_17-Second_Project\Images\Finances.png', key='-IMAGE-', size=(500, 425))],
        [
            sg.Column(table_column),
            sg.VSeparator(),
            sg.Column(button_column, vertical_alignment='top')
        ],
        [sg.Text("Total Income:"), sg.Text("0", key="-TOTAL_INCOME-")],
        [sg.Text("Total Expenses:"), sg.Text("0", key="-TOTAL_EXPENSES-")]
    
]

    #---- Window creation ----
    main_window = sg.Window("Personal Finance Manager", layout, finalize=True)

    total_income = 0.0
    total_expenses = 0.0

    # ---- To get table and income-expenses totals refreshed ----
    def refresh_table_and_totals():
        nonlocal total_income, total_expenses

        transactions = transaction_data.get_transaction_data()

        table_data_local = [
            [item["Title"], item["Category"], item["Amount"], item["Income"], item["Expenses"]]
            for item in transactions
        ]

        total_income = sum(
            float(item["Amount"]) for item in transactions
            if item["Income"] == "Yes"
        )
        total_expenses = sum(
            float(item["Amount"]) for item in transactions
            if item["Expenses"] == "Yes"
        )

        main_window['-TABLE-'].update(values=table_data_local)
        main_window["-TOTAL_INCOME-"].update(total_income)
        main_window["-TOTAL_EXPENSES-"].update(total_expenses)

    #---- To import transactions data once the app is running for the first time ----
    transaction_result = data_persistance_object.import_csv_file(CSV_FILE_PATH_TRANSACTIONS)

    if "error" not in transaction_result:
        imported_data = transaction_result["success"]
        transaction_data.transaction_data = imported_data
        refresh_table_and_totals()

    #---- To import the category list once the app is running for the first time ----
    category_result = data_persistance_object.import_categories(CSV_FILE_PATH_CATEGORIES)

    if "error" not in category_result:
        new_category_list = category_result["success"]
                        
        #---- To extract the values from Category header and turn it into a new list ----
        categories_data.category_list = [
            row["Category"]
            for row in new_category_list
        ]

    #---- Event Loop to process "events" and get the "values" from the inputs ----
    while True:
        
        event, values = main_window.read()


    #---- To export transactions data once the app has been closed ----
        if event == sg.WIN_CLOSED or event == 'Exit':

            data = transaction_data.get_transaction_data()

            result = data_persistance_object.export_csv_file(CSV_FILE_PATH_TRANSACTIONS, data, headings)
            if "error" not in result:
                result["success"]
            else:
                pass    

            break

    #---- To register a new Income ----
        elif event == 'Add Income':
            main_window.Hide()
            transaction_window.open_transaction_window(transaction_type="income")
            main_window.UnHide()

            incomes = transaction_data.get_transaction_data()

            refresh_table_and_totals()

    #---- To register a new Expense ----
        elif event == 'Add Expenses':
            main_window.Hide()
            transaction_window.open_transaction_window(transaction_type="expense")
            main_window.UnHide()

            refresh_table_and_totals()
    
    #---- To delete an item from the table ----
        elif event == 'Delete Item':

            selected_item = values['-TABLE-']
            if not selected_item:
                sg.popup("Warning", "Please select an item to delete", auto_close=True, auto_close_duration=4)
            else:
                index = selected_item[0]

                delete_item_result = transaction_data.delete_transaction_item(index)
                if "error" in delete_item_result:
                    sg.popup("Warning",result["error"], auto_close=True, auto_close_duration=5)

                else:
                    #new_items = delete_item_result["success"]
                   refresh_table_and_totals()
        
    #---- To show a summary for income and expenses ----
        # elif event == '-SHOW_SUMMARY-':
        #     sg.popup(
        #         "Summary",
        #         f"Total Income: {total_income}\nTotal Expenses: {total_expenses}",
        #         auto_close=False
        #     )

    #---- Bonus ----
        elif event == 'Bonus':
            main_window.Hide()
            visualization_object.show_bar_chart(total_income, total_expenses)
            main_window.UnHide()

    main_window.close()