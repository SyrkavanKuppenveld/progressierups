from code.classes import Graph
from code.algorithms import Greedy_RandomNet, Greedy_RandomPath, Greedy_RandomNet_LookAhead, Random, Greedy_RandomNet_NoIntersect, Greedy_RandomNet_NoIntersect_LookAhead, Greedy_RandomNet_LookAhead_Costs
from code.visualization import Chip_Visualization
import time
import sys
import csv
import re

def save_csv(netlist_file, outfile, wire_path):
    """
    Output a CSV file containing the wire path per connection.

    Parameters 
    ----------     
    netlist_file: a csv file
            Name of the csv file containing a netlist.

    outfile: a csv file
            A plain csv file for the output.

    wire_path: dict
            A dictionary containing the wire path per connection. 

    Output
    ------
    csv file
            A csv file containing the connections and the wire_path. 
            In the correct format for the check50.
    """

    # Generate chip and netlist number 
    plain = re.sub("[^0-9]", "", netlist_file)
    chip = plain[0]
    net = plain[1]

    # Initialize csv write object
    writer = csv.writer(outfile)

    # Write headers
    writer.writerow(['net', 'wires'])

    # Write rows for connection and wire path in correct format for check50
    for connection in wire_path:
        layout = ""
        for i, coordinate in enumerate(wire_path[connection]):
            if i == 0:
                layout += (f'([{coordinate[0]},{coordinate[1]},{coordinate[2]}),')
            elif i == len(wire_path[connection]) - 1:
                layout += (f'({coordinate[0]},{coordinate[1]},{coordinate[2]})]')
            else:
                layout += (f'({coordinate[0]},{coordinate[1]},{coordinate[2]}),')

        # Write row for connection and corresponding wire path
        writer.writerow([f"({connection[0]},{connection[1]})", f"{layout}"])

    # Write row with chip and netlist information
    writer.writerow([f'chip_{chip}_net_{net}', costs])

    print("output.csv DONE")

    # WAT ER NET MET QUINTEN BESPROKEN IS

    # # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     try:
    #         # Run algorithm
    #         graph = Graph(print_file, netlist_file)
    #         algo = Random(graph)
    #         wire_path = algo.run()

    #         # Compute and print wire costs
    #         costs = algo.wire.compute_costs()
    #         print(f'wire costs = {costs}')

    #         # Visualise algorithm 
    #         visualisation = Chip_Visualization(graph.gates, wire_path)
    #         visualisation.run()

    #         # Set found to True and break out of loop
    #         not_found = False
    #     except:
    #         print("restart algorithm")


if __name__ == "__main__":
    
    print_file = "gates&netlists/chip_0/print_0.csv"
    netlist_file = "gates&netlists/chip_0/netlist_1.csv"
    netlist_file = "gates&netlists/chip_0/netlist_2.csv"
    netlist_file = "gates&netlists/chip_0/netlist_3.csv"

    print_file = "gates&netlists/chip_1/print_1.csv"
    netlist_file = "gates&netlists/chip_1/netlist_4.csv"
    netlist_file = "gates&netlists/chip_1/netlist_5.csv"
    # netlist_file = "gates&netlists/chip_1/netlist_6.csv"

    # print_file = "gates&netlists/chip_2/print_2.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_7.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_8.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_9.csv"

    # Instantiate Graph object
    graph = Graph(print_file, netlist_file)

    # Repeat algorithm until solution is found
    not_found = True
    while not_found:
        while True:
    
            # Restart algorithm if error occurs
            try:
                # Run algorithm
                algo = Greedy_RandomNet_LookAhead_Costs(graph)
                wire_path = algo.run()

                # Compute and print wire costs
                costs = algo.wire.compute_costs()
                print(f'wire costs = {costs}')

                # Print wire path per connection
                print(algo.wire.path)
                print()
                print(wire_path)

                # Visualise algorithm 
                visualisation = Chip_Visualization(graph.gates, wire_path)
                visualisation.run()

                # Set not_found to True and break out of loop
                not_found = False
                break
            except ValueError:
                print("restart algorithm")
                break

    with open("output.csv", 'w', newline='') as output_file:
        save_csv(netlist_file, output_file, wire_path)

    

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
