import numpy as np
from colorama import Fore, Back, Style

class Screen:

    # Sets the dimension of the screen and level of game
    def __init__(self,x_dimension,y_dimension,level):
        self.x_dimension = x_dimension
        self.y_dimension = y_dimension
        self.level = level


    def generate(self):
        grid = np.array([['#' for col in range(0,self.y_dimension)]
                for row in range(0,self.x_dimension)])
        # 80 percent of the grid will be sky and 20 percent will be ground
        sky_limit = int(0.8*self.x_dimension)
        print(sky_limit)

        for i in range (0,sky_limit+1):
            print(Back.BLUE)
        for i in range (sky_limit+1,self.x_dimension+1):
            print(Back.GREEN)


    
