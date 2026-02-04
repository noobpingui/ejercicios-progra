from Classes.bubble_sort import SortingAlgorithms

# 1.Analice el algoritmo de bubble_sort usando la Big O Notation.


def bubble_Sort(self): 
        for column in range(0, len(self.num_list) -1): #O(n)
            for row in range(0, len(self.num_list) -column -1): #O(n)
                current_num = self.num_list[row] #O(1)
                next_num = self.num_list[row +1] #O(1)
                if(current_num) > (next_num): #O(1)
                    self.num_list[row] = next_num #O(1)
                    self.num_list[row+1] = current_num #O(1)
    
        return self.num_list #O(1)

num_list = [18, -11, 68, 6, 32, 53, -2] #O(1)
my_bubble_sort = SortingAlgorithms(num_list) #O(1)
print(f"List sorted: {my_bubble_sort.bubble_Sort()}") #O(n^2)

#R/ #O(n^2)


# 2.Analice los siguientes algoritmos usando la Big O Notation:

#print_numbers_times_2
def print_numbers_times_2(numbers_list): 
	for number in numbers_list: #O(n)
		print(number * 2) #O(1)
            
#R/ #O(n)

#check_if_lists_have_an_equal
def check_if_lists_have_an_equal(list_a, list_b): 
	for element_a in list_a: #O(n)
		for element_b in list_b: #O(n)
			if element_a == element_b: #O(1)
				return True #O(1)
				
	return False #O(1)

#R/ #O(n^2)

#print_10_or_less_elements
def print_10_or_less_elements(list_to_print):  
	list_len = len(list_to_print) #O(1)
	for index in range(min(list_len, 10)): #O(1) 
		print(list_to_print[index]) #O(1)
		

#generate_list_trios
def generate_list_trios(list_a, list_b, list_c): 
	result_list = [] #O(1)
	for element_a in list_a: #O(n)
		for element_b in list_b: #O(n)
			for element_c in list_c: #O(n)
				result_list.append(f'{element_a} {element_b} {element_c}') #O(1)
				
	return result_list #O(1)

# R/ #O(n^3)