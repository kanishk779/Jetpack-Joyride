import numpy as np
from creature import *

'''
Provides various functionality of the game
'''
class Game:

    def __init__(self, Manda):
        self.timeRemaining = configs.gameDuration
        self.score = 0
        self.Manda = Manda

    def updateScore(self,newScore):
        self.score = newScore

    def keepTime(self):
        if self.timeRemaining == 0:
            print("Sorry, you were not able to complete the game")
            print("GAME OVER")
            quit()
        else:
            self.timeRemaining -= 1
        

     # print the header
    def printHeader(self):
    
        print("")
        print("TIME LEFT : " + str(self.timeRemaining))
        print("YOUR SCORE IS : " + str(self.score) +
              "\t\t\t\t\t\t      LIVES LEFT : " + str(self.Manda.getStrength()))
        print("")
