
class Node():

    data: str

    def __init__(self, data, prev=None, next=None):
        self.data = data
        self.prev = prev
        self.next = next



class Double_Ended_Queue():
    head: Node
    tail: Node
    
    def __init__(self):
        self.head = None
        self.tail = None


    #PUSH METHODS
    def push_left(self, data):
        new_node = Node(data, None, self.head)
        if(self.head):
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        

    def push_right(self, data):
        new_node = Node(data, self.tail, None)
        if(self.tail):
            self.tail.next = new_node
        else:
            self.head = new_node
        self.tail = new_node

    def pop_left(self):
        if not self.head:
            print("The DEQUE is empty")
            return None

        removed_node = self.head.data
        self.head = self.head.next
        if(self.head):
            self.head.prev = None
        else:
            self.tail = None
        return removed_node


    #POP methods
    def pop_right(self):
        if not self.tail:
            print("The DEQUE is empty")
            return None

        removed_node = self.tail.data
        self.tail = self.tail.prev
        if(self.tail):
            self.tail.next = None
        else:
            self.head = None
        return removed_node
    


    def print_structure(self):
        current_node = self.head

        while current_node is not None:
            print(current_node.data)
            current_node = current_node.next

