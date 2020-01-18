from colorama import Fore, Back, Style
from game import *
from creature import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    myGame = Game(manda)
    period = 10
    i = 0
    while True:
        i+=1
        if i == period:
            myGame.keepTime()
            i = 0
        myGame.gameLoop()
        time.sleep(.1)

