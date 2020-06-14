import random
import copy
from code.classes.node import Node
from code.visualization.visualize import Chip_Visualization
# from class_eline import Chip_Visualization

class Random():

    def __init__(self, graph):
        
        self.graph = graph
        self.wire = set()        

    def check_collision(self, position, step):
        """Returns True if no collision, otherwise False."""

        position_coords = position.xcoord, position.ycoord, position.zcoord
        step_coords =  step.xcoord, step.ycoord, step.zcoord
        
        step = tuple(sorted((position_coords, step_coords)))

        return step not in self.wire
    
    def make_connection(self, gate_a, gate_b):
        """Returns wire connection between gate_a and gate_b."""
        
        connection = []

        # Get position and goal nodes
        position = self.graph.nodes[(gate_a.xcoord, gate_a.ycoord, gate_a.zcoord)]
        goal = self.graph.nodes[(gate_b.xcoord, gate_b.ycoord, gate_b.zcoord)]

        # Add position
        connection.append((position.xcoord, position.ycoord, position.zcoord))

        # Iterate until connection has been made
        while position != goal:
            allowed_neighbors = []

            # Iterate over neighbors current position
            for neighbor in position.neighbors:

                # If move is allowed compute and append Manhattan Distance
                if self.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                    allowed_neighbors.append(neighbor)
            
            # Assign new position
            tmp = position
            position = random.choice(allowed_neighbors)

            # Add wire to path
            tmp_coords = tmp.xcoord, tmp.ycoord, tmp.zcoord
            position_coords = position.xcoord, position.ycoord, position.zcoord
            wire_path = tuple(sorted((tmp_coords, position_coords)))
            self.wire.add(wire_path)

            # Append connection
            connection.append((position.xcoord, position.ycoord, position.zcoord))

        return tuple(connection)

    def run(self):

        route = {}
        completed = set()
        netlist = list(self.graph.netlist)

        while netlist:
            connection = netlist.pop(random.randrange(0, len(netlist)))
            a, b = connection[0], connection[1]
            gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]
            route[(a, b)] = self.make_connection(gate_a, gate_b)
            completed.add((a, b))
            visualisation = Chip_Visualization(self.graph.gates, route)
            visualisation.run()
    
        return route
      

        