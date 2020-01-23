import numpy as np
import random
import configs
from colorama import Fore, Back, Style


class LargeGrid:
    def __init__(self):
        self.currentRightColumn = configs.GRIDWIDTH
        self.currentLeftColumn = 0
        self.grid = []
        self.numericGrid = []
        # stores the location of magnet in grid
        self.startMagnetColumn = -1
        self.magnetX = -1
        self.magnetY = -1

    '''
    create the grid randomly
    '''

    def createGrid(self, N):

        # Make the basic objects of the game
        coins = "$$ $$ $$ $$$$ $$ $$ $$$$ $$ $$ $$"
        horizontalBeam = "           zzzzzzzzzzz           "
        verticalBeam = "zzzzzz"
        mainAngledBeam = "z      z      z      z      z      z"
        offAngledBeam = "     z    z    z    z    z    z     "
        dragon = "DDDD"
        magnet = "MMMM"

        coins = np.array(list(coins))
        horizontalBeam = np.array(list(horizontalBeam))
        verticalBeam = np.array(list(verticalBeam))
        mainAngledBeam = np.array(list(mainAngledBeam))
        offAngledBeam = np.array(list(offAngledBeam))
        dragon = np.array(list(dragon))
        magnet = np.array(list(dragon))

        coins = coins.reshape(3, 11)
        horizontalBeam = horizontalBeam.reshape(3, 11)
        verticalBeam = verticalBeam.reshape(6, 1)
        mainAngledBeam = mainAngledBeam.reshape(6, 6)
        offAngledBeam = offAngledBeam.reshape(6, 6)
        dragon = dragon.reshape(2, 2)
        magnet = magnet.reshape(2, 2)


        obstaclesSizes = \
        [[3,11],[3,11],[6,1],[6,6],[6,6],[2,2],[2,2]]
        obstacles = [
            coins, horizontalBeam, verticalBeam, mainAngledBeam, offAngledBeam,
            dragon, magnet
        ]
        '''
        we need to make a H*W*N grid which means N repetition of H*W grid
        '''
        H = configs.GRIDHEIGHT
        W = configs.GRIDWIDTH

        self.grid = [' ' for i in range(H * W * N)]
        self.grid = np.array(self.grid)
        self.grid = self.grid.reshape(H, W * N)

        self.numericGrid = [0 for i in range(H * W * N)]
        self.numericGrid = np.array(self.numericGrid)
        self.numericGrid = self.numericGrid.reshape(H, W * N)

        # create the ground
        for i in range(W * N):
            self.grid[H - 1][i] = self.grid[H - 2][i] = 'X'
            self.numericGrid[H-1][i] = self.numericGrid[H-2][i] =\
            configs.GROUNDID

        # create the sky
        for i in range(W * N):
            self.grid[0][i] = self.grid[1][i] = 'X'
            self.numericGrid[0] = self.numericGrid[1] = \
            configs.SKYID

        obstacleInterval = 30

        # After every 30 character a obstacle/coins will appear
        loops = int((W * N) / obstacleInterval)
        # randomly generate the starting location of the obstacle/coins
        currentStartCol = 0
        dragonFound = False
        magnetFound = False

        for loop in range(loops):
            if loop == 0:
                currentStartCol += obstacleInterval
                continue
            x_start1 = random.randrange(5, 12, 1)
            y_start1 = random.randrange(5, 8, 1)
            x_start2 = random.randrange(20, 28, 1)
            y_start2 = random.randrange(9, 12, 1)
            obj_type1 = random.randrange(0, configs.NUMBEROFOBSTACLES, 1)
            obj_type2 = random.randrange(0, configs.NUMBEROFOBSTACLES, 1)

            if obj_type1 + 1 == configs.DRAGONID:
                if dragonFound:
                    obj_type1 = configs.COINID
                else:
                    dragonFound = True
            if obj_type1 + 1 == configs.MAGNETID:
                if magnetFound:
                    obj_type1 = configs.COINID
                else:
                    magnetFound = True
                    self.startMagnetColumn = currentStartCol + y_start1
            if obj_type2 + 1 == configs.DRAGONID:
                if dragonFound:
                    obj_type2 = configs.COINID
                else:
                    dragonFound = True
            if obj_type2 + 1 == configs.MAGNETID:
                if magnetFound:
                    obj_type2 = configs.COINID
                else:
                    magnetFound = True
                    self.startMagnetColumn = currentStartCol + y_start2

            for i in range(obstaclesSizes[obj_type1][0]):
                for j in range(obstaclesSizes[obj_type1][1]):
                    char = obstacles[obj_type1][i][j]
                    self.grid[x_start1 + i][currentStartCol + y_start1 +
                                            j] = char
                    if char in ['z', '$', 'M', 'D']:
                        self.numericGrid[x_start1+i][currentStartCol+y_start1+j]\
                         =  obj_type1+1
            for i in range(obstaclesSizes[obj_type2][0]):
                for j in range(obstaclesSizes[obj_type2][1]):
                    char = obstacles[obj_type2][i][j]
                    self.grid[x_start2 + i][currentStartCol + y_start2 +
                                            j] = char
                    if char in ['z', '$', 'M', 'D']:
                        self.numericGrid[x_start2+i][currentStartCol+y_start2+j]\
                         =  obj_type2+1

            currentStartCol += obstacleInterval


'''
This will be the class which will interface with the rest of the game.
It will also manage the large Grid.
'''


class SmallGrid:
    def __init__(self):
        self.largeGrid = LargeGrid()
        self.grid = [['0' for j in range(configs.GRIDWIDTH)] for i in\
            range(configs.GRIDHEIGHT)]
        self.numericGrid = [[0 for j in range(configs.GRIDWIDTH)] for i in \
            range(configs.GRIDHEIGHT)]
        self.grid = np.array(list(self.grid))
        self.grid = self.grid.reshape(configs.GRIDHEIGHT, configs.GRIDWIDTH)
        self.numericGrid = np.array(list(self.numericGrid))
        self.numericGrid =\
        self.numericGrid.reshape(configs.GRIDHEIGHT,configs.GRIDWIDTH)
        self.N = 0

    # creates the large grid. This needs to be called only once.
    def initialiseLargeGrid(self, N):
        self.largeGrid.createGrid(N)
        self.N = N

    # moves the grid leftwards
    def progressGame(self, step):
        W = configs.GRIDWIDTH

        self.largeGrid.currentLeftColumn = \
            (self.largeGrid.currentLeftColumn+step)%(W*self.N)

        self.largeGrid.currentRightColumn = \
            (self.largeGrid.currentRightColumn+step)%(W*self.N)

    # moves the grid rightwards
    def regressGame(self, step):
        W = configs.GRIDWIDTH

        self.largeGrid.currentLeftColumn = \
            (self.largeGrid.currentLeftColumn -step + W*self.N)%(W*self.N)

        self.largeGrid.currentRightColumn = \
            (self.largeGrid.currentRightColumn -step + W*self.N)%(W*self.N)

    def loadSmallGrid(self):
        l = self.largeGrid.currentLeftColumn
        r = self.largeGrid.currentRightColumn
        W = configs.GRIDWIDTH
        '''
        There is a flaw in the game the enemy dragon fires the ice Ball they get
        repeated when the large grid hits end and start repeating from the
        beginning, so we have more ice balls on the screen then there should be
        '''
        iceBall = ['o', '\\', '/', '-']
        assert l >= 0 and l < W * self.N, "l correct"
        assert r >= 0 and r < W * self.N, "r correct"
        for i in range(configs.GRIDHEIGHT):
            if r > l:
                for j in range(self.largeGrid.currentLeftColumn,
                               self.largeGrid.currentRightColumn):
                    self.grid[i][j - l] = self.largeGrid.grid[i][j]
                    self.numericGrid[i][j -
                                        l] = self.largeGrid.numericGrid[i][j]
            else:
                cnt = 0
                for j in range(l, W * self.N):
                    cnt += 1
                    self.grid[i][j - l] = self.largeGrid.grid[i][j]
                    self.numericGrid[i][j -
                                        l] = self.largeGrid.numericGrid[i][j]
                for j in range(r):
                    self.grid[i][cnt + j] = self.largeGrid.grid[i][j]
                    self.numericGrid[i][cnt +
                                        j] = self.largeGrid.numericGrid[i][j]

    # Renders the small screen using colors(colorama)
    def printSmallGrid(self):

        coinsColor = Back.CYAN
        groundColor = Back.GREEN
        beamColor1 = Back.YELLOW
        beamColor2 = Back.RED
        bonusColor = Back.MAGENTA
        dragonColor = Back.GREEN
        magnetColor = Back.YELLOW

        for i in range(configs.GRIDHEIGHT):
            for j in range(configs.GRIDWIDTH):

                char = ''

                if self.numericGrid[i][j] == configs.COINID:
                    char = coinsColor + Fore.BLACK + '$'
                elif self.numericGrid[i][j] in [
                        configs.HORIZONTALBEAMID, configs.VERTICALBEAMID
                ]:
                    char = beamColor1 + Fore.RED + 'z'
                elif self.numericGrid[i][j] in\
                [configs.MAINANGLEDBEAMID, configs.OFFANGLEDBEAMID]:
                    char = beamColor2 + Fore.YELLOW + 'z'
                elif self.numericGrid[i][j] == configs.GROUNDID:
                    char = groundColor + Fore.RED + 'X'
                elif self.numericGrid[i][j] == configs.SKYID:
                    char = configs.BACKGROUNDCOLOR + Fore.RED + 'X'
                elif self.numericGrid[i][j] == configs.MAGNETID:
                    char = magnetColor + Fore.BLACK + 'M'
                elif self.numericGrid[i][j] == configs.DRAGONID:
                    char = dragonColor + Fore.MAGENTA + 'D'
                elif self.numericGrid[i][j] == configs.ICEBALLID:
                    char = configs.BACKGROUNDCOLOR + configs.CHARACTERFORECOLOR + self.grid[i][j]
                else:
                    char = configs.BACKGROUNDCOLOR + ' '

                print(char, end='')

            print(Style.RESET_ALL + '')
