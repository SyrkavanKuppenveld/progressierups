#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import sys
import time

# Own modules
from main import main
import code.visualization as vs

__author__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__copyright__ = 'Copyright 2020, Chips & Circuits'
__credits__ = ['Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld']
__license__ = 'GNU GPL 3.0'
__version__ = '0.1.0'
__maintainer__ = 'Eline van Groningen, Mimoun Boulfich, Syrka van Kuppenveld'
__email__ = 'elinevangroningen@gmail.com, mimounboulfich@live.nl, syrkavankuppenveld@gmail.com'
__status__ = 'Dev'


"""
User interface.


This module contains the code for the implementation of the user interface of the program. 
"""


def chip_input():
    """
    Returns the chip number choosen by the user.

    Returns
    -------
    int 
            A integer representing the chip number choosen by the user.
    """

    options = {'0', '1', '2'}
    correct = False

    while not correct:

        # Prompt user for chip
        chip = input("\033[1m"'Choose a chip: 0, 1 or 2?\n')

        # Quit if user input is correct
        if chip in options:
            correct = True
        
    return int(chip)


def netlist_input(chip):
    """
    Returns netlist number choosen by the user.

    Parameters
    ----------
    chip: a int
            The chip number.
    
    Returns
    -------
    int
            A integer representing the netlist number choosen bij the user.
    """
    
    # Ensure correct usage
    correct = False
    while not correct:

        # Prompt user for netlist and ensure correct usage based on previous chip choice
        if chip == 0:
            print("\033[1m""Choose a netlist: 1, 2 or 3?""\033[0m")
            netlist = input()
            options = {'1', '2', '3'}
            if netlist in options:
                correct = True
        elif chip == 1:
            print("\033[1m""Choose a netlist: 4, 5 or 6?""\033[0m")
            netlist = input()
            options = {'4', '5', '6'}
            if netlist in options:
                correct = True
        else:
            print("\033[1m""Choose a netlist: 7, 8 or 9?\n""\033[0m")
            netlist = input()
            options = {'7', '8', '9'}
            if netlist in options:
                correct = True

    return int(netlist)    


def algorithm_input(netlist):
    """
    Returns a integer representring the algorithm choosen by the user.
    Option to print more information on the algorithms. 

    Parameters
    ----------
    netlist: a int
            Het netlist number.

    Returns
    -------
    int
            A integer representing the algorithm choice
    """

    options = {'0', '1', '2', '3'}
    
    correct = False
    while not correct:

        # Prompt user for algorithm
        print("\033[1m""Which algorithm would you like to run?""\033[0m")
        print("For more information on the algorithms press 9 directly followed by the algorithm number.")
        print("> 0 = Random\n> 1 = Greedy\n> 2 = Greedy Look Ahead\n> 3 = Hillclimber")
        algorithm = input()
        print()

        # Information on random algorithm
        if algorithm == '90':
            print("\033[1m""INFORMATION RANDOM ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist.")
            print()
            print("Random elements:\n* The order of the connections are generated randomly.\n* The next position is generated randomly.")

            # Print warning message and prompt user for next approach
            if netlist > 2:
                print()
                print("WARNING! The random algorithm only works for netlist 1 and 2 within a reasonable amount of time.")
                print()
                restart_program()

        # Information on the greedy algorithm
        elif algorithm == '91':
            print("\033[1m""INFORMATION GREEDY ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist and according to the lowest Manhattan Distance.")
            print()
            print("Greedy elements:\n* The next position will be the neighbor with the lowest Manhattan distance.")
            print()
            print("Random element:\n* If multiple neighbors have the same distance, the next position is generated randomly.")
            print()
            print("The greedy algorithm works with the following heuristics:")
            print("* 'Social map'\n* 'Better a neighbor who is near than an brother far away?")
            print("Option for more information on the heuristics will be given later.")
            time.sleep(5)
            print()

        # Information on the greedy look ahead algorithm
        elif algorithm == '92':
            print("\033[1m""INFORMATION GREEDY LOOK AHEAD ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist and according to the lowest Manhattan Distance with a 4 step look ahead.")
            print()
            print("Greedy elements:\n* The next position will be the neighbor with the lowest Manhattan distance.")
            print()
            print("Random element:\n* If multiple neighbors have the same distance, the next position is generated randomly.")
            print()
            print("The greedy look ahead algorithm works with the following heuristics:")
            print("\n* 'Social map'\n* 'Better a neighbor who is near than an brother far away?\n* 'Sky is the Limit'")
            time.sleep(5)
            print()

        # Information on the hillclimber algorithm
        elif algorithm == '93':
            print("\033[1m""INFORMATION HILLCLIMBER ALGORITHM""\033[0m")
            # MEER INFORMATIE NOG TOEVOEGEN
            time.sleep(5)
            print()

        # Continue if algorithm choice is valid
        elif algorithm in options:
            correct = True

            # Print warning and prompt user for next approach
            if algorithm == '0' and netlist > 2:
                print("\033[1m""WARNING! The random algorithm only works for netlist 1 and 2 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()
            
    return int(algorithm)


def heuristic_input(netlist, algorithm):
    """
    Returns the integer representing the heuristic choosen by the user.
    Option to print extra information these heuristics. 

    Parameters
    ----------
    netlist: a int
            The netlist choosen by the user.
    
    algorith: a int
            The algorithm choosen by the user.

    Returns
    -------
    int
            A integer representing the choosen heuristic. 
    """

    options = {'0', '1', '2', '3'}

    correct = False
    while not correct:

        # Prompt user for heuristic 
        print("\033[1m""Which heuristic would you like to implement?""\033[0m")
        print("For more information on the algorithms press 9 directly followed by the heuristic number.")
        print("> 0 = none\n> 1 = 'Social Map'\n> 2 = 'Better a neighbor who is near than an brother far away?\n> 3 = 'Sky is the Limit'")
        heuristic = input()
        
        if heuristic == '91':
            print("\033[1m""INFORMATION SOCIAL MAP""\033[0m")
            print("The 'Social Map' heuristic orders the gates based on the number of gates within a pre-specified radius.")
            print()
            print("You have the option to order the gates:\n* From min to max density\n* From max to min density")
            time.sleep(3)
            print()

        elif heuristic == '92':
            print("\033[1m""INFORMATION BETTER A NEIGHBOR WHO IS NEAR THAN A BROTHER FAR AWAY?""\033[0m")
            print("The 'Better A Neighbor Who Is Near Than A Brother Far Away' heuristic orders the connections based on distance between the gates.")
            print()
            print("You have the option to order the connections:\n* From min to max distance\n* From max to min distance")
            time.sleep(3)
            print()

        elif heuristic == '93':
            print("\033[1m""INFORMATION SKY IS THE LIMIT""\033[0m")
            print("The 'Sky Is The Limit' heuristic increases the costs for not moving up in the grid if the Manhattan Distance between gates is higher than 4.")
            print()
            time.sleep(3)
            print()

        elif heuristic in options:

            # Set correct to true
            correct = True

            if netlist > 4 and algorithm == 1:
                print("\033[1m""WARNING: the combination of the algorithm (and heuristic) only works for netlist 1-4 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()
            elif netlist > 7 and algorithm == 2 and heuristic == '3':
                print("\033[1m""WARNING: the combination of the algorithm (and heuristic) only works for netlist 1-7 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()
           
    return int(heuristic)


def heuristic_order_input(chip, heuristic, graph):
    """
    chip: a int
            The chip number choosen by the user.

    heuristic: a int
            The heuristic choosen by the user.

    graph: a Graph object
            A graph object representing the chip grid.
    
    Returns
    -------
    list 
            A list containining containing gateIDs or connections.

    bool
            True if list contains connections, false if list contains gates.
    """

    options = {'0', '1'}
    
    # Only prompt for order for heuristic 1 or 2
    if heuristic == 1 or heuristic == 2:

        # Ensure correct usage
        correct = False
        while not correct:
            
            # Prompt user for order heuristic list
            order = input("\033[1m""How would you like to implement the heuristic?\n> 0 = min-max\n> 1 = max-min\n""\033[1m")

            # If usage is correct set correct to true and convert order to bool
            if order in options:
                correct == True
                order = bool(order)

        # Instantiate connection list based on heuristic and in correct order,
        # and return correct approach
        if heuristic == 1:

            # Set density radius based on chip
            if chip == 0:
                density_radius = 3
            else:
                density_radius = 5

            # Generate connection list
            connections = graph.get_gate_densities(order, density_radius)

            return connections, False
        elif heuristic == 2:

            # Generate connection list
            connections = graph.get_connection_distance(order)
            return connections, True
    else:

        # Generate connection list
        connections = list(graph.netlist)

        return connections, True

def visualize_save_results(graph, wire_path):
    """
    Visualizes and/orsaves the results of the algorithm.

    Parameters
    ----------
    graph: a Graph object
            Representing the chip grid.

    wire_path: a dict
            Dictionary with connection as key and list with path coordinates as value.

    Outputs
    -------
    plot 
            Visualization plot of the results of the wire in the grid. 
    
    png file
            A png file of the visualization.


    """

    options = {'y', 'n'}

    # Ensure correct usage
    correct = False
    while not correct:

        # Prompt user for input for visualization
        show = input("\033[1m""Would you like to visualize the results? (y/n)\n""\033[1m")

        # Check input user
        if show in options:
            correct = True

    correct = False
    while not correct:
        
        # Prompt user for input for saving visualization
        save = input("\033[1m""Would you like to save the visualization of the results? (y/n)\n""\033[1m")

        # Check input user
        if save in options:
            correct = True

    # Show and save visualization based on user input
    if show == 'y' and save == 'y':

        # Visualize and save the results
        visualisation = vs.ChipVisualization(graph.gates, wire_path)
        visualisation.run()
        
    elif show == 'y' and save == 'n':

        # Visualize the results
        visualisation = vs.ChipVisualization(graph.gates, wire_path)
        visualisation.run()
    elif show == 'n' and save == 'y':

        # Save the visualization of the resutls
        pass


def restart_program():
    """
    Continues, restarts or quits program, bases on user's input.
    """

    options = {'0', '1', '2'}

    # Ensure correct usage
    correct = False
    while not correct:

        # Prompt user for input
        restart = input("\033[1m""Would you like to ... ?\n> 0 = continue\n> 1 = restart program\n> 2 = quit program\n""\033[1m")
        if restart in options:
            correct = True

    # Approach based on user input
    if restart == '0':
        pass
    elif restart == '1':
        main()
    elif restart == '2':
        sys.exit("Thank you, bye!")
