# Jayden Holdsworth
# Task 2.1
# Algorithm to simulate Gompertz tumour growth using Euler's method.

import numpy as np
import matplotlib.pyplot as plt

# *O(n) time and space complexity
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
h = 0.001   # step size

# test different final times until steady state is reached
t_max = 1200
while True:
    t = np.arange(0, t_max+h, h)
    N = gompertz_growth(t_max, N0, k, M, h)
    
    if check_steady_state(N):
        print(f"Steady state reached at approximately t={t_max}")
        break
    t_max += 100

# test different M values
M_high = 10**14
M_low = 10**12

N_high = gompertz_growth(t_max, N0, k, M_high, h)
N_low = gompertz_growth(t_max, N0, k, M_low, h)

plt.figure(figsize=(12, 8))
plt.plot(t, N, label=f'M = {M:.0e}')
plt.plot(t, N_high, label=f'M = {M_high:.0e}')
plt.plot(t, N_low, label=f'M = {M_low:.0e}')
plt.xlabel('Time')
plt.ylabel('Number of Cells')
plt.title('Gompertz Tumour Growth Model')
plt.grid(True)
plt.legend()
plt.show()

print(f"\nSteady state analysis for different M values:")
print(f"M = {M_low:.0e}: {check_steady_state(N_low)}")
print(f"M = {M:.0e}: {check_steady_state(N)}")
print(f"M = {M_high:.0e}: {check_steady_state(N_high)}")