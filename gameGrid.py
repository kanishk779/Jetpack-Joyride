import numpy as np

class LargeGrid:
    
    def __init__(self,externalFile):
        self.__externalFile = externalFile
        self.currentRightColumn = configs.GridWidth
        self.currentLeftColumn = 0
        self.grid=[]
    
    '''
    create the grid randomly
    '''
    def createGrid(self,N):
        # Make the basic objects of the game
        coins = "$$ $$ $$ $$$$ $$ $$ $$$$ $$ $$ $$"
        horizontalBeam = "           zzzzzzzzzzz           "
        verticalBeam = "zzzzzz"
        angledBeam = "z      z      z      z      z      z"

        coins = np.array(list(coins))
        horizontalBeam = np.array(list(horizontalBeam))
        verticalBeam = np.array(list(verticalBeam))
        angledBeam = np.array(list(angledBeam))

        coins = coins.reshape(3,11)
        horizontalBeam = horizontalBeam.reshape(3,11)
        verticalBeam = verticalBeam.reshape(6,1)
        angledBeam = angledBeam.reshape(6,6)
        
        '''
        we need to make a H*W*N grid which means N repetition of H*W grid
        '''
        H = 60
        W = 180

        # create the ground and the sky
        for i in range(
        
