import time
import numpy as np

d1 = '_.~"~._.~"~._'
d2 = '._.~"~._.~"~.'
d3 = '~._.~"~._.~"~'
d4 = '"~._.~"~._.~"'
d5 = '~"~._.~"~._.~'
d6 = '.~"~._.~"~._.'
em = '             '
t1 = '  _p_  '
t2 = ' /  *\\ '
t4 = ' /  .\\ '
t3 = '/ /^`-\''
l = [d1,d2,d3,d4,d5,d6]
ind = 0
while True:
    time.sleep(0.1)
    if ind%2 == 0:
        d = em + t1 + l[ind] + t2 + l[ind] + t3
    else:
        d = em + t1 + l[ind] + t4 + l[ind] + t3
    d = np.array(list(d))
    d = d.reshape(3,20)
    for i in range(3):
        for j in range(20):
            print(d[i][j], end='')
        print()
    
    ind = (ind+1)%6
    print('\033[0;0H')

