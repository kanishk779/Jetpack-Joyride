import time
import numpy as np
from colorama import Fore, Back, Style

i = 0
while True:
    i+=1
    
    print('\033[2;10H', end='')
    if i%2 == 0:
        print(Back.GREEN + Fore.BLACK + 'X')
    else:
        print(Back.RED + Fore.BLACK + 'Y')
    time.sleep(1)
