
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

    def __init__(self, shield_present=True, shield_active=False):
        super().__init__(configs.MandaInitialLives,
                configs.MandaId,configs.MandaXLen,configs.MandaYLen)
        
        self.shield_present = shield_present
        self.shield_active = shield_active
        
        # make the image of hero
        self.shape =  "  O  >-|-<  /\\ "
        self.shape = np.array(list(self.shape))
        self.shape = self.shape.reshape(3, 5)
        
        self.shieldShape = "  O |>-|-|  /\\|"
        self.shieldShape = np.array(list(self.shieldShape))
        self.shieldShape = self.shieldShape.reshape(3,5)

        self.bullet = 'oo'
        self.bullet = np.array(list(self.bullet))
        self.bullet = self.bullet.reshape(1,2)
        # keep the list of the locations bullets fired by Manda 
        self.bulletList = []

        # vertical acceleration and speed 
        self.acceleration = configs.gravity
        self.velocityX = 0
        self.velocityY = 0

        # dragon form is on or not. Once it is on we need to cycle 
        self.dragonMode = False
        self.dragonIndex = 0
    
    def createDragon(self):
        d1 = '_.~"~._.~"~._'
        d2 = '._.~"~._.~"~.'
        d3 = '~._.~"~._.~"~'
        d4 = '"~._.~"~._.~"'
        d5 = '~"~._.~"~._.~'
        d6 = '.~"~._.~"~._.'
        empty = '             '
        t1 = '  _p_  '
        t2 = ' /  *\\ '
        t4 = ' /  .\\ '
        t3 = '/ /^`-\''
        dragonFrames = [d1,d2,d3,d4,d5,d6]
        if self.dragonIndex%2 == 0:
            dragon =\
            empty+t1+dragonFrames[self.dragonIndex]+t2+dragonFrames[self.dragonIndex]+t3
        else:
            dragon =\
            empty+t1+dragonFrames[self.dragonIndex]+t4+dragonFrames[self.dragonIndex]+t3
        
        dragon = np.array(list(dragon))
        dragon = dragon.reshape(3,20)
        self.dragonIndex = (self.dragonIndex+1)%6
        # print(self.dragonIndex,end='')
        return dragon


    '''
    fire the bullet in the forward direction, And also keep track of it if
    the bullet hit the Viserion. Firing a bullet will add location of the bullet
    to the list.
    '''
    def fireBullet(self):
        # get the position of Manda, that will be position of bullet
        x,y = self.obj_location.getLocation()
        x += 1
        if self.dragonMode:
            y += 20
        else:
            y += 5
        # don't fire bullets if they are outside the screen
        if y>= configs.GridWidth:
            return
        loc = Location(configs.BulletXLen,configs.BulletYLen) # need to pass the size of the bullets
        loc.setLocation(x,y)
        self.bulletList.append(loc)

        # TODO print the bullet on the screen this will be done in game.py

        

    def hittingViser(self,loc,ViserionXloc):
        x,y = loc.getLocation()
        result = False
        for i in range(configs.BulletXLen):
            for j in range(configs.BulletYLen):
                if x+i>=ViserionXloc and x+i<=ViserionXloc+configs.ViserionXLen:
                    result |= y+j>= configs.GridWidth - configs.ViserionYLen
        return result


    # shift forward each of the bullet, this function will be called from the
    # game.py or the main.py It returns the points scored by hitting viserion
    def updateBulletStatus(self,ViserionPresent,ViserionXloc):
        index = []
        cnt = 0
        for loc in self.bulletList:
            x,y = loc.getLocation()
            y += 1
            loc.setLocation(x,y)
            # check if the bullet is out of the grid
            if y < configs.GridWidth:
                index.append(cnt)
            cnt += 1

        '''
        If Viser is present than find out the bullets which are hitting
        him and delete those bullets, also update the game score.
        '''
        cnt = 0
        incrementScore = 0
        if ViserionPresent:
            for loc in self.bulletList:
                if self.hittingViser(loc,ViserionXloc):
                    incrementScore += 1
                else:
                    index.append(cnt)
                cnt += 1
        index = set(index)
        temp = [self.bulletList[i] for i in index]
        self.bulletList = temp[:]
        return incrementScore

            
    '''
    There can be two ways:-
    1. We can just increase the speed of moving the background and the Manda
       remains in his same position on the grid.
    2. We actually change the position of manda on the grid my moving him one 
       column forward.
    '''

    # here we need to implement gravity as well
    # the Impulse will change the velocity in upward and gravity will try to
    # change the velocity in the downward direction . Also keep if the upper
    # right corner touches the upper wall of the grid than don't further
    # increase the velocity , it will imitate the collision with the wall
    # because the impulse provided by the user up button will counteract the 
    # collision with the wall.
    
    def move(self, keyPressed):
         
        # This function only changes the position of Manda. Grid repainting, and
        # other things will be done in game.py
        
        # now place manda on grid after updating the location of manda
        x,y = self.obj_location.getLocation()
        if keyPressed in ['a', 'A']:
            y -= 1
        elif keyPressed in ['d', 'D']:
            y += 1
        elif keyPressed in ['w', 'W']:
            #print('up pressed')
            self.velocityY += configs.Impulse
        elif keyPressed in ['b', 'B']:
            self.fireBullet()
        
        # the shield activation will be handled in game.py
        x += self.velocityY
        if y>= configs.GridWidth-configs.MandaYLen:
            y -= 1
        if y<0 :
            y += 1
        if x >= configs.GridHeight - configs.MandaXLen:
            x = configs.GridHeight - configs.MandaXLen
            
        if x<=0:
            x = 0
        self.obj_location.setLocation(x,y)

'''
Boss enemy of the game . Changes position according to position of Mandalorian
and throws ice balls at him.
'''
class Viserion(Person):

    def __init__(self):
        super().__init__(configs.ViserionInitialStrength,
                configs.ViserionId,configs.ViserionXLen,configs.ViserionYLen)
        
        # make the image of Viserion
        self.shape =  "VISER  O  >-|-<  /\\ "
        self.shape = np.array(list(self.shape))
        self.shape = self.shape.reshape(4, 5)
        self.ball = "  -   / \\ ooooo \\ /   -  "
        self.ball = np.array(list(self.ball))
        self.ball = self.ball.reshape(5,5)

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

        if not self.present:
            return 
        x,y = self.obj_location.getLocation()
        y -= 5
        

        # now return co-ordinates of the IceBall to be painted on the grid
        return x,y


