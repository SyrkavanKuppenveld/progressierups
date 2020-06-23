import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt 
import csv 
import numpy as np

min_costs = []

# Get min costs greedy
net3_greedy = pd.read_csv("part1/greedy/netlist_3.csv")
net3_greedy_min = net3_greedy['costs'].min()
min_costs.append(net3_greedy_min)

# Get min costs greedy look ahead
net3_lookahead = pd.read_csv("part1/greedy_lookahead/netlist_3.csv")
net3_lookahead_min = net3_lookahead ['costs'].min()
min_costs.append(net3_lookahead_min)

# Get min costs greedy look ahead no intersect
net3_nointersect = pd.read_csv("part1/no_inter_lookahead/netlist_3.csv")
net3_nointersect_min = net3_nointersect['costs'].min()
min_costs.append(net3_nointersect_min)

labels = ['Greedy', 'Greedy Look Ahead', 'Greedy Look Ahead No Intersections']


y_pos = np.arange(len(labels))
 
# Create bars
plt.bar(y_pos, min_costs, color='g')
 
# Create names on the x-axis
plt.xticks(y_pos, labels)

# Plot title
plt.title("Min Costs Per Algorithm For Netlist 3", fontsize=20)
 
# Show graphic
plt.show()
