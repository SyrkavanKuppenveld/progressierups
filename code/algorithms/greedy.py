from code.classes import Wire
from code.visualization.visualize import Chip_Visualization

class Greedy():
    """ Provide Object to perform the Greedy algorithm with.
    
    Net order
    ---------
    The algorithm starts with building wires between the gate with number "1" as
    ID and its connected gates. Paths to the connected gates will also be made in 
    ascending order of the ID of the connected gate. It will continue building 
    connections according to the ID-numbers of the gates.  
    
    Path
    ----
    The algorithm will first walk along the Manhattan distance of the x-dimension and 
    subsequently along Manhattan distance of the y-dimension of the chip.
    
    w.r.t. = with respect to
    ********************************************************************************
    """
    
    def __init__(self, graph):
        """ Retrieves a graph environment for the algorithm to navigate in.

        Parameters
        ----------
        graph : Graph object of the used chip and one of its netlists
        """
        
        self.graph = graph
        self.wire = Wire()
        
        # Storage of already connected gate-net-duo's
        self.completed_connections = set()
        
        # Dictionary of wire paths (key = tuple of gate duo, value = list of coordinates)
        self.total_path = {}

    def determine_net_order(self):
        """ Returns order in which the nets will be build (list)."""
        
        gates = []
        
        # Create tuple of gateID and Gate Object to enable sorting
        for gate in self.graph.connections:
            gates.append((gate.gateID, gate))

        # Sort gates by ID
        ordered_gates = sorted(gates, key=lambda x:x[0])
        
        return ordered_gates
    
    def compute_steps(self, current_gate_coords, connected_gate_coords):
        """ Computes the lowest number of steps needed to get to the connected gate.
        
        Parameters
        ----------
        current_gate_coords : Coordinates (x, y, z) of the current gate
        connected_gate_coords : Coordinates (x, y, z) of the to be connected gate

        Return
        ------
        steps_x : The lowest number of steps needed to get to the connected gate
        w.r.t. the x-axes
        steps_y : The lowest number of steps needed to get to the connected gate
        w.r.t. the y-axes
        
        """
        
        steps_x = abs(current_gate_coords[0] - connected_gate_coords[0])
        steps_y = abs(current_gate_coords[1] - connected_gate_coords[1])
        
        return (steps_x, steps_y)

    def compute_rel_Manhattandist(self, current_gate_coords, connected_gate_coords):
        """ Computes the relative distance between the current gate and the to be 
        connected gate.
        
        Parameters
        ----------
        current_gate_coords : Coordinates (x, y, z) of the current gate
        connected_gate_coords : Coordinates (x, y, z) of the to be connected gate

        Return
        ------
        relative_dist_x : Relative number of lengt-units between the current gate 
        and the to be connected gate w.r.t. the x-axes
        relative_dist_y : Relative number of lengt-units between the current gate 
        and the to be connected gate w.r.t. the x-axes
        
        """
        
        relative_dist_x = connected_gate_coords[0] - current_gate_coords[0]
        relative_dist_y = connected_gate_coords[1] - current_gate_coords[1]

        return (relative_dist_x, relative_dist_y)
    
    def create_path(self, start_coordinates, relative_dist_x, relative_dist_y, connected_gate_coords):
        """ Builds shortest possible path according to the connected gate.
        
        Parameters
        ----------
        start_coordinates : Coordinates (x, y, z) of the start of the path (= current gate)
        relative_dist_x : Relative Manhattan distance between the gates w.r.t. the x-axis 
        reltive_dist_y : Relative Manhattan distance between the gates w.r.t. the y-axis
        connected_gate_coords : Coordinates (x, y, z) of the endpoint of the path (= connected gate)
        
        Return
        ------
        path : Coordinates of the created path (list)
        """
        
        path = []
        path.append(start_coordinates)
        
        current_coords = start_coordinates
        goal_coords = connected_gate_coords

        x_coord, y_coord, z_coord = current_coords[0], current_coords[1], current_coords[2]

        # Change x-coordinate
        if relative_dist_x != 0:
            # Walk along the x-axis until the x-coord equals the x-coord of the connected gate
            while current_coords[0] != goal_coords[0]:

                # Get coordinate-node of position A
                old_position = self.graph.nodes[(current_coords)]
                
                #  Determine direction
                if relative_dist_x > 0:
                    x_coord += 1
                else:
                    x_coord -= 1
                
                # Update path
                current_coords = (x_coord, y_coord, z_coord)
                path.append(current_coords)
                
                # Get coordinate-node of position B
                new_position = self.graph.nodes[(current_coords)]

                # Update wire
                self.wire.update_path(old_position, new_position)
                self.wire.update_coords(new_position)                

        # Change y-coordinate
        if relative_dist_y != 0:
            # Walk along the y-axis until the x-coord equals the y-coord of the connected gate
            while current_coords[1] != goal_coords[1]:

                # Get coordinate-node of position A
                old_position = self.graph.nodes[(current_coords)]
                
                #  Determine direction
                if relative_dist_y > 0:
                    y_coord += 1
                else:
                    y_coord -= 1
                
                # Update path
                current_coords = (x_coord, y_coord, z_coord)
                path.append(current_coords)
                
                # Get coordinate-node of position B
                new_position = self.graph.nodes[(current_coords)]

                # Update wire
                self.wire.update_path(old_position, new_position)
                self.wire.update_coords(new_position) 

        return path
    
    def run(self):
        """Runs the Greedy algorithm to build the wire path with.
        
        Return
        ------
        total_path = Dictionary (key = net) of paths between the gates (value: list of coordinates)
        """

        # Get a list of gates sorted by ID
        gate_order = self.determine_net_order()

        # Build wire paths
        for gate in gate_order:

            current_gateID, current_gateObject = gate
            connections = list(self.graph.connections[current_gateObject])
            
            # Build paths to each to be connected gate of the current gate
            for connection in connections:
                connected_gateObject = connection
                connected_gateID = connected_gateObject.gateID
    
                current_path = []

                # Get net (= tuple)
                net = tuple(sorted([current_gateID, connected_gateID]))

                # Do not continue if the net has already been completed
                if net not in self.completed_connections:

                    # Get coordinates (= tuple: (x, y, z))
                    current_gate_coords = (current_gateObject.xcoord, current_gateObject.ycoord, current_gateObject.zcoord)
                    connected_gate_coords = (connected_gateObject.xcoord, connected_gateObject.ycoord, connected_gateObject.zcoord)

                    # Compute relative Manhattan distances
                    relative_dist_x, relative_dist_y = self.compute_rel_Manhattandist(current_gate_coords, connected_gate_coords)
                    
                    # Create path
                    current_path_coordinates = self.create_path(current_gate_coords, relative_dist_x, relative_dist_y, connected_gate_coords)
                    current_path.extend(current_path_coordinates)

                    # Append current path to the total path
                    self.total_path[net] = current_path

                    # Update the completed connections set
                    self.completed_connections.add(net)

                    # Visulalize chip on each path of the algorithm
                    # visualisation = Chip_Visualization(self.graph.gates, self.total_path)
                    # visualisation.run()
        
        return self.total_path

                
