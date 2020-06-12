import random
from code.visualization.visualize import Chip_Visualization

class Algorithm():

    def __init__(self, graph):

        self.wire = set()        

    def get_next_gate(self, gates):
        """Gets random gate and removes it from the list."""

        return gates.pop(random.randrange(0, len(gates)))

    def get_next_connection(self, connections):

        return connections.pop(random.randrange(0, len(connections)))

    def compute_manhattan_dist(self, start, finish):
        """Returns the Manhattan Distance between start and finish."""

        x_dist = abs(start[0] - finish[0])
        y_dist = abs(start[1] - finish[1])
        z_dist = abs(start[2] - finish[2])

        return x_dist + y_dist + z_dist

    def check_collision(self, position, step):
        """Returns True if no collision, otherwise False."""
        
        step = tuple(sorted((position, step)))

        return step not in self.wire
    

    def make_connection(self, graph, gate_a, gate_b):
        """Returns wire connection between gate_a and gate_b."""
        
        connection = []

        # Get position and goal
        position = gate_a.xcoord, gate_a.ycoord, gate_a.zcoord
        goal = gate_b.xcoord, gate_b.ycoord, gate_b.zcoord

        # Add position
        connection.append(position)

        # Iterate until connection has been made
        while position != goal:

            neighbors = graph.nodes[position]
            mdist = []

            # print(f"neighbors = {neighbors}")

            for neighbor in neighbors:
                
                # Check if collision occurs 
                if self.check_collision(position, neighbor):
                    
                    dist = self.compute_manhattan_dist(neighbor, goal)
                    mdist.append((neighbor, dist))
            
            # Get location with lowest Manhattan Distance
            tmp = position
            min_dist = min(mdist, key=lambda x: x[1])

            minimum = []
            
            # Get random minimum distance if multiple
            for dist in mdist:
                if dist == min_dist:
                    minimum.append(dist[0])
            position = random.choice(minimum)

            # Add wire to paths
            wire_path = tuple(sorted((tmp, position)))
            self.wire.add(wire_path)

            # Append connection
            connection.append(position)
      
        return tuple(connection)

    def run(self, graph):

        route = {}
        gates = list(graph.gates.values())
        completed = set()

        # Iterate until all connection are made
        while gates:

            # Get random gate object and corresponding connections
            gate = self.get_next_gate(gates)
            print(f"gate = {gate}")
            connections = list(graph.connections[gate])
            
            # Iterate over the connections randomly
            while connections:

                # Get random connection
                connection = self.get_next_connection(connections)
                print(f"connection = {connection}")

                # Check if combination has already been made
                gate_a, gate_b = gate, connection
                combination = tuple(sorted((gate_a.gateID, gate_b.gateID)))
                if combination not in completed:

                    route[combination] = self.make_connection(graph, gate_a, gate_b)
                    completed.add(combination)
                    visualisation = Chip_Visualization(graph.gates, route)
                    visualisation.run()

                    # Test print
                    print("COMPLETED")
                    print(route)

        return route
                    
        




