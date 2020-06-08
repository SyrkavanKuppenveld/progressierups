
class Graph():
    """Graph datastructure"""

    def __init__(self, connections):
        """Initialize Graph object."""

        self.graph = self.createGraph(connections)
        self.vertices = self.getVertices()
        
    def createGraph(self, connections):
        """Returns filled gdict."""

        gdict = {}

        # Append the edges to the corresponding vertices
        for element in connections:
            if element[0] in gdict:
                gdict[element[0]].append(element[1])
            else:
                gdict[element[0]] = [element[1]]
            if element[1] in gdict:
                gdict[element[1]].append(element[0])
            else:
                gdict[element[1]] = [element[0]]    

        
        return gdict

    def getVertices(self):
        """Returns the keys of the graph dictionary."""

        return list(self.graph.keys())


        

