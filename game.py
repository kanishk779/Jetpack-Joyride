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
    def __init__(self, Manda, keys):
        self.timeRemaining = int(configs.GAMEDURATION)
        self.score = 0
        self.keys = keys
        self.manda = Manda
        self.manda.obj_location.setLocation(
            configs.GRIDHEIGHT - configs.MANDAXLEN, 10)
        self.gameGrid = SmallGrid()
        self.screen = Screen()
        self.gameGrid.initialiseLargeGrid(10)
        self.Viserion = Viserion()
        self.Viserion.obj_location.setLocation(
            configs.GRIDHEIGHT - configs.DRAGONXLEN,
            configs.GRIDWIDTH - configs.DRAGONYLEN)

    def keepTime(self):
        if self.timeRemaining == 0:
            self.keys.flush()
            self.keys.originalTerm()
            print("Sorry, you were not able to complete the game")
            print("Your score was : " + str(self.score))
            print("GAME OVER")
            quit()
        else:
            self.timeRemaining -= 1

    # print the header
    def printHeader(self):

        if self.manda.shield_active:
            shieldActive = "YES"
        else:
            shieldActive = "NO "
        if self.manda.shield_present:
            shieldPresent = "YES"
        else:
            shieldPresent = "NO "
        print(
            "TIME LEFT : {t:5d} \t\t\tSHIELD PRESENT : {p}     \t SHIELD ACTIVE : {a}"
            .format(t=self.timeRemaining, p=shieldPresent, a=shieldActive))
        print("YOUR SCORE IS : " + str(self.score) +
              "\t\t\t\t\t\t      LIVES LEFT : " +
              str(self.manda.getStrength()))

    # check if there is any collision, x,y are location of manda
    def checkCollision(self):
        hit = False
        x, y = self.manda.obj_location.getLocation()
        stCol = self.gameGrid.largeGrid.currentLeftColumn
        if self.manda.dragonMode:
            xLen = configs.DRAGONXLEN
            yLen = configs.DRAGONYLEN
        else:
            xLen = configs.MANDAXLEN
            yLen = configs.MANDAYLEN
        H = configs.GRIDHEIGHT
        W = configs.GRIDWIDTH
        N = self.gameGrid.N
        total = N * W
        for i in range(xLen):
            for j in range(yLen):
                tempx = -1
                tempy = -1
                if x + i < 0:
                    tempx = 0
                if x + i >= H:
                    tempx = H - 1
                if y + j < 0:
                    tempy = 0
                if y + j >= W:
                    tempy = W - 1
                if tempx != -1:
                    x = tempx - i
                if tempy != -1:
                    y = tempy - j

                if self.gameGrid.grid[x + i][y + j] == '$':
                    # change actual self.gameGrid and numeric self.gameGrid and ++ score
                    xstart = x + i - 8
                    xend = x + i + 8
                    if xstart < 0:
                        xstart = 0
                    if xend >= H:
                        xend = H
                    ystart = y + j - 10
                    yend = y + j + 18
                    if ystart < 0:
                        ystart = 0
                    if yend >= W:
                        yend = W
                    for xx in range(xstart, xend):
                        for yy in range(ystart, yend):
                            k = (stCol + yy) % (total)
                            if self.gameGrid.largeGrid.grid[xx][k] in [
                                    'X', 'M', 'D', 'z'
                            ]:
                                pass
                            else:
                                self.gameGrid.largeGrid.grid[xx][k] = ' '
                                self.gameGrid.largeGrid.numericGrid[xx][k] = 0
                    self.score += 20
                    hit = True
                if x+i>=0 and x+i<H and self.gameGrid.grid[x+i][y+j] == 'D' and\
                self.gameGrid.numericGrid[x+i][y+j] == configs.DRAGONID:
                    hit = True
                    # remove manda from screen and bring in the dragon to the screen.
                    if self.manda.shield_active:
                        self.manda.shield_active = False
                        self.manda.shield_present = False
                    self.manda.dragonMode = True

                if self.gameGrid.grid[x + i][y + j] == 'z':
                    if self.manda.shield_active:
                        # if shield is active than nothing happens to manda
                        continue

                    hit = True
                    # decrease live and step ahead of that beam so that in
                    # next iteration you do not encounter the beam. Move the
                    # background , do not move Manda

                    if self.manda.dragonMode:
                        self.gameGrid.progressGame(configs.DRAGONYLEN + 12)
                        self.manda.dragonMode = False
                    else:
                        self.gameGrid.progressGame(configs.MANDAYLEN +
                                                   12)  # progress by 17 column
                        lives = self.manda.getStrength()
                        lives -= 1

                        self.manda.setStrength(lives)
                        if lives == 0:
                            print('You lost , your score is : ' +
                                  str(self.score))
                            self.keys.originalTerm()
                            quit()

                if self.gameGrid.numericGrid[x + i][y +
                                                    j] == configs.ICEBALLID:
                    if self.manda.shield_active:
                        continue
                    hit = True
                    if self.manda.dragonMode:
                        self.gameGrid.progressGame(configs.DRAGONYLEN + 7)
                        self.manda.dragonMode = False
                    else:
                        self.gameGrid.progressGame(configs.MANDAYLEN +
                                                   7)  # progress by 17 column
                        lives = self.manda.getStrength()
                        lives -= 1
                        if lives == 0:
                            print('You lost , your score is : ' +
                                  str(self.score))
                            self.keys.originalTerm()
                            quit()
                        self.manda.setStrength(lives)

                if hit:
                    break
            if hit:
                break

    def magnetPresent(self):
        stCol = self.gameGrid.largeGrid.startMagnetColumn
        left = self.gameGrid.largeGrid.currentLeftColumn
        right = self.gameGrid.largeGrid.currentRightColumn

        if stCol == -1:
            return False
        if stCol >= left and stCol <= right:
            stCol -= left
            startY = max(0, stCol - 15)
            endY = min(configs.GRIDWIDTH - 1, stCol + 10)
            x, y = self.manda.obj_location.getLocation()
            if y > startY and y < endY:
                return True
            else:
                return False
        else:
            return False

    def magnetAttract(self):
        if self.magnetPresent():
            configs.GRAVITY = -0.5
            x, y = self.manda.obj_location.getLocation()
            x -= 2
            x = max(2, x)
            self.manda.obj_location.setLocation(x, y)
        else:
            configs.GRAVITY = 1

    # change the underlying large numeric and actual grid
    def fireIceBalls(self):
        x, y = self.Viserion.fireIceBalls()
        stCol = self.gameGrid.largeGrid.currentLeftColumn
        W = configs.GRIDWIDTH
        N = self.gameGrid.N
        total = W * N
        x -= 3
        if x < 2:
            x = 2
        for i in range(configs.BALLXLEN):
            for j in range(configs.BALLYLEN):
                if x + i < 0:
                    x = -i
                if x + i >= configs.GRIDHEIGHT:
                    x = -i + configs.GRIDHEIGHT - configs.BALLXLEN
                k = (stCol + y + j) % (total)
                self.gameGrid.largeGrid.grid[x +
                                             i][k] = self.Viserion.ball[i][j]
                self.gameGrid.largeGrid.numericGrid[x +
                                                    i][k] = configs.ICEBALLID

    # emulates the game loop

    def gameLoop(self):
        # Progress game and use screen to paint the grid
        print('\033[2;0H', end='')
        self.gameGrid.progressGame(1)
        self.printHeader()
        self.screen.generateScreen(self.gameGrid)

        # update location and place manda
        x, y = self.manda.obj_location.getLocation()
        if self.manda.dragonMode:
            XLen = configs.DRAGONXLEN
            YLen = configs.DRAGONYLEN
        else:
            XLen = configs.MANDAXLEN
            YLen = configs.MANDAYLEN
        if x >= configs.GRIDHEIGHT - XLen - 1:
            if not self.magnetPresent():
                self.manda.velocityY = 0
            x = configs.GRIDHEIGHT - XLen
        else:
            self.manda.velocityY += configs.GRAVITY
            x += self.manda.velocityY
            if x < 0:
                x = 0
            if x > configs.GRIDHEIGHT - XLen:
                x = configs.GRIDHEIGHT - XLen

        x = int(math.ceil(x))
        y = int(math.ceil(y))
        if x < 2:
            x = 2
        if x > (configs.GRIDHEIGHT - XLen):
            x = configs.GRIDHEIGHT - XLen
        if y < 0:
            y = 0
        if y > (configs.GRIDWIDTH - YLen):
            y = configs.GRIDWIDTH - YLen

        self.manda.obj_location.setLocation(x, y)
        x += configs.XOFFSET
        self.checkCollision()
        # we need to move the cursor to these position
        if x < 4:
            x = 5
        print('\033[' + str(x) + ';' + str(y) + 'H', end='')
        cx = x
        if self.manda.dragonMode:
            dragon = self.manda.createDragon()
            for i in range(configs.DRAGONXLEN):
                for j in range(configs.DRAGONYLEN):
                    if dragon[i][j] != ' ':
                        print(configs.BACKGROUNDCOLOR + configs.CHARACTERFORECOLOR + dragon[i][j], end='')
                    else:
                        print(configs.BACKGROUNDCOLOR + ' ', end='')
                cx += 1
                print('\033[' + str(cx) + ';' + str(y) + 'H', end='')
        elif self.manda.shield_active:
            for i in range(configs.MANDAXLEN):
                for j in range(configs.MANDAYLEN):
                    if self.manda.shieldShape[i][j] != ' ':
                        print(configs.BACKGROUNDCOLOR + configs.CHARACTERFORECOLOR +
                              self.manda.shieldShape[i][j],
                              end='')
                    else:
                        print(configs.BACKGROUNDCOLOR + ' ', end='')
                cx += 1
                print('\033[' + str(cx) + ';' + str(y) + 'H', end='')
        else:
            for i in range(configs.MANDAXLEN):
                for j in range(configs.MANDAYLEN):
                    if self.manda.shape[i][j] != ' ':
                        print(configs.BACKGROUNDCOLOR + configs.CHARACTERFORECOLOR + self.manda.shape[i][j],
                              end='')
                    else:
                        print(configs.BACKGROUNDCOLOR + ' ', end='')
                cx += 1
                print('\033[' + str(cx) + ';' + str(y) + 'H', end='')

        # print Viserion if present
        if self.Viserion.present:
            vx, vy = self.Viserion.obj_location.getLocation()
            mx, my = self.manda.obj_location.getLocation()

            vx = mx
            self.Viserion.obj_location.setLocation(vx, vy)
            vx += configs.XOFFSET
            cx = vx
            print('\033[' + str(vx) + ';' + str(vy) + 'H', end='')
            shape = self.Viserion.createDragon()
            for i in range(configs.DRAGONXLEN):
                for j in range(configs.DRAGONYLEN):
                    if shape[i][j] != ' ':
                        print(configs.BACKGROUNDCOLOR + configs.CHARACTERFORECOLOR + shape[i][j], end='')
                    else:
                        print(configs.BACKGROUNDCOLOR + ' ', end='')

                cx += 1
                print('\033[' + str(cx) + ';' + str(vy) + 'H', end='')

        # update status of bullets and print them
        x, y = self.Viserion.obj_location.getLocation()
        incrementScore =\
        self.manda.updateBulletStatus(self.Viserion.present,x)
        self.score += incrementScore

        # need to check if they are hitting ice ball or zappers
        for loc in self.manda.bulletList:
            x, y = loc.getLocation()
            hit = False
            W = configs.GRIDWIDTH
            N = self.gameGrid.N
            H = configs.GRIDHEIGHT
            total = W * N
            zappers =\
            [configs.HORIZONTALBEAMID,configs.VERTICALBEAMID,configs.MAINANGLEDBEAMID,configs.OFFANGLEDBEAMID]
            for i in range(configs.BULLETXLEN):
                for j in range(configs.BULLETYLEN):
                    if hit:
                        break
                    # need to change the large grid
                    if y + j < configs.GRIDWIDTH:

                        if self.gameGrid.numericGrid[x + i][y + j] in zappers:
                            l = self.gameGrid.largeGrid.currentLeftColumn
                            k = (l + y + j) % total
                            Id = self.gameGrid.largeGrid.numericGrid[x + i][k]
                            if Id == configs.HORIZONTALBEAMID:
                                ind = k
                                while self.gameGrid.largeGrid.grid[
                                        x + i][ind] == 'z':
                                    self.gameGrid.largeGrid.grid[x +
                                                                 i][ind] = ' '
                                    self.gameGrid.largeGrid.numericGrid[
                                        x + i][ind] = 0
                                    ind += 1
                                    ind = ind % total
                                ind = k - 1
                                ind = (ind + total) % total
                                while self.gameGrid.largeGrid.grid[
                                        x + i][ind] == 'z':
                                    self.gameGrid.largeGrid.grid[x +
                                                                 i][ind] = ' '
                                    self.gameGrid.largeGrid.numericGrid[
                                        x + i][ind] = 0
                                    ind -= 1
                                    ind = (ind + total) % total
                            elif Id == configs.VERTICALBEAMID:
                                ind = x + i
                                while self.gameGrid.largeGrid.grid[ind][
                                        k] == 'z':
                                    self.gameGrid.largeGrid.grid[ind][k] = ' '
                                    self.gameGrid.largeGrid.numericGrid[ind][
                                        k] = 0
                                    ind += 1
                                    if ind >= H:
                                        break
                                ind = x + i - 1
                                ind = (ind + total) % total
                                while self.gameGrid.largeGrid.grid[ind][
                                        k] == 'z':
                                    self.gameGrid.largeGrid.grid[ind][k] = ' '
                                    self.gameGrid.largeGrid.numericGrid[ind][
                                        k] = 0
                                    ind -= 1
                                    if ind < 0:
                                        break
                            elif Id == configs.MAINANGLEDBEAMID:
                                indx = x + i
                                indy = k
                                while self.gameGrid.largeGrid.grid[indx][
                                        indy] == 'z':
                                    self.gameGrid.largeGrid.grid[indx][
                                        indy] = ' '
                                    self.gameGrid.largeGrid.numericGrid[indx][
                                        indy] = 0
                                    indx += 1
                                    if indx >= H:
                                        break
                                    indy += 1
                                    indy = indy % total
                                indx = x + i - 1
                                indy = k - 1
                                if indx < 0:
                                    indx = 0
                                indy = (indy + total) % total
                                while self.gameGrid.largeGrid.grid[indx][
                                        indy] == 'z':
                                    self.gameGrid.largeGrid.grid[indx][
                                        indy] = ' '
                                    self.gameGrid.largeGrid.numericGrid[indx][
                                        indy] = 0
                                    indx -= 1
                                    if indx < 0:
                                        break
                                    indy -= 1
                                    indy = (indy + total) % total
                            elif Id == configs.OFFANGLEDBEAMID:
                                indx = x + i
                                indy = k
                                while self.gameGrid.largeGrid.grid[indx][
                                        indy] == 'z':
                                    self.gameGrid.largeGrid.grid[indx][
                                        indy] = ' '
                                    self.gameGrid.largeGrid.numericGrid[indx][
                                        indy] = 0
                                    indx -= 1
                                    indy += 1
                                    if indx < 0:
                                        break
                                    indy = (indy + total) % total
                                indx = x + i + 1
                                if indx >= H:
                                    indx = H - 1
                                indy = k - 1
                                indy = (indy + total) % total
                                while self.gameGrid.largeGrid.grid[indx][
                                        indy] == 'z':
                                    self.gameGrid.largeGrid.grid[indx][
                                        indy] = ' '
                                    self.gameGrid.largeGrid.numericGrid[indx][
                                        indy] = 0
                                    indx += 1
                                    indy -= 1
                                    if indx >= H:
                                        break
                                    indy = (indy + total) % total

                            self.score += configs.OBSDESTROYSCR
                            hit = True
                if hit:
                    break

        strength = self.Viserion.getStrength()
        strength -= incrementScore
        self.Viserion.setStrength(strength)
        if strength <= 0:
            print('\n THE GAME IS OVER YOU WON!!')
            print('\n YOU HAVE ACHIEVED THE IMPOSSIBLE')
            self.keys.flush()
            self.keys.originalTerm()
            quit()

        for loc in self.manda.bulletList:
            x, y = loc.getLocation()
            x += configs.XOFFSET
            if y >= configs.GRIDWIDTH:
                continue
            print('\033[' + str(x) + ';' + str(y) + 'H', end='')
            for i in range(configs.BULLETXLEN):
                for j in range(configs.BULLETYLEN):
                    print(Back.GREEN + Fore.BLACK + self.manda.bullet[i][j],
                          end='')
                x += 1
                print('\033[' + str(x) + ';' + str(y) + 'H', end='')

        print(Style.RESET_ALL)
