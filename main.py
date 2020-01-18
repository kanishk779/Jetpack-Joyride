from colorama import Fore, Back, Style
from game import *
from creature import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    myGame = Game(manda)
    while True:
        myGame.gameLoop()
        time.sleep(.1)

