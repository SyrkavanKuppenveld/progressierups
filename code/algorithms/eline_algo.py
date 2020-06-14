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
                  
        # Assign new position
        position = self.get_random_min(mdist)

        return position

    def get_random_min(self, lst):
        """Returns random minimum."""
        
        min_value = min(lst, key=lambda x: x[1])
        minimum = []
        for dist in lst:
            if dist == min_value:
                minimum.append(dist[0])

        return random.choice(minimum)

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

    # def run(self):

    #     route = {}
    #     gates = list(self.graph.gates.values())
    #     completed = set()

    #     # Iterate until all connection are made
    #     while gates:

    #         # Get random gate object and corresponding connections
    #         gate = self.get_next_gate(gates)
    #         connections = list(self.graph.connections[gate])
            
    #         # Iterate over the connections randomly
    #         while connections:

    #             # Get random connection
    #             connection = self.get_next_connection(connections)

    #             # Check if combination has already been made
    #             gate_a, gate_b = gate, connection
    #             combination = tuple(sorted((gate_a.gateID, gate_b.gateID)))

    #             # Check if combination is already completed
    #             if combination not in completed:
                 
    #                 route[combination] = self.make_connection(gate_a, gate_b)
    #                 completed.add(combination)

    #     return route           
   
    def run(self):

        route = {}
        netlist = list(self.graph.netlist)

        while netlist:

            # Get random connection 
            connection = netlist.pop(random.randrange(0, len(netlist)))

            # Get corresponding Gate objects
            a, b = connection[0], connection[1]
            gate_a, gate_b = self.graph.gates[a], self.graph.gates[b]

            # Generate the connection between gate a and b
            route[(a, b)] = self.make_connection(gate_a, gate_b)

        return route


class LookAHead(Algorithm):

    def next_position(self, position, goal):
        """Returns the next position."""

        mdist = []

        # Iterate over neighbors current position
        for neighbor in position.neighbors:
            dist = 0

            # If move is allowed compute and append Manhattan Distance
            if self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                original = neighbor
                dist += self.compute_manhattan_dist(neighbor, goal)
                next_position = neighbor

                # Look a head 1
                for neighbor in next_position.neighbors:
                    if neighbor == goal:
                        mdist.append((original, dist))
                    elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                        dist += self.compute_manhattan_dist(neighbor, goal)
                        next_position = neighbor

                        # Look a head 2
                        for neighbor in next_position.neighbors:
                            if neighbor == goal:
                                mdist.append((original, dist))
                            elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                dist += self.compute_manhattan_dist(neighbor, goal)
                                next_position = neighbor

                                # Look a head 3
                                for neighbor in next_position.neighbors:
                                    if neighbor == goal:
                                        mdist.append((original, dist))
                                    elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                        dist += self.compute_manhattan_dist(neighbor, goal)  
                                        next_position = neighbor

                                        # Look a head 4
                                        for neighbor in next_position.neighbors:
                                            if neighbor == goal:
                                                mdist.append((original, dist))
                                            elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                                dist += self.compute_manhattan_dist(neighbor, goal) 
                                                next_position = neighbor
                                                if dist > 0:
                                                    mdist.append((original, dist)) 
                                                

                                                # Look a head 5
                                                for neighbor in next_position.neighbors:
                                                    if neighbor == goal:
                                                        mdist.append((original, dist))
                                                    elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                                        dist += self.compute_manhattan_dist(neighbor, goal)  
                                                        next_position = neighbor
                # if dist > 0:
                #     mdist.append((original, dist)) 

                                                        # # Look a head 6
                                                        # for neighbor in next_position.neighbors:
                                                        #     if neighbor == goal:
                                                        #         mdist.append((original, dist))
                                                        #     elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                                        #         dist += self.compute_manhattan_dist(neighbor, goal)  
                                                        #         next_position = neighbor

                                                                # # Look a head 7
                                                                # for neighbor in next_position.neighbors:
                                                                #     if neighbor == goal:
                                                                #         mdist.append((original, dist))
                                                                #     elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                                                #         dist += self.compute_manhattan_dist(neighbor, goal)  
                                                                #         next_position = neighbor

                                                                #         # Look a head 8
                                                                #         for neighbor in next_position.neighbors:
                                                                #             if neighbor == goal:
                                                                #                 mdist.append((original, dist))
                                                                #             elif self.wire.check_collision(position, neighbor) and (neighbor.isgate is False or neighbor == goal):
                                                                #                 dist += self.compute_manhattan_dist(neighbor, goal)  
                                                                #                 next_position = neighbor
                # if dist > 0:
                #     mdist.append((original, dist))

        # Assign new position
        position = self.get_random_min(mdist)

        return position

