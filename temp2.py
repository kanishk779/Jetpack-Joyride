import collections
import numpy as np

de = collections.deque()
de.append(4)

print(de)

de.appendleft(7)
de.append(6)

print(de)
de.popleft()
print(de)
