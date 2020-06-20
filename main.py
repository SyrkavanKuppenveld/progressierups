from code.classes import Graph
from code.algorithms import Greedy_RandomNet, Greedy_RandomPath, Greedy_RandomNet_LookAhead, Random, Greedy_RandomNet_NoIntersect, Greedy_RandomNet_NoIntersect_LookAhead, Greedy_RandomNet_LookAhead_Costs
from code.visualization import Chip_Visualization
from code.algorithms_revised import Greedy, GreedyLookAhead, GreedyLookAheadCosts, GreedyNoIntersect, GreedyNoIntersectLookAhead
from helpers import save_csv~
import sys
import csv


if __name__ == "__main__":
    
    # IMPORTANT: ZELF HET ALGORITHME NOG INVULLEN EN DENSITY AANROEPEN WERKT NOG NIET
    chip = int(input('Chip?\n'))
    netlist = int(input('Netlist?\n'))
    heuristic = input("Heuristic: density or distance?\n")
    order = bool(input("Order >> Max-min = True or min-max = False?\n"))

    print_file = f"gates&netlists/chip_{chip}/print_{chip}.csv"
    netlist_file = f"gates&netlists/chip_{chip}/netlist_{netlist}.csv"

    # Instantiate Graph object and order connections
    graph = Graph(print_file, netlist_file)

    # Instantiate connection list in correct order
    if heuristic == "density":
        connections = graph.getGateDensities()
    elif heuristic == "distance":
        connections = graph.getConnectionDistance(order)

    # Run algorithm
    algo = GreedyLookAhead(graph, connections)
    wire_path = algo.run()

    # Compute and print wire costs
    costs = algo.wire.compute_costs()
    print(f'wire costs = {costs}')

    # Visualise algorithm 
    visualisation = Chip_Visualization(graph.gates, wire_path)
    visualisation.run()

    with open("output.csv", 'w', newline='') as output_file:
        save_csv(netlist_file, output_file, wire_path, costs)

    

#     # Clear terminal
#     sys.stderr.write("\x1b[2J\x1b[H")

#     # List of working algorithms and netlists
#     working_algorithms = []

#     # Prompt user for chip selection
#     chosen_chip = input('Which chip do you want to use: 0, 1 or 2?\n')

#     # Activate print_file
#     # Prompt user for netlist selection based on selected chip
#     if chosen_chip == '0':
#         print_file = "gates&netlists/chip_0/print_0.csv"
#         chosen_netlist = input('\nWhich netlist do you want to use: 1, 2 or 3?\n')
#     elif chosen_chip == '1':
#         print_file = "gates&netlists/chip_1/print_1.csv"
#         chosen_netlist = input('\nWhich netlist do you want to use: 4, 5 or 6?\n')
#     elif chosen_chip == '2':
#         print_file = "gates&netlists/chip_2/print_2.csv"
#         chosen_netlist = input('\nWhich netlist do you want to use: 7, 8 or 9?\n')
#     else:
#         print('Please enter one of the given options.\n')

#     chosen_algorithm = input(f'\nWhich of the following algorithms do you want to use?\n\n 1 for Random \n 2 for Greedy Random Path \n 3 for Greedy Random Net \n 4 for Greedy Random Lookahead \n 5 for Greedy Random Net without Intersections \n 6 for Greedy Random Net Lookahead without Intersections \n\n')

#     ## If not in working_algorithms, print 'Not yet working.'?
#     # if (chosen_algorithm, chosen_netlist) not in working_algorithms:
#     #     print('Unfortunately, netlist ' + chosen_netlist + ' cannot be solved with ' + chosen_algorithm + ' , yet.')
#     #     sys.exit()

#     # Activate chosen netlist
#     netlist_file = "gates&netlists/chip_" + chosen_chip + "/netlist_" + chosen_netlist + ".csv"

#     # Instantiate Graph object
#     graph = Graph(print_file, netlist_file)


#     # -------------------------- RANDOM --------------------------

#     if chosen_algorithm == '1':

#         # Perform algorithm once, print costs and visualise
#         algo = Random(graph)
#         wire_path = algo.run()
#         costs = algo.wire.compute_costs()
#         print(f'wire costs = {costs}')
#         visualisation = Chip_Visualization(graph.gates, wire_path)
#         visualisation.run()

#         # Repeat algorithm until solution is found
#         not_found = True
#         while not_found:
#             while True:

#                 # Restart algorithm if error occurs
#                 try:
#                     # Run algorithm
#                     algo = Random(graph)
#                     wire_path = algo.run()

#                     # Compute and print wire costs
#                     costs = algo.wire.compute_costs()
#                     print(f'wire costs = {costs}')

#                     # Visualise algorithm 
#                     visualisation = Chip_Visualization(graph.gates, wire_path)
#                     visualisation.run()

#                     # Set not_found to True and break out of loop
#                     not_found = False
#                     break
#                 except:
#                     print("restart algorithm")
#                     break    

#     # -------------------- RANDOM GREEDY PATH --------------------

#     elif chosen_algorithm == '2':

#         # Graph
#         graph = Graph(print_file, netlist_file)

#         # Algorithms
#         algorithm = Greedy_RandomPath(graph)
#         wire_path = algorithm.run()

#         # Visualization
#         visualization = Chip_Visualization(graph.gates, wire_path)
#         visualization.run()

#     # -------------------- RANDOM GREEDY NET --------------------
    
#     elif chosen_algorithm == '3':

#         # Perform algorithm once, print costs and visualise
#         algo = Greedy_RandomNet(graph)
#         wire_path = algo.run()
#         costs = algo.wire.compute_costs()
#         print(f'wire costs = {costs}')
#         visualisation = Chip_Visualization(graph.gates, wire_path)
#         visualisation.run()

#         # Repeat algorithm until solution is found
#         not_found = True
#         while not_found:
#             while True:

#                 # Restart algorithm if error occurs
#                 try:
#                     # Run algorithm
#                     algo = Greedy_RandomNet(graph)
#                     wire_path = algo.run()

#                     # Compute and print wire costs
#                     costs = algo.wire.compute_costs()
#                     print(f'wire costs = {costs}')

#                     # Visualise algorithm 
#                     visualisation = Chip_Visualization(graph.gates, wire_path)
#                     visualisation.run()

#                     # Set not_found to True and break out of loop
#                     not_found = False
#                     break
#                 except:
#                     print("restart algorithm")
#                     break


# # --------------- RANDOM GREEDY NET LOOK AHEAD ---------------

#     elif chosen_algorithm == '4':
        
#         # Perform algorithm once print costs and visualise
#         algo = Greedy_RandomNet_LookAhead(graph)
#         wire_path = algo.run()
#         costs = algo.wire.compute_costs()
#         print(f'wire costs = {costs}')
#         visualisation = Chip_Visualization(graph.gates, wire_path)
#         visualisation.run()

#         # Repeat algorithm until solution is found
#         not_found = True
#         while not_found:
#             while True:

#                 # Restart algorithm if error occurs
#                 try:
#                     # Run algorithm
#                     algo = Greedy_RandomNet_LookAhead(graph)
#                     wire_path = algo.run()

#                     # Compute and print wire costs
#                     costs = algo.wire.compute_costs()
#                     print(f'wire costs = {costs}')

#                     # Visualise algorithm 
#                     visualisation = Chip_Visualization(graph.gates, wire_path)
#                     visualisation.run()

#                     # Set found to True and break out of loop
#                     not_found = False
#                     break
#                 except:
#                     print("restart algorithm")
#                     break

# # --------------- RANDOM GREEDY NET NO INTERSECT ---------------
   
#     elif chosen_algorithm == '5':

#         # Perform algorithm once print costs and visualise
#         algo = Greedy_RandomNet_NoIntersect(graph)
#         wire_path = algo.run()
#         costs = algo.wire.compute_costs()
#         print(f'wire costs = {costs}')
#         visualisation = Chip_Visualization(graph.gates, wire_path)
#         visualisation.run()

#         # Repeat algorithm until solution is found
#         not_found = True
#         while not_found:
#             while True:
        
#                 # Restart algorithm if error occurs
#                 try:
#                     # Run algorithm
#                     algo = Greedy_RandomNet_NoIntersect(graph)
#                     wire_path = algo.run()

#                     # Compute and print wire costs
#                     costs = algo.wire.compute_costs()
#                     print(f'wire costs = {costs}')

#                     # Visualise algorithm 
#                     # visualisation = Chip_Visualization(graph.gates, wire_path)
#                     # visualisation.run()

#                     # Set found to True and break out of loop
#                     not_found = False
#                     break
#                 except:
#                     print(algo.wire.path)
#                     print("restart algorithm")
#                     time.sleep(1)
#                     break


# # ---------- RANDOM GREEDY NET NO INTERSECT LOOK AHEAD ----------

#     elif chosen_algorithm == '6':

#         # Perform algorithm once print costs and visualise
#         algo = Greedy_RandomNet_NoIntersect_LookAhead(graph)
#         wire_path = algo.run()
#         costs = algo.wire.compute_costs()
#         print(f'wire costs = {costs}')
#         visualisation = Chip_Visualization(graph.gates, wire_path)
#         visualisation.run()

#         # Repeat algorithm until solution is found
#         not_found = True
#         while not_found:
#             while True:
        
#                 # Restart algorithm if error occurs
#                 try:
#                     # Run algorithm
#                     algo = Greedy_RandomNet_NoIntersect_LookAhead(graph)
#                     wire_path = algo.run()

#                     # Compute and print wire costs
#                     costs = algo.wire.compute_costs()
#                     print(f'wire costs = {costs}')

#                     # Visualise algorithm 
#                     visualisation = Chip_Visualization(graph.gates, wire_path)
#                     visualisation.run()

#                     # Set found to True and break out of loop
#                     not_found = False
#                     break
#                 except:
#                     print(algo.wire.path)
#                     time.sleep(1)
#                     print("restart algorithm")
#                     break
