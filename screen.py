import numpy as np
from colorama import Fore, Back, Style
import game
import gameGrid
'''
Provides the functionality of the game screen
'''
class Screen:

    # Obtains the game object
    def __init__(self, game):
        self.game = game
    
    

    # print the header and gameGrid
    def generateScreen(self, gameGrid):

        # first print the header
        self.game.printHeader()

        # than print the grid
        gameGrid.printSmallGrid()
        

    
