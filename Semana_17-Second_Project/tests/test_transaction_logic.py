from Business_Logic.transaction import Transaction
import pytest


# ---- Unit Tests for function: add_new_transaction ----
#Expected input: title:str, amount: str, category: str, transaction_type: str

def test_add_new_transaction_with_empty_title():
    # Arrange
    input = ""
    # Act / Assert
    transaction_object = Transaction()
    result = transaction_object.add_new_transaction(input, "40", "Health", "income")

    assert "error" in result
    assert "The title cannot be empty" in result["error"]


def test_add_new_transaction_with_invalid_characters_in_title():
    # Arrange
    input = "@#%&34"
    # Act / Assert
    transaction_object = Transaction()
    result = transaction_object.add_new_transaction(input, "40", "Health", "income")

    assert "error" in result
    assert "The title can only contain alphabetic characters and no spaces" in result["error"]

def test_add_new_transaction_with_empty_amount():
    # Arrange
    input = ""
    # Act / Assert
    transaction_object = Transaction()
    result = transaction_object.add_new_transaction("Gym", input, "Health", "income")

    assert "error" in result
    assert "The amount cannot be empty" in result["error"]

def test_add_new_transaction_with_invalid_characters_in_amount():
    # Arrange
    input = "#Fss#$@"
    # Act / Assert
    transaction_object = Transaction()
    result = transaction_object.add_new_transaction("Gym", input, "Health", "income")

    assert "error" in result
    assert "The amount can only contain digits and no spaces" in result["error"]

# ---- Unit Tests for function: delete_transaction_item ----
#Expected input: index: int

def test_delete_transaction_item_without_transaction_data():
    # Arrange
    input = ""
    # Act / Assert
    transaction_object = Transaction()
    result = transaction_object.delete_transaction_item(input)

    assert "error" in result
    assert "There are no transactions to delete" in result["error"]

