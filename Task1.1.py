# Jayden Holdsworth
# Task 1.1
# Algorithm to simulate a random walk on a 2D grid with only cardinal directions, uses random.unfiorm to determine the direction of the next step.

import numpy as np
import matplotlib.pyplot as plt
import time

# !MAIN (this should be its own function __main__)
start_time = time.time()

grid_size = 100
total_steps = 10000 
milestones = [100, 500, 1000, 5000, 10000] 

grid = np.zeros((grid_size, grid_size))

x, y = grid_size // 2, grid_size // 2
path = [(x, y)]
grid[x, y] = 1

milestone_counts = {steps: {'N': 0, 'S': 0, 'W': 0, 'E': 0} for steps in milestones}
N = S = W = E = 0

for step in range(total_steps):
   rand_x = np.random.uniform(0, 1) > 0.5
   rand_y = np.random.uniform(0, 1) > 0.5

   if rand_x and rand_y:
       x = max(x - 1, 0)
       N += 1
   elif rand_x and not rand_y:
       x = min(x + 1, grid_size - 1)
       S += 1
   elif not rand_x and rand_y:
       y = max(y - 1, 0)
       W += 1
   else:
       y = min(y + 1, grid_size - 1)
       E += 1

   path.append((x, y))
   grid[x, y] = 1

   if (step + 1) in milestones:
       milestone_counts[step + 1]['N'] = N
       milestone_counts[step + 1]['S'] = S
       milestone_counts[step + 1]['W'] = W
       milestone_counts[step + 1]['E'] = E


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
    plt.ylim(0, 50)
    
    for j, v in enumerate(percentages.values()):
        plt.text(j, v + 0.5, f'{v:.1f}%', ha='center')

plt.tight_layout(pad=3.0)
plt.show()

# *simulation time is only here because i was testing efficacy of different rng methods
end_time = time.time()
print(f"\nSimulation Time: {end_time - start_time:.6f} seconds")

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