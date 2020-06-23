#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import random
import os
import math

# Libs
import matplotlib.pyplot as plt

# Own modules
from code.classes import Graph
from code.algorithms import Random, GreedyLookAhead
from code.visualization import ChipVisualization

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'


class HillClimber(GreedyLookAhead):
    """ 
    Provide Object to perform the (stochastic) Hillclimber algorithm with.
    
    Start State
    ---------
    The algorithm starts with a Random start State. 

    Random adjustments
    ------------------
    The path that is to be rebuilt, is chosen randomly.

    New path
    --------
    The new path will be build with the use of the Greedy LookaHead algorithm.
    """

    def __init__(self, graph, frequency, start_state_flow, conversion_flow, chip, netlist):
        """ 
        Initializes the states of the algorithm.

        Parameters
        ---------
        graph: a Graph Object
                A Graph Object of the used chip and netlist.

        frequency: an int
                The number of times the HillClimber needs to run.

        start_state_flow: boolean tuple
                A boolean tuple needed for showing and saving the visualization of the start state.

        conversion_flow: boolean tuple
                A boolean tuple needed for showing and saving the visualization of the conversion plot.

        chip: an int
                The number of the used chip.

        netlist: an int
                The number of the used netlist.
        """

        # Empirically chosen number of iterations
        self.ITERATIONS = 300
        
        # Used chip and netlist
        self.chip = chip
        self.netlist = netlist

        # Answers to whether the plots should be shown/saved or not
        self.show_start_state = start_state_flow[0]
        self.save_start_state = start_state_flow[1]
        self.show_conversion_plot = conversion_flow[0]
        self.save_conversion_plot = conversion_flow[1]

        # Frequency of restarts entered by user
        self.frequency = int(frequency)

        # Visualization of the start state
        self.visualization = None

        # Keeps track state after adjustment
        self.graph = graph
        self.wire = None
        self.wire_path = None
        self.cost = None

        # Keeps track of best state encountered in run
        self.best_graph = graph
        self.best_wire = None
        self.best_wire_path = None
        self.best_cost = None

        # Keeps track of best cost and wire path built by the Hillclimbers
        self.overall_best_wire_path = None
        self.overall_best_cost = math.inf

        # Used to check on conversion
        self.improvements = [True]

        # Keep track of the HillClimbers' cost
        self.climbers_costs = []
        self.iteration = []
    
    def get_random_start_state(self, i):
        
        # Update user on which climber is running if multiple
        if i > 1:
            print(f"Hillclimber no. : {i}")
        
        print(f"Computing random start state...")
        
        # Get random Start State
        algo = Random(self.best_graph)
        self.wire_path = algo.run()
        self.best_wire_path = self.wire_path
        self.wire = algo.wire
        self.best_wire = algo.wire
        self.cost = algo.wire.compute_costs()
        self.best_cost = algo.wire.compute_costs()
        
        print("Start state found")
        print("Running algorithm...")
    
    def get_random_connection(self):
        """
        Retrieves a random connection from the netlist and returns the corresponding gateIDs
        and gate Objects.

        Returns
        -------
        connection : tuple
                A tuple of gateIDs (int).
        gates : tuple
                A tuple of Gate Objects.
        """

        # Randomly choose a net that is to be re-build
        connections_list = list(self.wire_path.keys())
        connection = random.choice(connections_list)
        
        # Get Gate Objects
        gate_a = self.graph.gates[connection[0]]
        gate_b = self.graph.gates[connection[1]]
        gates = (gate_a, gate_b)

        return connection, gates
    
    def remove_connection(self, connection, gates):
        """"
        Removes the path form the Wire object that is to be rebuilt.

        Paramters
        ---------
        connection : tuple
                A tuple of gateIDs (int).
        gates : tuple
                A tuple of Gate Objects.
        """

        connection_path = self.wire_path[connection]
       
        for coordinates in connection_path:    
            # Remove old path coordinates from the coordinate storage of the Wire Object
            # Gates can never be an intersection and thus will not be taken into account
            node = self.graph.nodes[coordinates]
            if node.isgate is False:
                # Remove node from coordinate storage
                self.wire.coords.remove(node)

                # Correct intersection-count of the Node object of the current coordinate
                node.decrement_intersection()
        
        # Remove old wire units from the path storage of the Wire Object
        for i in range(len(connection_path)):
            if i > 0:
                combination = tuple(sorted((connection_path[i - 1], connection_path[i])))
                self.wire.path.remove(combination)

    def apply_random_adjustment(self, connection, gates):
        """
        Rebuilds the path of the given connection with the use of a function from
        the Random algorithm.

        Parameters
        ----------
        connection : tuple of ints
                A tuple of gateIDs.
        gates : tuple
                A tuple of Gate Objects.
        """

        gate_a, gate_b = gates
        
        not_found = True
        new_path = None
        # Repeat until a path is correctly built
        while not_found:
                try:
                        # Construct a new path via a function inherited from the Greedy LookAhead algorithm  
                        new_path = self.make_connection(gate_a, gate_b)
                        not_found = False
                except:
                        pass
 
        # Update wire_path
        self.wire_path[connection] = new_path

    def check_improvement(self):
        """ 
        Checks if the adjusment was an improvent or not.

        Returns 
        -------
        Bool:
                True if the state improved, else false.
        """

        return self.cost < self.best_cost

    def confirm_improvement(self, improvement):
        """
        Update best found state if the adjusted state was an improvement.

        Paramters
        ---------
        improvement: bool
                A boolean representing the answer to wether or not the costs decreased.
        """
        
        # If state improved (i.e. cost decreased):
        if improvement:
            # Confirm adjustment
            self.best_cost = self.cost
            self.best_graph = self.graph
            self.best_wire = self.wire
            self.best_wire_path = self.wire_path

    def check_overall_improvement(self):
        """ 
        Checks if the current Hillclimber generated a solution with the lowest
        cost thusfar.

        Returns 
        -------
        Bool:
                True if the overall best cost improved, else false.
        """
        return self.best_cost < self.overall_best_cost
    
    def track_iterations(self):
        """
        Tracks previous iterations.
        """
        
        # Keep track of the past N iterations
        if len(self.improvements) == self.ITERATIONS:
            # Make room for next iteration
            self.improvements.pop(0)
    
    def visualize_chip(self):
        """
        Constructs a visualization of the start state of the chip.

        Returns
        -------
        fig
                A matplotlib figure of the start state of the chip.
        """
        self.visualization = ChipVisualization(self.graph.gates, self.wire_path)
        start_state_visualisation = self.visualization.run(False)
        
        return start_state_visualisation

    def show_chip(self, visualization):
        """
        Shows the visualization of the start state of the chip.

        Parameters
        ---------
        visualization: matplotlib figure
                A matplotlibfigure representing the start state of the Hillclimber.
        """
        _ = self.visualization.run(True)

    def save_plot(self, plt, filename):
        """
        Saves the start state to the results folder.

        Paramters
        --------
        plt: a matplotlib figure
                A matplotlib figure of the visualization that needs to be saved.
        filename: a string
                A string representing the name of the figure.
        """

        # Save conversion plot to results folder
        script_dir = os.path.dirname(__file__)
        results_dir = os.path.join(script_dir, f'results/chip_{self.chip}/netlist_{self.netlist}/')

        # Create results folder if the results folder does not yet exist
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        # Save figure
        plt.savefig(results_dir + filename)
    
    def visualize_conversion(self):
        """
        Visualizes the performance of the HillClimber.

        Returns
        -------
        fig
                A matplotlib figure of the Conversion plot.
        """

        # Initialize figure
        fig, ax = plt.subplots() 

        # Plot the costs as a function of the iterations
        ax.plot(self.iteration, self.climbers_costs, color='lightseagreen')
        
        # Set labels
        title_dict = {'fontsize': 12}
        ax.set_title(label='Conversion Plot', fontdict=title_dict)
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Cost')

        return fig

    def show_conversion(self, plt):
        """
        Shows conversion plot of the HillClimber

        Paramters
        ---------
        plt: a matplotlib figure
                A matplotlib figure representing the conversion plot.
        """
        plt.show()

    
    def run(self):
        """
        Runs the HillClimber algorithm a number of times, the frequency is given by user.
        """

        iteration = 0

        for i in range(self.frequency):  

            # Get random start state
            self.get_random_start_state(i)

            # Construct visualisation of the start state
            start_state_visualisation = self.visualize_chip()

            # Visualise start state
            if self.show_start_state:
                self.show_chip(start_state_visualisation)
            
            # Personalize the filenames of the start state
            filename = None
            if self.frequency == 1:
                filename = 'Start state Hillclimber.png'
            else:
                filename = f'Start state Restart Hillclimber no. {i}.png'
            
            # Save start state
            if self.save_start_state:
                self.save_plot(start_state_visualisation, filename)

            iter_count = 0

            # Repeat until conversion has occured
            while True in self.improvements:

                # Update user on progress 
                print(f"Iteration: {iter_count}")

                # Keep track of the HillClimbers' cost
                self.climbers_costs.append(self.best_cost)
                self.iteration.append(iteration)
                iteration += 1
                
                # Apply random adjustment
                # Get random net
                connection, gates = self.get_random_connection()

                # Remove old net path form wire object
                self.remove_connection(connection, gates)

                # Apply random adjustment on net
                self.apply_random_adjustment(connection, gates)

                # Compute cost of adjusted state
                self.cost = self.wire.compute_costs()

                # Check is adjustment resulted in an improved state
                improvement = self.check_improvement()

                # Confirm adjustment if state improved
                self.confirm_improvement(improvement)

                # Update improvements list
                self.improvements.append(improvement)

                # Keep track of the past N iterations of all climbs if multiple
                self.track_iterations()

                # Update iter count of current climb
                iter_count += 1

            # Check if an overall improvement has taken place
            overall_improvement = self.check_overall_improvement()

            # If an overall improvement has taken place, update overall best cost en best wire path
            if overall_improvement:
                self.overall_best_cost = self.best_cost
                self.overall_best_wire_path = self.best_wire_path
            
            # Reset conversion status
            self.improvements = [True]
        
        # Construct conversion plot
        conversion_plot_visualisation = self.visualize_conversion()

        # Notify user
        print("Algorithm converged")
        print(f"Best cost: {self.best_cost}")

        # Visualize conversion plot
        if self.show_conversion_plot:
            self.show_conversion(conversion_plot_visualisation)

        # Personalize the filenames of the conversion plot
        filename = None
        if self.frequency == 1:
                filename = 'Conversion Plot Hillclimber.png'
        else:
                filename = f'Conversion Plot Restart Hillclimber no. {i}.png'

        # Save conversion plot
        if self.save_conversion_plot:
            self.save_plot(conversion_plot_visualisation, filename)
        
        # Returns a dictionary of the connections (=key) and the constructed path (=value)
        return self.overall_best_wire_path
