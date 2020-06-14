

class Node():

    def __init__(self, coords):
        self.xcoord = coords[0]
        self.ycoord = coords[1]
        self.zcoord = coords[2]
        self.neighbors = set()
        self.isgate = False
        self.wired_neighbors = 0

    def __hash__(self):
        return hash((self.xcoord, self.ycoord, self.zcoord))

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)

    def set_isgate(self):
        self.isgate = True

    def update_neighbors(self):
        self.wired_neighbors += 1

    def __repr__(self):
        """Ensure that the object is printed properly if it is in a list/dict."""

        return str((self.xcoord, self.ycoord, self.zcoord))

    



    
