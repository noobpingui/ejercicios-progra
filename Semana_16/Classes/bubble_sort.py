
class SortingAlgorithms:
    def __init__(self, num_list: list):
        self.num_list = num_list
        pass


    def bubble_Sort(self):
        if not isinstance(self.num_list, list):
            raise TypeError (f"The parameter is not a list")
        else:
            for column in range(0, len(self.num_list) -1):
                for row in range(0, len(self.num_list) -column -1):
                    current_num = self.num_list[row]
                    next_num = self.num_list[row +1]
                    if(current_num) > (next_num):
                        self.num_list[row] = next_num
                        self.num_list[row+1] = current_num
    
        return self.num_list