# Jayden Holdsworth
# Task 1.2
# Algorithm to simulate a random walk on a 2D grid with both cardinal and diagonal directions, uses random.unfiorm to determine the direction of the next step.

import numpy as np
import matplotlib.pyplot as plt

# !MAIN (this should be its own function __main__)
grid_size = 100
total_steps = 10000
milestones = [100, 500, 1000, 5000, 10000]

grid = np.zeros((grid_size, grid_size))

x, y = grid_size // 2, grid_size // 2
path = [(x, y)]
grid[x, y] = 1

milestone_counts = {steps: {'N': 0, 'S': 0, 'W': 0, 'E': 0, 
                         'NE': 0, 'NW': 0, 'SE': 0, 'SW': 0} 
                  for steps in milestones}
N = S = W = E = NW = NE = SW = SE = 0

for step in range(total_steps):
   movement_type = np.random.uniform(0, 1) > 0.5
   
   rand_x = np.random.uniform(0, 1) > 0.5
   rand_y = np.random.uniform(0, 1) > 0.5
   
   # *cardinal 
   if movement_type:
       if rand_x and rand_y:
           x = min(x + 1, grid_size - 1)
           y = max(y - 1, 0)
           NE += 1
       elif rand_x:
           x = min(x + 1, grid_size - 1)
           y = min(y + 1, grid_size - 1)
           SE += 1
       elif rand_y:
           x = max(x - 1, 0) 
           y = max(y - 1, 0)
           NW += 1
       else:
           x = max(x - 1, 0)
           y = min(y + 1, grid_size - 1)
           SW += 1
           
   # *diagonal
   else:
       if rand_x and rand_y:
           y = max(y - 1, 0)
           N += 1
       elif rand_x:
           y = min(y + 1, grid_size - 1)
           S += 1
       elif rand_y:
           x = max(x - 1, 0)
           W += 1
       else:
           x = min(x + 1, grid_size - 1)
           E += 1

   path.append((x, y))
   grid[x, y] = 1
   
   if (step + 1) in milestones:
       milestone_counts[step + 1]['N'] = N
       milestone_counts[step + 1]['S'] = S
       milestone_counts[step + 1]['W'] = W
       milestone_counts[step + 1]['E'] = E
       milestone_counts[step + 1]['NE'] = NE
       milestone_counts[step + 1]['NW'] = NW
       milestone_counts[step + 1]['SE'] = SE
       milestone_counts[step + 1]['SW'] = SW

fig = plt.figure(figsize=(10, 15))

plt.subplot(3, 2, 1)
plt.imshow(grid, cmap="binary", interpolation="nearest")
plt.title("Final Path")

for plot_num, milestone in enumerate(milestones):
    plt.subplot(3, 2, plot_num + 2)
    counts = milestone_counts[milestone]
    total = sum(counts.values())
    
    percentages = {k: (v/total)*100 for k, v in counts.items()}
    
    plt.bar(percentages.keys(), percentages.values(), width=0.8)
    plt.title(f'After {milestone} steps')
    plt.ylabel('Percentage')
    plt.ylim(0, 25)
    plt.xticks(rotation=45)
    
    for j, v in enumerate(percentages.values()):
        plt.text(j, v + 0.5, f'{v:.1f}%', ha='center')

plt.tight_layout(pad=3.0)
plt.show()

print("\nRaw counts at each milestone:")
for milestone in milestones:
   counts = milestone_counts[milestone]
   total = sum(counts.values())
   percentages = {k: (v/total)*100 for k, v in counts.items()}
   print(f"\nAfter {milestone} steps:")
   print(f"North: {counts['N']} ({percentages['N']:.1f}%)")
   print(f"South: {counts['S']} ({percentages['S']:.1f}%)")
   print(f"West: {counts['W']} ({percentages['W']:.1f}%)")
   print(f"East: {counts['E']} ({percentages['E']:.1f}%)")
   print(f"North-East: {counts['NE']} ({percentages['NE']:.1f}%)")
   print(f"North-West: {counts['NW']} ({percentages['NW']:.1f}%)")
   print(f"South-East: {counts['SE']} ({percentages['SE']:.1f}%)")
   print(f"South-West: {counts['SW']} ({percentages['SW']:.1f}%)")