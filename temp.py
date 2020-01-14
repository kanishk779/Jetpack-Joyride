import os
os.system('clear')
import numpy as np
grid = [['$' for j in range(5)] for i in range(5)]
for i in range(5):
    for j in range(5):
        print(grid[i][j],end = '')
    print()
print('\033[1;0H')
grid = [[i for j in range(5)] for i in range(5)]
for i in range(5):
    for j in range(5):
        print(grid[i][j],end='')
    print()

