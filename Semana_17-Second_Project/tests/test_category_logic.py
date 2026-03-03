from Business_Logic.categories import Category_Logic
import pytest

# use command 'python -m pytest' to run tests

# ---- Unit Tests for function: add_new_category ----

def test_add_new_category_with_empty_string():
    # Arrange
    input = ""
    # Act / Assert
    category_logic_object = Category_Logic()
    result = category_logic_object.add_new_category(input)

    assert "error" in result
    assert "The title cannot be empty" in result["error"]

def test_add_new_category_with_invalid_characters():
    # Arrange
    input = "@#$"
    # Act / Assert
    category_logic_object = Category_Logic()
    result = category_logic_object.add_new_category(input)

    assert "error" in result
    assert "The category can only contain alphabetic characters and no spaces" in result["error"]

# ---- Unit Tests for function: delete_category ----

def test_delete_category_when_no_categories_have_been_added_yet():
    # Arrange
    input = ""
    # Act / Assert
    category_logic_object = Category_Logic()
    result = category_logic_object.delete_category(input)

    assert "error" in result
    assert "No categories have been added yet" in result["error"]



