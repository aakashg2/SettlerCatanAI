from .Node import Node

class Tile:
    resource = None
    number = -1
    nodes = None
    def __init__(self, resource, number, G):
        self.resource = resource
        self.number = number
        self.nodes = [Node(resource, number) for i in range(6)]
        for i in range(len(self.nodes)-1):
            G.add_edge(self.nodes[i], self.nodes[i+1])
        G.add_edge(self.nodes[5], self.nodes[0])
    def show(self):
        output = ""
        for i, node in enumerate(self.nodes):
            output+= f"Node {str(i)} : {node.show()}\n\n"
        return output
