import numpy as np
from colorama import Fore, Back, Style
import Game
'''
Provides the functionality of the game screen
'''
class Screen:

    # Obtains the game object
    def __init__(self,game):
        self.game = game
    
    # print the header
    def printHeader(self):
    
        print("")
        print("TIME LEFT : " + str(game.))
        print("YOUR SCORE IS : " + str(Manage.score) +
              "\t\t\t\t\t\t      LIVES LEFT : " + str(Manage.lives))
        print("")


    # print the header and gameGrid
    def generateScreen(self, gameGrid):
        

    
