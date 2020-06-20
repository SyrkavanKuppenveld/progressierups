from code.classes import Graph
from code.algorithms import Greedy_RandomNet_LookAhead, Greedy_RandomNet_LookAhead_Costs, Greedy_RandomNet, Random
from code.visualization import Chip_Visualization
import random
import matplotlib.pyplot as plt

class HillClimber(Random):
    """ 
    Provide Object to perform the (stochastic) Hillclimber algorithm with.
    
    Start State
    ---------
    The algorithm starts with a Random start State 

    Random elements
    ---------------
    The path that is to be rebuild, is randomly chosen.
    The new path will be built with the use of the Random algorithm.

    """

    def __init__(self, graph, random_startWireObject, start_wire_path_dict, start_cost):
        """ 
        Initializes the start state of the algorithm.

        [Dit nog aan passen aan opgeschoonde algoritmes!!]

        """

        # 1. Initialize a random start state
        # Keeps track of current state
        self.graph = graph
        self.wire = random_startWireObject
        self.wire_path_dict = start_wire_path_dict
        self.cost = start_cost

        # Keeps track of best state
        self.best_graph = graph
        self.best_wire = random_startWireObject
        self.best_wire_path_dict = start_wire_path_dict
        self.best_cost = start_cost

        # Used to check on conversion
        self.improvements = []
        self.conversion = False

        # Keep track of the HillClimbers' cost
        self.climbers_costs = []
        self.iteration = []

    def get_random_net(self):
        """
        Retrieves a random net from the netlist and returns the corresponding gateIDs
        and gate Objects.

        Returns
        -------
        net : tuple
                A tuple of gateIDs (int)
        gates : tuple
                A tuple of Gate Objects
        """

        # Randomly choose a net that is to be re-build
        nets = list(self.wire_path_dict.keys())
        net = random.choice(nets)
        
        gate_a = self.graph.gates[net[0]]
        gate_b = self.graph.gates[net[1]]
        gates = (gate_a, gate_b)

        return net, gates
    
    def remove_net(self, net, gates):
        """"
        Removes the path form the Wire object that is to be rebuild.

        Paramters
        ---------
        net : tuple
                A tuple of gateIDs (int)
        gates : tuple
                A tuple of Gate Objects
        """

        net_path = self.wire_path_dict[net]
        
        # coord_storage = []
        for coordinates in net_path:    
            # Remove old path coordinates from the coordinate storage of the Wire Object
            # Gates can never be an intersection and thus will not be taken into account
            node = self.graph.nodes[coordinates]
            if not node.isgate:
                # Remove node form coordinate storage
                self.wire.coords.remove(node)

                # Correct intersection-count of the Node object of the current coordinate
                node.decrement_intersection()
        
        # Remove old wire units from the path storage of the Wire Object
        for i, coordinate in enumerate(net_path):
            if i > 0:
                combination = tuple(sorted((net_path[i - 1], net_path[i])))
                self.wire.path.remove(combination)

    def apply_random_adjustment(self, net, gates):
        """
        Rebuilds the path of the given net with the use of a function from
        the Random algorithm.

        Parameters
        ----------
        net : tuple
                A tuple of gateIDs (int)
        gates : tuple
                A tuple of Gate Objects
        """

        gate_a, gate_b = gates
        # new_path = self.make_connection(gate_a, gate_b)
        not_found = True
        while not_found:
            while True:

                # Restart algorithm if error occurs
                try:
                    new_path = self.make_connection(gate_a, gate_b)
                    not_found = False
                    break
                except ValueError:
                    break

        # Update wire_path
        self.wire_path_dict[net] = new_path

    def visualizeChip(self):
        """
        Visualizes the chip in the current state.
        """

        visualisation = Chip_Visualization(self.graph.gates, self.wire_path_dict)
        visualisation.run()

    def visualizeConversion(self):
        """
        Visualizes the performance of the HillClimber
        """

        # Initialize figure
        fig, ax = plt.subplots() 

        # Plot the costs as a function of the iterations
        ax.plot(self.iteration, self.climbers_costs, color='lightseagreen')
        
        # Set labels
        titleDict = {'fontsize': 12}
        ax.set_title(label='Conversion Plot', fontdict=titleDict)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Cost')
        
        # Show conversion plot
        plt.show()

    def run(self):
        """
        Runs the HillClimber algorithm
        """

        ITERATIONS = 100
        iteration = 0

        # Visualise starting State
        self.visualizeChip()
        
        # 2. Repeat until cost does not improve after N iterations:
        while not self.conversion:

            # # Keep track of the HillClimbers' cost
            self.climbers_costs.append(self.best_cost)
            self.iteration.append(iteration)
            print(f"Iteration: {iteration}")
            iteration += 1
            print(f"Best cost: {self.best_cost}")
            
            # 3. Apply random adjustment
            # Get random net
            net, gates = self.get_random_net()

            # Remove old net path form wire object
            self.remove_net(net, gates)

            # Apply random adjustment on net
            self.apply_random_adjustment(net, gates)

            # Compute cost of adjusted state
            cost = self.wire.compute_costs()

            # 4. If state improved (cost decreased):
            if cost < self.best_cost:
                # 5. Confirm adjustment
                self.best_cost = cost
                self.best_graph = self.graph
                self.best_wire = self.wire
                self.best_wire_path_dict = self.wire_path_dict
                self.improvements.append(True)
            else:
                self.improvements.append(False)

            # Check if conversion has occured over the past 20 iterations
            if len(self.improvements) == ITERATIONS:
                # If no improvement occured, quit the HillClimber algorithm
                if True not in self.improvements:
                    self.conversion = True

                # Make room for next iteration
                self.improvements.pop(0)
        
        # Visualize end result
        self.visualizeChip()

        # Visualize Conversion
        self.visualizeConversion()






            


        