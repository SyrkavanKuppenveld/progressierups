import sys

def initialize():

    # Clear terminal
    sys.stderr.write("\x1b[2J\x1b[H")

    # Dict of unsolvable netlists per algorithm
    missing_algorithms = {}
    missing_algorithms['2'] = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    # Dict of heuristics per algorithm
    # possible_heuristics = {}
    # possible_heuristics['1'] = 


    # Prompt user for chip selection
    chosen_chip = input('Which chip do you want to use: 0, 1 or 2?\n')

    # Activate print_file
    # Prompt user for netlist selection based on selected chip
    if chosen_chip == '0':
        print_file = "gates&netlists/chip_0/print_0.csv"
        chosen_netlist = input('\nWhich netlist do you want to use: 1, 2 or 3?\n')
    elif chosen_chip == '1':
        print_file = "gates&netlists/chip_1/print_1.csv"
        chosen_netlist = input('\nWhich netlist do you want to use: 4, 5 or 6?\n')
    elif chosen_chip == '2':
        print_file = "gates&netlists/chip_2/print_2.csv"
        chosen_netlist = input('\nWhich netlist do you want to use: 7, 8 or 9?\n')
    else:
        print('Please enter one of the given options.\n')

    # Prompt user for algorithm selection
    chosen_algorithm = input(f'\nWhich of the following algorithms do you want to use?\n\n 1 for Random \n 2 for Greedy Random Path \n 3 for Greedy Random Net \n 4 for Greedy Random Lookahead \n 5 for Greedy Random Net without Intersections \n 6 for Greedy Random Net Lookahead without Intersections \n\n')

    # If in missing_algorithms, stop
    try:
        if chosen_netlist in missing_algorithms[chosen_algorithm]:
            print('Unfortunately, netlist ' + chosen_netlist + ' cannot be solved with algorithm ' + chosen_algorithm + ' , yet.')
            sys.exit()
    except KeyError:
        pass

    # If chosen algorithm has multiple heuristics, choose one
    # try:
    #     if len(possible_heuristics[chosen_algorithm]) > 1:
    #         chosen_heuristic = input('Which heuristic do you want to use?\n\n 1 for Random gate order \n 2 for Gate order based on density \n')
    # except KeyError:
    #     pass


    return chosen_chip, chosen_netlist, chosen_algorithm
