import time
import numpy as np
from colorama import Fore, Back, Style
from utility import *
# task is to get the user input till he presses q

clear()
print('hello')
keys = NonBlockingInput()
inp = ''
keys.nonBlockingTerm()
l = []
while inp != 'q':
    #keys.flush()
    if keys.keyboardHit():
        #keys.flush()
        inp = keys.getChar()
        inp = keypress(inp)
        if inp is None:
            pass
        else:
            l.append(inp)
keys.flush()
keys.originalTerm()
print(l)
