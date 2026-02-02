
class Node():

    data: str

    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

class Binary_Tree():
    root: Node

    def __init__(self):
        self.root = None

    def print_structure_inOrder(self, node): #Left-Root-Right
        if (node is None):
            return
        
        self.print_structure_inOrder(node.left)
        print(node.data)
        self.print_structure_inOrder(node.right)

    def print_structure_preOrder(self, node): #Root-Left-Right
        if (node is None):
            return

        print(node.data)
        self.print_structure_preOrder(node.left)
        self.print_structure_preOrder(node.right)

    def print_structure_postOrder(self, node): #Left-Right-Root
        if (node is None):
            return
        
        self.print_structure_postOrder(node.left)
        self.print_structure_postOrder(node.right)
        print(node.data)
