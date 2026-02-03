

class SortingAlgorithms:
    def __init__(self, num_list: list):
        self.num_list = num_list
        pass

#Exercise 1 - Crea un bubble_sort por tu cuenta sin revisar el código de la lección.
# [18, -11, 68, 6, 32, 53, -2]

    def bubble_Sort(self):
        for column in range(0, len(self.num_list) -1):
            for row in range(0, len(self.num_list) -column -1):
                current_num = self.num_list[row]
                next_num = self.num_list[row +1]
                if(current_num) > (next_num):
                    self.num_list[row] = next_num
                    self.num_list[row+1] = current_num
    
        return self.num_list
    
#Exercise 2 - Modifica el bubble_sort para que funcione de derecha a izquierda, ordenando los números menores primero
# [18, -11, 68, 6, 32, 53, -2]

    def reversed_bubble_Sort(self):
        for column in range(len(self.num_list) -1, -1, -1):
            for row in range(len(self.num_list)-1 , 0, -1):
                current_num = self.num_list[row]
                next_num = self.num_list[row -1]
                if(current_num) > (next_num):
                    self.num_list[row-1] = current_num
                    self.num_list[row] = next_num
    
        return self.num_list
