from colorama import Fore, Back, Style
from game import *
from creature import *
from utility import *
import time

if __name__ == "__main__":
    manda = Mandalorian()
    i = 0
    clear()
    keys = NonBlockingInput()
    keys.nonBlockingTerm()
    myGame = Game(manda, keys)
    ViserionEntry = int(0.2 * configs.GAMEDURATION)
    bulletTime = 0
    speedTime = 0
    shieldActivateTime = 0
    timeFromLastShield = configs.SHIELDREACTIVATE
    while True:
        i += 1
        if i == configs.PERIOD:
            myGame.keepTime()
            myGame.magnetAttract()
            if not manda.shield_active:
                if timeFromLastShield == configs.SHIELDREACTIVATE:
                    manda.shield_present = True
                else:
                    timeFromLastShield += 1
            else:
                shieldActivateTime += 1
                if shieldActivateTime == configs.SHIELDTIME:
                    manda.shield_present = False
                    manda.shield_active = False
                    timeFromLastShield = 0
                    shieldActivateTime = 0
            if configs.SPEED:
                speedTime += 1
                if speedTime == 5:
                    speedTime = 0
                    configs.PERIOD = 10
                    configs.RATE = 0.01
                    configs.SPEED = False
            # entry time of Viserion
            if myGame.Viserion.present:
                # throw an ice ball
                bulletTime += 1
                if bulletTime == configs.VISERBULLETDURATION:
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
                elif inp == 'v' or inp == 'V':
                    print('V pressed')
                    configs.SPEED = True
                    configs.PERIOD = 40
                    configs.RATE = 0.0025
                else:
                    manda.move(inp)
        myGame.gameLoop()
        time.sleep(configs.RATE)
