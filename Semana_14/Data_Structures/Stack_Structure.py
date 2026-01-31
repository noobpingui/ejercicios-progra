
class Node():

    data: str

    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class Stack():
    top: Node
    
    def __init__(self):
        self.top = None
        

    def push_nodes(self, data):
        new_node = Node(data, self.top)
        self.top = new_node 


    def pop_nodes(self):
        if self.top is None:
            print("The stack is empty")
            return None

        removed_node = self.top
        self.top = self.top.next
        return removed_node.data

    def print_structure(self):
        current_node = self.top

        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next
