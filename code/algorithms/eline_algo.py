import random
import copy
from code.classes.node import Node
from code.visualization.visualize import Chip_Visualization
# from class_eline import Chip_Visualization

class Algorithm():

    def __init__(self, graph):
        
        self.graph = graph
        self.wire = set()        

    def get_next_gate(self, gates):
        """Gets random gate and removes it from the list."""

        next_gate = gates.pop(random.randrange(0, len(gates)))

        # Ensure that next_gate has connections
        while next_gate not in self.graph.connections:
            next_gate = gates.pop(random.randrange(0, len(gates)))

        return next_gate

    def get_next_connection(self, connections):

        return connections.pop(random.randrange(0, len(connections)))

    def compute_manhattan_dist(self, start, finish):
        """Returns the Manhattan Distance between start and finish."""

        x_dist = abs(start.xcoord - finish.xcoord)
        y_dist = abs(start.ycoord - finish.ycoord)
        z_dist = abs(start.zcoord - finish.zcoord)

        return x_dist + y_dist + z_dist

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
            mdist = []

            # Iterate over neighbors current position
            for neighbor in position.neighbors:

                # If move is allowed compute and append Manhattan Distance
                if self.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                    dist = self.compute_manhattan_dist(neighbor, goal)
                    mdist.append((neighbor, dist))
            
            # Get get node with minimal Manhattan Distance
            min_dist = min(mdist, key=lambda x: x[1])
            minimum = []
            
            # Get random minimum distance if multiple
            for dist in mdist:
                if dist == min_dist:
                    minimum.append(dist[0])
            
            # Assign new position
            tmp = position
            position = random.choice(minimum)

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
        gates = list(self.graph.gates.values())
        completed = set()

        # Iterate until all connection are made
        while gates:

            # Get random gate object and corresponding connections
            gate = self.get_next_gate(gates)
            connections = list(self.graph.connections[gate])
            
            # Iterate over the connections randomly
            while connections:

                # Get random connection
                connection = self.get_next_connection(connections)

                # Check if combination has already been made
                gate_a, gate_b = gate, connection
                combination = tuple(sorted((gate_a.gateID, gate_b.gateID)))
                # print(combination)
                if combination not in completed:
                 
                    route[combination] = self.make_connection(gate_a, gate_b)
                    completed.add(combination)
                    print(f'Combos completed = {len(completed)}')
                    visualisation = Chip_Visualization(self.graph.gates, route)
                    visualisation.run()

        return route
                    
        




