#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import random
import os

# Libs
import matplotlib.pyplot as plt

# Own modules
from code.classes import Graph
from code.algorithms_revised import Random, GreedyLookAhead
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
    INFORMATIE
    """

    def __init__(self, graph, frequency):
        """ 
        Initializes the states of the algorithm.
        """
        
        # Empirically chosen number of iterations
        self.iterations = 200

        # Frequency of restarts entered by user
        self.frequency = frequency

        # Keeps track state after adjustment
        self.graph = graph
        self.wire = None
        self.wirePathDict = None
        self.cost = None

        # Keeps track of best state encountered
        self.bestGraph = graph
        self.bestWire = None
        self.bestWirePathDict = None
        self.bestCost = None

        # Used to check on conversion
        self.improvements = [True]

        # Keep track of the HillClimbers' cost
        self.climbers_costs = []
        self.iteration = []

    
    def get_random_start_state(self):
        
        print("Computing random start state...")
        
        # Get random Start State
        algo = Random(self.bestGraph)
        self.wirePathDict = algo.run()
        self.bestWirePathDict = self.wirePathDict
        self.wire = algo.wire
        self.bestWire = algo.wire
        self.cost = algo.wire.compute_costs()
        self.bestCost = algo.wire.compute_costs()
        
        print("Start State found")
    
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
        nets = list(self.wirePathDict.keys())
        net = random.choice(nets)
        
        # Get Gate Objects
        gate_a = self.graph.gates[net[0]]
        gate_b = self.graph.gates[net[1]]
        gates = (gate_a, gate_b)

        return net, gates
    
    def remove_net(self, net, gates):
        """"
        Removes the path form the Wire object that is to be rebuilt.

        Paramteres
        ---------
        net : tuple
                A tuple of gateIDs (int)
        gates : tuple
                A tuple of Gate Objects
        """

        net_path = self.wirePathDict[net]
       
        for coordinates in net_path:    
            # Remove old path coordinates from the coordinate storage of the Wire Object
            # Gates can never be an intersection and thus will not be taken into account
            node = self.graph.nodes[coordinates]
            if node.isgate is False:
                # Remove node from coordinate storage
                self.wire.coords.remove(node)

                # Correct intersection-count of the Node object of the current coordinate
                node.decrement_intersection()
        
        # Remove old wire units from the path storage of the Wire Object
        for i in range(len(net_path)):
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
        new_path = self.make_connection(gate_a, gate_b)
 
        # Update wire_path
        self.wirePathDict[net] = new_path

    def check_improvement(self, cost):
        """ Returns True if the state improved, else false."""
        return cost < self.bestCost

    def confirm_improvement(self, improvement, cost):
        """
        Update improvement
        """
        
        # If state improved (cost decreased):
        if improvement:
            # Confirm adjustment
            self.bestCost = cost
            self.bestGraph = self.graph
            self.bestWire = self.wire
            self.bestWirePathDict = self.wirePathDict
    
    def track_iterations(self):
        """
        INFORMATIE
        """
        
        # Keep track of the past N iterations
        if len(self.improvements) == self.iterations:
            # Make room for next iteration
            self.improvements.pop(0)
    
    def visualize_chip(self):
        """
        Visualizes the chip in the current state.
        """

        visualisation = ChipVisualization(self.graph.gates, self.wirePathDict)
        visualisation.run(True)
    
    def visualize_conversion(self):
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
        Runs the HillClimber algorithm a number of times, frequency is given by user.
        """

        iteration = 0

        for i in range(self.frequency):

            # Get random Start State
            self.get_random_start_state()

            # Visualise starting State
            self.visualize_chip()

            # Repeat until conversion has occured
            while True in self.improvements:

                # # Keep track of the HillClimbers' cost
                self.climbers_costs.append(self.bestCost)
                self.iteration.append(iteration)
                print(f"Iteration: {iteration}")
                iteration += 1
                print(f"Best cost: {self.bestCost}")
                
                # Apply random adjustment
                # Get random net
                net, gates = self.get_random_net()

                # Remove old net path form wire object
                self.remove_net(net, gates)

                # Apply random adjustment on net
                self.apply_random_adjustment(net, gates)

                # Compute cost of adjusted state
                cost = self.wire.compute_costs()

                # Check is adjusment resulted in an improved state
                improvement = self.check_improvement(cost)

                # Confirm adjustment if state improved
                self.confirm_improvement(improvement, cost)

                # Update improvements list
                self.improvements.append(improvement)

                # Keep track of the pas N iterations
                self.track_iterations()
            
            # Reset conversion status
            self.improvements = [True]

        # Visualize end result
        self.visualize_chip()

        # Visualize Conversion
        self.visualize_conversion()

