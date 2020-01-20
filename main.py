from colorama import Fore, Back, Style
from game import *
from creature import *
from utility import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    period = configs.period
    i = 0
    clear()
    keys = NonBlockingInput()
    keys.nonBlockingTerm()
    myGame = Game(manda,keys)
    ViserionEntry = int(0.8*configs.gameDuration)
    bulletTime = 0
    speedTime = 0
    shieldActivateTime = 0
    timeFromLastShield = configs.shieldReactivate
    while True:
        i += 1
        if i == period:
            myGame.keepTime()
            if not manda.shield_active:
                if timeFromLastShield == configs.shieldReactivate:
                    manda.shield_present = True
                else:
                    timeFromLastShield += 1
            else:
                shieldActivateTime += 1
                if shieldActivateTime == configs.shieldTime:
                    manda.shield_present = False
                    manda.shield_active = False
                    timeFromLastShield = 0
                    shieldActivateTime = 0
            speedTime += 1
            if configs.speed:
                speedTime += 1
                if speedTime == 5:
                    speedTime = 0
                    configs.period = 10
                    configs.rate = 0.01
                    configs.speed = False
            # entry time of Viserion
            if myGame.Viserion.present:
                # throw an ice ball
                bulletTime += 1
                if bulletTime == configs.viserBulletDuration:
                    myGame.fireIceBalls()
                    bulletTime = 0
            if myGame.timeRemaining == ViserionEntry:
                myGame.Viserion.present = True
            i = 0
        if keys.keyboardHit():
            #keys.flush()
            inp = keys.getChar()
            inp = keypress(inp)
            if inp is None:
                pass
            else:
                if inp == ' ':
                    if manda.shield_present:
                        manda.shield_active = True
                else:
                    manda.move(inp)
        myGame.gameLoop()
        time.sleep(configs.rate)

