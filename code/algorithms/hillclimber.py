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

"""
Code for Hillclimber algorithm.


This module contains the code for the hillclimber algorithm. 
"""

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
        self.restart_climbers_costs = []
        self.iteration = []
    
    def get_random_start_state(self, i):
        
        # Update user on which climber is running if multiple
        if self.frequency > 1:
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
        
        print("Random start state found")
        print("Running Hillclimber algorithm...")
    
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
    
    def handle_start_state_visualization(self, i):
        """
        Handles the showing and saving of the start state visualization.
        """
        # Construct visualisation of the start state
        start_state_visualisation = self.visualize_chip()

        # Visualise start state
        if self.show_start_state:
            self.show_chip(start_state_visualisation)
        
        # Save start state
        if self.save_start_state:
            filename = self.get_filename_startstate(i)
            self.save_plot(start_state_visualisation, filename)
    
    
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

    def get_filename_startstate(self, i):
        """ 
        Personalizes and returns filename of the start state according to 
        the type of Hillclimber used.

        Returns
        -------
        string
                A string representing the name of the file
        """
        
        filename = None
        if self.frequency == 1:
            filename = 'start_state_hillclimber.png'
        else:
            filename = f'start_state_restart_hillclimber_{i}.png'
        
        return filename

    def get_filename_conversion(self):
        """ 
        Personalizes and returns filename of the conversion plot according to 
        the type of Hillclimber used.

        Returns
        -------
        string
                A string representing the name of the file
        """
        
        filename = None
        if self.frequency == 1:
                filename = 'conversion_plot_hillclimber.png'
        else:
                filename = f'conversion_plot_restart_hillclimber.png'

        return filename

    def save_plot(self, plot, filename):
        """
        Saves the start state to the results folder.

        Paramters
        --------
        plot: a matplotlib figure
                A matplotlib figure of the visualization that needs to be saved.

        filename: a string
                A string representing the name of the figure.
        """

        # Save plot in results folder
        plot.savefig(f"results/{filename}")

    def handle_conversion_plot_visualization(self):
        """
        Handles the showing and saving of the conversion plot of the hillclimber(s).
        """

        # Construct conversion plot
        conversion_plot_visualisation = self.visualize_conversion()

        # Visualize conversion plot
        if self.show_conversion_plot:
            self.show_conversion(conversion_plot_visualisation)

        # Save conversion plot
        if self.save_conversion_plot:
            filename = self.get_filename_conversion()
            self.save_plot(conversion_plot_visualisation, filename)
    
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

    def show_conversion(self, plot):
        """
        Shows conversion plot of the HillClimber

        Paramters
        ---------
        plot: a matplotlib figure
                A matplotlib figure representing the conversion plot.
        """
        
        plot.show()

    def track_restart(self):
        """
        Keep track of the best path and costs generated by the restart Hillclimber and 
        update them if necessary.
        """
        
        # Keep track of best costs found per restart
        self.restart_climbers_costs.append(self.best_cost)

        # Check if an overall improvement has taken place
        overall_improvement = self.check_overall_improvement()

        # If an overall improvement has taken place, update overall best cost en best wire path
        if overall_improvement:
            self.overall_best_cost = self.best_cost
            self.overall_best_wire_path = self.best_wire_path
    
    def notify_user(self):
        """
        Notify user on the found costs.
        """

        # If a normal hillclimber was run, print best found cost
        if self.frequency == 1:
            print("\033[33m"f"Wire costs = {self.best_cost}\n""\033[0m")
        
        # If a restart hillclimber was run print best found costs of all hillclimbers
        # and the overall best found cost
        else:
            for i, cost in enumerate(self.restart_climbers_costs):
                print(f"Best wire cost Hillclimber no. {i} = {cost}")
            print("\033[33m"f"Overall best wire costs = {self.overall_best_cost}\n""\033[0m")

    def get_return_path(self):
        """
        Returns the best path acquired by the hillclimber.

        Returns
        -------
        dict
                A dict with connections as key and the wire path as value.
        """

        return_path = None

        # Returns a dictionary the best found path of the single Hillclimber
        if self.frequency == 1:
            return_path = self.best_wire_path

        # Returns a dictionary the overall best found path by the Restart hillclimber
        else:
            return_path = self.overall_best_wire_path

        return return_path

    def run(self):
        """
        Runs the HillClimber algorithm a number of times, the frequency is given by user.

        Returns
        -------

        dict
                A dict with connections as key and the wire path as value.
        """

        hillclimber_count = 0
        iteration = 0

        for i in range(self.frequency):  

            # Get random start state
            self.get_random_start_state(i)

            # Handle the visualization of the start state
            self.handle_start_state_visualization(i)

            reset_iter = 0

            # Repeat until conversion has occured
            while True in self.improvements:

                # Update user on progress 
                print(f"Iteration: {reset_iter}")
                reset_iter += 1

                # Keep track of the HillClimbers' costs
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

                # Update count of current hillclibmer
                hillclimber_count += 1
            
            # Notify user on conversion of algorithm
            print("Algorithm converged\n")

            # If a restart hillclimber is run:
            if self.frequency != 1:
                # Handle the tracking of the best costs and wire path of the Restart Hillclimber
                self.track_restart()
            
            # Reset conversion status
            self.improvements = [True]

        # Notify user on conversion and costs
        self.notify_user()

        # Handle the showing and saving of the conversion plot
        self.handle_conversion_plot_visualization()
        
        # Determine path to return
        return_path = self.get_return_path()

        return return_path