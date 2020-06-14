import random
import copy
from code.classes.node import Node
from code.classes.wire_new import Wire
from code.visualization.visualize import Chip_Visualization

class Algorithm():

    def __init__(self, graph):
        
        self.graph = graph
        self.wire = Wire()   

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

    def next_position(self, position, goal):
        """Returns the next position."""

        mdist = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                dist = self.compute_manhattan_dist(neighbor, goal)
                mdist.append((neighbor, dist))
            
        # Move position to neighbor with minimal Manhattan Distance
        # Random choice if multiple minimum
        min_dist = min(mdist, key=lambda x: x[1])
        minimum = []
        for dist in mdist:
            if dist == min_dist:
                minimum.append(dist[0])
        
        # Assign new position
        position = random.choice(minimum)

        return position

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
            
            # Store current position in temporary value
            tmp = position

            # Get next posotion
            position = self.next_position(position, goal)

            # Update wire path and coordinates
            self.wire.update_path(tmp, position)
            self.wire.update_coords(position)

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

                # Check if combination is already completed
                if combination not in completed:
                 
                    route[combination] = self.make_connection(gate_a, gate_b)
                    completed.add(combination)

        return route           
   