import numpy as np
import random
import configs
from colorama import Fore, Back, Style

class LargeGrid:
    
    def __init__(self):
        self.currentRightColumn = configs.GridWidth
        self.currentLeftColumn = 0
        self.grid = []
        self.numericGrid = []
        # stores the location of magnet in grid
        self.startMagnetColumn= -1
        self.magnetX = -1
        self.magnetY = -1
    
    '''
    create the grid randomly
    '''
    def createGrid(self,N):

        # Make the basic objects of the game
        coins = "$$ $$ $$ $$$$ $$ $$ $$$$ $$ $$ $$"
        horizontalBeam = "           zzzzzzzzzzz           "
        verticalBeam = "zzzzzz"
        mainAngledBeam = "z      z      z      z      z      z"
        offAngledBeam = "     z    z    z    z    z    z     "
        bonus = "BBBB"
        shield = "SSSS"
        dragon = "DDDD"
        magnet = "MMMM"

        coins = np.array(list(coins))
        horizontalBeam = np.array(list(horizontalBeam))
        verticalBeam = np.array(list(verticalBeam))
        mainAngledBeam = np.array(list(mainAngledBeam))
        offAngledBeam = np.array(list(offAngledBeam))
        bonus = np.array(list(bonus))
        # shield is not going to appear as an obstacle in the game but it will
        # automatically fill in after every 60 seconds and the manda will be
        # able to use it once it is available.

        dragon = np.array(list(dragon))
        magnet = np.array(list(dragon))

        coins = coins.reshape(3,11)
        horizontalBeam = horizontalBeam.reshape(3,11)
        verticalBeam = verticalBeam.reshape(6,1)
        mainAngledBeam = mainAngledBeam.reshape(6,6)
        offAngledBeam = offAngledBeam.reshape(6,6)
        bonus = bonus.reshape(2,2)
        dragon = dragon.reshape(2,2)
        magnet = magnet.reshape(2,2)


        obstaclesSizes = \
        [[3,11],[3,11],[6,1],[6,6],[6,6],[2,2],[2,2],[2,2]]
        obstacles = [coins, horizontalBeam, verticalBeam, mainAngledBeam,
                offAngledBeam, bonus,dragon,magnet]
        
        '''
        we need to make a H*W*N grid which means N repetition of H*W grid
        '''
        H = configs.GridHeight
        W = configs.GridWidth
        
        self.grid = ['0' for i in range(H*W*N)]
        self.grid = np.array(self.grid)
        self.grid = self.grid.reshape(H,W*N)

        self.numericGrid = [0  for i in range(H*W*N)]
        self.numericGrid = np.array(self.numericGrid)
        self.numericGrid = self.numericGrid.reshape(H,W*N)


        # create the ground
        for i in range(W*N):
            self.grid[H-1][i] = self.grid[H-2][i] = 'X'
            self.numericGrid[H-1][i] = self.numericGrid[H-2][i] =\
            configs.groundId 

        # create the sky
        for i in range(W*N):
            self.grid[0][i] =  self.grid[1][i] = 'X'
            self.numericGrid[0] = self.numericGrid[1] = \
            configs.skyId
        
        obstacleInterval = 40
        
        # After every 40 character a obstacle/coins will appear 
        loops = int((W*N)/obstacleInterval)
        print("loops " + str(loops))
        # randomly generate the starting location of the obstacle/coins
        currentStartCol = 0
        dragonFound = False
        magnetFound = False

        for loop in range(loops):
            x_start = random.randrange(5 ,28, 1)
            y_start = random.randrange(5, 12, 1)
            obj_type = random.randrange(0,configs.NumberOfObstacles,1)
            if obj_type+1 == configs.dragonId:
                if dragonFound:
                    obj_type = configs.coinId
                else:
                    dragonFound = True
            if obj_type+1 == configs.magnetId:
                if magnetFound:
                    obj_type = configs.coinId
                else:
                    magnetFound = True
                    self.startMagnetColumn = currentStartCol+y_start

            if obj_type+1 == configs.iceBallId:
                currentStartCol += obstacleInterval
                continue

            for i in range(obstaclesSizes[obj_type][0]):
                for j in range(obstaclesSizes[obj_type][1]):
                    self.grid[x_start+i][currentStartCol+ y_start+j] = obstacles[obj_type][i][j]
                    char = obstacles[obj_type][i][j] 
                    if char in ['z','$','M','D','B']:
                        self.numericGrid[x_start+i][currentStartCol+y_start+j]\
                         =  obj_type+1

            currentStartCol += obstacleInterval

'''
This will be the class which will interface with the rest of the game.
It will also manage the large Grid.
'''
class SmallGrid:
    
    def __init__(self):
        self.largeGrid = LargeGrid()
        self.grid = [[0 for j in range(configs.GridWidth)] for i in\
            range(configs.GridHeight)]
        self.numericGrid = [[0 for j in range(configs.GridWidth)] for i in \
            range(configs.GridHeight)]
        self.N = 0

    # creates the large grid. This needs to be called only once.
    def initialiseLargeGrid(self,N):
        self.largeGrid.createGrid(N)
        self.N = N

    # moves the grid leftwards
    def progressGame(self, step):
        W = configs.GridWidth

        self.largeGrid.currentLeftColumn = \
            (self.largeGrid.currentLeftColumn+step)%(W*self.N)

        self.largeGrid.currentRightColumn = \
            (self.largeGrid.currentRightColumn+step)%(W*self.N)
    # moves the grid rightwards
    def regressGame(self, step):
        W = configs.GridWidth

        self.largeGrid.currentLeftColumn = \
            (self.largeGrid.currentLeftColumn -step + W*self.N)%(W*self.N)

        self.largeGrid.currentRightColumn = \
            (self.largeGrid.currentRightColumn -step + W*self.N)%(W*self.N)

    def loadSmallGrid(self):
        
        for i in range(configs.GridHeight):
            for j in range(self.largeGrid.currentLeftColumn,self.largeGrid.currentRightColumn):
                self.grid[i][j-self.largeGrid.currentLeftColumn] = \
                self.largeGrid.grid[i][j]

                self.numericGrid[i][j - self.largeGrid.currentLeftColumn] = \
                self.largeGrid.numericGrid[i][j]

    # Renders the small screen using colors(colorama)
    def printSmallGrid(self):
        
        skyColor = Back.BLUE
        coinsColor = Back.CYAN
        groundColor = Back.GREEN
        beamColor1 = Back.YELLOW
        beamColor2 = Back.RED
        bonusColor = Back.MAGENTA
        dragonColor = Back.GREEN
        magnetColor = Back.YELLOW
        iceBallColor = Back.WHITE

        for i in range(configs.GridHeight):
            for j in range(configs.GridWidth):
                
                char = ''

                if self.numericGrid[i][j] == configs.coinId:
                    char = coinsColor + Fore.BLACK + '$'                
                elif self.numericGrid[i][j] in [configs.horizontalBeamId,
                        configs.verticalBeamId]:
                    char =  beamColor1 + Fore.RED + 'z'
                elif self.numericGrid[i][j] in\
                [configs.mainAngledBeamId, configs.offAngledBeamId]:
                    char = beamColor2 + Fore.YELLOW + 'z'
                elif self.numericGrid[i][j] == configs.groundId:
                    char = groundColor + Fore.RED + 'X'
                elif self.numericGrid[i][j] == configs.skyId:
                    char = skyColor + Fore.RED + 'X'
                elif self.numericGrid[i][j] == configs.bonusId:
                    char = bonusColor + Fore.GREEN + 'B'
                elif self.numericGrid[i][j] == configs.magnetId:
                    char = magnetColor + Fore.BLACK + 'M'
                elif self.numericGrid[i][j] == configs.dragonId:
                    char = dragonColor + Fore.MAGENTA + 'D'
                elif self.numericGrid[i][j] == configs.iceBallId:
                    char = iceBallColor + Fore.BLACK + self.grid[i][j]
                else:
                    char = skyColor + ' '
                
                print(char,end='')

            print(Style.RESET_ALL+'')
        

