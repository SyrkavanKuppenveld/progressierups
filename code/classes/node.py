

class Node():

    def __init__(self, coords):
        self.xcoord = coords[0]
        self.ycoord = coords[1]
        self.zcoord = coords[2]
        self.neighbors = set()
        self.isgate = False

    def __hash__(self):
        return hash((self.xcoord, self.ycoord, self.zcoord))
    
    def set_isgate(self):
        self.isgate = True

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)



    
