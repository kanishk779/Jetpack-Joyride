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
        self.timeRemaining = configs.gameDuration
        self.score = 0
        self.Manda = Manda
        self.gameGrid = SmallGrid()
        self.screen = Screen(self)
        self.gameGrid.initialiseLargeGrid(4)
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
        
        if self.Manda.shieldActive:
            shieldStatus = "YES"
        else:
            shieldStatus = "NO"
        print("")
        print("TIME LEFT : " + str(self.timeRemaining) +
                "\t\t\t\t\t\t     SHIELD ACTIVE : " + shieldStatus)
        print("YOUR SCORE IS : " + str(self.score) +
              "\t\t\t\t\t\t      LIVES LEFT : " + str(self.Manda.getStrength()))
        print("")

    
    # check if there is any collision, x,y are location of manda    
    def checkCollision(self):
        beamSeen = False
        dragonSeen = False
        bonusSeen = False
        x,y = self.manda.getLocation()
        stCol = self.gameGrid.largeGrid.currentLeftColumn

        for i in configs.MandaXLen:
            for j in configs.MandaYLen:
                
                if self.gameGrid[x+i][y+j] == '$':
                    # change actual self.gameGrid and numeric self.gameGrid and ++ score
                    self.gameGrid.largeGrid.grid[x+i][stCol+y+j] = ' '
                    self.gameGrid.largeGrid.numeric[x+i][stCol+y+j] = 0
                    self.score += 1

                if self.gameGrid[x+i][y+j] == 'z':
                    if self.manda.shieldActive: 
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

                if self.gameGrid[x+i][y+j] == 'B':
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
                
                if self.gameGrid[x+i][y+j] == 'D':
                    if not dragonSeen:
                        dragonSeen = True
                        # remove manda from screen and bring in the dragon to
                        # the screen. Dragon needs to move in a wriggly manner. 
                        if self.manda.shieldActive:
                            self.manda.shieldActive = False
                            self.manda.shieldPresent = False
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
        self.gameGrid.progressGame(1)
        printHeader()
        self.screen.generateScreen()

        # update location and place manda
        x,y = self.manda.getLocation()
        if x > configs.GridHeight - configs.MandaXLen:
            self.manda.velocityY = 0
        else:
            self.manda.velocityY += self.manda.acceleration
            x += self.manda.velocityY
            if x<0:
                x = 0
            if x > configs.GridHeight - configs.MandaXLen:
                x = configs.GridHeight - configs.MandaXLen

        if self.manda.dragonMode:
            for i in range(configs.DragonXLen):
                for j in range(configs.DragonYLen):
                    dragon = self.manda.createDragon()
                    self.gameGrid[x+i][y+j] = Back.GREEN + Fore.RED +\
                        dragon[i][j]
        else:
            for i in range(configs.MandaXLen):
                for j in range(configs.MandaYLen):
                    self.gameGrid[x+i][y+j] = Back.GREEN + Fore.RED +\
                    self.manda.shape[i][j]

        # print Viserion if present
        if self.Viserion.present:
            vx,vy = self.Viserion.getLocation()
            mx,my = self.manda.getLocation()

            vx = mx

            for i in range(configs.ViserionXLen):
                for j in range(configs.ViserionYLen):
                    self.gameGrid[vx+i][vy+j] = Back.YELLOW + Fore.BLACK +\
                        self.Viserion.shape[i][j]
        
        # update status of bullets and print them
        x,y = self.Viserion.getLocation()
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
            self.gameGrid[x][y] = Back.GREEN + Fore.MAGENTA + self.manda.bullet

        checkCollision()

