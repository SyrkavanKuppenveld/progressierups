#!/usr/bin/python
# -*- coding: utf-8 -*-

# Built-in/Generic Imports
import sys
import time

# Own modules
from main import main
import code.visualization as vs
import matplotlib.pyplot as plt

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
    Returns the chip number chosen by the user.

    Returns
    -------
    int 
            An integer representing the chip number chosen by the user.
    """

    options = {'0', '1', '2'}
    correct = False

    while not correct:

        # Prompt user for chip
        print("\n\033[1m""Choose a chip: 0, 1 or 2?""\033[0m")
        chip = input()

        # Quit if user input is correct
        if chip in options:
            correct = True
        
    return int(chip)


def netlist_input(chip):
    """
    Returns netlist number chosen by the user.

    Parameters
    ----------
    chip: an int
            The chip number.
    
    Returns
    -------
    int
            An integer representing the netlist number chosen by the user.
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
            print("\033[1m""Choose a netlist: 7, 8 or 9?""\033[0m")
            netlist = input()
            options = {'7', '8', '9'}
            if netlist in options:
                correct = True

    return int(netlist)    


def algorithm_input(netlist):
    """
    Asks user which algorithm is to be used.
    Returns an integer representing the algorithm chosen by the user.
    Provides an option to print more information on the algorithms. 

    Parameters
    ----------
    netlist: an int
            Het netlist number.

    Returns
    -------
    int
            An integer corresponding with the chosen algorithm.
    """

    options = {'0', '1', '2', '3', '4'}
    
    correct = False
    while not correct:

        # Prompt user for algorithm
        print("\033[1m""Which algorithm would you like to run?""\033[0m")
        print("For more information on the algorithms press 9 directly followed by the algorithm number.")
        print("> 0 = Random\n> 1 = Greedy\n> 2 = Greedy Look Ahead\n> 3 = Hillclimber\n> 4 = Restart Hillclimber")
        algorithm = input()
        print()

        # Provide information on random algorithm
        if algorithm == '90':
            print("\033[1m""INFORMATION RANDOM ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist.")
            print()
            print("Random elements:\n* The order of the connections are generated randomly.\n* The next position is generated randomly.")

            # Print warning message and prompt user for next approach
            if netlist > 2:
                print()
                print("\033[31m""WARNING! The random algorithm only works for netlist 1 and 2 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

        # Provide information on the greedy algorithm
        elif algorithm == '91':
            print("\033[1m""INFORMATION GREEDY ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist and according to the lowest Manhattan Distance.")
            print()
            print("Greedy elements:\n* The next position will be the neighbor with the lowest Manhattan distance.")
            print()
            print("Random element:\n* If multiple neighbors have the same distance, the next position is generated randomly.")
            print()
            print("The greedy algorithm works with the following heuristics:")
            print("* 'Social map'\n* 'Better a neighbor who is near than an brother far away?'\n* 'Wire Jam'")
            print("Option for more information on the heuristics will be given later.")
            time.sleep(5)
            print()

        # Provide information on the greedy look ahead algorithm
        elif algorithm == '92':
            print("\033[1m""INFORMATION GREEDY LOOK AHEAD ALGORITHM:""\033[0m")
            print("Creates a Wire object that connects the gates according to the netlist and according to the lowest Manhattan Distance with a 4 step look ahead.")
            print()
            print("Greedy elements:\n* The next position will be the neighbor with the lowest Manhattan distance.")
            print()
            print("Random element:\n* If multiple neighbors have the same distance, the next position is generated randomly.")
            print()
            print("The greedy look ahead algorithm works with the following heuristics:")
            print("\n* 'Social map'\n* 'Better a neighbor who is near than an brother far away?\n* 'Sky is the Limit'\n* 'Wire Jam'")
            time.sleep(5)
            print()

        # Provide information on the hillclimber algorithm
        elif algorithm == '93' or algorithm == '94':
            print("\033[1m""INFORMATION HILLCLIMBER ALGORITHM""\033[0m")
            print("The HillCLimber is a stochastic HillClimber.")
            print()
            print("Start state:\n* Acquires a Random start state using the Random algorithm.")
            print()
            print("Random adjustments:\n* The path that is to be re-build is chosen randomly.")
            print()
            print("New path:\n* The new path will be build with the use of the Greedy LookaHead algorithm.")
            time.sleep(5)
            print()

        # Continue if algorithm choice is valid
        if algorithm in options:
            correct = True

            # Print warning and prompt user for next approach
            if algorithm == '0' and netlist > 2:
                print("\033[31m""WARNING! The random algorithm only works for netlist 1 and 2 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()
            
            # Print warning and prompt user for next approach
            if algorithm == '3' and netlist > 2:
                print("\033[31m""WARNING! The hillclimber algorithm only works for netlist 1 and 2 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

    return int(algorithm)


def hillclimber_restarts():
    """
    Prompts user for the number of times the Hillclimber should be run and returns the frequency.

    Returns
    -------
    int
            A number representing the number of times the Hillclimber will be run.
    """

    correct = False
    while not correct:
        
        # Prompt user for the number of restarts
        print("\033[1m""How many times would you like the hillclimber to restart?""\033[0m")
        frequency = input()

        # Quit if user input is correct
        if frequency.isdigit():
            correct = True
        
    return frequency


def get_flow(plot):
    """
    Asks user if the given plot needs to be shown and/or saved. Returns True or 
    False on both questions.

    Returns
    -------
    boolean tuple
            A tuple representing the choice on whether the plot needs to be 1) shown
            and/or 2) saved
    """

    options = {'y', 'n'}
    correct = False

    # Questions
    q1_start_state = "Would you like to see the start states of the hillclimber algorithm?"
    q1_conversion = "\nWould you like to see the conversion plot of the hillclimber algorithm?"

    q2_start_state = "Would you like to save the start states of the hillclimber algorithm?"
    q2_conversion = "Would you like to save the conversion plot of the hillclimber algorithm?"

    # Adapt questions to the plot being asked
    if plot == 'start_state':
        q1 = q1_start_state
        q2 = q2_start_state
    else:
        q1 = q1_conversion
        q2 = q2_conversion

    # Ensure proper usage
    while not correct:
        
        # Ask user if the plot should be shown
        print("\033[1m"f"{q1} (y/n)""\033[0m")
        show = input()

        # Quit if user input is correct
        if show in options:
            correct = True

    # Convert show to bool
    if show == 'y':
        show_bool = True
    else:
        show_bool = False

    # Reset correct-status
    correct = False

    # Ensure proper usage
    while not correct:

        # Ask user if the plot of the Hillclimber algorithm should be saved
        print()
        print("\033[1m"f"{q2} (y/n)""\033[0m")
        save = input()

        # Quit if user input is correct
        if save in options:
            correct = True
    
    # Convert save to bool
    if save == 'y':
        save_bool = True
    else:
        save_bool = False
        
    return show_bool, save_bool


def get_hillclimber_flow(algorithm):
    """
    Asks user what the prefered work flow of the hillblimber is.

    Parameters
    ----------
    algorithm: an int
            The algorithm that is chosen, 3 for Hillclimber, 4 for Restart Hillclimber

    Returns
    -------
    boolean tuple
            A tuple representing the answers on 1) what the frequency should be of 
            the Restart Hillclimber and whether or not 2) the start states 3) and
            the conversion plot shouldbe shown.
    """

    # Get the frequency of the Restart Hillclimber
    if algorithm == 4:
        frequency = hillclimber_restarts()

    # Default frequency for the normal Hillclimber  to 1
    else:
        frequency = 1

    # Get answer to whether or not the plots should be shown and/or saved
    plot = 'start_state'
    start_state_flow =  get_flow(plot)
    plot = 'conversion_plot'
    conversion_plot_flow = get_flow(plot)

    return frequency, start_state_flow, conversion_plot_flow


def heuristic_input(netlist, algorithm):
    """
    Returns the integer representing the heuristic chosen by the user.
    Option to print extra information on the heuristics. 

    Parameters
    ----------
    netlist: int
            The netlist chosen by the user.
    
    algorith: int
            The algorithm chosen by the user.

    Returns
    -------
    int
            An integer representing the chosen heuristic. 
    """

    options = {'0', '1', '2', '3', '4', '5'}

    correct = False
    while not correct:

        # Prompt user for heuristic 
        print("\n\033[1m""Which heuristic would you like to implement?""\033[0m")
        print("For more information on the algorithms press 9 directly followed by the heuristic number.")
        print("> 0 = none\n> 1 = 'Social Map'\n> 2 = 'Better a neighbor who is near than an brother far away?\n> 3 = 'Sky is the Limit'\n> 4 = 'Can't Touch This'\n> 5 = 'Wire Jam'")
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
            print("The 'Sky Is The Limit' heuristic increases the costs for not moving up in the grid and wired neighbors if the Manhattan Distance between gates is higher than 4.")
            print("This heuristic can be combined with 'Social Map' and 'Better A Neighbor Who Is Near Than A Brother Far Away'.")
            print()
            time.sleep(3)
            print()

        elif heuristic == '94':
            print("\033[1m""INFORMATION CANT TOUCH THIS""\033[0m")
            print("The 'Can't Touch This' heuristic has intersections as hard contrained.")
            print("This heuristic can be combined with 'Social Map' and 'Better A Neighbor Who Is Near Than A Brother Far Away'.")
            print()
            time.sleep(3)
            print()

        elif heuristic == '95':
            print("\033[1m""INFORMATION WIRE JAM""\033[0m")
            print("The 'Wire Jam' heuristic avoids places on the grid that are crowed with wire.")
            print("This heuristic can be combined with 'Social Map' and 'Better A Neighbor Who Is Near Than A Brother Far Away'.")
            print()
            time.sleep(3)
            print()

        # Only continue if heuristic for correct input
        if heuristic in options:

            # Convert heuristic to integer
            heuristic = int(heuristic)

            # Set correct to true
            correct = True

            # Print warning for greedy with none or no intersect heuristic
            if netlist > 3 and algorithm == 1 and (heuristic < 3 or heuristic == 4):
                print()
                print("\033[31m""WARNING: the combination of the algorithm and heuristic only works for netlist 1-3 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # Print warning for greedy look ahead for heuristics 1 and 2
            elif netlist > 4 and algorithm == 2 and (heuristic == 1 or heuristic == 2):
                print()
                print("\033[31m""WARNING: the combination of the algorithm and heuristic only works for netlist 1-4 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # Print warning for greedy look ahead with none or no intersect heuristic
            elif netlist > 3 and algorithm == 2 and heuristic == 4:
                print()
                print("\033[31m""WARNING: the combination of the algorithm and heuristic only works for netlist 1-3 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # Print warning for greedy look ahead with none 
            elif netlist > 3 and algorithm == 2 and heuristic == 0:
                print()
                print("\033[31m""WARNING: the combination of the algorithm and heuristic only works for netlist 1-4 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # Print warning for greedy and greedy look ahead with costs heuristic
            elif netlist > 7 and (algorithm == 1 or algorithm == 2) and heuristic == 3:
                print()
                print("\033[31m""WARNING: the combination of the algorithm (and heuristic) only works for netlist 1-7 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # Print warning for greedy and greedy look ahead with costs heuristic
            elif netlist > 4 and (algorithm == 1 or algorithm == 2) and heuristic == 5:
                print()
                print("\033[31m""WARNING: the combination of the algorithm (and heuristic) only works for netlist 1-4 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()
           
    return heuristic 


def heuristic_extention(chip, heuristic, graph):
    """
    Returns the correct connections list based on heuristic and the corresponding run approach.

    chip: an int
            The chip number chosen by the user.

    graph: a Graph object
            A graph object representing the chip grid.
    
    Returns
    -------
    list 
            A list containing gateIDs or connections.

    bool
            True if list contains connections, false if list contains gates.
    """

    extention_options = {'0', '1', '2'}
    
    # Set correct heuristic name for formatting
    if heuristic == 3:
        heur_name = "Sky Is The Limit"
    elif heuristic == 4:
        heur_name = "Can't Touch This"
    elif heuristic == 5:
        heur_name ="Wire Jam"
        
    # Ensure correct usage
    correct = False
    while not correct:
        
        # Prompt user for order heuristic list
        print("\033[1m"f"With which second heuristic would you like to extent '{heur_name}'?""\033[0m")
        print("> 0 = none\n> 1 = 'Social Map'\n> 2 = 'Better a neighbor who is near than an brother far away?")
        extention = input()

        # If usage is correct set correct to true and convert order to bool
        if extention in extention_options:
            correct = True
            extention = int(extention)
    
    order_options = {'0', '1'}
    
    # Only prompt for order if user wants an extention
    if extention > 0:

        # Ensure correct usage
        correct = False
        while not correct:
            
            # Prompt user for the order in which the heuristic list should be
            print()
            print("\033[1m""How would you like to implement the heuristic?""\033[0m")
            print("> 0 = sorted from min-max\n> 1 = sorted from max-min")
            order = input()

            # If usage is correct set correct to true and convert order to bool
            if order in order_options:
                correct = True
                order = bool(order)

        # Instantiate connection list based on heuristic, in correct order
        # and return correct approach
        if extention == 1:

            # Set density radius based on chip
            if chip == 0:
                density_radius = 3
            else:
                density_radius = 5

            # Generate connection list
            connections = graph.get_gate_densities(order, density_radius)
            return connections, False
        
        elif extention == 2:

            # Generate connection list
            connections = graph.get_connection_distance(order)
            return connections, True
    else:

        # Generate connection list
        connections = list(graph.netlist)
        return connections, True
    

def heuristic_order_input(chip, netlist, algorithm, heuristic, graph):
    """
    Returns the correct connections list based on heuristic and the corresponding run approach.

    chip: int
            The chip number chosen by the user.

    netlist: int
            The netlist number chosen by the user.

    algorithm: int
            A integer representing the algorithm chosen by the user.

    heuristic: int
            The heuristic chosen by the user.

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
    
    # Only prompt for order for heuristic 1 and 2
    if heuristic > 0:

        # Ensure correct usage
        correct = False
        while not correct:
            
            # Prompt user for order heuristic list
            print("\033[1m""How would you like to implement the heuristic?""\033[0m")
            print("> 0 = sorted from min-max\n> 1 = sorted from max-min")
            order = input()

            # Print warning for greedy look ahead with none 
            if netlist > 3 and algorithm == 2 and heuristic == 2 and order == '0':
                print()
                print("\033[31m""WARNING: the combination of the algorithm, heuristic and orer only works for netlist 1-3 within a reasonable amount of time.""\033[0m")
                print()
                restart_program()

            # If usage is correct set correct to true and convert order to bool
            if order in options:
                correct = True
                order = bool(order)

        # Instantiate connection list based on heuristic, correct order
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
    Visualizes and/or saves the results of the algorithm based on user input.

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
        print("\033[1m""Would you like to visualize the results? (y/n)""\033[0m")
        show = input()

        # Check input user
        if show in options:
            correct = True

    # Ensure correct usage
    correct = False
    while not correct:
        
        # Prompt user for input for saving visualization
        print()
        print("\033[1m""Would you like to save the visualization of the results? (y/n)""\033[0m")
        save = input()

        # Check input user
        if save in options:
            correct = True

    # Show and save visualization based on user input
    if show == 'y' and save == 'y':

        # Visualize and save the results
        visualisation = vs.ChipVisualization(graph.gates, wire_path)
        plot = visualisation.run(True)
        plot.savefig("results/visualization_algorithm.png")
        print()
        print("For saved visualization see: 'results/visualization_algorithm.png'.")
    elif show == 'y' and save == 'n':

        # Visualize the results
        visualisation = vs.ChipVisualization(graph.gates, wire_path)
        plot = visualisation.run(True)
    elif show == 'n' and save == 'y':

        # Save the visualization of the resutls
        visualisation = vs.ChipVisualization(graph.gates, wire_path)
        plot = visualisation.run(False)
        plot.savefig("results/visualization_algorithm.png")
        print()
        print("For saved visualization see: 'results/visualization_algorithm.png'.")


def heatmap_visualize_save(graph, wire_path):
    """
    Visualizes and/or saves the wire heatmap of the chip grid. 

    Parameters
    ----------
    graph: a Graph object
            Representing the chip grid.

    wire_path: a dict
            Dictionary with connection as key and list with path coordinates as value.

    Outputs
    -------
    plot 
            Wire heatmap of the results of the wire in the grid. 
    
    png file
            A png file of the visualization.
    """

    options = {'y', 'n'}

    # Ensure correct usage
    correct = False
    while not correct:

        # Prompt user for input for visualization heatmap
        print("\033[1m""Would you like see the wire heatmap of the chip grid? (y/n)""\033[0m")
        show = input()

        # Check input user
        if show in options:
            correct = True

    # Ensure correct usage
    correct = False
    while not correct:
        
        # Prompt user for input for saving heatmap
        print()
        print("\033[1m""Would you like to save the wire heatmap of the chipgrid? (y/n)""\033[0m")
        save = input()

        # Check input user
        if save in options:
            correct = True

    # Show and save heatmap visualization based on user input
    if show == 'y' and save == 'y':

        # Visualize and save the heatmap
        heatmap = vs.WireHeatmap(graph.gates, wire_path)
        plot = heatmap.run(True)
        plot.savefig("results/heatmap_algorithm.png")
        print()
        print("For saved visualization see: 'results/heatmap_algorithm.png'.")
    elif show == 'y' and save == 'n':

        # Visualize the heatmap
        heatmap = vs.WireHeatmap(graph.gates, wire_path)
        plot = heatmap.run(True)
    elif show == 'n' and save == 'y':

        # Save the visualization of the resutls
        heatmap = vs.WireHeatmap(graph.gates, wire_path)
        plot = heatmap.run(False)
        plot.savefig("results/heatmap_algorithm.png")
        print()
        print("For saved visualization see: 'results/heatmap_algorithm.png'.")


def restart_program():
    """
    Continues, restarts or quits program, bases on user's input.
    """

    options = {'0', '1', '2'}

    # Ensure correct usage
    correct = False
    while not correct:

        # Prompt user for input
        print("\033[1m""Would you like to ... ?""\033[0m")
        print("> 0 = continue\n> 1 = restart program\n> 2 = quit program")
        restart = input()
        if restart in options:
            correct = True

    # Approach based on user input
    if restart == '0':
        pass
    elif restart == '1':
        main()
    elif restart == '2':
        sys.exit()
