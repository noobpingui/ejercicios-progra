from Data_Structures.Stack_Structure import Stack
from Data_Structures.Double_Ended_Queue_Structure import Double_Ended_Queue 
from Data_Structures.Binary_Tree_Structure import Binary_Tree, Node

#----------------
#----------------
#----------------
#----------------
#----------------
#----------------
#Exercise1
my_stack = Stack()

#Creating Nodes - Pushing nodes into the Stack
my_stack.push_nodes("Im the first node")
my_stack.push_nodes("Im the second node")
my_stack.push_nodes("Im the third node")

print("Printing STACK structure after adding nodes: ")
my_stack.print_structure()

#Removing Nodes - Popping nodes from the Stack
my_stack.pop_nodes()

print("Printing STACK structure after removing a node")
my_stack.print_structure()

#----------------
#----------------
#----------------
#----------------
#----------------
#----------------
#Exercise2
my_deque = Double_Ended_Queue()

#Creating Nodes - Pushing nodes into the DEQUE
my_deque.push_left("I got in from head/1st node")
my_deque.push_right("I got in from tail/2nd node")
my_deque.push_left("I got in from head/3rd node")

print("Printing DEQUE structure after adding nodes: ")
my_deque.print_structure()

#Removing Nodes - Popping nodes from the DEQUE
my_deque.pop_left()
my_deque.pop_right()

print("Printing DEQUE structure after removing nodes: ")
my_deque.print_structure()

#----------------
#----------------
#----------------
#----------------
#----------------
#----------------
#Exercise3
my_binary_tree = Binary_Tree()

#Instancing root node
root_node = Node(10)

#Instancing nodes for left side from root node
root_node.left = Node(5)
root_node.left.left = Node(2)
root_node.left.right = Node(6)

#Instancing nodes for right side from root node
root_node.right = Node(15)
root_node.right.right = Node(7)
root_node.right.left = Node(3)


print("In-order:")
my_binary_tree.print_structure_inOrder(root_node)

print("Pre-order:")
my_binary_tree.print_structure_preOrder(root_node)

print("Post-order:")
my_binary_tree.print_structure_postOrder(root_node)