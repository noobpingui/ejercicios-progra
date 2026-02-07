from Classes.Exercises_Week_6 import sum_list, reverse_string, get_upper_case, get_lower_case, sort_list, get_prime_numbers
import pytest

#Cree unit tests para probar 3 casos de éxito distintos de cada uno de los ejercicios de semana 6 (exceptuando el 1 y 2).

#---------------------------------

# a. Exercise 3
def test_sum_list_with_big_list():
    # Arrange
    input_list = [143, 59, 12, 178, 33, 91, 4, 157, 83, 129, 
    47, 3, 199, 65, 150, 88, 19, 110, 55, 134, 
    26, 140, 101, 73, 39, 186, 98, 45, 170, 9]
    # Act
    result = sum_list(input_list)
    # Assert
    assert result == 2646

def test_sum_list_with_a_different_input():
    # Arrange
    input = 1456
    # Act / Assert
    with pytest.raises(TypeError):
        assert sum_list(input)

def test_sum_list_with_empty_list(): 
    # Arrange
    input_list = []
    # Act
    result = sum_list(input_list)
    # Assert
    assert result == 0

#---------------------------------

# b. Exercise 4
def test_reverse_string_with_a_different_input():
    # Arrange
    input = [2,4,"f","fdsfg",54]
    # Act / Assert
    with pytest.raises(TypeError):
        assert reverse_string(input)

def test_reverse_string_success():
    # Arrange
    input = "This is a string"
    # Act
    result = reverse_string(input)
    # Assert
    assert result == "gnirts a si sihT"

def test_reverse_string_with_no_string_given():
    # Arrange
    input = ""
    # Act
    result = reverse_string(input)
    # Assert
    assert result == ""

#---------------------------------

#c. Exercise 5
def test_get_upper_case_with_a_different_input():
    # Arrange
    input = 234.524
    # Act / Assert
    with pytest.raises(TypeError):
        assert get_upper_case(input)

def test_get_upper_case_success():
    # Arrange
    input = "I would love visiting Costa Rica"
    # Act
    result = get_upper_case(input)
    # Assert
    assert result == 3

def test_get_upper_case_with_invalid_characters():
    # Arrange
    input = "A n3w P@th f0r You#g pp/"
    # Act / Assert
    with pytest.raises(ValueError):
        assert get_upper_case(input)



def test_get_lower_case_with_a_different_input():
    # Arrange
    input = ["friday",4,"uy","fdsfg",{'value':35}]
    # Act / Assert
    with pytest.raises(TypeError):
        assert get_lower_case(input)

def test_get_lower_case_success():
    # Arrange
    input = "I would love visiting Costa Rica"
    # Act
    result = get_lower_case(input)
    # Assert
    assert result == 24

def test_get_lower_case_with_invalid_characters():
    # Arrange
    input = "A n3w P@th f0r You#g pp/"
    # Act / Assert
    with pytest.raises(ValueError):
        assert get_lower_case(input)

#---------------------------------

#d. Exercise 6
def test_sort_list_with_a_different_input():
    # Arrange
    input = ["friday",4,"uy","fdsfg",{'value':35}]
    # Act / Assert
    with pytest.raises(TypeError):
        assert sort_list(input)

def test_sort_list_success():
    # Arrange
    input = "house-zoo-juice-sweater-hammer-worm-picture-board-airplane-gun"
    # Act
    result = sort_list(input)
    # Assert
    assert result == "airplane-board-gun-hammer-house-juice-picture-sweater-worm-zoo"

def test_sort_list_with_invalid_characters():
    # Arrange
    input = "house/zoo/juices/weater/hammer-worm-picture@board^airplane-g#n"
    # Act / Assert
    with pytest.raises(ValueError):
        assert sort_list(input)

#---------------------------------

#e. Exercise 7
def test_get_prime_numbers_with_a_different_input():
    # Arrang"e
    input = "Im not a list"
    input2 = []
    # Act / Assert
    with pytest.raises(TypeError):
        assert get_prime_numbers(input, input2)

def test_get_prime_numbers_success():
    # Arrange
    input = [1, 3, 4, 60, 7, 13, 9, 67, 22, 37, 44, 71, 99, 25]
    input2 = []
    # Act
    result = get_prime_numbers(input, input2)
    # Assert
    assert result == [3, 7, 13, 67, 37, 71]

def test_get_prime_numbers_with_invalid_characters_in_the_list():
    # Arrang"e
    input = [60, "&", 15, 19, "A", 3, "n"]
    input2 = []
    # Act / Assert
    with pytest.raises(ValueError):
        assert get_prime_numbers(input, input2)