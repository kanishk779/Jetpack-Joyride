from colorama import Fore, Back, Style
from game import *
from creature import *
from utility import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    period = 10
    i = 0
    clear()
    keys = NonBlockingInput()
    keys.nonBlockingTerm()
    myGame = Game(manda,keys)
    while True:
        i += 1
        if i == period:
            myGame.keepTime()
            i = 0
        if keys.keyboardHit():
            #keys.flush()
            inp = keys.getChar()
            inp = keypress(inp)
            if inp is None:
                pass
            else:
                manda.move(inp)
        myGame.gameLoop()
        time.sleep(.01)

