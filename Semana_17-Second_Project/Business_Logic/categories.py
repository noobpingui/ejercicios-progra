
class Category_Logic:
    def __init__(self):

        self.category_list = []

    def add_new_category(self, new_category: str):
        new_category = new_category.strip().capitalize()

        try:
            if new_category.strip() == "":
                raise ValueError(f"The title cannot be empty")

            elif not all(char.isalpha() for char in new_category):
                raise TypeError(f"The category can only contain alphabetic characters and no spaces")

            elif new_category in self.category_list:
                raise ValueError(f"The category already exists")

            elif new_category and new_category not in self.category_list:
                self.category_list.append(new_category)
                return  {"success": self.category_list}

        except Exception as ex:
            return {"error": str(ex)}


    def delete_category(self, selected_category: str):

        selected_category = selected_category.strip().capitalize()

        try:
            if not self.category_list:
                raise ValueError(f"No categories have been added yet")
            
            elif selected_category == "":
                raise ValueError(f"Please make sure to select a category from the list first")
            
            elif selected_category in self.category_list:
                self.category_list.remove(selected_category)
                return  {"success": self.category_list}
                

        except Exception as ex:
            return {"error": str(ex)}
    

    def get_categories(self):
        return self.category_list
