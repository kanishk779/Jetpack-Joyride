import numpy as np
from colorama import Fore, Back, Style
from game import *
from gameGrid import *
'''
Provides the functionality of the game screen
'''
class Screen:

    # Obtains the game object
    def __init__(self, game):
        self.__game = game
    
    

    # print the header and gameGrid
    def generateScreen(self, gameGrid):

        # first print the header
        self.__game.printHeader()
        
        # load the grid
        gameGrid.loadSmallGrid()

        # than print the grid
        gameGrid.printSmallGrid()
        

    
