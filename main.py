from code.classes import Graph
from code.algorithms import Greedy_RandomNet, Greedy_RandomNet_LookAhead, Random, Greedy_RandomNet_NoIntersect, Greedy_RandomNet_NoIntersect_LookAhead
from code.visualization import Chip_Visualization
import time

if __name__ == "__main__":

    print_file = "gates&netlists/chip_0/print_0.csv"
    netlist_file = "gates&netlists/chip_0/netlist_1.csv"
    # netlist_file = "gates&netlists/chip_0/netlist_2.csv"
    # netlist_file = "gates&netlists/chip_0/netlist_3.csv"

    # print_file = "gates&netlists/chip_1/print_1.csv"
    # netlist_file = "gates&netlists/chip_1/netlist_4.csv"
    # netlist_file = "gates&netlists/chip_1/netlist_5.csv"
    # netlist_file = "gates&netlists/chip_1/netlist_6.csv"

    # print_file = "gates&netlists/chip_2/print_2.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_7.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_8.csv"
    # netlist_file = "gates&netlists/chip_2/netlist_9.csv"

    # Instantiate Graph object
    graph = Graph(print_file, netlist_file)


    # -------------------------- RANDOM --------------------------

    # # Perform algorithm once, print costs and visualise
    # algo = Random(graph)
    # wire_path = algo.run()
    # costs = algo.wire.compute_costs()
    # print(f'wire costs = {costs}')
    # visualisation = Chip_Visualization(graph.gates, wire_path)
    # visualisation.run()

    # # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     while True:
            
    #         # Restart algorithm if error occurs
    #         try:
    #             # Run algorithm
    #             algo = Random(graph)
    #             wire_path = algo.run()

    #             # Compute and print wire costs
    #             costs = algo.wire.compute_costs()
    #             print(f'wire costs = {costs}')

    #             # Visualise algorithm 
    #             visualisation = Chip_Visualization(graph.gates, wire_path)
    #             visualisation.run()

    #             # Set not_found to True and break out of loop
    #             not_found = False
    #             break
    #         except:
    #             print("restart algorithm")
    #             break    


    # -------------------- RANDOM GREEDY NET --------------------
    
    # # Perform algorithm once, print costs and visualise
    # algo = Greedy_RandomNet(graph)
    # wire_path = algo.run()
    # costs = algo.wire.compute_costs()
    # print(f'wire costs = {costs}')
    # visualisation = Chip_Visualization(graph.gates, wire_path)
    # visualisation.run()

    # # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     while True:
    # 
    #         # Restart algorithm if error occurs
    #         try:
    #             # Run algorithm
    #             algo = Greedy_RandomNet(graph)
    #             wire_path = algo.run()

    #             # Compute and print wire costs
    #             costs = algo.wire.compute_costs()
    #             print(f'wire costs = {costs}')

    #             # Visualise algorithm 
    #             visualisation = Chip_Visualization(graph.gates, wire_path)
    #             visualisation.run()

    #             # Set not_found to True and break out of loop
    #             not_found = False
    #             break
    #         except:
    #             print("restart algorithm")
    #             break


# --------------- RANDOM GREEDY NET LOOK AHEAD ---------------

    # # Perform algorithm once print costs and visualise
    # algo = Greedy_RandomNet_LookAhead(graph)
    # wire_path = algo.run()
    # costs = algo.wire.compute_costs()
    # print(f'wire costs = {costs}')
    # visualisation = Chip_Visualization(graph.gates, wire_path)
    # visualisation.run()

    # # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     while True:
    
    #         # Restart algorithm if error occurs
    #         try:
    #             # Run algorithm
    #             algo = Greedy_RandomNet_LookAhead(graph)
    #             wire_path = algo.run()

    #             # Compute and print wire costs
    #             costs = algo.wire.compute_costs()
    #             print(f'wire costs = {costs}')

    #             # Visualise algorithm 
    #             visualisation = Chip_Visualization(graph.gates, wire_path)
    #             visualisation.run()

    #             # Set found to True and break out of loop
    #             not_found = False
    #             break
    #         except:
    #             print("restart algorithm")
    #             break

# --------------- RANDOM GREEDY NET NO INTERSECT ---------------

    # # Perform algorithm once print costs and visualise
    # algo = Greedy_RandomNet_NoIntersect(graph)
    # wire_path = algo.run()
    # costs = algo.wire.compute_costs()
    # print(f'wire costs = {costs}')
    # visualisation = Chip_Visualization(graph.gates, wire_path)
    # visualisation.run()

    # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     while True:
    
    #         # Restart algorithm if error occurs
    #         try:
    #             # Run algorithm
    #             algo = Greedy_RandomNet_NoIntersect(graph)
    #             wire_path = algo.run()

    #             # Compute and print wire costs
    #             costs = algo.wire.compute_costs()
    #             print(f'wire costs = {costs}')

    #             # Visualise algorithm 
    #             # visualisation = Chip_Visualization(graph.gates, wire_path)
    #             # visualisation.run()

    #             # Set found to True and break out of loop
    #             not_found = False
    #             break
    #         except:
    #             print(algo.wire.path)
    #             print("restart algorithm")
    #             time.sleep(1)
    #             break


# ---------- RANDOM GREEDY NET NO INTERSECT LOOK AHEAD ----------

    # # Perform algorithm once print costs and visualise
    # algo = Greedy_RandomNet_NoIntersect_LookAhead(graph)
    # wire_path = algo.run()
    # costs = algo.wire.compute_costs()
    # print(f'wire costs = {costs}')
    # visualisation = Chip_Visualization(graph.gates, wire_path)
    # visualisation.run()

    # # Repeat algorithm until solution is found
    # not_found = True
    # while not_found:
    #     while True:
    
    #         # Restart algorithm if error occurs
    #         try:
    #             # Run algorithm
    #             algo = Greedy_RandomNet_NoIntersect_LookAhead(graph)
    #             wire_path = algo.run()

    #             # Compute and print wire costs
    #             costs = algo.wire.compute_costs()
    #             print(f'wire costs = {costs}')

    #             # Visualise algorithm 
    #             visualisation = Chip_Visualization(graph.gates, wire_path)
    #             visualisation.run()

    #             # Set found to True and break out of loop
    #             not_found = False
    #             break
    #         except:
    #             print(algo.wire.path)
    #             time.sleep(1)
    #             print("restart algorithm")
    #             break


