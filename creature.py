import numpy as np
import collections
import configs
from godObject import *
'''
Class which describes all the persons in the game.
'''
class Person(GodObject):
    # strength means lives for Mandalorian
    def __init__(self, strength,identifier,x_len,y_len):
        obj_loc = Location(x_len,y_len)
        super().__init__(identifier,obj_loc)
        self.__strength = strength

    def getStrength(self):
        return self.__strength

    def setStrength(self, strength):
        self.__strength = strength

'''
Hero of the game
'''
class Mandalorian(Person):

    def __init__(self, shield_present=False, shield_active=False):
        super().__init__(configs.MandaInitialLives,
                configs.MandaId,configs.MandaXLen,configs.MandaYLen)
        
        self.shield_present = shield_present
        self.shield_active = shield_active
        
        # make the image of hero
        self.shape =  "  O  >-|-<  /\\ "
        self.shape = np.array(list(self.shape))
        self.shape = self.shape.reshape(3, 5)
        
        self.bullet = 'o'
        # keep the list of the locations bullets fired by Manda 
        self.bulletList = []

    
    '''
    fire the bullet in the forward direction, And also keep track of it if
    the bullet hit the Viserion. Firing a bullet will add location of the bullet
    to the list.
    '''
    def fireBullet(self):
        pass
    
    def hittingViser(self,loc):
        return if loc.y_loc >= configs.GridWidth - configs.ViserionYLen and \
                        loc.x_loc >= configs.GridHeight - configs.ViserionXLen:

    # shift forward each of the bullet this function will be called from the
    # game.py or the main.py
    def updateBulletStatus(self,ViserionPresent):
        bulletsToBeDeleted = []
        index = 0
        for loc in self.bulletList:
            loc.y_loc += 1
            # check if the bullet is out of the grid
            if loc.y_loc >= configs.GridWidth:
                bulletsToBeDeleted.append(index)
            index += 1
        for i in bulletsToBeDeleted:
            del self.bulletList[i]

        '''
        If Viser is present than find out the bullets which are hitting
        him and delete those bullets, also update the game score.
        '''
        if ViserionPresent:
            index = 0
            for loc in self.bulletList:
                if hittingViser(loc):
                    bulletsToBeDeleted.append(index)



            
    '''
    There can be two ways:-
    1. We can just increase the speed of moving the background and the Manda
       remains in his same position on the grid.
    2. We actually change the position of manda on the grid my moving him one 
       column forward.
    '''
    def moveForward(self):

        # now move manda according to the one of the above mentioned ways

    def moveBackward(self):
        pass

    def jump(self):
        pass
    
    # checks if there is any collision and accordingly
    def move(self, keyPressed):
         
        # first repaint the grid by bringing the cursor to the starting.
        print('')  # escape sequence to bring the cursor to the starting

        
'''
Boss enemy of the game
'''
class Viserion(Person):

    def __init__(self):
        super().__init__(configs.ViserionInitialStrength,
                configs.ViserionId,configs.ViserionXLen,configs.ViserionYLen)
        
        # make the image of Viserion
        self.shape =  "VISER  O  >-|-<  /\\ "
        self.shape = np.array(list(self.shape))
        self.shape = self.shape.reshape(4, 5)
        self.ball = "  -   / \ ooooo \ /   -  "
        self.ball = np.array(list(ball))
        self.ball = ball.reshape(5,5)

        # Tells if viser is present on the game screen
        self.present = False
    
   
   '''
    There can be two ways of doing this:-
    1. The ball move with the same speed as the background moves. Which means
       the ball becomes a part of the background . This one is easy to code.
    2. The ball moves with 2X speed as the background moves. Here the ball needs 
       to be repainted and also the previous version of the ball needs to
       cleared , which is tough to do. For one cycle you will need to move the
       ball, but for the other just stick the ball to the screen and screen will move the
       ball. So for the cycle the ball will move you will need to store the
       matrix of the background before moving it, and than you will restore that 
       piece of the background after you have moved the ball to next location.
       
    '''
    def fireIceBalls(self):
        # trying the first method

        

