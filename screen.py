import numpy as np
from colorama import Fore, Back, Style
from game import *
from gameGrid import *
'''
Provides the functionality of the game screen
'''


class Screen:

    # Obtains the game object
    def __init__(self):
        pass

    # print the header and gameGrid
    def generateScreen(self, gameGrid):

        # first print the header before calling this function

        # load the grid
        gameGrid.loadSmallGrid()

        # than print the grid
        gameGrid.printSmallGrid()
