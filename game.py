import math
import numpy as np
from creature import *
from gameGrid import *
from screen import *
'''
Provides various functionality of the game
1. Render the screen every time and update various things
2. Print Manda by updating his velocity and adding the velocity to the location
   to get new location.
3. Iterate through the list of the Bullets and update their status and than
   print the bullets
4. Iterate through the list of the Fire Balls emitted by the Boss Enemy update
   their location and also print them
5. Print Viserion
'''
class Game:

    def __init__(self, Manda):
        self.timeRemaining = int(configs.gameDuration)
        self.score = 0
        self.manda = Manda
        self.manda.obj_location.setLocation(configs.GridHeight-configs.MandaXLen,10)
        self.gameGrid = SmallGrid()
        self.screen = Screen()
        self.gameGrid.initialiseLargeGrid(8)
        self.Viserion = Viserion()


    def keepTime(self):
        if self.timeRemaining == 0:
            print("Sorry, you were not able to complete the game")
            print("GAME OVER")
            quit()
        else:
            self.timeRemaining -= 1
        

    # print the header
    def printHeader(self):
        
        if self.manda.shield_active:
            shieldStatus = "YES"
        else:
            shieldStatus = "NO"
        print("TIME LEFT : {a:5d} \t\t\t\t\t\t      SHIELD ACTIVE : {p}".format(a = self.timeRemaining,p = shieldStatus))
        print("YOUR SCORE IS : " + str(self.score) +
              "\t\t\t\t\t\t      LIVES LEFT : " + str(self.manda.getStrength()))

    
    # check if there is any collision, x,y are location of manda    
    def checkCollision(self):
        beamSeen = False
        dragonSeen = False
        bonusSeen = False
        x,y = self.manda.obj_location.getLocation()
        stCol = self.gameGrid.largeGrid.currentLeftColumn

        for i in range(configs.MandaXLen):
            for j in range(configs.MandaYLen):
                
                if self.gameGrid.grid[x+i][y+j] == '$':
                    # change actual self.gameGrid and numeric self.gameGrid and ++ score
                    self.gameGrid.largeGrid.grid[x+i][stCol+y+j] = ' '
                    self.gameGrid.largeGrid.numeric[x+i][stCol+y+j] = 0
                    self.score += 1

                if self.gameGrid.grid[x+i][y+j] == 'z':
                    if self.manda.shield_active: 
                        # if shield is active than nothing happens to manda
                        continue
                    if not beamSeen:
                        beamseen = True
                        # decrease live and step ahead of that beam so that in
                        # next iteration you do not encounter the beam. Move the
                        # background , do not move Manda
    
                        
                        if self.manda.dragonMode:
                            self.gameGrid.progressGame(configs.DragonYLen+12)
                            self.manda.dragonMode = False
                        else:
                            self.gameGrid.progressGame(configs.MandaYLen+12) # progress by 17 column
                            lives = self.manda.getStrength()
                            lives -= 1
                            self.manda.setStrength(lives)

                if self.gameGrid.grid[x+i][y+j] == 'B':
                    if not bonusSeen:
                        bonusSeen = True
                        # speed up the game for 5 seconds keep a check on time
                        # so that we can stop it after 5 seconds, step ahead of
                        # bonus.

                        # TODO increase speed
                        if self.manda.dragonMode:
                            self.gameGrid.progressGame(configs.DragonYLen+3)
                        else:
                            self.gameGrid.progressGame(configs.MandaYLen+3) # progress by 8 columns
                
                if self.gameGrid.grid[x+i][y+j] == 'D':
                    if not dragonSeen:
                        dragonSeen = True
                        # remove manda from screen and bring in the dragon to
                        # the screen. Dragon needs to move in a wriggly manner. 
                        if self.manda.shield_active:
                            self.manda.shield_active = False
                            self.manda.shield_present = False
                        self.manda.dragonMode = True


  
    def magnetPresent(self):
        stCol = self.gameGrid.largeGrid.startMagnetColumn
        left = self.gameGrid.largeGrid.currentLeftColumn
        right = self.gameGrid.largeGrid.currentRightColumn

        if stCol == -1 :
            return False
        if stCol >= left and stcol <= right:
            return True
        else:
            return False

    # change the underlying large numeric and actual grid
    def fireIceBalls(self):
        x,y = self.Viserion.fireIceBalls()
        stCol = self.gameGrid.largeGrid.currentLeftColumn
        for i in range(configs.BallXLen):
            for j in range(configs.BallYLen):
                self.gameGrid.largeGrid.grid[x+i][stCol+y+j] = configs.iceBallId
                self.gameGrid.largeGrid.numericGrid[x+i][stCol+y+j] = self.Viserion.ball[i][j]
        
    # emulates the game loop

    def gameLoop(self):
        # Progress game and use screen to paint the grid
        print('\033[2;0H',end='')
        self.gameGrid.progressGame(1)
        self.printHeader()
        self.screen.generateScreen(self.gameGrid)

        # update location and place manda
        x,y = self.manda.obj_location.getLocation()
        if x > configs.GridHeight - configs.MandaXLen:
            self.manda.velocityY = 0
        else:
            self.manda.velocityY += self.manda.acceleration
            x += self.manda.velocityY
            if x<0:
                x = 0
            if x > configs.GridHeight - configs.MandaXLen:
                x = configs.GridHeight - configs.MandaXLen
        
        x = int(math.ceil(x))
        x += configs.Xoffset
        y = int(math.ceil(y))
        # we need to move the cursor to these position
        print('\033['+str(x)+';'+str(y)+'H',end = '')
        cx = x
        if self.manda.dragonMode:
            for i in range(configs.DragonXLen):
                for j in range(configs.DragonYLen):
                    dragon = self.manda.createDragon()
                    #self.gameGrid.grid[x+i][y+j] = Back.GREEN + Fore.RED+dragon[i][j]
                    print(Back.GREEN + Fore.RED+self.manda.shape[i][j],end='')
                cx += 1
                print('\033['+str(cx)+';'+str(y)+'H',end='')
        else:
            for i in range(configs.MandaXLen):
                for j in range(configs.MandaYLen):
                    assert type(x) == int,"x should be int"
                    #self.gameGrid.grid[x+i][y+j] = Back.GREEN + Fore.RED+self.manda.shape[i][j]
                    print(Back.GREEN + Fore.RED+self.manda.shape[i][j],end='')
                cx += 1
                print('\033['+str(cx)+';'+str(y)+'H',end='')

        # print Viserion if present
        if self.Viserion.present:
            vx,vy = self.Viserion.obj_location.getLocation()
            mx,my = self.manda.obj_location.getLocation()

            vx = mx
            vx += configs.Xoffset
            cx = vx
            print('\033['+str(vx)+';'+str(vy)+'H',end = '')

            for i in range(configs.ViserionXLen):
                for j in range(configs.ViserionYLen):
                    #self.gameGrid[vx+i][vy+j] = Back.YELLOW + Fore.BLACK +self.Viserion.shape[i][j]
                    print(Back.YELLOW+Fore.BLACK+self.Viserion.shape[i][j],end='')
                cx += 1
                print('\033['+str(cx)+';'+str(y)+'H',end='')


        
        # update status of bullets and print them
        x,y = self.Viserion.obj_location.getLocation()
        incrementScore =\
        self.manda.updateBulletStatus(self.Viserion.present,x)
        self.score += incrementScore

        # need to check if they are hitting ice ball or zappers
        for loc in self.manda.bulletList:
            x,y = loc.getLocation()
            hit = False
            zappers =\
            [configs.horizontalBeamId,configs.verticalBeamId,configs.mainAngledBeamId,configs.offAngledBeamId]
            for i in range(configs.BulletXLen):
                for j in range(configs.BulletYLen):
                    if hit:
                        break
                    # need to change the large grid
                    if y+j< configs.GridWidth:
                        if self.gameGrid.numericGrid[x+i][y+j] in zappers:
                            l = self.gameGrid.largeGrid.currentLeftColumn
                            self.gameGrid.largeGrid.grid[x+i][l+y+j] = ' '
                            self.gameGrid.largeGrid.numericGrid[x+i][l+y+j] = 0
                            self.score += configs.ObsDestroyScr 
                            hit = True
                        if self.gameGrid.numericGrid[x+i][y+j] == configs.iceBallId:
                            # delete the ball from the large grid.
                            # we can change the way we have stored the Ice Ball
                            hit = True
                            x_start = min(0,x-configs.BallXLen)
                            y_start = min(0,y-configs.BallYLen)
                            l = self.gameGrid.largeGrid.currentLeftColumn
                            self.score += configs.ObsDestroyScr
                            for i in range(10):
                                for j in range(10):
                                    if x_start+i>=configs.gridHeight or y_start+j>= configs.gridWidth:
                                        continue
                                    if self.gameGrid.largeGrid.numericGrid[x_start+i][l+y_start+j] ==configs.iceBallId:
                                        self.gameGrid.largeGrid.grid[x_start+i][l+y_start+j]=' '
                                        self.gameGrid.largeGrid.numericGrid[x_start+i][l+y_start+j]=0 


                if hit:
                    break
        # decrease the strength of the Viserion
        strength = self.Viserion.getStrength()
        strength -= incrementScore

        if strength <= 0:
            print('\n THE GAME IS OVER YOU WON!!')
            print('\n YOU HAVE ACHIEVED THE IMPOSSIBLE')
            quit()

        for loc in self.manda.bulletList:
            x,y = loc.getLocation()
            x += configs.Xoffset
            print('\033['+str(x)+';'+str(y)+'H',end='')
            for i in range(configs.BulletXLen):
                for j in range(configs.BulletYLen):
                    print(Back.GREEN+Fore.MAGENTA+self.manda.bullet[i][j],end='')
                x += 1
                print('\033['+str(x)+';'+str(y)+'H',end='')


        print(Style.RESET_ALL)
        self.checkCollision()
        self.keepTime()
