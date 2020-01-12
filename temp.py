import numpy as np
arr = [[i for j in range(4)] for i in range(3)]
print(arr[1][3])
arr = np.array(arr)
print(arr)
print(arr[1][3])
