from colorama import Fore, Back, Style
from screen import Screen
from game import *
from gameGrid import *
from creature import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    myGame = Game(manda)
    myGameGrid = SmallGrid()
    my_screen = Screen(myGame)
    myGameGrid.initialiseLargeGrid(4)
    myGameGrid.loadSmallGrid()
    i = 100
    step = 1
    while i>0:
        i=i-1
        myGameGrid.progressGame(step)
        print(myGameGrid.largeGrid.currentLeftColumn)
        my_screen.generateScreen(myGameGrid)
        time.sleep(.01)

