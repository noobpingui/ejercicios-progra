from Classes.bubble_sort import SortingAlgorithms
import pytest

# use command 'python -m pytest' to run tests

# Cree los siguientes unit tests para el algoritmo bubble_sort:

# a. Funciona con una lista pequeña.
def test_bubble_sort_algorithm_with_small_list():
    # Arrange
    input_list = [-11, 68, 6,]
    # Act
    my_bubble_sort = SortingAlgorithms(input_list)
    result = my_bubble_sort.bubble_Sort()
    # Assert
    assert result == [-11,6,68]



# b. Funciona con una lista grande (de más de 100 elementos.)
def test_bubble_sort_algorithm_with_big_list():
    # Arrange
    input_list = [143, 59, 12, 178, 33, 91, 4, 157, 83, 129, 
    47, 3, 199, 65, 150, 88, 19, 110, 55, 134, 
    26, 140, 101, 73, 39, 186, 98, 45, 170, 9, 
    67, 112, 123, 35, 160, 80, 152, 14, 49, 176,
    30, 96, 21, 121, 57, 166, 7, 118, 131, 104,
    41, 195, 28, 87, 15, 190, 60, 125, 99, 24,
    174, 52, 137, 82, 1, 158, 38, 115, 108, 69,
    181, 46, 135, 17, 153, 10, 173, 85, 34, 197,
    63, 126, 142, 71, 187, 54, 119, 93, 29, 168,
    13, 111, 146, 5, 182, 44, 120, 78, 27, 161,
    95, 50, 193, 31, 109, 90, 25, 183, 74, 132,
    76, 16, 172, 36, 149, 8, 180, 56, 141, 72,
    194, 58, 113, 89, 23, 167, 62, 138, 84, 2,
    155, 40, 147, 11, 171, 48, 117, 94, 22, 188,
    79, 133, 75, 18, 154, 6, 175, 53, 139, 92,
    196, 64, 122, 86, 20, 165, 61, 130, 81, 97,
    184, 43, 145, 32, 159, 51, 114, 100, 37, 192,
    66, 124, 70, 28, 185, 42, 136, 77, 26, 164,
    68, 127, 102, 35, 198, 57, 144, 73, 14, 189,
    52, 151, 107, 41, 179, 60, 128, 83, 29, 163]
    # Act
    my_bubble_sort = SortingAlgorithms(input_list)
    result = my_bubble_sort.bubble_Sort()
    # Assert
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                      25, 26, 26, 27, 28, 28, 29, 29, 30, 31, 32, 33, 34, 35, 35, 36, 37, 38, 39, 40, 41, 41, 42, 
                      43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 52, 53, 54, 55, 56, 57, 57, 58, 59, 60, 60, 61, 62, 
                      63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 83, 
                      84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 104, 107, 108, 
                      109, 110, 111, 112, 113, 114, 115, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 
                      129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 
                      149, 150, 151, 152, 153, 154, 155, 157, 158, 159, 160, 161, 163, 164, 165, 166, 167, 168, 170, 
                      171, 172, 173, 174, 175, 176, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 
                      192, 193, 194, 195, 196, 197, 198, 199]
    


# c. Funciona con una lista vacía.
def test_bubble_sort_algorithm_with_empty_list():
    # Arrange
    input_list = []
    # Act
    my_bubble_sort = SortingAlgorithms(input_list)
    result = my_bubble_sort.bubble_Sort()
    # Assert
    assert result == []



# d. No funciona con parámetros que no sean una lista.
def test_bubble_sort_algorithm_with_a_diferent_input():
    # Arrange
    input = "AIUGNBD"
    # Act / Assert
    with pytest.raises(TypeError):
        my_bubble_sort = SortingAlgorithms(input)
        my_bubble_sort.bubble_Sort()
  
