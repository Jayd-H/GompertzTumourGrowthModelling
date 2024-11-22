# Jayden Holdsworth
# Task 2.2
# Algorithm to simulate Gompertz tumour growth and spread on a grid using translation approach

import numpy as np
import matplotlib.pyplot as plt

# each  time step calculates new population based on the current population, growth rate (k), and carrying capacity (M)
def gompertz_growth(t, N0, k, M, h=0.001):
    steps = int(t/h) 
    N = np.zeros(steps+1)
    N[0] = N0
    
    for i in range(steps):
        # Gompertz equation (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gompertz.html)
        dN = k * N[i] * np.log(M/N[i])
        # Euler's method (https://en.wikipedia.org/wiki/Euler_method)
        N[i+1] = N[i] + h * dN
    
    return N

# checks if the system has reached steady state
# it does this by checking if the relative change in population is less than a threshold
def check_steady_state(N, threshold=0.001):
    # check if system has reached steady state by comparing consecutive values
    return abs((N[-1] - N[-2])/N[-2]) < threshold

# !MAIN (this should be its own function __main__)

# initial parameters (from brief)
k = 0.006  # growth rate
M = 10**13  # carrying capacity
N0 = 10**9  # initial population
h = 0.001 # steps size

# max amount of time freo steady state
t_max = 1200

max_tumours = 1000
milestones = [ 10, 25, 50, 100, 200, 400 ]

# calculate the steady state once, and then use this value for all cells (translation approach)
# does this because its computationally expensive to calculate for each cell 
N = gompertz_growth(t_max, N0, k, M, h)
while not check_steady_state(N):
    t_max += 100
    N = gompertz_growth(t_max, N0, k, M, h)
steady_state_value = N[-1]

# creates grid and whatnot
grid_size = 100
grid = np.zeros((grid_size, grid_size))
cell_values = np.zeros((grid_size, grid_size))
occupied_cells = set()

x, y = grid_size // 2, grid_size // 2
occupied_cells.add((x, y))
grid[x, y] = 1
cell_values[x, y] = steady_state_value
tumour_count = 1
path = [(x, y)]

# records direction spread statistics at specific tumour milestones
milestone_counts = {steps: {'N': 0, 'S': 0, 'W': 0, 'E': 0, 
                         'NE': 0, 'NW': 0, 'SE': 0, 'SW': 0} 
                  for steps in milestones}
N = S = W = E = NW = NE = SW = SE = 0

# this is a modified version of task 1.2 that keeps track of occupied cells
# i opted to just use a simple randint to determine direction instead of random.uniform this time
# this is for ease of implementation and to keep the code simple
# uniform distribution still occurs because randint uses uniform distribution
while tumour_count < max_tumours:
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            new_x, new_y = x + dx, y + dy
            if (0 <= new_x < grid_size and 
                0 <= new_y < grid_size and 
                (new_x, new_y) not in occupied_cells):
                if dy == -1:  # North
                    if dx == -1: direction = 'NW'
                    elif dx == 0: direction = 'N'
                    else: direction = 'NE'
                elif dy == 0:  # East/West
                    if dx == -1: direction = 'W'
                    else: direction = 'E'
                else:  # South
                    if dx == -1: direction = 'SW'
                    elif dx == 0: direction = 'S'
                    else: direction = 'SE'
                neighbors.append((new_x, new_y, direction))
    
    if not neighbors:
        break
        
    next_x, next_y, direction = neighbors[np.random.randint(len(neighbors))]
    
    if direction == 'N': N += 1
    elif direction == 'S': S += 1
    elif direction == 'W': W += 1
    elif direction == 'E': E += 1
    elif direction == 'NE': NE += 1
    elif direction == 'NW': NW += 1
    elif direction == 'SE': SE += 1
    elif direction == 'SW': SW += 1
    
    x, y = next_x, next_y
    occupied_cells.add((x, y))
    grid[x, y] = 1
    cell_values[x, y] = steady_state_value
    path.append((x, y))
    tumour_count += 1
    
    if tumour_count in milestones:
        milestone_counts[tumour_count]['N'] = N
        milestone_counts[tumour_count]['S'] = S
        milestone_counts[tumour_count]['W'] = W
        milestone_counts[tumour_count]['E'] = E
        milestone_counts[tumour_count]['NE'] = NE
        milestone_counts[tumour_count]['NW'] = NW
        milestone_counts[tumour_count]['SE'] = SE
        milestone_counts[tumour_count]['SW'] = SW

if tumour_count not in milestones:
    milestones.append(tumour_count)
    milestone_counts[tumour_count] = {'N': N, 'S': S, 'W': W, 'E': E,
                                    'NE': NE, 'NW': NW, 'SE': SE, 'SW': SW}


# plot the final path and the spread statistics at each milestone
milestones.sort()

num_milestone_plots = sum(1 for m in milestones if m <= tumour_count)
total_plots = num_milestone_plots + 1

num_rows = (total_plots + 1) // 2 
num_cols = 2

fig = plt.figure(figsize=(12, 4 * num_rows))

plt.subplot(num_rows, num_cols, 1)
plt.imshow(grid, cmap="binary", interpolation="nearest")
plt.title(f"Final Path\n(Tumours: {tumour_count})")

for plot_num, milestone in enumerate(milestones):
    if milestone <= tumour_count:
        plt.subplot(num_rows, num_cols, plot_num + 2)
        counts = milestone_counts[milestone]
        total = sum(counts.values())
        
        percentages = {k: (v/total)*100 for k, v in counts.items()}
        
        plt.bar(percentages.keys(), percentages.values(), width=0.8)
        plt.title(f'After {milestone} tumours')
        plt.ylabel('Percentage')
        plt.ylim(0, 50)
        plt.xticks(rotation=45)
        
        for j, v in enumerate(percentages.values()):
            plt.text(j, v + 0.5, f'{v:.1f}%', ha='center')

plt.tight_layout(pad=3.0)
plt.show()

print(f"\nFinal number of tumuors: {tumour_count}")
print(f"Final steady state value: {steady_state_value:.2e}")
print(f"Number of cells occupied: {len(occupied_cells)}")

print("\nRaw counts at each milestone:")
for milestone in milestones:
    if milestone <= tumour_count:
        counts = milestone_counts[milestone]
        total = sum(counts.values())
        percentages = {k: (v/total)*100 for k, v in counts.items()}
        print(f"\nAfter {milestone} tumours:")
        print(f"North: {counts['N']} ({percentages['N']:.1f}%)")
        print(f"South: {counts['S']} ({percentages['S']:.1f}%)")
        print(f"West: {counts['W']} ({percentages['W']:.1f}%)")
        print(f"East: {counts['E']} ({percentages['E']:.1f}%)")
        print(f"North-East: {counts['NE']} ({percentages['NE']:.1f}%)")
        print(f"North-West: {counts['NW']} ({percentages['NW']:.1f}%)")
        print(f"South-East: {counts['SE']} ({percentages['SE']:.1f}%)")
        print(f"South-West: {counts['SW']} ({percentages['SW']:.1f}%)")