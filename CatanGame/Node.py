# class Node:
#     occupied = None
#     # Whether or not this spot has a settlement or city on it.   
#     def __init__(self, resource, number):
#         self.resources = [resource]
#         self.numbers = [number]
#         self.owner = None

#     def show(self):
#         display = f"The resources are: {self.resources} and the numbers are: {self.numbers} /n It is currently owned by {self.owner}"
#         return display
class Node:
    # Whether or not this spot has a settlement or city on it.   
    def __init__(self, resource, number):
        self.occupied = None
        self.resources_idx = [None, None, None]
        self.resources = [None, None, None]
        self.numbers = [None, None, None]
        self.owner = None
        return
    def show(self):
        display = f"The resources are: {self.resources} and the numbers are: {self.numbers} /n It is currently owned by {self.owner}"
        return display
